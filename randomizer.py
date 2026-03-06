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

def log_value_set(field_name: str, value, source: str):
    """Log when a session state value is set."""
    if ENABLE_RANDOMIZER_LOGGING:
        randomizer_logger.debug(f"SET {field_name} = {value} [Source: {source}]")

def log_layer_start(layer_name: str):
    """Log when a layer starts."""
    if ENABLE_RANDOMIZER_LOGGING:
        randomizer_logger.info(f"{'='*50}")
        randomizer_logger.info(f"STARTING: {layer_name}")
        randomizer_logger.info(f"{'='*50}")


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
# EPISODE GENERATION (발병 에피소드)
# ============================================================================

# Disease-specific episode templates (발병 에피소드 템플릿)
EPISODE_TEMPLATES = {
    "감기": [
        "영하 {temp}도의 추운 날씨에 버스 정류장에서 {time}분간 대기한 후 다음날부터 증상이 시작되었다.",
        "에어컨이 강하게 작동하는 사무실에서 {hours}시간 근무 후 퇴근길에 오한이 시작되었다.",
        "비를 맞고 젖은 옷을 갈아입지 못한 채 {hours}시간가량 지낸 후 발열이 시작되었다.",
        "수영장에서 수영 후 머리를 말리지 않고 외출하였고 다음날부터 콧물이 시작되었다.",
        "환절기에 얇은 옷차림으로 외출하였다가 저녁부터 몸살 기운이 시작되었다.",
        "감기에 걸린 가족을 간호하던 중 본인도 {days}일 후 비슷한 증상이 발생하였다.",
        "과로와 수면 부족이 {days}일간 지속된 후 면역력이 저하되어 증상이 발생하였다.",
        "야근이 {days}일간 계속된 후 피로가 누적되어 감기 증상이 나타났다.",
    ],
    "알레르기비염": [
        "봄철 꽃가루가 날리기 시작한 후 {days}일째 증상이 악화되었다.",
        "새로 이사한 집에서 {days}일간 지낸 후 증상이 시작되었다.",
        "반려동물(고양이/개)을 키우는 친구 집을 방문한 후 증상이 시작되었다.",
        "환절기 기온 변화가 심해지면서 {days}일 전부터 증상이 악화되었다.",
        "황사/미세먼지가 심한 날 외출 후 저녁부터 재채기와 콧물이 심해졌다.",
        "집 대청소를 한 후 먼지에 노출되어 증상이 악화되었다.",
        "새 카펫을 깐 후 {days}일째부터 코막힘이 심해졌다.",
        "직장에서 새 사무실로 이동한 후 {days}일째 증상이 시작되었다.",
    ],
    "기능성소화불량": [
        "회식에서 과음과 과식을 한 다음날부터 증상이 시작되었다.",
        "스트레스가 심한 업무가 {days}일간 계속된 후 소화불량이 시작되었다.",
        "기름진 음식을 과식한 후 {hours}시간 뒤부터 속이 불편하기 시작하였다.",
        "불규칙한 식사가 {days}일간 지속된 후 증상이 발생하였다.",
        "야식을 먹고 바로 누운 후 다음날 아침부터 속쓰림이 시작되었다.",
        "매운 음식을 먹은 후 {hours}시간 뒤부터 복부 불편감이 시작되었다.",
        "중요한 시험/면접을 앞두고 긴장하면서 {days}일 전부터 식욕이 떨어지기 시작하였다.",
        "장기간 진통제 복용 후 {days}일째부터 속쓰림이 시작되었다.",
    ],
    "요통": [
        "무거운 물건을 들다가 '뚝' 소리와 함께 허리 통증이 시작되었다.",
        "장시간 운전 후 차에서 내리면서 허리가 뻣뻣해지기 시작하였다.",
        "오랜 시간 책상에 앉아 일한 후 {days}일 전부터 허리가 아프기 시작하였다.",
        "골프/테니스를 치다가 스윙하는 순간 허리에 통증이 발생하였다.",
        "이사할 때 짐을 나르다가 허리를 삐끗하였다.",
        "잠을 잘못 자고 일어난 후 아침부터 허리가 뻣뻣하고 아팠다.",
        "계단에서 미끄러져 엉덩방아를 찧은 후 허리 통증이 시작되었다.",
        "추운 날씨에 야외 작업을 {hours}시간 한 후 허리가 굳어지기 시작하였다.",
        "헬스장에서 데드리프트 운동 중 허리에 통증이 발생하였다.",
        "장거리 비행기 탑승 후 내리면서 허리 통증이 시작되었다.",
    ]
}


