"""
═══════════════════════════════════════════════════════════════════════════════
Monte Carlo Mosaic Viewer  (removable tab)
Runs REAL sampling N times and shows live-updating distributions.

To REMOVE: delete this file and remove the 2 lines in app.py that reference it.
═══════════════════════════════════════════════════════════════════════════════
"""

import time
import random
import pandas as pd
import streamlit as st
from collections import Counter, OrderedDict

from json_patient_sampler import (
    _sample_option, load_disease_data, _merge_cold_temp,
    get_syndrome_keys,
)
from json_var_mapping import (
    DISEASE_FILES, DISEASE_SPECIFIC_MAPS,
    VAR_MAP, VAR_MAP_PULSE_TONGUE, SKIP, SECTION_DUPES,
    get_full_var_map,
)
from constants import DISEASE_PATTERNS


# ── Color palette ──
_PALETTE = [
    "#4C78A8", "#F58518", "#E45756", "#72B7B2",
    "#54A24B", "#EECA3B", "#B279A2", "#FF9DA6",
    "#9D755D", "#BAB0AC", "#D67195", "#7EB0D5",
]

# ── Reverse map: session_key → Korean label ──
def _build_labels():
    rev = {}
    for var_map in (VAR_MAP, VAR_MAP_PULSE_TONGUE):
        for kr, entry in var_map.items():
            skey, ctype = entry[0], entry[1]
            if not skey.startswith("_") and ctype != SKIP and skey not in rev:
                rev[skey] = kr
    for disease_maps in DISEASE_SPECIFIC_MAPS.values():
        for kr, entry in disease_maps.items():
            skey, ctype = entry[0], entry[1]
            if not skey.startswith("_") and ctype != SKIP and skey not in rev:
                rev[skey] = kr
    return rev

_LABELS = _build_labels()

# Which session keys to track (clinical data only, skip internal/UI keys)
_SKIP_KEYS = {
    "_disease_key", "_bmi_cat", "disease", "scenario_generated",
    "generated_summary", "generated_scenario", "generated_patient_info",
}


def _get_trackable_keys(disease_key):
    """Return sorted list of session keys that the sampler produces."""
    var_map = get_full_var_map(disease_key)
    keys = set()
    for kr, entry in var_map.items():
        skey, ctype = entry[0], entry[1]
        if ctype != SKIP and not skey.startswith("_"):
            keys.add(skey)
    # Also add composed keys
    keys.update(["history_conditions", "family_hx", "meds_specific"])
    keys -= _SKIP_KEYS
    return sorted(keys)


