"""
JSON-based Patient Sampler
Part 1: Loading + General (vertical) sampling
"""
import json
import random
import os

from json_var_mapping import (
    SCALE, CAT, RANGE, BOOL2, LIST_CAT, SKIP,
    DISEASE_FILES, CONSTRAINTS_FILE, SECTION_DUPES,
    get_full_var_map,
)

# ── Cache loaded JSON data ──
_cache = {}


def _load_json(path):
    """Load JSON with caching."""
    if path not in _cache:
        with open(path, "r", encoding="utf-8") as f:
            _cache[path] = json.load(f)
    return _cache[path]


def load_disease_data(disease_key):
    """Return (general_data, syndrome_data) for a disease."""
    info = DISEASE_FILES[disease_key]
    gen = _load_json(info["general"])
    syn = _load_json(info["syndrome"])
    return gen, syn


def _merge_cold_temp(variables):
    """Cold file splits 체온 into 3 entries. Merge into one."""
    temp_entries = [v for v in variables if v["variable"] == "체온"]
    if len(temp_entries) <= 1:
        return variables
    # Build merged options list
    merged_opts = []
    merged_general = 0.0
    for entry in temp_entries:
        for opt in entry["options"]:
            merged_opts.append(opt)
            merged_general += opt.get("general", 0) or 0
    # Create merged entry
    merged = {
        "section": temp_entries[0]["section"],
        "subcategory": temp_entries[0]["subcategory"],
        "variable": "체온",
        "num_options": len(merged_opts),
        "general_sum": merged_general,
        "general_OK": True,
        "options": merged_opts,
    }
    # Replace in list: remove all 체온 entries, insert merged
    result = [v for v in variables if v["variable"] != "체온"]
    result.append(merged)
    return result


def _sample_option(options, prob_key="general"):
    """Pick one option using probability weights."""
    weights = []
    valid_opts = []
    for opt in options:
        p = opt.get(prob_key)
        if p is None or p <= 0:
            continue
        weights.append(p)
        valid_opts.append(opt)
    if not valid_opts:
        return None
    # Normalize if needed
    total = sum(weights)
    if total <= 0:
        return None
    weights = [w / total for w in weights]
    chosen = random.choices(valid_opts, weights=weights, k=1)[0]
    return chosen


def _convert_value(option_num, conv_type, lookup):
    """Convert sampled option number to session state value."""
    if conv_type == SCALE:
        if lookup and option_num in lookup:
            return lookup[option_num]
        # Default: option 1=0, 2=1, 3=2, 4=3, 5=4 → but most scales
        # are 1-5 mapping directly, so return option_num as-is
        return option_num
    elif conv_type == CAT:
        if lookup and option_num in lookup:
            return lookup[option_num]
        return option_num
    elif conv_type == RANGE:
        if lookup and option_num in lookup:
            lo, hi = lookup[option_num]
            if isinstance(lo, float):
                return round(random.uniform(lo, hi), 1)
            return random.randint(lo, hi)
        return option_num
    elif conv_type == BOOL2:
        if lookup and option_num in lookup:
            return lookup[option_num]
        return option_num == 1
    elif conv_type == LIST_CAT:
        if lookup and option_num in lookup:
            return lookup[option_num]
        return str(option_num)
    elif conv_type == SKIP:
        return None
    return option_num