def _generate_episode(disease: str) -> str:
    """
    Generate a random episode (발병 에피소드) for the given disease.
    
    Args:
        disease: Disease name in Korean (감기, 알레르기비염, 기능성소화불량, 요통)
    
    Returns:
        A randomly generated episode string
    """
    templates = EPISODE_TEMPLATES.get(disease, EPISODE_TEMPLATES["감기"])
    template = random.choice(templates)
    
    # Fill in placeholders with random values
    episode = template.format(
        temp=random.randint(5, 15),
        time=random.randint(20, 60),
        hours=random.randint(2, 8),
        days=random.randint(2, 7)
    )
    
    return episode


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
            _apply_cold_symptoms(session, patient_data)
        elif disease_name == "알레르기비염":
            _apply_rhinitis_symptoms(session, patient_data)
        elif disease_name == "기능성소화불량":
            _apply_dyspepsia_symptoms(session, patient_data)
        elif disease_name == "요통":
            _apply_backpain_symptoms(session, patient_data)
        
        # Common symptoms (diet, stool, urine, sleep, etc.)
        _apply_common_symptoms(session, patient_data)
        
        return True
        
    except Exception as e:
        print(f"Error in CSV-based randomization: {e}")
        import traceback
        traceback.print_exc()
        return False


def _apply_cold_symptoms(session, patient_data):
    """Apply cold-specific symptoms from CSV data."""
    
    # Onset
    if "감기환자_O/S_감기증상 발현시점" in patient_data:
        opt = patient_data["감기환자_O/S_감기증상 발현시점"]["option_number"]
        onset_map = {
            1: "1일 전", 
            2: "2-3일 전", 
            3: "1주 전",
            4: "2주 전",
            5: "1개월 전",
            6: "만성 3개월 이상"
        }
        session.onset = onset_map.get(opt, "2-3일 전")
    
    # Fever severity - map to temp if not already set
    if "감기환자_감기주소증 유형_발열" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_발열"]["option_number"]
        # Store as severity level for UI display
        session.fever_sev = int(opt) if opt else 1
    
    # Chills severity
    if "감기환자_감기주소증 유형_오한" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_오한"]["option_number"]
        session.chills_sev = int(opt) if opt else 1
    
    # Nasal discharge amount
    if "감기환자_감기주소증 유형_콧물 감기" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_콧물 감기"]["option_number"]
        session.snot_sev = int(opt) if opt else 1
    
    # Nasal discharge color - map option number to UI string
    if "감기환자_감기주소증 유형_콧물 색" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_콧물 색"]["option_number"]
        snot_color_map = {
            1: "없음",
            2: "맑음/투명",
            3: "백색",
            4: "황색",
            5: "녹색"
        }
        session.snot_color = snot_color_map.get(opt, "없음")
    
    # Nasal congestion
    if "감기환자_감기주소증 유형_코막힘" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_코막힘"]["option_number"]
        session.nasal_congestion = opt
    
    # Sore throat
    if "감기환자_감기주소증 유형_인후통" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_인후통"]["option_number"]
        session.sore_throat = opt
    
    # Sneezing
    if "감기환자_감기주소증 유형_재채기" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_재채기"]["option_number"]
        session.sneeze_sev = opt
    
    # Cough
    if "감기환자_감기주소증 유형_기침" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_기침"]["option_number"]
        session.cough_sev = int(opt) if opt else 1
    
    # Phlegm amount
    if "감기환자_감기주소증 유형_담(가래) 양" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_담(가래) 양"]["option_number"]
        session.phlegm_amt = int(opt) if opt else 0
    
    # Phlegm color - map option number to UI string
    if "감기환자_감기주소증 유형_담(가래) 색" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_담(가래) 색"]["option_number"]
        phlegm_color_map = {
            1: "맑음",
            2: "백색",
            3: "황색",
            4: "녹색"
        }
        session.phlegm_color = phlegm_color_map.get(opt, "맑음")
    
    # Body ache
    if "감기환자_감기주소증 유형_몸살, 신체통, 근육통" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_몸살, 신체통, 근육통"]["option_number"]
        session.body_ache = opt
    
    # Body heaviness
    if "감기환자_감기주소증 유형_신중(身重)" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_신중(身重)"]["option_number"]
        session.body_heavy = opt
    
    # Headache
    if "감기환자_감기주소증 유형_두부, 뒷목 불편감(강도)" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_두부, 뒷목 불편감(강도)"]["option_number"]
        session.headache = opt
    
    # Sweating during cold
    if "감기환자_감기주소증 유형_감기 시 땀 유무" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_감기 시 땀 유무"]["option_number"]
        session.sweat_during_cold = opt
        # Also set sweat amount based on this
        sweat_map = {1: "무한", 2: "보통", 3: "보통", 4: "다한", 5: "다한"}
        session.sweat_amt = sweat_map.get(opt, "보통")
    
    # Throat exam - map to UI string values
    if "감기환자_한의사 진찰 및 검사소견_인후부 진찰" in patient_data:
        opt = patient_data["감기환자_한의사 진찰 및 검사소견_인후부 진찰"]["option_number"]
        session.throat_redness = opt
        # Map to exam_throat_visual UI option
        throat_visual_map = {
            1: "정상",
            2: "발적",
            3: "부종",
            4: "삼출물"
        }
        session.exam_throat_visual = throat_visual_map.get(opt, "정상")
    else:
        session.exam_throat_visual = random.choice(["정상", "발적", "부종"])
    
    # Tonsil exam - map to UI string values
    if "감기환자_한의사 진찰 및 검사소견_편도진찰" in patient_data:
        opt = patient_data["감기환자_한의사 진찰 및 검사소견_편도진찰"]["option_number"]
        session.tonsil_swelling = opt
        # Map to exam_tongue_depressor UI option
        tongue_dep_map = {
            1: "정상",
            2: "편도비대",
            3: "삼출물",
            4: "염증"
        }
        session.exam_tongue_depressor = tongue_dep_map.get(opt, "정상")
    else:
        session.exam_tongue_depressor = random.choice(["정상", "편도비대"])
    
    # Stethoscope exam (lung sounds)
    if "감기환자_한의사 진찰 및 검사소견_호흡음(폐음) 진찰" in patient_data:
        opt = patient_data["감기환자_한의사 진찰 및 검사소견_호흡음(폐음) 진찰"]["option_number"]
        stethoscope_map = {
            1: "정상",
            2: "수포음",
            3: "천명음",
            4: "감소"
        }
        session.exam_stethoscope = stethoscope_map.get(opt, "정상")
    else:
        session.exam_stethoscope = random.choice(["정상", "수포음"])
    
    # Rhinoscope exam
    if "감기환자_한의사 진찰 및 검사소견_비경 검사" in patient_data:
        opt = patient_data["감기환자_한의사 진찰 및 검사소견_비경 검사"]["option_number"]
        rhinoscope_map = {
            1: "정상",
            2: "충혈"
        }
        session.exam_rhinoscope_finding = rhinoscope_map.get(opt, "정상")
    else:
        session.exam_rhinoscope_finding = random.choice(["정상", "충혈", "분비물"])
    
    # Smell reduction
    if "감기환자_감기주소증 유형_후각 감퇴" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_후각 감퇴"]["option_number"]
        session.smell_reduction = int(opt) if opt else 0
    else:
        session.smell_reduction = random.randint(0, 3)
    
    # Alternating chills-fever
    if "감기환자_감기주소증 유형_한열왕래" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_한열왕래"]["option_number"]
        session.alternating_chills_fever = int(opt) if opt else 0
    else:
        session.alternating_chills_fever = random.randint(0, 3)
    
    # Dyspnea
    if "감기환자_감기주소증 유형_숨이 가쁨" in patient_data:
        opt = patient_data["감기환자_감기주소증 유형_숨이 가쁨"]["option_number"]
        session.cold_dyspnea = bool(opt >= 2)
    else:
        session.cold_dyspnea = random.choice([True, False, False])  # Usually False
    
    # Cold onset specific (days)
    if "감기환자_O/S_감기증상 발현시점" in patient_data:
        opt = patient_data["감기환자_O/S_감기증상 발현시점"]["option_number"]
        onset_specific_map = {
            1: "1일 전",
            2: "2일 전",
            3: "3일 전",
            4: "4일 전",
            5: "5일 전",
            6: "1주일 전"
        }
        session.cold_onset_specific = onset_specific_map.get(opt, "3일 전")
    else:
        session.cold_onset_specific = random.choice(["1일 전", "2일 전", "3일 전", "4일 전", "5일 전"])
    
    # =========================================================================
    # Set cold_symptoms_spec based on pattern and CSV data
    # This maps various CSV symptoms to the UI multiselect options
    # =========================================================================
    cold_symptoms = []
    
    # Check for sweating (무한 = no sweat = 풍한)
    sweat_opt = patient_data.get("감기환자_감기주소증 유형_감기 시 땀 유무", {}).get("option_number", 3)
    if sweat_opt == 1:  # No sweating
        cold_symptoms.append("무한 (無汗) - 풍한")
    
    # Check phlegm color for yellow (황담 = 풍열)
    phlegm_color_opt = patient_data.get("감기환자_감기주소증 유형_담(가래) 색", {}).get("option_number", 1)
    if phlegm_color_opt == 3:  # Yellow
        cold_symptoms.append("황담 (黃痰) - 풍열")
    elif phlegm_color_opt in [1, 2]:  # Clear or White
        cold_symptoms.append("희박담 (稀薄白痰) - 풍한")
    
    # Check for sore throat/dry throat (인후건조 = 풍조)
    throat_opt = patient_data.get("감기환자_감기주소증 유형_인후통", {}).get("option_number", 1)
    if throat_opt >= 3:  # Significant throat symptoms
        cold_symptoms.append("인후건조 (咽乾) - 풍조")
    
    # Check for body ache (골절동통 = 풍한)
    body_ache_opt = patient_data.get("감기환자_감기주소증 유형_몸살, 신체통, 근육통", {}).get("option_number", 1)
    if body_ache_opt >= 3:  # Significant body ache
        cold_symptoms.append("골절동통 (骨節疼痛) - 풍한")
    
    # Check cough with little phlegm (객담소 = 풍조)
    cough_opt = patient_data.get("감기환자_감기주소증 유형_기침", {}).get("option_number", 1)
    phlegm_amt_opt = patient_data.get("감기환자_감기주소증 유형_담(가래) 양", {}).get("option_number", 1)
    if cough_opt >= 3 and phlegm_amt_opt <= 2:  # Cough but little phlegm
        cold_symptoms.append("객담소 (咳嗽少痰) - 풍조")
    
    # Set cold_symptoms_spec (ensure at least 1-2 symptoms for realism)
    if not cold_symptoms:
        # Default based on randomization
        cold_symptoms = random.sample([
            "무한 (無汗) - 풍한",
            "희박담 (稀薄白痰) - 풍한",
            "골절동통 (骨節疼痛) - 풍한"
        ], k=random.randint(1, 2))
    
    session.cold_symptoms_spec = cold_symptoms
    
    # =========================================================================
    # Set cold chief complaint checkboxes based on CSV data
    # =========================================================================
    # Sore throat checkbox
    session.sore_throat = bool(throat_opt >= 2)
    
    # Body ache checkbox
    session.body_ache_cold = bool(body_ache_opt >= 2)
    
    # Body heaviness checkbox
    body_heavy_opt = patient_data.get("감기환자_감기주소증 유형_신중(身重)", {}).get("option_number", 1)
    session.body_heaviness_cold = bool(body_heavy_opt >= 2)
    
    # Headache checkbox
    headache_opt = patient_data.get("감기환자_감기주소증 유형_두부, 뒷목 불편감(강도)", {}).get("option_number", 1)
    session.headache_cold = bool(headache_opt >= 2)
    
    # Neck pain checkbox (based on headache area)
    session.neck_pain_cold = bool(headache_opt >= 3)
    
    # Sweating checkbox
    session.cold_sweating_check = bool(sweat_opt >= 3)
    
    # Cold chief type (at least 1 required)
    # [교수님 피드백] 인후통(목감기), 몸살(신체통)도 주소증으로 포함 가능하도록
    cold_chief_types = []
    if session.fever_sev >= 2:
        cold_chief_types.append("발열")
    if session.chills_sev >= 2:
        cold_chief_types.append("오한")
    if session.snot_sev >= 2:
        cold_chief_types.append("콧물")
    if session.cough_sev >= 2:
        cold_chief_types.append("기침")
    if throat_opt >= 2:
        cold_chief_types.append("인후통")  # 목감기
    
    # [교수님 피드백] 몸살(신체통) 주소증 추가
    if body_ache_opt >= 2:
        cold_chief_types.append("몸살")  # 신체통
    
    # Ensure at least 1 chief type
    if not cold_chief_types:
        cold_chief_types = ["기침"]
    
    session.cold_chief_type = cold_chief_types