# ── Section groupings for display ──
SECTION_ORDER = [
    ("인구학적정보", ["age", "sex", "job", "height", "weight"]),
    ("활력징후", ["sbp", "temp", "pulse_rate", "resp"]),
    ("현병력/가족력", ["history_conditions", "family_hx", "meds_specific"]),
    ("사회력", ["social_alcohol_freq", "social_alcohol_amt", "social_smoke_daily",
                "social_smoke_years", "social_exercise_freq", "social_exercise_time",
                "social_exercise_int"]),
    ("여성력", ["mens_cycle", "mens_regular", "mens_duration", "mens_pain_score",
               "mens_color", "mens_amt", "mens_clot"]),
    ("식사/소화", ["diet_freq", "diet_regular", "diet_amt", "diet_speed",
                  "water_intake", "digestion", "appetite"]),
    ("대변", ["stool_freq", "stool_color", "stool_form", "stool_discomfort",
             "stool_residual"]),
    ("소변", ["urine_color", "urine_freq_day", "urine_freq_night", "urine_stream",
             "urine_discomfort", "urine_residual_sev", "urine_incontinence"]),
    ("수면", ["sleep_hours", "sleep_depth", "sleep_waking_state", "insomnia_onset",
             "insomnia_freq", "insomnia_maintain_count", "insomnia_reentry", "dreams"]),
    ("땀", ["sweat_amt", "sweat_time", "sweat_area", "sweat_feeling"]),
    ("한열", ["cold_heat_body", "cold_heat_distribution", "drink_temp",
             "cold_sensitivity", "heat_sensitivity", "cold_hands_feet",
             "warm_body_areas", "cold_body_areas"]),
    ("전신상태", ["body_solidity", "physical_strength", "fatigue_level",
                "body_ache", "body_heaviness", "condition_bad_area",
                "edema", "bruising", "limb_weakness"]),
    ("피부/면색", ["skin_dry", "skin_itch", "skin_trouble", "face_color", "face_gloss"]),
    ("눈/귀", ["eye_discomfort", "eye_red", "vision_blackout",
              "tinnitus_sev", "tinnitus_freq", "hearing_sev", "dizziness_sev"]),
    ("구강", ["lip_color", "lip_dry", "mouth_dry", "throat_dry", "mouth_bitter",
             "bad_breath", "sore_throat", "cough_sev", "phlegm_amt", "phlegm_color",
             "hiccup"]),
    ("두부/경항", ["head_discomfort_freq", "head_discomfort_sev",
                 "neck_nape_freq", "neck_nape_sev"]),
    ("흉부", ["breath_sound", "palpitation", "chest_tight_freq", "chest_tight_sev",
             "chest_pain_freq", "chest_pain_sev", "sighing_freq"]),
    ("복부", ["nausea", "nausea_sev", "bloating", "flatulence", "belching",
             "belching_smell", "food_stag_sev", "lower_abd_discomfort",
             "abd_pain_sev", "abd_pain_type", "abd_tenderness",
             "abd_muscle_tension", "abd_mass", "abd_pulsation", "bowel_sound"]),
    ("근골격", ["flank_freq", "flank_sev", "back_freq", "back_sev",
              "pelvis_freq", "pelvis_sev", "shoulder_freq", "shoulder_sev",
              "elbow_freq", "elbow_sev", "hand_foot_freq", "hand_foot_sev",
              "cold_hands_feet", "leg_discomfort", "knee_freq", "knee_sev"]),
    ("성격", ["personality_speed", "personality_soft", "personality_io",
             "personality_static", "voice_vol"]),
    ("감정", ["excitement", "emot_anger", "emot_depress", "emot_anxiety",
             "emot_fear", "emot_startle", "emot_thought", "emot_grief"]),
    ("정신", ["mental_clarity", "memory", "motivation", "stress_coping", "mood_swing"]),
    ("맥진", ["pulse_depth", "pulse_width", "pulse_length", "pulse_smooth",
             "pulse_strength", "pulse_tension"]),
    ("설진", ["tongue_color", "tongue_size", "tongue_coat_color", "tongue_coat_thick",
             "tongue_marks", "tongue_coat_particle"]),
]

DISEASE_SECTION_ORDER = {
    "감기": [
        ("감기 증상", [
            "fever_sev", "chills_sev", "alternating_chills_fever",
            "snot_sev", "snot_color", "nose_block_sev", "nose_dry",
            "smell_reduction", "sneeze_sev", "body_ache_cold",
            "body_heaviness_cold", "headache_cold", "cold_sweating_check",
            "cold_dyspnea", "cold_onset_specific",
            "past_illness_cold", "past_cold_problem_area",
            "cold_modifying_factors", "course",
            "exam_lung_sound", "exam_throat", "exam_tonsil",
            "exam_xray", "exam_otoscope", "exam_rhinoscope", "exam_blood_test",
        ]),
    ],
    "알레르기비염": [
        ("비염 증상", [
            "sneeze_sev", "sneeze_freq", "nose_itch_sev",
            "snot_sev", "snot_color", "rhinitis_onset", "rhinitis_past",
            "rhinitis_modifying_factors", "exam_rhinoscope_finding",
        ]),
    ],
    "기능성소화불량": [
        ("소화불량 증상", [
            "dyspepsia_onset", "dyspepsia_past",
            "postprandial_fullness", "early_satiety",
            "epigastric_discomfort", "epigastric_burning",
            "dyspepsia_modifying_factors", "exam_endoscopy",
        ]),
    ],
    "요통": [
        ("요통 증상", [
            "backpain_onset", "backpain_past",
            "back_discomfort_area", "back_discomfort_freq",
            "back_discomfort_sev", "radiation_pain", "pain_duration",
            "back_pain_nature", "back_modifying_factors",
            "slr_test", "exam_ct", "exam_mri",
        ]),
    ],
}


