"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Severity Level Descriptors (Pages 27-35)
정량 표현 - Quantitative Severity Descriptions
═══════════════════════════════════════════════════════════════════════════════

This module provides human-readable severity descriptions for all numeric/level
session variables, based on the canonical Korean descriptions in CLINICAL_DATA.

Features:
- Maps session attributes to their clinical data keys
- Converts various numeric ranges (0-5, 0-10, hours, etc.) to 1-5 levels
- Populates *_desc attributes with Korean clinical descriptions
- Supports all symptom categories from Pages 27-35

Usage:
    from constraints.severity_descriptors import apply_severity_descriptions
    apply_severity_descriptions(session)
    # Now session.fever_sev_desc contains the Korean description
"""

from data_mappings import get_desc


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL CONVERSION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _clamp_level(v):
    """Clamp a value to 1-5 level range."""
    try:
        lv = int(v)
    except Exception:
        return None
    if lv <= 0:
        return 1
    if lv > 5:
        return 5
    return lv


def _level_0_to_5(v):
    """Convert 0-5 scale to 1-5 (0 becomes 1)."""
    try:
        lv = int(v)
    except Exception:
        return None
    if lv <= 0:
        return 1
    if lv > 5:
        return 5
    return lv


def _hours_to_level(hours):
    """Map sleep hours to guideline level 1-5 (Page 33)."""
    try:
        h = int(hours)
    except Exception:
        return None
    if h <= 4:
        return 1
    if 5 <= h <= 6:
        return 2
    if 7 <= h <= 9:
        return 3
    if 10 <= h <= 11:
        return 4
    return 5


def _nrs10_to_level(score):
    """Convert NRS 0-10 pain scale to 1-5 level (Page 34)."""
    try:
        s = int(score)
    except Exception:
        return None
    if s <= 0:
        return 1
    if 1 <= s <= 3:
        return 2
    if 4 <= s <= 6:
        return 3
    if 7 <= s <= 9:
        return 4
    return 5


def _urine_day_to_level(freq):
    """Convert daily urine frequency to level (Page 31-32)."""
    try:
        f = int(freq)
    except Exception:
        return None
    if f <= 2:
        return 1
    if 3 <= f <= 4:
        return 2
    if 5 <= f <= 7:
        return 3
    if 8 <= f <= 10:
        return 4
    return 5


def _urine_night_to_level(freq):
    """Convert nocturia frequency to level (Page 31-32)."""
    try:
        f = int(freq)
    except Exception:
        return None
    if f == 0:
        return 1
    if f == 1:
        return 2
    if f == 2:
        return 3
    if 3 <= f <= 4:
        return 4
    return 5


def _meal_freq_to_level(freq):
    """Convert daily meal frequency to level (Page 31)."""
    try:
        f = int(freq)
    except Exception:
        return None
    if f == 1:
        return 1
    if f == 2:
        return 2
    if f == 3:
        return 3
    if f == 4:
        return 4
    return 5


def _temp_to_fever_level(temp):
    """Convert temperature to fever severity level (Page 27)."""
    try:
        t = float(temp)
    except Exception:
        return None
    if t < 35.0:
        return 1
    if t < 37.4:
        return 2
    if t < 38.0:
        return 3
    if t < 40.0:
        return 4
    return 5


def _water_intake_to_level(intake_str):
    """Convert water intake string to level (Page 34)."""
    if not intake_str:
        return 3
    intake = str(intake_str).lower()
    if '0.5' in intake and '미만' in intake:
        return 1
    if '0.5' in intake or '<0.5' in intake:
        return 1
    if '0.5-1' in intake or '0.5~1' in intake:
        return 2
    if '1-2' in intake or '1~2' in intake:
        return 3
    if '1l' in intake and '2l' not in intake:
        return 3
    if '>2' in intake or '2l 이상' in intake or '2L 이상' in intake:
        return 5
    return 3


def _snot_color_to_level(color_str):
    """Convert snot color string to level (Page 27-28)."""
    if not color_str:
        return 1
    color = str(color_str).lower()
    if '투명' in color or 'clear' in color or '맑' in color:
        return 1
    if '흰' in color or 'white' in color or '백' in color:
        return 2
    if '누런' in color or 'yellow' in color or '황' in color:
        return 3
    return 2


# ═══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE VARIABLE MAPPING (Pages 27-35)
# Format: session_attr -> (clinical_data_key, converter_type)
# ═══════════════════════════════════════════════════════════════════════════════

SEVERITY_MAP = {
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 27: COLD SYMPTOMS (감기 증상)
    # ═══════════════════════════════════════════════════════════════════════════
    'fever_sev': ('fever_sev', 'int'),
    'chills_sev': ('chills_sev', 'int'),
    'snot_sev': ('snot_sev', 'int'),
    'snot_color': ('snot_color', 'snot_color'),
    'snot_type': ('snot_color', 'snot_color'),
    'cough_sev': ('cough_sev', 'int'),
    'phlegm_amt': ('phlegm_amt', 'int'),
    'phlegm_color': ('phlegm_color', 'int'),
    'alternating_chills_fever': ('alternating_chills_fever', 'int'),
    'temp': ('fever_sev', 'temp'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 28: RHINITIS SYMPTOMS (비염 증상)
    # ═══════════════════════════════════════════════════════════════════════════
    'rhinitis_sneeze': ('rhinitis_sneeze', 'int'),
    'rhinitis_block': ('rhinitis_block', 'int'),
    'rhinitis_itch': ('rhinitis_itch', 'int'),
    'rhinitis_snot_sev': ('rhinitis_snot_sev', 'int'),
    'rhinitis_snot_type': ('rhinitis_snot_type', 'int'),
    'smell_reduction': ('smell_reduction', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 31: DIET & APPETITE (식이 및 식욕)
    # ═══════════════════════════════════════════════════════════════════════════
    'diet_freq': ('diet_freq', 'meal_freq'),
    'diet_regular': ('diet_regular', 'int'),
    'diet_amt': ('diet_amt', 'int'),
    'digestion': ('digestion', 'int'),
    'appetite': ('appetite', 'int'),
    'appetite_level': ('appetite', 'int'),
    'motivation_level': ('motivation_level', 'int'),
    'motivation': ('motivation', 'int'),
    'water_intake': ('drink_amt', 'water_intake'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 31: STOOL (대변)
    # ═══════════════════════════════════════════════════════════════════════════
    'stool_freq': ('stool_freq', 'int'),
    'stool_color': ('stool_color', 'int'),
    'stool_form': ('stool_form', 'int'),
    'stool_discomfort': ('stool_discomfort', 'int'),
    'stool_residual': ('stool_residual', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 31-32: URINE (소변)
    # ═══════════════════════════════════════════════════════════════════════════
    'urine_freq_day': ('urine_freq_day', 'urine_day'),
    'urine_freq_night': ('urine_freq_night', 'urine_night'),
    'urine_color': ('urine_color', 'int'),
    'urine_discomfort': ('urine_discomfort', 'int'),
    'urine_residual': ('urine_residual', 'int'),
    'urine_comfort': ('urine_comfort', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 33: SLEEP (수면)
    # ═══════════════════════════════════════════════════════════════════════════
    'sleep_hours': ('sleep_hours', 'hours'),
    'sleep_depth': ('sleep_depth', 'int'),
    'sleep_latency': ('sleep_latency', 'int'),
    'sleep_quality': ('sleep_quality', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 33-34: BODY TEMPERATURE & SWEAT (체열 및 땀)
    # ═══════════════════════════════════════════════════════════════════════════
    'cold_heat_pref': ('cold_heat_pref', 'int'),
    'cold_heat_level': ('cold_heat_pref', 'int'),
    'sweat_amt': ('sweat_amt', 'int'),
    'sweat_level': ('sweat_amt', 'int'),
    'drink_amt': ('drink_amt', 'int'),
    'drink_temp': ('drink_temp', 'int'),
    'drink_temp_pref': ('drink_temp', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 32-33: PHYSICAL STRENGTH & FATIGUE (체력 및 피로)
    # ═══════════════════════════════════════════════════════════════════════════
    'physical_strength': ('physical_strength', 'int'),
    'physical_strength_level': ('physical_strength', 'int'),
    'fatigue': ('fatigue', 'int'),
    'fatigue_level': ('fatigue', 'int'),
    'body_muscle_pain': ('body_muscle_pain', 'int'),
    'body_heaviness': ('body_heaviness', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 34: PAIN (통증)
    # ═══════════════════════════════════════════════════════════════════════════
    'pain_presence': ('pain_presence', 'int'),
    'pain_severity': ('pain_severity', 'int'),
    'pain_sev': ('pain_severity', 'int'),
    'abd_pain_sev': ('pain_severity', 'int'),
    'back_pain_sev': ('back_pain_sev', 'int'),
    'back_sev': ('back_pain_sev', 'int'),
    'neck_nape_sev': ('pain_severity', 'int'),
    'chest_pain_sev': ('pain_severity', 'int'),
    'chest_tight_sev': ('pain_severity', 'int'),
    'flank_sev': ('pain_severity', 'int'),
    'shoulder_sev': ('pain_severity', 'int'),
    'elbow_sev': ('pain_severity', 'int'),
    'knee_sev': ('pain_severity', 'int'),
    'hand_foot_sev': ('pain_severity', 'int'),
    'pelvis_sev': ('pain_severity', 'int'),
    
    # Pain frequency variables (0-5)
    'neck_nape_freq': ('tinnitus_freq', 'int'),  # Use tinnitus_freq as template for freq
    'chest_pain_freq': ('tinnitus_freq', 'int'),
    'chest_tight_freq': ('tinnitus_freq', 'int'),
    'flank_freq': ('tinnitus_freq', 'int'),
    'back_freq': ('tinnitus_freq', 'int'),
    'shoulder_freq': ('tinnitus_freq', 'int'),
    'elbow_freq': ('tinnitus_freq', 'int'),
    'knee_freq': ('tinnitus_freq', 'int'),
    'hand_foot_freq': ('tinnitus_freq', 'int'),
    'pelvis_freq': ('tinnitus_freq', 'int'),
    
    # NRS-10 pain scores (convert to 1-5)
    'mens_pain_score': ('pain_severity', 'nrs10'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 33-34: SKIN & FACE (피부 및 안면)
    # ═══════════════════════════════════════════════════════════════════════════
    'skin_dry': ('skin_dry', 'int'),
    'skin_dryness': ('skin_dry', 'int'),
    'face_gloss': ('face_gloss', 'int'),
    'face_color': ('face_color', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 34: SENSORY (감각)
    # ═══════════════════════════════════════════════════════════════════════════
    'tinnitus_freq': ('tinnitus_freq', 'int'),
    'tinnitus_sev': ('tinnitus_sev', 'int'),
    'tinnitus': ('tinnitus', 'int'),
    'hearing_sev': ('tinnitus_sev', 'int'),
    'dizziness_sev': ('tinnitus_sev', 'int'),
    'eye_discomfort': ('eye_discomfort', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 35: MENTAL STATE & EMOTION (정신 및 감정)
    # ═══════════════════════════════════════════════════════════════════════════
    'mental_state': ('mental_state', 'int'),
    'mental_clarity': ('mental_state', 'int'),
    'memory': ('memory', 'int'),
    'memory_level': ('memory', 'int'),
    'personality_speed': ('personality_speed', 'int'),
    'emot_anger': ('emot_anger', 'int'),
    'emot_anxiety': ('emot_anxiety', 'int'),
    'emot_depress': ('emot_depress', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 35: EDEMA & BRUISING (부종 및 멍)
    # ═══════════════════════════════════════════════════════════════════════════
    'edema': ('edema', 'int'),
    'edema_level': ('edema', 'int'),
    'bruising': ('bruising', 'int'),
    'bruising_level': ('bruising', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PULSE & TONGUE DIAGNOSIS (맥진 및 설진)
    # ═══════════════════════════════════════════════════════════════════════════
    'pulse_rate': ('pulse_rate', 'int'),
    'pulse_depth': ('pulse_depth', 'int'),
    'pulse_strength': ('pulse_strength', 'int'),
    'tongue_color': ('tongue_color', 'int'),
    'tongue_coat': ('tongue_coat', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BACK PAIN SPECIFIC (요통)
    # ═══════════════════════════════════════════════════════════════════════════
    'back_pain_cold_agg': ('back_pain_cold_agg', 'int'),
    'back_pain_warmth_relief': ('back_pain_warmth_relief', 'int'),
    'back_pain_stabbing': ('back_pain_stabbing', 'int'),
    'back_pain_moving': ('back_pain_moving', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DYSPEPSIA SPECIFIC (소화불량)
    # ═══════════════════════════════════════════════════════════════════════════
    'dyspepsia_bloating': ('dyspepsia_bloating', 'int'),
    'dyspepsia_cold_food_agg': ('dyspepsia_cold_food_agg', 'int'),
    'dyspepsia_acid_reflux': ('dyspepsia_acid_reflux', 'int'),
    'dyspepsia_foul_belch': ('dyspepsia_foul_belch', 'int'),
    'dyspepsia_cold_limbs': ('dyspepsia_cold_limbs', 'int'),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GI SYMPTOMS (소화기 증상)
    # ═══════════════════════════════════════════════════════════════════════════
    'nausea': ('digestion', 'int'),
    'nausea_sev': ('digestion', 'int'),
    'bloating': ('dyspepsia_bloating', 'int'),
    'belching': ('digestion', 'int'),
    'food_stag_sev': ('digestion', 'int'),
    'lower_abd_discomfort': ('pain_severity', 'int'),
    'palpitation': ('tinnitus_sev', 'int'),
    'sighing_freq': ('tinnitus_freq', 'int'),
    'mouth_dry': ('skin_dry', 'int'),
}


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERTER DISPATCH TABLE
# ═══════════════════════════════════════════════════════════════════════════════

CONVERTERS = {
    'int': _clamp_level,
    'level_0_5': _level_0_to_5,
    'hours': _hours_to_level,
    'nrs10': _nrs10_to_level,
    'urine_day': _urine_day_to_level,
    'urine_night': _urine_night_to_level,
    'meal_freq': _meal_freq_to_level,
    'temp': _temp_to_fever_level,
    'water_intake': _water_intake_to_level,
    'snot_color': _snot_color_to_level,
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def apply_severity_descriptions(session):
    """
    Populate `*_desc` attributes for all session severity fields.
    
    For each mapped session attribute, this function will:
    1. Compute a guideline level (1-5) using the appropriate converter
    2. Fetch the textual description from data_mappings.get_desc()
    3. Write the description to session.<attr>_desc
    
    Args:
        session: Streamlit session_state or similar object with symptom attributes
    
    Example:
        session.fever_sev = 4
        apply_severity_descriptions(session)
        # session.fever_sev_desc now contains:
        # "몸이 뜨겁다고 느끼고, 이로 인한 전신 근육통이나 두통이 동반됨..."
    """
    for attr, (clinical_key, conv_type) in SEVERITY_MAP.items():
        # Skip if session does not have attribute
        if not hasattr(session, attr):
            continue
        
        val = getattr(session, attr)
        
        # Skip None values
        if val is None:
            continue
        
        # Get the converter function
        converter = CONVERTERS.get(conv_type, _clamp_level)
        
        # Convert value to level
        level = converter(val)
        
        if level is None:
            continue
        
        # Get description from clinical data
        desc = get_desc(clinical_key, level)
        
        # If we didn't find a description, skip
        if not desc:
            continue
        
        # Set descriptive attribute, e.g. fever_sev_desc
        try:
            setattr(session, f"{attr}_desc", desc)
        except Exception:
            # Be defensive - ignore attributes we cannot set
            pass


def get_severity_description(attr_name, value):
    """
    Get severity description for a single attribute value.
    
    Args:
        attr_name: The session attribute name (e.g., 'fever_sev')
        value: The numeric value
    
    Returns:
        Korean description string, or empty string if not found
    """
    if attr_name not in SEVERITY_MAP:
        return ""
    
    clinical_key, conv_type = SEVERITY_MAP[attr_name]
    converter = CONVERTERS.get(conv_type, _clamp_level)
    level = converter(value)
    
    if level is None:
        return ""
    
    return get_desc(clinical_key, level) or ""


def get_all_severity_descriptions(session):
    """
    Get all severity descriptions as a dictionary.
    
    Args:
        session: Streamlit session_state or similar object
    
    Returns:
        Dictionary of {attr_name: description}
    """
    descriptions = {}
    
    for attr, (clinical_key, conv_type) in SEVERITY_MAP.items():
        if not hasattr(session, attr):
            continue
        
        val = getattr(session, attr)
        if val is None:
            continue
        
        converter = CONVERTERS.get(conv_type, _clamp_level)
        level = converter(val)
        
        if level is None:
            continue
        
        desc = get_desc(clinical_key, level)
        if desc:
            descriptions[attr] = desc
    
    return descriptions


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def list_mapped_attributes():
    """Return list of all mapped attribute names."""
    return list(SEVERITY_MAP.keys())


def get_attribute_info(attr_name):
    """
    Get mapping info for an attribute.
    
    Returns:
        Tuple of (clinical_key, converter_type) or None
    """
    return SEVERITY_MAP.get(attr_name)


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Quick self-test
    class MockSession:
        pass
    
    s = MockSession()
    
    # Test various attributes
    s.fever_sev = 4
    s.chills_sev = 3
    s.tinnitus_freq = 4
    s.sleep_hours = 6
    s.urine_freq_day = 8
    s.urine_freq_night = 2
    s.pain_severity = 3
    s.appetite = 2
    s.motivation = 4
    s.fatigue = 3
    s.emot_anxiety = 4
    
    apply_severity_descriptions(s)
    
    print("=" * 60)
    print("Severity Descriptor Test Results")
    print("=" * 60)
    
    test_attrs = [
        'fever_sev', 'chills_sev', 'tinnitus_freq', 'sleep_hours',
        'urine_freq_day', 'urine_freq_night', 'pain_severity',
        'appetite', 'motivation', 'fatigue', 'emot_anxiety'
    ]
    
    for attr in test_attrs:
        desc_attr = f"{attr}_desc"
        if hasattr(s, desc_attr):
            desc = getattr(s, desc_attr)
            print(f"\n{attr} = {getattr(s, attr)}")
            print(f"  → {desc[:80]}..." if len(desc) > 80 else f"  → {desc}")
        else:
            print(f"\n{attr} = {getattr(s, attr)} (no description)")
    
    print("\n" + "=" * 60)
    print(f"Total mapped attributes: {len(SEVERITY_MAP)}")
    print("=" * 60)