def _apply_rhinitis_symptoms(session, patient_data):
    """Apply allergic rhinitis-specific symptoms from CSV data."""
    
    # Onset
    if "알러지비염가상환자_O/S_알러지비염 발현시점" in patient_data:
        opt = patient_data["알러지비염가상환자_O/S_알러지비염 발현시점"]["option_number"]
        onset_map = {
            1: "1주 전",
            2: "2-3주 전", 
            3: "1개월 전",
            4: "3개월 전",
            5: "6개월 전",
            6: "만성 1년 이상"
        }
        session.onset = onset_map.get(opt, "1개월 전")
    
    # Nasal discharge amount
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_콧물 량" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_콧물 량"]["option_number"]
        session.snot_sev = int(opt) if opt else 1
    
    # Nasal discharge color - map to snot_type for rhinitis (different UI options)
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_콧물 색" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_콧물 색"]["option_number"]
        snot_type_map = {
            1: "청수양 (淸水樣) - 맑은 콧물",
            2: "백점액 (白粘) - 희고 끈적",
            3: "황농성 (黃膿) - 누렇고 찐득"
        }
        session.snot_type = snot_type_map.get(opt, "청수양 (淸水樣) - 맑은 콧물")
    
    # Nasal congestion
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_코막힘" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_코막힘"]["option_number"]
        session.nose_block_sev = int(opt) if opt else 1
    
    # Sneezing intensity
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_재채기(정도)" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_재채기(정도)"]["option_number"]
        session.sneeze_intensity = int(opt) if opt else 1
    
    # Sneezing frequency
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_재채기(빈도)" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_재채기(빈도)"]["option_number"]
        session.sneeze_sev = int(opt) if opt else 1
    
    # Nose itching
    if "알러지비염가상환자_알러지비염 주증 및 동반증상_코 가려움" in patient_data:
        opt = patient_data["알러지비염가상환자_알러지비염 주증 및 동반증상_코 가려움"]["option_number"]
        session.nose_itch_sev = int(opt) if opt else 1