def sample_general_patient(disease_key):
    """Sample a 'general' patient using vertical probabilities.
    
    Returns dict of {session_key: value} pairs.
    """
    gen_data, _ = load_disease_data(disease_key)
    variables = gen_data["variables"]
    
    # Merge split 체온 for cold
    if disease_key == "감기":
        variables = _merge_cold_temp(variables)
    
    var_map = get_full_var_map(disease_key)
    result = {}
    seen_section_vars = {}  # Track (variable, section) for dupes
    
    for var_entry in variables:
        var_name = var_entry["variable"]
        section = var_entry.get("section", "")
        
        # Handle section-disambiguated duplicates
        if var_name in SECTION_DUPES:
            dupe_key = (var_name, section)
            if dupe_key in seen_section_vars:
                continue
            seen_section_vars[dupe_key] = True
        
        # Look up mapping
        if var_name not in var_map:
            continue  # unmapped variable
        
        session_key, conv_type, lookup = var_map[var_name]
        
        if conv_type == SKIP:
            continue
        
        # Sample an option
        chosen = _sample_option(var_entry["options"], prob_key="general")
        if chosen is None:
            continue
        
        option_num = chosen["option"]
        value = _convert_value(option_num, conv_type, lookup)
        
        if value is None:
            continue
        
        # Handle list-type keys (LIST_CAT): append to list
        if conv_type == LIST_CAT:
            if session_key not in result:
                result[session_key] = []
            if value != "없음" and value != "없음":
                result[session_key].append(value)
        # Handle section-aware duplicates for history/family
        elif var_name in SECTION_DUPES:
            if "가족력" in section:
                fam_key = "family_hx"
                if fam_key not in result:
                    result[fam_key] = []
                if value is True:
                    result[fam_key].append(var_name)
            elif "현병력" in section:
                hx_key = "history_conditions"
                if hx_key not in result:
                    result[hx_key] = []
                if value is True:
                    result[hx_key].append(var_name)
            elif "약물력" in section:
                med_key = "meds_specific"
                if med_key not in result:
                    result[med_key] = []
                if value is True:
                    result[med_key].append(var_name)
        else:
            result[session_key] = value
    
    return result


# ══════════════════════════════════════════════════════════════
# Part 2: Syndrome (horizontal) sampling + Correlation constraints
# ══════════════════════════════════════════════════════════════

def get_syndrome_keys(disease_key):
    """Return list of syndrome keys for a disease."""
    _, syn_data = load_disease_data(disease_key)
    return syn_data.get("syndrome_keys", [])


def sample_syndrome_patient(disease_key, syndrome_key):
    """Sample a patient for a specific syndrome using horizontal probs.
    
    Uses normalized_probabilities from horizontal syndrome files.
    Returns dict of {session_key: value} pairs.
    """
    _, syn_data = load_disease_data(disease_key)
    variables = syn_data["variables"]
    
    if disease_key == "감기":
        variables = _merge_cold_temp(variables)
    
    var_map = get_full_var_map(disease_key)
    result = {}
    seen_section_vars = {}
    
    for var_entry in variables:
        var_name = var_entry["variable"]
        section = var_entry.get("section", "")
        
        if var_name in SECTION_DUPES:
            dupe_key = (var_name, section)
            if dupe_key in seen_section_vars:
                continue
            seen_section_vars[dupe_key] = True
        
        if var_name not in var_map:
            continue
        
        session_key, conv_type, lookup = var_map[var_name]
        if conv_type == SKIP:
            continue
        
        # Build options with syndrome-specific probabilities
        syn_options = []
        for opt in var_entry["options"]:
            norm = opt.get("normalized_probabilities", {})
            p = norm.get(syndrome_key)
            if p is not None and p > 0:
                syn_options.append({"option": opt["option"],
                                    "description": opt.get("description", ""),
                                    "prob": p})
        
        if not syn_options:
            continue
        
        # Sample using syndrome probs
        weights = [o["prob"] for o in syn_options]
        total = sum(weights)
        if total <= 0:
            continue
        weights = [w / total for w in weights]
        chosen = random.choices(syn_options, weights=weights, k=1)[0]
        option_num = chosen["option"]
        value = _convert_value(option_num, conv_type, lookup)
        
        if value is None:
            continue
        
        if conv_type == LIST_CAT:
            if session_key not in result:
                result[session_key] = []
            if value != "없음":
                result[session_key].append(value)
        elif var_name in SECTION_DUPES:
            if "가족력" in section:
                result.setdefault("family_hx", [])
                if value is True:
                    result["family_hx"].append(var_name)
            elif "현병력" in section:
                result.setdefault("history_conditions", [])
                if value is True:
                    result["history_conditions"].append(var_name)
            elif "약물력" in section:
                result.setdefault("meds_specific", [])
                if value is True:
                    result["meds_specific"].append(var_name)
        else:
            result[session_key] = value
    
    return result


