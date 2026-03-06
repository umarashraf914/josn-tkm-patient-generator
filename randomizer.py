"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Randomization Functions
═══════════════════════════════════════════════════════════════════════════════
"""

import random
import logging
from data_mappings import get_weights
from constants import (
    DISEASE_PATTERNS, PAST_COLD_PROBLEM_AREAS, AGGRAVATING_FACTORS,
    RELIEVING_FACTORS, FREQUENT_COMORBIDITIES,
    get_random_additional_symptoms, get_random_comorbidities
)
from constraint_rules import apply_constraint_rules, apply_symptom_correlation_rules

# Import CSV-based generation rules
try:
    from generation_rules import (
        load_rules, 
        generate_patient_from_rules,
        get_patterns_for_disease,
        CSV_PATHS
    )
    CSV_RULES_AVAILABLE = True
except ImportError:
    CSV_RULES_AVAILABLE = False
    print("Warning: generation_rules module not available, using fallback randomization")

from episode_generator import generate_episode
from csv_symptom_mappers import (
    apply_cold_symptoms,
    apply_rhinitis_symptoms,
    apply_common_symptoms,
    apply_dyspepsia_symptoms,
    apply_backpain_symptoms,
    log_value_set,
    log_layer_start,
)


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Create a logger for randomization tracking
randomizer_logger = logging.getLogger("randomizer")
randomizer_logger.setLevel(logging.DEBUG)

# Create console handler if not already present
if not randomizer_logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s [%(name)s] %(message)s')
    console_handler.setFormatter(formatter)
    randomizer_logger.addHandler(console_handler)

# Enable/disable detailed logging (set to True to see all value changes)
# Set to False to disable console output
ENABLE_RANDOMIZER_LOGGING = False  # Change to True to enable detailed logging


def print_randomization_summary(session):
    """Print a human-readable summary of key randomized values."""
    print("\n" + "="*60)
    print("🎲 RANDOMIZATION SUMMARY")
    print("="*60)
    print(f"Disease: {getattr(session, 'disease', 'N/A')}")
    print(f"Pattern Index: {getattr(session, 'pattern_idx', 'N/A')}")
    print("-"*60)
    print("COMORBIDITIES (현병력) - FROM CSV:")
    hx = getattr(session, 'history_conditions', [])
    if hx:
        for c in hx:
            print(f"  ✓ {c}")
    else:
        print("  (None)")
    print("-"*60)
    print("Expected CSV Probabilities:")
    print("  당뇨: 15%  |  고혈압: 30%  |  이상지질혈증: 45%")
    print("="*60 + "\n")

# ============================================================================
# CSV-BASED RANDOMIZATION (NEW)
# ============================================================================

def randomize_from_csv_rules(st, disease_name: str, pattern: str = None):
    """
    Randomize patient inputs using CSV-based generation rules.
    
    Args:
        st: Streamlit module with session_state
        disease_name: Disease name in Korean (감기 or 알레르기비염)
        pattern: Optional pattern name for pattern-specific probabilities
    
    Returns:
        True if successful, False if fallback is needed
    """
    if not CSV_RULES_AVAILABLE:
        return False
    
    try:
        # Generate patient data from CSV rules
        patient_data = generate_patient_from_rules(disease_name, pattern)
        
        if not patient_data:
            return False
        
        session = st.session_state
        
        # =============================================================================
        # Map CSV symptom keys to session state variables
        # CSV keys follow pattern: "Category_Subcategory_ItemName"
        # =============================================================================
        
        # Helper function to find key by partial match
        def find_key(partial_name):
            """Find a key in patient_data containing the partial name."""
            for key in patient_data:
                if partial_name in key:
                    return key
            return None
        
        # Demographics - use actual CSV keys
        sex_key = find_key("성별")
        if sex_key and sex_key in patient_data:
            opt = patient_data[sex_key]["option_number"]
            session.sex = "남" if opt == 1 else "여"
        
        age_key = find_key("나이")
        if age_key and age_key in patient_data:
            opt = patient_data[age_key]["option_number"]
            # Map age category to actual age range
            age_ranges = {1: (10, 19), 2: (20, 39), 3: (40, 54), 4: (55, 69), 5: (70, 85)}
            age_range = age_ranges.get(opt, (20, 80))
            session.age = random.randint(age_range[0], age_range[1])
        
        job_key = find_key("직업")
        if job_key and job_key in patient_data:
            opt = patient_data[job_key]["option_number"]
            job_map = {
                1: "사무직", 2: "사무직", 
                3: "사무직", 4: "사무직",
                5: "사무직", 6: "현장직",
                7: "현장직", 8: "현장직",
                9: "현장직", 10: "사무직",
                11: "사무직"
            }
            session.job = job_map.get(opt, "사무직")
        
        # Height/Weight from category
        height_key = find_key("키")
        if height_key and height_key in patient_data:
            opt = patient_data[height_key]["option_number"]
            # Map to approximate height ranges - SEX SPECIFIC
            if session.sex == "남":
                # Male height ranges (Korean average ~172cm)
                height_ranges = {1: (155, 162), 2: (163, 170), 3: (171, 178), 4: (179, 186), 5: (187, 195)}
            else:
                # Female height ranges (Korean average ~159cm, max 170cm)
                height_ranges = {1: (145, 152), 2: (153, 158), 3: (159, 165), 4: (166, 170), 5: (168, 170)}
            h_range = height_ranges.get(opt, (160, 175) if session.sex == "남" else (152, 165))
            session.height = random.randint(h_range[0], h_range[1])
        
        weight_key = find_key("몸무게")
        if weight_key and weight_key in patient_data:
            opt = patient_data[weight_key]["option_number"]
            weight_ranges = {1: (45, 55), 2: (56, 63), 3: (64, 76), 4: (77, 85), 5: (86, 100)}
            w_range = weight_ranges.get(opt, (55, 85))
            session.weight = random.randint(w_range[0], w_range[1])
        
        # Vitals - use actual CSV keys
        temp_key = find_key("체온")
        if temp_key and temp_key in patient_data:
            opt = patient_data[temp_key]["option_number"]
            temp_ranges = {1: (34.5, 35.5), 2: (36.0, 37.3), 3: (37.4, 37.9), 4: (38.0, 39.9), 5: (40.0, 41.0)}
            t_range = temp_ranges.get(opt, (36.0, 37.5))
            session.temp = round(random.uniform(t_range[0], t_range[1]), 1)
        
        pulse_key = find_key("맥박")
        if pulse_key and pulse_key in patient_data:
            opt = patient_data[pulse_key]["option_number"]
            pulse_ranges = {1: (45, 50), 2: (50, 60), 3: (60, 80), 4: (80, 100), 5: (100, 120)}
            p_range = pulse_ranges.get(opt, (60, 90))
            session.pulse_rate = random.randint(p_range[0], p_range[1])
        
        resp_key = find_key("호흡")
        if resp_key and resp_key in patient_data:
            opt = patient_data[resp_key]["option_number"]
            resp_ranges = {1: (8, 12), 2: (12, 20), 3: (21, 28)}
            r_range = resp_ranges.get(opt, (12, 20))
            session.resp = random.randint(r_range[0], r_range[1])
        
        bp_key = find_key("혈압")
        if bp_key and bp_key in patient_data:
            opt = patient_data[bp_key]["option_number"]
            bp_ranges = {
                1: ((80, 90), (50, 60)),      # 저혈압
                2: ((100, 119), (60, 79)),    # 정상
                3: ((120, 139), (80, 89)),    # 고혈압전단계
                4: ((140, 159), (90, 99)),    # 고혈압1기
                5: ((160, 179), (100, 109))   # 고혈압2기
            }
            sbp_range, dbp_range = bp_ranges.get(opt, ((100, 140), (60, 90)))
            session.sbp = random.randint(sbp_range[0], sbp_range[1])
            session.dbp = random.randint(dbp_range[0], dbp_range[1])
        
        # Disease-specific symptoms
        if disease_name == "감기":
            apply_cold_symptoms(session, patient_data)
        elif disease_name == "알레르기비염":
            apply_rhinitis_symptoms(session, patient_data)
        elif disease_name == "기능성소화불량":
            apply_dyspepsia_symptoms(session, patient_data)
        elif disease_name == "요통":
            apply_backpain_symptoms(session, patient_data)
        
        # Common symptoms (diet, stool, urine, sleep, etc.)
        apply_common_symptoms(session, patient_data)
        
        return True
        
    except Exception as e:
        print(f"Error in CSV-based randomization: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# ORIGINAL RANDOMIZATION (Keep for fallback/other diseases)
# ============================================================================

def get_weighted_level(variable_key, pattern_key, levels=None):
    """
    Select a level (1-5) based on weighted probabilities from CLINICAL_DATA.
    
    Args:
        variable_key: The variable name in CLINICAL_DATA (e.g., 'fever_sev')
        pattern_key: The pattern identifier (e.g., 'Cold_WC', 'R_Minor')
        levels: Optional list of levels to choose from (default: [1,2,3,4,5])
    
    Returns:
        A single level value selected based on probability weights
    """
    if levels is None:
        levels = [1, 2, 3, 4, 5]
    
    weights = []
    for lvl in levels:
        w_dict = get_weights(variable_key, lvl)
        # Get weight for specific pattern, default to 0.1 for uniform fallback
        weights.append(w_dict.get(pattern_key, 0.1))
    
    # Ensure at least some weight exists to avoid error
    if sum(weights) == 0:
        weights = [1] * len(levels)  # Uniform fallback
    
    return random.choices(levels, weights=weights, k=1)[0]


def randomize_inputs(st, randomize_disease=True):
    """Randomize all patient input fields.
    
    Args:
        st: Streamlit instance (or mock)
        randomize_disease: If True, always randomize the disease. 
                          If False, keep existing disease if set (for batch generation).
    """
    session = st.session_state
    
    log_layer_start("LAYER 1: Hardcoded Random Values")
    
    # ===========================================
    # 1. DEMOGRAPHICS (인구학적정보)
    # NOTE: Minimum age = 10 to match CSV rule categories (options 1-5 start at age 10-19)
    # UI BOUNDS: height min=130, weight min=30
    # ===========================================
    session.age = random.randint(10, 85)  # Min 10 to match CSV rules
    session.sex = random.choice(["남", "여"])
    session.job = random.choice(["학생", "사무직", "현장직", "가사"])
    
    # Height: Sex-specific ranges (Korean averages)
    # 남성 평균: ~172cm, 여성 평균: ~159cm
    if session.sex == "남":
        session.height = random.randint(160, 185)  # Male: 160-185cm
    else:
        session.height = random.randint(150, 170)  # Female: 150-170cm (max adjusted per feedback)
    
    session.weight = random.randint(45, 100)   # Adjusted for age 10+, UI min is 30
    log_value_set("age/sex/job/height/weight", f"{session.age}/{session.sex}/.../...", "HARDCODED")
    
    # ===========================================
    # 2. VITALS (SAFETY RULES - Keep within safe clinical ranges)
    # ===========================================
    session.sbp = random.randint(95, 170)
    session.dbp = random.randint(60, 100)
    if session.dbp >= session.sbp:
        session.dbp = session.sbp - random.randint(20, 40)
    session.pulse_rate = random.randint(55, 120)
    session.temp = round(random.uniform(36.0, 40.0), 1)
    session.resp = random.randint(12, 24)
    
    # ===========================================
    # 3. HISTORY & ONSET (병력 및 경과)
    # ===========================================
    session.onset = random.choice(["1일 전", "2-3일 전", "1주 전", "만성 3개월 이상"])
    session.course = random.choice(["악화중", "호전중", "비슷/오르내림"])
    
    # 발병 에피소드는 질환이 선택된 후에 생성됨 (아래 참조)
    # Episode will be generated after disease is selected (see below)
    
    session.history_conditions = random.sample(["고혈압", "당뇨", "이상지질혈증", "기타"], k=random.randint(0, 2))
    log_value_set("history_conditions", session.history_conditions, "HARDCODED (will be overwritten by CSV)")
    session.meds_specific = random.sample(["혈압약", "당뇨약", "이상지질혈증약", "수면제", "항우울제", "항불안제"], k=random.randint(0, 3))
    session.family_hx = random.sample(["고혈압", "당뇨", "이상지질혈증", "심장병", "중풍", "기타"], k=random.randint(0, 2))
    session.past_cold_problem_area = random.sample(PAST_COLD_PROBLEM_AREAS, k=random.randint(0, 2))
    session.aggravating_factors = random.sample(AGGRAVATING_FACTORS, k=random.randint(0, 3))
    session.relieving_factors = random.sample(RELIEVING_FACTORS, k=random.randint(0, 2))
    
    # Additional Symptoms & Comorbidities (추가 증상 및 동반질환 - Pages 24-25)
    # Pass sex and age parameters to exclude menstrual symptoms for males and young children
    session.additional_symptoms = get_random_additional_symptoms(count=random.randint(1, 2), sex=session.sex, age=session.age)
    session.additional_comorbidities = get_random_comorbidities(count=random.randint(0, 2))
    
    # Social History (사회력)
    session.social_alcohol_freq = random.choice(["비음주", "주간", "매일"])
    session.social_alcohol_amt = round(random.uniform(0, 5), 1) if session.social_alcohol_freq != "비음주" else 0.0
    session.social_smoke_daily = round(random.uniform(0, 20), 1)
    session.social_exercise_int = random.choice(["저", "중", "고"])
    session.social_exercise_time = random.randint(0, 120)
    
    # ===========================================
    # 4. WOMEN'S HEALTH (여성력)
    # ===========================================
    if session.sex == "여":
        # 나이에 따른 폐경 확률 조정
        if session.age >= 55:
            # 55세 이상: 대부분 폐경
            session.mens_regular = random.choices(["폐경", "불규칙"], weights=[90, 10])[0]
        elif session.age >= 45:
            # 45-54세: 폐경 가능성 있음
            session.mens_regular = random.choices(["규칙", "불규칙", "폐경"], weights=[30, 40, 30])[0]
        else:
            # 45세 미만: 폐경 거의 없음
            session.mens_regular = random.choices(["규칙", "불규칙"], weights=[70, 30])[0]
        
        # 폐경인 경우 생리 관련 정보 초기화
        if session.mens_regular == "폐경":
            session.mens_cycle = 0
            session.mens_duration = 0
            session.mens_pain_score = 0
            session.mens_amt = "N/A"
            session.mens_clot = False
            session.mens_color = "N/A"
        else:
            session.mens_cycle = random.randint(21, 35)
            session.mens_amt = random.choice(["적음", "보통", "많음"])
            session.mens_clot = random.choice([True, False])
            session.mens_color = random.choice(["연함", "적색", "흑자색"])
            session.mens_duration = random.randint(3, 7)
            session.mens_pain_score = random.randint(0, 10)
    
    # ===========================================
    # 5. EXCRETION & DIET (배설 및 식사)
    # ===========================================
    session.diet_speed = random.choice(["빠름 (<10분)", "보통 (20분)", "느림 (>30분)"])
    session.appetite = random.choice(["없음", "저하", "보통", "항진"])
    session.diet_freq = random.choice([1, 2, 3, 4])
    session.diet_regular = random.choice(["규칙적", "불규칙"])
    session.water_intake = random.choice(["0.5L 미만", "0.5-1L", "1-2L", "2L 이상"])
    
    session.stool_freq = random.choice(["1회/일", "2-3회/일", "변비"])
    session.stool_form = random.choice(["보통", "묽음/연변", "굳음/경변"])
    session.stool_discomfort = random.choice([True, False])
    session.stool_color = random.choice(["황색", "황갈색", "흑색", "녹색"])
    
    session.urine_freq_day = random.randint(3, 12)
    session.urine_freq_night = random.randint(0, 4)
    session.urine_stream = random.choice(["정상", "약함", "끊김"])
    session.urine_residual = random.choice([True, False])
    session.urine_incontinence = random.choice([True, False])
    session.urine_color = random.choice(["맑음", "황색", "적색/혈뇨"])
    
    # ===========================================
    # 6. SLEEP, SWEAT, COLD/HEAT (수면, 땀, 한열)
    # ===========================================
    session.sleep_hours = random.randint(4, 10)
    session.sleep_waking_state = random.choice(["개운함", "피곤함", "무거움"])
    session.sleep_depth = random.choice(["깊음", "얕음"])
    session.insomnia_onset = random.randint(0, 5)  # 입면장애 정도 0-5
    session.insomnia_maintain = random.randint(0, 5)  # 중도각성 정도 0-5
    session.insomnia_reentry = random.randint(0, 5)  # 재입면장애 정도 0-5
    session.dreams = random.choice(["거의 없음", "가끔", "자주", "악몽"])
    
    session.sweat_amt = random.choice(["무한 (無汗)", "보통", "다한 (多汗)"])
    session.sweat_area = random.choice(["전신", "두부", "야간/도한"])
    session.sweat_feeling = random.choice(["상쾌", "피곤/냉함", "열감"])
    
    session.cold_heat_pref = random.choice(["오한/추위탐", "보통", "열감/더위탐"])
    session.drink_temp = random.choice(["냉수", "온수", "열수"])
    
    # ===========================================
    # 7. MENTAL, SENSORY & INSPECTION
    # ===========================================
    session.personality_speed = random.randint(1, 5)
    session.personality_io = random.randint(1, 5)
    session.personality_soft = random.randint(1, 5)
    session.personality_static = random.randint(1, 5)
    
    session.emot_anger = random.randint(1, 5)
    session.emot_depress = random.randint(1, 5)
    session.emot_anxiety = random.randint(1, 5)
    session.excitement = random.randint(1, 5)
    session.emot_fear = random.randint(1, 5)
    session.emot_thought = random.randint(1, 5)
    session.emot_grief = random.randint(1, 5)
    
    session.fatigue_level = random.choice(["없음", "약함", "중등도", "심함"])
    session.voice_vol = random.choice(["작음", "보통", "큼"])
    session.voice_vol_slider = random.randint(1, 3)
    
    session.memory = random.choice(["좋음", "건망", "나쁨"])
    session.motivation = random.choice(["높음", "보통", "낮음", "무기력"])
    session.stress_coping = random.choice(["좋음", "보통", "나쁨"])
    
    session.edema = random.choice(["없음", "안면", "하지", "전신"])
    session.bruising = random.choice(["정상", "잘듦", "절로 생김"])
    session.limb_weakness = random.choice([True, False])
    session.vision_blackout = random.choice([True, False])
    
    session.body_solidity = random.choice(["물렁", "보통", "단단"])
    session.face_color = random.choice(["정상", "창백", "홍조", "황색", "암색"])
    session.face_gloss = random.choice(["칙칙", "보통", "윤기"])
    session.eye_red = random.choice([True, False])
    session.lip_dry = random.choice([True, False])
    
    session.skin_dry = random.choice(["정상", "건조", "각질"])
    session.skin_itch = random.choice([True, False])
    
    session.tinnitus_freq = random.randint(0, 5)
    session.tinnitus_sev = random.randint(0, 5)
    session.hearing_sev = random.randint(0, 5)
    session.dizziness_sev = random.randint(0, 5)
    
    session.lip_color = random.choice(["정상", "창백", "붉음", "어두움"])
    session.mouth_dry = random.randint(0, 5)
    session.throat_dry = random.choice([True, False])
    session.mouth_bitter = random.choice([True, False])
    session.bad_breath = random.choice([True, False])
    session.hiccup = random.choice([True, False])
    
    session.neck_nape_freq = random.randint(0, 5)
    session.neck_nape_sev = random.randint(0, 5)
    
    session.breath_sound = random.choice(["정상", "큼", "약함"])
    session.palpitation = random.randint(0, 5)
    session.chest_tight_freq = random.randint(0, 5)
    session.chest_tight_sev = random.randint(0, 5)
    session.chest_pain_freq = random.randint(0, 5)
    session.chest_pain_sev = random.randint(0, 5)
    session.sighing_freq = random.randint(0, 5)
    session.nausea = random.randint(0, 5)
    session.bloating = random.randint(0, 5)
    session.flatulence = random.choice(["없음", "보통", "잦음"])
    
    session.lower_abd_discomfort = random.randint(0, 5)
    session.abd_pain_sev = random.randint(0, 5)
    session.abd_pain_type = random.choice(["없음", "둔통", "예리통", "산통/경련통"])
    session.abd_tenderness = random.choice([True, False])
    session.nausea_sev = random.randint(0, 5)
    session.belching = random.randint(0, 5)
    session.belching_smell = random.choice(["없음", "신맛/산취", "부패취"])
    session.food_stag_sev = random.randint(0, 5)
    session.abd_muscle_tension = random.choice([True, False])
    session.abd_mass = random.choice([True, False])
    session.abd_pulsation = random.choice([True, False])
    session.bowel_sound = random.choice(["정상", "항진", "저하"])
    
    session.cold_heat_body = random.choice(["한 (寒)", "보통", "열 (熱)"])
    session.cold_heat_distribution = random.choice(["균등", "상열 (上熱)", "하한 (下寒)", "상열하한 (上熱下寒)"])
    session.cold_sensitivity = random.randint(1, 5)
    session.heat_sensitivity = random.randint(1, 5)
    
    session.physical_strength = random.choice(["허약", "보통", "강건"])
    session.condition_bad_area = random.sample(["두부", "위장", "요배부", "사지"], k=random.randint(0, 2))
    
    session.sweat_time = random.choice(["주간", "야간/도한", "운동시"])
    
    session.mental_clarity = random.choice(["맑음/청명", "흐릿/혼미", "혼란"])
    session.mood_swing = random.choice(["안정", "약간", "심함"])
    session.emot_startle = random.randint(1, 5)
    
    session.flank_freq = random.randint(0, 5)
    session.flank_sev = random.randint(0, 5)
    session.back_freq = random.randint(0, 5)
    session.back_sev = random.randint(0, 5)
    session.pelvis_freq = random.randint(0, 5)
    session.pelvis_sev = random.randint(0, 5)
    session.shoulder_freq = random.randint(0, 5)
    session.shoulder_sev = random.randint(0, 5)
    session.elbow_freq = random.randint(0, 5)
    session.elbow_sev = random.randint(0, 5)
    session.hand_foot_freq = random.randint(0, 5)
    session.hand_foot_sev = random.randint(0, 5)
    session.leg_discomfort = random.randint(0, 5)
    session.knee_freq = random.randint(0, 5)
    session.knee_sev = random.randint(0, 5)
    
    # ===========================================
    # 8. PULSE & TONGUE (맥진 및 설진)
    # ===========================================
    # 맥진: 질환별 허용 맥 규칙 적용 (pulse_rules.py에서 처리)
    # 기본값 설정 (apply_pulse_rules에서 덮어씀)
    session.compound_pulse = "완맥"  # 복합맥 (출력용)
    session.pulse_depth = random.choice(["부맥", "중맥", "침맥"])
    session.pulse_width = random.choice(["세맥", "대맥", "홍맥"])
    session.pulse_length = random.choice(["단맥", "장맥", "장맥"])
    session.pulse_strength = random.choice(["무력", "유력", "강력"])
    session.pulse_smooth = random.choice(["활맥", "완맥", "삽맥"])
    session.pulse_tension = random.choice(["유맥", "완맥", "긴맥"])
    
    session.tongue_color = random.choice(["담백", "담홍", "홍설", "강홍/자설"])
    session.tongue_size = random.choice(["소", "정상", "대/태"])
    session.tongue_coat_color = random.choice(["백태", "황태", "회태"])
    session.tongue_coat_thick = random.choice(["박태", "후태", "니태"])
    session.tongue_coat_particle = random.choice(["조태", "윤태", "활태"])
    session.tongue_marks = random.choice([True, False])
    
    # ===========================================
    # 9. PAIN GRID
    # ===========================================
    for part in ["pain_neck", "pain_shoulder", "pain_back", "pain_knee", "pain_hand", "pain_elbow", "pain_flank", "pain_pelvis", "pain_hip"]:
        freq = random.randint(0, 5)
        intensity = random.randint(0, 10) if freq > 0 else 0
        session[part] = [freq, intensity]
        session[f"{part}_f"] = freq
        session[f"{part}_i"] = intensity
    
    session.cold_hands_feet = random.choice([True, False])
    
    # ===========================================
    # 10. DISEASE & PATTERN SELECTION
    # All 4 diseases are now supported with CSV rules:
    # 감기, 알레르기비염, 기능성소화불량, 요통
    # ===========================================
    # Use Korean disease names to match UI dropdown options
    supported_disease_opts = [
        "감기/급성상기도감염", 
        "알레르기비염",
        "기능성소화불량",
        "요통"
    ]
    
    # Randomize disease if requested, otherwise keep existing (for batch generation)
    if randomize_disease:
        session.disease = random.choice(supported_disease_opts)
    elif not hasattr(session, 'disease') or session.disease is None or session.disease == "":
        session.disease = random.choice(supported_disease_opts)
    else:
        # Normalize disease name format for consistency
        if session.disease == "감기":
            session.disease = "감기/급성상기도감염"
        elif session.disease == "기능성 소화불량":
            session.disease = "기능성소화불량"
    
    # Check for disease type using Korean keywords
    if "감기" in session.disease:
        num_patterns = len(DISEASE_PATTERNS["감기"]["patterns"])
        session.pattern_idx = random.randint(0, num_patterns - 1)
        # Try to use CSV-based randomization for Cold
        _apply_csv_cold_randomization(st)
    elif "비염" in session.disease:
        num_patterns = len(DISEASE_PATTERNS["알레르기비염"]["patterns"])
        session.pattern_idx = random.randint(0, num_patterns - 1)
        # Try to use CSV-based randomization for Rhinitis
        _apply_csv_rhinitis_randomization(st)
    elif "소화불량" in session.disease:
        num_patterns = len(DISEASE_PATTERNS["기능성소화불량"]["patterns"])
        session.pattern_idx = random.randint(0, num_patterns - 1)
        # Try to use CSV-based randomization for Dyspepsia
        _apply_csv_dyspepsia_randomization(st)
    elif "요통" in session.disease:
        num_patterns = len(DISEASE_PATTERNS["요통"]["patterns"])
        session.pattern_idx = random.randint(0, num_patterns - 1)
        # Try to use CSV-based randomization for Back Pain
        _apply_csv_backpain_randomization(st)
    
    # ===========================================
    # 10.5 발병 에피소드 생성 (Episode generation)
    # 질환이 선택된 후에 생성해야 올바른 에피소드가 매칭됨
    # ===========================================
    # Map disease names to episode template keys
    if "감기" in session.disease:
        episode_disease_key = "감기"
    elif "비염" in session.disease:
        episode_disease_key = "알레르기비염"
    elif "소화불량" in session.disease:
        episode_disease_key = "기능성소화불량"
    elif "요통" in session.disease:
        episode_disease_key = "요통"
    else:
        episode_disease_key = "감기"  # fallback
    
    session.episode = generate_episode(episode_disease_key)
    
    # ===========================================
    # 11. APPLY CONSTRAINT RULES
    # Constraints must be applied HERE during randomization,
    # NOT during patient generation (after widgets are rendered)
    # because Streamlit prevents modifying widget-bound session_state
    # ===========================================
    log_layer_start("LAYER 3: Constraint Rules")
    apply_constraint_rules(st)
    log_layer_start("LAYER 4: Symptom Correlation Rules")
    apply_symptom_correlation_rules(st.session_state)
    
    # ===========================================
    # FINAL SAFETY CLAMP: Ensure all values are within UI bounds
    # This prevents Streamlit errors when widget values < min_value
    # ===========================================
    log_layer_start("LAYER 5: UI Bounds Safety Clamp")
    session = st.session_state
    # Age: UI min=10, max=100
    session.age = max(10, min(100, session.age))
    # Height: UI min=130, max=220
    session.height = max(130, min(220, session.height))
    # Weight: UI min=30, max=150
    session.weight = max(30, min(150, session.weight))
    # SBP: UI min=90, max=180
    session.sbp = max(90, min(180, session.sbp))
    # DBP: UI min=50, max=120
    session.dbp = max(50, min(120, session.dbp))
    # Pulse: UI min=50, max=130
    session.pulse_rate = max(50, min(130, session.pulse_rate))
    # Temp: UI min=35.0, max=40.5
    session.temp = max(35.0, min(40.5, session.temp))
    # Resp: UI min=8, max=30
    session.resp = max(8, min(30, session.resp))
    
    log_layer_start("RANDOMIZATION COMPLETE")
    log_value_set("FINAL history_conditions", st.session_state.history_conditions, "After all layers")


def _apply_csv_cold_randomization(st):
    """Apply CSV-based randomization for Common Cold (감기)."""
    if not CSV_RULES_AVAILABLE:
        return
    
    session = st.session_state
    
    # Get the pattern name for CSV lookup
    patterns = DISEASE_PATTERNS["감기"]["patterns"]
    idx = session.get("pattern_idx", 0)
    if 0 <= idx < len(patterns):
        pattern_name = patterns[idx]["name"]  # e.g., "풍한형" or "풍열형"
    else:
        pattern_name = None
    
    # Use CSV-based randomization
    success = randomize_from_csv_rules(st, "감기", pattern_name)
    if not success:
        print("Warning: CSV randomization failed for 감기, using fallback")


def _apply_csv_rhinitis_randomization(st):
    """Apply CSV-based randomization for Allergic Rhinitis (알레르기비염)."""
    if not CSV_RULES_AVAILABLE:
        return
    
    session = st.session_state
    
    # Get the pattern/prescription name for CSV lookup
    patterns = DISEASE_PATTERNS["알레르기비염"]["patterns"]
    idx = session.get("pattern_idx", 0)
    if 0 <= idx < len(patterns):
        # For rhinitis, we use prescription name as pattern (e.g., "소청룡탕")
        prescriptions = patterns[idx].get("prescriptions", [])
        pattern_name = prescriptions[0] if prescriptions else None
    else:
        pattern_name = None
    
    # Use CSV-based randomization
    success = randomize_from_csv_rules(st, "알레르기비염", pattern_name)
    if not success:
        print("Warning: CSV randomization failed for 알레르기비염, using fallback")


def _apply_csv_dyspepsia_randomization(st):
    """Apply CSV-based randomization for Functional Dyspepsia (기능성소화불량)."""
    if not CSV_RULES_AVAILABLE:
        return
    
    session = st.session_state
    
    # Get the pattern name for CSV lookup (한증형, 열증형, 기허형, etc.)
    patterns = DISEASE_PATTERNS["기능성소화불량"]["patterns"]
    idx = session.get("pattern_idx", 0)
    if 0 <= idx < len(patterns):
        # Extract pattern name (e.g., "한증형" from "한증형 (寒證型)")
        full_pattern_name = patterns[idx]["name"]
        pattern_name = full_pattern_name.split()[0] if full_pattern_name else None
    else:
        pattern_name = None
    
    # Use CSV-based randomization
    success = randomize_from_csv_rules(st, "기능성소화불량", pattern_name)
    if success:
        # Apply dyspepsia-specific symptoms
        try:
            patient_data = generate_patient_from_rules("기능성소화불량", pattern_name)
            if patient_data:
                apply_dyspepsia_symptoms(session, patient_data)
        except Exception as e:
            print(f"Warning: Failed to apply dyspepsia symptoms: {e}")
    else:
        print("Warning: CSV randomization failed for 기능성소화불량, using fallback")


def _apply_csv_backpain_randomization(st):
    """Apply CSV-based randomization for Back Pain (요통)."""
    if not CSV_RULES_AVAILABLE:
        return
    
    session = st.session_state
    
    # Get the pattern name for CSV lookup (한증형, 열증형, 기허형, etc.)
    patterns = DISEASE_PATTERNS["요통"]["patterns"]
    idx = session.get("pattern_idx", 0)
    if 0 <= idx < len(patterns):
        # Extract pattern name (e.g., "한증형" from "한증형 (寒證型)")
        full_pattern_name = patterns[idx]["name"]
        pattern_name = full_pattern_name.split()[0] if full_pattern_name else None
    else:
        pattern_name = None
    
    # Use CSV-based randomization
    success = randomize_from_csv_rules(st, "요통", pattern_name)
    if success:
        # Apply back pain-specific symptoms
        try:
            patient_data = generate_patient_from_rules("요통", pattern_name)
            if patient_data:
                apply_backpain_symptoms(session, patient_data)
        except Exception as e:
            print(f"Warning: Failed to apply back pain symptoms: {e}")
    else:
        print("Warning: CSV randomization failed for 요통, using fallback")