def _apply_common_symptoms(session, patient_data):
    """Apply common symptoms that are shared across diseases."""
    log_layer_start("LAYER 2: CSV-based Common Symptoms")
    
    # History conditions - use correct CSV key pattern
    hx_conditions = []
    for key in patient_data:
        if "현병력" in key and "고혈압" in key:
            if patient_data[key]["option_number"] == 2:
                hx_conditions.append("고혈압")
        elif "현병력" in key and "당뇨" in key:
            if patient_data[key]["option_number"] == 2:
                hx_conditions.append("당뇨")
        elif "현병력" in key and "이상지질혈증" in key:
            if patient_data[key]["option_number"] == 2:
                hx_conditions.append("이상지질혈증")
    session.history_conditions = hx_conditions
    log_value_set("history_conditions", hx_conditions, "CSV (현병력)")
    
    # Medications - match with history conditions
    meds = []
    if "고혈압" in hx_conditions:
        meds.append("혈압약")
    if "당뇨" in hx_conditions:
        meds.append("당뇨약")
    if "이상지질혈증" in hx_conditions:
        meds.append("이상지질혈증약")
    session.meds_specific = meds
    
    # Family history - use correct CSV key pattern
    fam_hx = []
    for key in patient_data:
        if "가족력" in key:
            if "고혈압" in key and patient_data[key]["option_number"] == 2:
                fam_hx.append("고혈압")
            elif "당뇨" in key and patient_data[key]["option_number"] == 2:
                fam_hx.append("당뇨")
            elif "심장병" in key and patient_data[key]["option_number"] == 2:
                fam_hx.append("심장병")
            elif "중풍" in key and patient_data[key]["option_number"] == 2:
                fam_hx.append("중풍")
    session.family_hx = fam_hx
    
    # Alcohol - find correct key pattern
    for key in patient_data:
        if "월간 음주 횟수" in key:
            opt = patient_data[key]["option_number"]
            freq_map = {1: "비음주", 2: "가끔", 3: "주간", 4: "자주", 5: "매일"}
            session.social_alcohol_freq = freq_map.get(opt, "비음주")
            break
    
    for key in patient_data:
        if "1회당 음주량" in key:
            opt = patient_data[key]["option_number"]
            # Map to approximate amount
            if session.social_alcohol_freq == "비음주":
                session.social_alcohol_amt = 0.0
            else:
                amt_map = {1: 0.5, 2: 1.0, 3: 2.0, 4: 3.0, 5: 4.0}
                session.social_alcohol_amt = amt_map.get(opt, 1.0)
            break
    
    # Smoking
    for key in patient_data:
        if "일간 개피" in key:
            opt = patient_data[key]["option_number"]
            smoke_map = {1: 0.0, 2: 5.0, 3: 15.0, 4: 25.0, 5: 35.0}
            session.social_smoke_daily = smoke_map.get(opt, 0.0)
            break
    
    # Exercise
    for key in patient_data:
        if "운동 강도" in key:
            opt = patient_data[key]["option_number"]
            intensity_map = {1: "저", 2: "저", 3: "중", 4: "고", 5: "고"}
            session.social_exercise_int = intensity_map.get(opt, "중")
            break
    
    for key in patient_data:
        if "1회당 평균 운동 시간" in key:
            opt = patient_data[key]["option_number"]
            time_map = {1: 0, 2: 10, 3: 30, 4: 50, 5: 75}
            session.social_exercise_time = time_map.get(opt, 30)
            break
    
    # Diet
    for key in patient_data:
        if "1회 평균식사시간" in key:
            opt = patient_data[key]["option_number"]
            speed_map = {1: "빠름", 2: "빠름", 3: "보통", 4: "느림", 5: "느림"}
            session.diet_speed = speed_map.get(opt, "보통")
            break
    
    for key in patient_data:
        if "입맛" in key:
            opt = patient_data[key]["option_number"]
            appetite_map = {1: "없음", 2: "저하", 3: "보통", 4: "항진", 5: "항진"}
            session.appetite = appetite_map.get(opt, "보통")
            break
    
    for key in patient_data:
        if "1일 식사횟수" in key:
            opt = patient_data[key]["option_number"]
            session.diet_freq = min(opt, 4)
            break
    
    for key in patient_data:
        if "식사 규칙성" in key:
            opt = patient_data[key]["option_number"]
            regular_map = {1: "규칙적", 2: "규칙적", 3: "불규칙", 4: "불규칙", 5: "불규칙"}
            session.diet_regular = regular_map.get(opt, "규칙적")
            break
    
    # Stool
    for key in patient_data:
        if "대변 횟수" in key:
            opt = patient_data[key]["option_number"]
            freq_map = {1: "변비", 2: "변비", 3: "1회/일", 4: "2-3회/일", 5: "2-3회/일"}
            session.stool_freq = freq_map.get(opt, "1회/일")
            break
    
    for key in patient_data:
        if "대변 굳기" in key:
            opt = patient_data[key]["option_number"]
            form_map = {1: "굳음/경변", 2: "굳음/경변", 3: "보통", 4: "보통", 5: "묽음/연변", 6: "묽음/연변", 7: "묽음/연변"}
            session.stool_form = form_map.get(opt, "보통")
            break
    
    # Urine
    for key in patient_data:
        if "1일 소변 횟수" in key:
            opt = patient_data[key]["option_number"]
            urine_freq_map = {1: 2, 2: 4, 3: 6, 4: 9, 5: 12}
            session.urine_freq_day = urine_freq_map.get(opt, 6)
            break
    
    for key in patient_data:
        if "야간뇨 횟수" in key:
            opt = patient_data[key]["option_number"]
            night_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 5}
            session.urine_freq_night = night_map.get(opt, 0)
            break
    
    for key in patient_data:
        if "소변 굵기" in key:
            opt = patient_data[key]["option_number"]
            stream_map = {1: "약함", 2: "약함", 3: "정상", 4: "정상", 5: "정상"}
            session.urine_stream = stream_map.get(opt, "정상")
            break
    
    # Sleep
    for key in patient_data:
        if "수면 시간" in key:
            opt = patient_data[key]["option_number"]
            hours_map = {1: 3, 2: 5, 3: 7, 4: 10, 5: 12}
            session.sleep_hours = hours_map.get(opt, 7)
            break
    
    for key in patient_data:
        if "기상시 상쾌도" in key:
            opt = patient_data[key]["option_number"]
            waking_map = {1: "무거움", 2: "피곤함", 3: "피곤함", 4: "개운함", 5: "개운함"}
            session.sleep_waking_state = waking_map.get(opt, "피곤함")
            break
    
    for key in patient_data:
        if "수면 깊이" in key:
            opt = patient_data[key]["option_number"]
            depth_map = {1: "얕음", 2: "얕음", 3: "깊음", 4: "깊음", 5: "깊음"}
            session.sleep_depth = depth_map.get(opt, "깊음")
            break
    
    for key in patient_data:
        if "불면 빈도" in key:
            opt = patient_data[key]["option_number"]
            # Set insomnia severity based on frequency (0-5 scale)
            session.insomnia_onset = max(0, opt - 1) if opt >= 2 else 0  # 0-5
            session.insomnia_maintain = max(0, opt - 2) if opt >= 3 else 0  # 0-5
            session.insomnia_reentry = max(0, opt - 2) if opt >= 3 else 0  # 0-5
            break
    
    for key in patient_data:
        if "꿈의 빈도" in key:
            opt = patient_data[key]["option_number"]
            dreams_map = {1: "거의 없음", 2: "가끔", 3: "자주", 4: "악몽", 5: "악몽"}
            session.dreams = dreams_map.get(opt, "가끔")
            break


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
    
    session.episode = _generate_episode(episode_disease_key)
    
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
                _apply_dyspepsia_symptoms(session, patient_data)
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
                _apply_backpain_symptoms(session, patient_data)
        except Exception as e:
            print(f"Warning: Failed to apply back pain symptoms: {e}")
    else:
        print("Warning: CSV randomization failed for 요통, using fallback")