def apply_correlation_constraints(sampled, max_retries=5):
    """Apply CP_01-CP_19 constraints: resample conflicting values.
    
    Args:
        sampled: dict of {session_key: value} from sampling
        max_retries: max attempts to fix each constraint
    Returns:
        Modified sampled dict with conflicts resolved.
    """
    constraints_path = CONSTRAINTS_FILE
    if not os.path.exists(constraints_path):
        return sampled
    
    data = _load_json(constraints_path)
    pairs = data.get("constraint_pairs", [])
    
    # Build reverse lookup: session_key -> Korean variable name
    # We need this to match constraint variable names to sampled keys
    from json_var_mapping import VAR_MAP, VAR_MAP_PULSE_TONGUE
    all_maps = {}
    all_maps.update(VAR_MAP)
    all_maps.update(VAR_MAP_PULSE_TONGUE)
    
    korean_to_session = {}
    for kr_name, (sess_key, _, _) in all_maps.items():
        korean_to_session[kr_name] = sess_key
    
    for pair in pairs:
        incomp = pair.get("incompatible_combinations", [])
        if not incomp:
            continue
        
        for rule in incomp:
            when_left = rule.get("when_left", {})
            then_right = rule.get("then_right_excluded", {})
            
            left_var = when_left.get("variable", "")
            right_var = then_right.get("variable", "")
            left_opts = set(when_left.get("options", []))
            right_excluded = set(then_right.get("options", []))
            
            left_key = korean_to_session.get(left_var)
            right_key = korean_to_session.get(right_var)
            
            if not left_key or not right_key:
                continue
            if left_key not in sampled or right_key not in sampled:
                continue
            
            left_val = sampled[left_key]
            right_val = sampled[right_key]
            
            # Check if left value triggers the constraint
            if isinstance(left_val, (int, float)) and int(left_val) in left_opts:
                # Check if right value is in excluded set
                if isinstance(right_val, (int, float)) and int(right_val) in right_excluded:
                    # Fix: set right to option 1 (lowest/none)
                    sampled[right_key] = 1
    
    return sampled


# ══════════════════════════════════════════════════════════════
# Part 3: Session population + main entry point
# ══════════════════════════════════════════════════════════════

def populate_session_state(st_session, sampled):
    """Write sampled values into Streamlit session state.
    
    Args:
        st_session: streamlit session_state object (dict-like)
        sampled: dict from sample_general_patient or sample_syndrome_patient
    """
    from session_defaults import SESSION_DEFAULTS
    
    for key, value in sampled.items():
        # Only write keys that exist in SESSION_DEFAULTS
        if key in SESSION_DEFAULTS:
            st_session[key] = value
        # Special internal keys starting with _ are intermediate
        # and should not be written to session state
    
    # Derive computed fields
    if "height" in sampled and "weight" in sampled:
        h = sampled["height"]
        w = sampled["weight"]
        if h > 0:
            h_m = h / 100.0
            bmi = round(w / (h_m * h_m), 1)
            st_session["height"] = h
            st_session["weight"] = w
    
    # Set disease label — but skip if widget already controls it
    # (Streamlit forbids modifying widget-bound keys after render)
    disease_key = sampled.get("_disease_key")
    # st_session["disease"] is bound to a selectbox, so we do NOT set it here


def generate_json_patient(st_session, disease_key, mode="general",
                          syndrome_key=None):
    """Main entry point: sample + constrain + populate session.
    
    Args:
        st_session: streamlit session_state
        disease_key: one of "감기", "알레르기비염", "기능성소화불량", "요통"
        mode: "general" or "syndrome"
        syndrome_key: e.g. "syndrome_1" (required if mode="syndrome")
    
    Returns:
        dict of sampled values (for inspection/debugging)
    """
    if mode == "syndrome" and syndrome_key:
        sampled = sample_syndrome_patient(disease_key, syndrome_key)
    else:
        sampled = sample_general_patient(disease_key)
    
    # Apply correlation constraints
    sampled = apply_correlation_constraints(sampled)
    
    # Tag with disease key for populate step
    sampled["_disease_key"] = disease_key
    
    # Write to session state
    populate_session_state(st_session, sampled)
    
    return sampled