def _short_desc(desc, max_len=25):
    """Truncate long option descriptions for display."""
    desc = str(desc).strip()
    # Strip leading option-like prefixes
    if desc and desc[0].isdigit() and ". " in desc[:5]:
        desc = desc.split(". ", 1)[1]
    if len(desc) > max_len:
        return desc[:max_len] + "…"
    return desc


def _extract_theoretical_probs(variables, var_map, prob_key="general"):
    """Build {session_key: [(tagged_desc, probability), ...]} from JSON variables.
    
    Same tagging logic as _sample_one_patient so keys match the counters.
    For SECTION_DUPES (현병력/가족력/약물력), build composite keys matching
    the counter format: each condition name is a value with its "있음" probability.
    """
    result = {}
    seen_section_vars = {}
    # Collect SECTION_DUPES probs separately for composite keys
    composite_probs = {}   # {composite_key: [(var_name, p_present), ...]}

    for var_entry in variables:
        var_name = var_entry["variable"]
        section = var_entry.get("section", "")

        if var_name in SECTION_DUPES:
            dupe_key = (var_name, section)
            if dupe_key in seen_section_vars:
                continue
            seen_section_vars[dupe_key] = True

            # Determine composite key
            if "가족력" in section:
                comp_key = "family_hx"
            elif "현병력" in section:
                comp_key = "history_conditions"
            elif "약물력" in section:
                comp_key = "meds_specific"
            else:
                comp_key = None

            if comp_key:
                # Get probability of option 1 (= condition present, "있음")
                options = var_entry["options"]
                p_present = 0
                for opt in options:
                    opt_num = opt.get("option", 0) or 0
                    if opt_num == 1:
                        if prob_key == "general":
                            p_present = opt.get("general", 0) or 0
                        else:
                            norm = opt.get("normalized_probabilities", {})
                            p_present = norm.get(prob_key, 0) or 0
                        break
                composite_probs.setdefault(comp_key, [])
                composite_probs[comp_key].append((var_name, p_present))
                continue

        if var_name not in var_map:
            continue

        session_key, conv_type, lookup = var_map[var_name]
        if conv_type == SKIP:
            continue

        options = var_entry["options"]
        probs = []
        for opt in options:
            opt_num = opt.get("option", 0) or 0
            desc = _short_desc(opt.get("description", str(opt_num)))
            tagged = f"{int(opt_num):02d}\u2502{desc}"

            if prob_key == "general":
                p = opt.get("general", 0) or 0
            else:
                norm = opt.get("normalized_probabilities", {})
                p = norm.get(prob_key, 0) or 0

            probs.append((tagged, p))

        if probs and any(p > 0 for _, p in probs):
            result[session_key] = probs

    # Add composite keys — each condition name becomes an entry
    for comp_key, items in composite_probs.items():
        probs = [(var_name, p) for var_name, p in items if p > 0]
        if probs:
            result[comp_key] = probs

    return result


def _sample_one_patient(variables, var_map, prob_key="general"):
    """Sample one patient from JSON variables, return {session_key: short_description}.
    
    Uses option descriptions (not converted values) for clean visualization.
    """
    result = {}
    seen_section_vars = {}

    for var_entry in variables:
        var_name = var_entry["variable"]
        section = var_entry.get("section", "")

        # Handle section-disambiguated duplicates
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

        # For syndrome mode, build options with syndrome probs
        if prob_key != "general":
            syn_options = []
            for opt in var_entry["options"]:
                norm = opt.get("normalized_probabilities", {})
                p = norm.get(prob_key)
                if p is not None and p > 0:
                    syn_options.append({
                        "option": opt["option"],
                        "description": opt.get("description", str(opt["option"])),
                        "prob": p,
                    })
            if not syn_options:
                continue
            weights = [o["prob"] for o in syn_options]
            total = sum(weights)
            if total <= 0:
                continue
            weights = [w / total for w in weights]
            chosen = random.choices(syn_options, weights=weights, k=1)[0]
        else:
            chosen = _sample_option(var_entry["options"], prob_key="general")

        if chosen is None:
            continue

        opt_num = chosen.get("option", 0) or 0
        desc = _short_desc(chosen.get("description", str(opt_num)))
        # Prefix with zero-padded option number for correct sort order
        tagged = f"{int(opt_num):02d}\u2502{desc}"

        # Handle section-aware duplicates (병력, 가족력, 약물력)
        if var_name in SECTION_DUPES:
            if "가족력" in section:
                skey = "family_hx"
            elif "현병력" in section:
                skey = "history_conditions"
            elif "약물력" in section:
                skey = "meds_specific"
            else:
                skey = session_key
            # For bool-like dupes: "있음" means this condition is present
            if opt_num == 1:  # option 1 = "있음" for these
                result.setdefault(skey, [])
                result[skey].append(var_name)
        elif conv_type == "list_cat":
            result.setdefault(session_key, [])
            if desc != "없음":
                result[session_key].append(tagged)
        else:
            result[session_key] = tagged

    return result