def _apply_dyspepsia_symptoms(session, patient_data):
    """Apply functional dyspepsia-specific symptoms from CSV data."""
    
    # Helper function to find key by partial match
    def find_key(partial_name):
        for key in patient_data:
            if partial_name in key:
                return key
        return None
    
    # Onset / Duration (소화불량 시작시점)
    onset_key = find_key("소화불량 시작시점") or find_key("발현시점")
    if onset_key and onset_key in patient_data:
        opt = patient_data[onset_key]["option_number"]
        onset_map = {
            1: "1주일 이내",
            2: "1주-1개월 이내",
            3: "1개월 이상-3개월 이내",
            4: "3개월 이상-6개월 이내",
            5: "6개월 이상-1년 이내",
            6: "1년 이상"
        }
        session.onset = onset_map.get(opt, "6개월 이상-1년 이내")
    
    # Past experience (과거유사경험)
    past_exp_key = find_key("과거유사경험")
    if past_exp_key and past_exp_key in patient_data:
        opt = patient_data[past_exp_key]["option_number"]
        session.past_similar_experience = opt == 2  # 2 = 과거에도 소화불량이 있었음
    
    # Postprandial fullness (식후포만감)
    fullness_key = find_key("식후포만감")
    if fullness_key and fullness_key in patient_data:
        opt = patient_data[fullness_key]["option_number"]
        session.postprandial_fullness = int(opt) if opt else 1
    
    # Early satiation (조기포만감)
    early_sat_key = find_key("조기포만감")
    if early_sat_key and early_sat_key in patient_data:
        opt = patient_data[early_sat_key]["option_number"]
        session.early_satiation = int(opt) if opt else 1
    
    # Epigastric discomfort (상복부 불편감)
    epi_discomfort_key = find_key("상복부 불편감")
    if epi_discomfort_key and epi_discomfort_key in patient_data:
        opt = patient_data[epi_discomfort_key]["option_number"]
        session.epigastric_discomfort = int(opt) if opt else 1
    
    # Epigastric pain (상복부 통증)
    epi_pain_key = find_key("상복부 통증")
    if epi_pain_key and epi_pain_key in patient_data:
        opt = patient_data[epi_pain_key]["option_number"]
        session.epigastric_pain = int(opt) if opt else 1
    
    # Nausea (오심/메스꺼움)
    nausea_key = find_key("오심") or find_key("메스꺼움")
    if nausea_key and nausea_key in patient_data:
        opt = patient_data[nausea_key]["option_number"]
        session.nausea_sev = int(opt) if opt else 0
    
    # Belching (트림)
    belch_key = find_key("트림")
    if belch_key and belch_key in patient_data:
        opt = patient_data[belch_key]["option_number"]
        session.belching = int(opt) if opt else 0
    
    # Bloating (복부팽만감/더부룩함)
    bloating_key = find_key("복부팽만") or find_key("더부룩")
    if bloating_key and bloating_key in patient_data:
        opt = patient_data[bloating_key]["option_number"]
        session.bloating = int(opt) if opt else 0
    
    # Flatulence (가스)
    gas_key = find_key("가스")
    if gas_key and gas_key in patient_data:
        opt = patient_data[gas_key]["option_number"]
        gas_map = {1: "없음", 2: "보통", 3: "보통", 4: "잦음", 5: "잦음"}
        session.flatulence = gas_map.get(opt, "보통")
    
    # Acid reflux (산역류/신물)
    reflux_key = find_key("신물") or find_key("역류")
    if reflux_key and reflux_key in patient_data:
        opt = patient_data[reflux_key]["option_number"]
        session.acid_reflux = int(opt) if opt else 0
    
    # Heartburn (속쓰림)
    heartburn_key = find_key("속쓰림")
    if heartburn_key and heartburn_key in patient_data:
        opt = patient_data[heartburn_key]["option_number"]
        session.heartburn = int(opt) if opt else 0
    
    # Appetite (식욕)
    appetite_key = find_key("식욕")
    if appetite_key and appetite_key in patient_data:
        opt = patient_data[appetite_key]["option_number"]
        appetite_map = {1: "없음", 2: "저하", 3: "보통", 4: "보통", 5: "항진"}
        session.appetite = appetite_map.get(opt, "보통")
    
    # Set dyspepsia chief complaints based on symptom severity
    dyspepsia_chiefs = []
    if session.postprandial_fullness >= 3:
        dyspepsia_chiefs.append("식후포만감")
    if session.early_satiation >= 3:
        dyspepsia_chiefs.append("조기포만감")
    if session.epigastric_discomfort >= 3:
        dyspepsia_chiefs.append("상복부 불편감")
    if session.bloating >= 3:
        dyspepsia_chiefs.append("복부팽만")
    if session.nausea_sev >= 3:
        dyspepsia_chiefs.append("오심")
    
    if not dyspepsia_chiefs:
        dyspepsia_chiefs = ["소화불량"]
    
    session.dyspepsia_chief_type = dyspepsia_chiefs


def _apply_backpain_symptoms(session, patient_data):
    """Apply back pain-specific symptoms from CSV data."""
    
    # Helper function to find key by partial match
    def find_key(partial_name):
        for key in patient_data:
            if partial_name in key:
                return key
        return None
    
    # Onset / Duration (요통 발현시점)
    onset_key = find_key("요통 발현시점") or find_key("발현시점")
    if onset_key and onset_key in patient_data:
        opt = patient_data[onset_key]["option_number"]
        onset_map = {
            1: "1주일 이내",
            2: "1주-1개월 이내",
            3: "1개월 이상-3개월 이내",
            4: "3개월 이상-6개월 이내",
            5: "6개월 이상-1년 이내",
            6: "1년 이상"
        }
        session.onset = onset_map.get(opt, "1주-1개월 이내")
    
    # Past experience (과거 요통)
    past_exp_key = find_key("과거 요통") or find_key("과거유사경험")
    if past_exp_key and past_exp_key in patient_data:
        opt = patient_data[past_exp_key]["option_number"]
        session.past_back_pain = opt == 2  # 2 = 과거에도 요통이 있었음
    
    # Pain location (허리 불편부위)
    location_key = find_key("허리 불편부위")
    if location_key and location_key in patient_data:
        opt = patient_data[location_key]["option_number"]
        location_map = {
            1: "모름",
            2: "허리 아래 부위",
            3: "허리 위 부위",
            4: "허리 정 중간",
            5: "허리 좌/우 편측",
            6: "허리전반"
        }
        session.back_pain_location = location_map.get(opt, "허리전반")
    
    # Radiating pain (방산통)
    radiating_key = find_key("방산통")
    if radiating_key and radiating_key in patient_data:
        opt = patient_data[radiating_key]["option_number"]
        session.radiating_pain = int(opt) if opt else 1
    
    # Pain frequency (허리 불편 빈도)
    freq_key = find_key("허리 불편(빈도)")
    if freq_key and freq_key in patient_data:
        opt = patient_data[freq_key]["option_number"]
        session.back_freq = int(opt) if opt else 3
    
    # Pain intensity (허리 불편 강도)
    intensity_key = find_key("허리 불편(강도)")
    if intensity_key and intensity_key in patient_data:
        opt = patient_data[intensity_key]["option_number"]
        session.back_sev = int(opt) * 2 if opt else 4  # Scale 1-5 to 2-10
    
    # Pain type (통증 양상)
    type_key = find_key("통증 양상")
    if type_key and type_key in patient_data:
        opt = patient_data[type_key]["option_number"]
        pain_type_map = {
            1: "둔통",
            2: "예리통",
            3: "찌르는 통증",
            4: "당기는 통증",
            5: "저리는 통증"
        }
        session.back_pain_type = pain_type_map.get(opt, "둔통")
    
    # Morning stiffness (아침 뻣뻣함)
    stiff_key = find_key("아침") or find_key("뻣뻣")
    if stiff_key and stiff_key in patient_data:
        opt = patient_data[stiff_key]["option_number"]
        session.morning_stiffness = int(opt) if opt else 1
    
    # Aggravating factors (악화 요인)
    aggr_key = find_key("악화")
    if aggr_key and aggr_key in patient_data:
        opt = patient_data[aggr_key]["option_number"]
        session.back_aggravating = opt
    
    # Relieving factors (완화 요인)
    relief_key = find_key("완화")
    if relief_key and relief_key in patient_data:
        opt = patient_data[relief_key]["option_number"]
        session.back_relieving = opt
    
    # Leg numbness/tingling (다리 저림)
    leg_key = find_key("다리") or find_key("저림")
    if leg_key and leg_key in patient_data:
        opt = patient_data[leg_key]["option_number"]
        session.leg_numbness = int(opt) if opt else 0
    
    # Hip/buttock pain (엉덩이 통증)
    hip_key = find_key("엉덩이")
    if hip_key and hip_key in patient_data:
        opt = patient_data[hip_key]["option_number"]
        session.hip_pain = int(opt) if opt else 0
    
    # Set back pain chief complaints based on symptom severity
    backpain_chiefs = []
    if session.back_freq >= 2:
        backpain_chiefs.append("요통")
    if hasattr(session, 'radiating_pain') and session.radiating_pain >= 2:
        backpain_chiefs.append("방산통")
    if hasattr(session, 'leg_numbness') and session.leg_numbness >= 2:
        backpain_chiefs.append("다리 저림")
    if hasattr(session, 'morning_stiffness') and session.morning_stiffness >= 3:
        backpain_chiefs.append("아침 뻣뻣함")
    
    if not backpain_chiefs:
        backpain_chiefs = ["요통"]
    
    session.backpain_chief_type = backpain_chiefs