def _run_simulation_live(disease_key, mode, syndrome_key, n,
                         progress_bar, status_text, results_placeholder):
    """Run simulation with live progress updates using JSON-level sampling."""
    gen_data, syn_data = load_disease_data(disease_key)
    var_map = get_full_var_map(disease_key)

    if mode == "syndrome" and syndrome_key:
        variables = syn_data["variables"]
        prob_key = syndrome_key
    else:
        variables = gen_data["variables"]
        prob_key = "general"

    # Merge split 체온 for cold
    if disease_key == "감기":
        variables = _merge_cold_temp(variables)

    # Extract theoretical probabilities for comparison
    theo_probs = _extract_theoretical_probs(variables, var_map, prob_key)
    st.session_state["_mc_theo_probs"] = theo_probs

    counters = {}
    batch_size = max(1, n // 50)

    for i in range(n):
        sampled = _sample_one_patient(variables, var_map, prob_key)

        for k, v in sampled.items():
            if k in _SKIP_KEYS or k.startswith("_"):
                continue
            if k not in counters:
                counters[k] = Counter()
            if isinstance(v, list):
                for item in v:
                    counters[k][str(item)] += 1
            else:
                counters[k][str(v)] += 1

        done = i + 1
        if done % batch_size == 0 or done == n:
            pct = done / n
            progress_bar.progress(pct, text=f"시뮬레이션 중... {done}/{n}명")
            status_text.caption(
                f"⏱ {done}/{n} 환자 생성 완료 · "
                f"{len(counters)}개 변수 추적 중"
            )
            if done % max(1, n // 10) == 0 or done == n:
                with results_placeholder.container():
                    _render_all_sections(counters, done, disease_key, theo_probs=theo_probs)

    return counters


def _strip_tag(val):
    """Remove the '02\u2502' option-number prefix for display."""
    s = str(val)
    if len(s) > 2 and s[2] == '\u2502':
        return s[3:]
    return s


def _natural_sort_key(val):
    """Sort by embedded option number prefix (e.g. '02\u2502desc')."""
    s = str(val)
    if len(s) > 2 and s[2] == '\u2502':
        try:
            return (0, int(s[:2]), s)
        except ValueError:
            pass
    try:
        return (0, float(s), s)
    except (ValueError, TypeError):
        return (1, 0, s)


def _short_label(description):
    """Extract a short Korean label from a full description.
    E.g. '소아·청소년: ~ 19세 이하' -> '소아·청소년'
         '콧물이 계속 흘러...' -> '콧물이 계속 흘러'
    Truncates at first colon/comma/period or 10 chars, whichever is shorter."""
    for sep in (':', '：', ',', '.', '(', '（'):
        if sep in description:
            return description[:description.index(sep)].strip()
    return description[:10].strip()


def _bar_html(counter, n):
    """Build HTML for a stacked mosaic bar from a Counter.
    Options shown in natural order with fixed color per position."""
    items = sorted(counter.items(), key=lambda x: _natural_sort_key(x[0]))
    if not items:
        return ""

    parts = []
    for idx, (val, count) in enumerate(items):
        pct = count / n * 100
        if pct < 0.3:
            continue
        color = _PALETTE[idx % len(_PALETTE)]
        display = _strip_tag(val)
        # Always show percentage in bar
        label = f"{pct:.0f}%"
        parts.append(
            f'<div style="display:inline-block;width:{pct:.1f}%;'
            f'background:{color};color:#fff;font-size:11px;font-weight:500;'
            f'text-align:center;padding:5px 2px;overflow:hidden;'
            f'white-space:nowrap;box-sizing:border-box;'
            f'border-right:1px solid rgba(255,255,255,0.4);" '
            f'title="{display} \u2014 {count}\uba85 ({pct:.1f}%)">' 
            f'{label}'
            f'</div>'
        )
    if not parts:
        return ""

    return (
        '<div style="display:flex;width:100%;border-radius:6px;'
        'overflow:hidden;margin-bottom:4px;box-shadow:0 1px 3px rgba(0,0,0,0.12);">'
        + "".join(parts)
        + '</div>'
    )


def _legend_html(counter, n):
    """Compact colored legend under each bar — each item in a colored badge box."""
    items = sorted(counter.items(), key=lambda x: _natural_sort_key(x[0]))
    parts = []
    for idx, (val, count) in enumerate(items):
        pct = count / n * 100
        color = _PALETTE[idx % len(_PALETTE)]
        display = _strip_tag(val)
        parts.append(
            f'<span style="'
            f'display:inline-block;'
            f'background:{color}20;'
            f'border:1px solid {color}55;'
            f'border-left:3px solid {color};'
            f'border-radius:5px;'
            f'padding:4px 10px;'
            f'margin:2px 4px;'
            f'font-size:12px;'
            f'line-height:1.5;'
            f'color:#222;'
            f'">'
            f'<b style="color:{color};">●</b> '
            f'{display} '
            f'<span style="color:#555;font-size:11px;font-weight:500;">'
            f'{count}명 ({pct:.1f}%)</span>'
            f'</span>'
        )
    return (
        '<div style="display:flex;flex-wrap:wrap;margin-bottom:10px;">'
        + "".join(parts)
        + '</div>'
    )


def _render_var_block(k, ctr, n, theo_probs):
    """Render one variable: title, theoretical bar (JSON), simulation bar, legend."""
    label = _LABELS.get(k, k)

    theo = theo_probs.get(k) if theo_probs else None

    st.markdown(f"**{label}** (`{k}`)")

    # ── Theoretical bar (JSON probabilities) ──
    if theo:
        sorted_theo = sorted(theo, key=lambda x: _natural_sort_key(x[0]))
        theo_parts = []
        for idx, (tagged, p) in enumerate(sorted_theo):
            pct = p * 100
            if pct < 0.3:
                continue
            color = _PALETTE[idx % len(_PALETTE)]
            display = _strip_tag(tagged)
            label_txt = f"{pct:.0f}%"
            theo_parts.append(
                f'<div style="display:inline-block;width:{pct:.1f}%;'
                f'background:{color};color:#fff;font-size:11px;font-weight:500;'
                f'text-align:center;padding:5px 2px;overflow:hidden;'
                f'white-space:nowrap;box-sizing:border-box;opacity:0.55;'
                f'border-right:1px solid rgba(255,255,255,0.4);" '
                f'title="{display} — 이론 {pct:.1f}%">'
                f'{label_txt}'
                f'</div>'
            )
        if theo_parts:
            st.markdown(
                '<div style="font-size:10px;color:#888;margin-bottom:1px;font-weight:600;">'
                '📋 JSON 이론</div>'
                '<div style="display:flex;width:100%;border-radius:6px;'
                'overflow:hidden;margin-bottom:2px;'
                'box-shadow:0 1px 3px rgba(0,0,0,0.08);">'
                + "".join(theo_parts)
                + '</div>',
                unsafe_allow_html=True,
            )

    # ── Simulation bar ──
    if n > 0:
        st.markdown(
            '<div style="font-size:10px;color:#888;margin-bottom:1px;font-weight:600;">'
            '🎲 시뮬레이션</div>',
            unsafe_allow_html=True,
        )
    st.markdown(_bar_html(ctr, n), unsafe_allow_html=True)
    st.markdown(_legend_html(ctr, n), unsafe_allow_html=True)


def _render_all_sections(counters, n, disease_key, theo_probs=None):
    """Render all variable sections from counters dict."""
    # General sections
    for sec_name, keys in SECTION_ORDER:
        active = [(k, counters[k]) for k in keys if k in counters]
        if not active:
            continue
        with st.expander(f"📂 {sec_name} ({len(active)}개 변수)", expanded=False):
            for k, ctr in active:
                _render_var_block(k, ctr, n, theo_probs)

    # Disease-specific sections
    disease_secs = DISEASE_SECTION_ORDER.get(disease_key, [])
    for sec_name, keys in disease_secs:
        active = [(k, counters[k]) for k in keys if k in counters]
        if not active:
            continue
        with st.expander(f"🔬 {sec_name} ({len(active)}개 변수)", expanded=False):
            for k, ctr in active:
                _render_var_block(k, ctr, n, theo_probs)

    # Uncategorized — keys in counters but not in any section
    all_sec_keys = set()
    for _, keys in SECTION_ORDER:
        all_sec_keys.update(keys)
    for _, secs in DISEASE_SECTION_ORDER.items():
        for _, keys in secs:
            all_sec_keys.update(keys)
    uncategorized = {k: c for k, c in counters.items() if k not in all_sec_keys}
    if uncategorized:
        with st.expander(f"📦 기타 ({len(uncategorized)}개 변수)", expanded=False):
            for k, ctr in sorted(uncategorized.items()):
                _render_var_block(k, ctr, n, theo_probs)


def render_mosaic_tab():
    """Render the Monte Carlo simulation mosaic tab."""

    st.markdown("## 📊 Monte Carlo 확률 분포 시뮬레이터")
    st.caption(
        "실제 샘플러를 N회 실행하여 환자 데이터를 생성하고, "
        "각 변수별 분포를 실시간으로 시각화합니다."
    )

    # ── Controls ──
    col1, col2 = st.columns([2, 1])
    with col1:
        disease_labels = {k: f"{v['label']} ({v['code']})" for k, v in DISEASE_FILES.items()}
        disease_key = st.selectbox(
            "질환 선택",
            list(disease_labels.keys()),
            format_func=lambda k: disease_labels[k],
            key="_mc_disease",
        )
    with col2:
        n_patients = st.number_input(
            "환자 수 (N)",
            min_value=10, max_value=5000, value=100, step=10,
            key="_mc_n",
        )

    # Mode selection
    col3, col4 = st.columns([1, 2])
    with col3:
        mode = st.radio(
            "샘플링 방식",
            ["general", "syndrome"],
            format_func=lambda m: "전체 확률 (general)" if m == "general" else "변증별 (syndrome)",
            key="_mc_mode",
        )
    syndrome_key = None
    with col4:
        if mode == "syndrome":
            syn_keys = get_syndrome_keys(disease_key)
            if disease_key in DISEASE_PATTERNS:
                pats = DISEASE_PATTERNS[disease_key]["patterns"]
                syn_display = [
                    f"{sk} — {pats[i]['name']}" if i < len(pats) else sk
                    for i, sk in enumerate(syn_keys)
                ]
            else:
                syn_display = syn_keys
            sel = st.selectbox("변증 선택", syn_display, key="_mc_syn_sel")
            syndrome_key = sel.split(" — ")[0] if " — " in sel else sel

    st.markdown("---")

    # ── Run button ──
    if st.button("🚀 시뮬레이션 시작", type="primary", width='stretch',
                 key="_mc_run"):
        progress_bar = st.progress(0, text="시뮬레이션 준비 중...")
        status_text = st.empty()
        results_placeholder = st.empty()

        t0 = time.time()

        counters = _run_simulation_live(
            disease_key, mode, syndrome_key, n_patients,
            progress_bar, status_text, results_placeholder,
        )

        elapsed = time.time() - t0
        progress_bar.progress(1.0, text="✅ 시뮬레이션 완료!")
        status_text.caption(
            f"✅ {n_patients}명 생성 완료 · {len(counters)}개 변수 · "
            f"{elapsed:.1f}초 소요 · {n_patients/elapsed:.0f} 환자/초"
        )

        # Cache for re-display after rerun
        st.session_state["_mc_last_counters"] = counters
        st.session_state["_mc_last_n"] = n_patients
        st.session_state["_mc_last_dk"] = disease_key

    # ── Show cached results if available ──
    elif "_mc_last_counters" in st.session_state:
        counters = st.session_state["_mc_last_counters"]
        n = st.session_state.get("_mc_last_n", 100)
        dk = st.session_state.get("_mc_last_dk", disease_key)
        theo_probs = st.session_state.get("_mc_theo_probs")
        st.info(f"이전 시뮬레이션 결과 표시 중 ({n}명, {dk})")
        _render_all_sections(counters, n, dk, theo_probs=theo_probs)
