"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - 맥진 규칙 (Pulse Diagnosis Rules)
교수님 피드백 기반 맥 조합 규칙 (Prof. Lee Sanghun Feedback)
═══════════════════════════════════════════════════════════════════════════════

가. 변증형의 문제 (Pattern-Type Pulse Rules):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1) 감기:
   - 풍한(風寒): 부맥, 지맥, 완맥, 긴맥 위주 (삭맥 가능)
   - 풍열(風熱): 부맥, 삭맥, 홍맥 위주 (지맥 불가 ❌)

2) 소화불량, 요통:
   - 허증(양허, 음허, 기허): 허맥류만 → 홍맥, 완맥, 실맥, 활맥, 장맥, 대맥 불가 ❌
   - 실증(기체, 담음, 식적, 어혈): 실맥류만 → 허맥, 세맥, 단맥 불가 ❌
   - 기체/어혈: 보통 또는 삭맥 위주
   - 담음/식적: 보통 또는 활맥 위주
   - 한증: 긴맥, 지맥 등 (삭맥, 홍맥 불가 ❌)
   - 열증: 홍맥 등 빠른 맥 (지맥 불가 ❌)

나. 조합의 문제 (Combination Rules):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 부맥류(부, 홍) ↔ 침맥류(침, 복) 겹침 불가 ❌
2. 지맥류(지, 완, 삽) ↔ 삭맥류(삭) 겹침 불가 ❌
3. 허맥류(허, 세, 단) ↔ 실맥류(실, 활, 긴, 장, 현) 겹침 불가 ❌
4. 부맥류 + 실맥류 + 삭맥류 → 겹침 가능 ✅
5. 침맥류 + 허맥류 + 지맥류 → 겹침 가능 ✅
6. 홍맥, 완맥 ↔ 허맥류 겹침 불가 ❌
7. 허맥(무력) ↔ 실맥(유력) 겹침 불가 ❌

═══════════════════════════════════════════════════════════════════════════════
"""

import random


# ═══════════════════════════════════════════════════════════════════════════════
# 맥 분류 (Pulse Categories) - Prof. Lee's Classification
# ═══════════════════════════════════════════════════════════════════════════════

# 정상맥
NORMAL_PULSE = "완맥"

# 부맥류 (浮脈類, Floating Pulses) - 부맥, 홍맥
FLOATING_GROUP = ["부맥", "홍맥"]

# 침맥류 (沈脈類, Deep Pulses) - 침맥, 복맥
DEEP_GROUP = ["침맥", "복맥"]

# 지맥류 (遲脈類, Slow Pulses) - 지맥, 완맥, 삽맥
SLOW_GROUP = ["지맥", "완맥", "삽맥"]

# 삭맥류 (數脈類, Rapid Pulses) - 삭맥
RAPID_GROUP = ["삭맥"]

# 허맥류 (虛脈類, Deficient/Weak Pulses) - 허맥, 세맥, 단맥
DEFICIENT_GROUP = ["허맥", "세맥", "단맥"]

# 실맥류 (實脈類, Excess/Strong Pulses) - 실맥, 활맥, 긴맥, 장맥, 현맥
EXCESS_GROUP = ["실맥", "활맥", "긴맥", "장맥", "현맥"]

# 모든 단일 맥 목록
ALL_SINGLE_PULSES = list(set(
    [NORMAL_PULSE] + FLOATING_GROUP + DEEP_GROUP + SLOW_GROUP + 
    RAPID_GROUP + DEFICIENT_GROUP + EXCESS_GROUP
))


# ═══════════════════════════════════════════════════════════════════════════════
# 질환별/변증별 허용 맥 규칙 (Disease & Pattern-Specific Pulse Rules)
# ═══════════════════════════════════════════════════════════════════════════════

# 감기 - 풍한형 (Wind-Cold): 부맥, 지맥, 완맥, 긴맥 위주 (삭맥 가능)
COLD_WIND_COLD_PULSES = ["부맥", "지맥", "완맥", "긴맥", "삭맥"]

# 감기 - 풍열형 (Wind-Heat): 부맥, 삭맥, 홍맥 위주 (지맥 불가)
COLD_WIND_HEAT_PULSES = ["부맥", "삭맥", "홍맥"]

# 허증 (Deficiency patterns: 양허, 음허, 기허) - 허맥류만
# 불가: 홍맥, 완맥, 실맥, 활맥, 장맥, 대맥
DEFICIENCY_PATTERN_PULSES = ["허맥", "세맥", "단맥", "침맥"]

# 실증 (Excess patterns: 기체, 담음, 식적, 어혈) - 실맥류
# 불가: 허맥, 세맥, 단맥
EXCESS_PATTERN_PULSES = ["실맥", "활맥", "긴맥", "장맥", "현맥", "부맥"]

# 기체/어혈 - 보통 또는 삭맥 위주
QI_STAG_BLOOD_STASIS_PULSES = ["완맥", "삽맥", "현맥", "긴맥"]

# 담음/식적 - 보통 또는 활맥 위주
PHLEGM_FOOD_STAG_PULSES = ["완맥", "활맥", "현맥"]

# 한증 (Cold pattern) - 긴맥, 지맥 등 (삭맥, 홍맥 불가)
COLD_PATTERN_PULSES = ["긴맥", "지맥", "완맥", "침맥", "삽맥"]

# 열증 (Heat pattern) - 홍맥 등 빠른 맥 (지맥 불가)
HEAT_PATTERN_PULSES = ["홍맥", "삭맥", "부맥", "실맥", "활맥"]


# ═══════════════════════════════════════════════════════════════════════════════
# 변증 ID → 맥 그룹 매핑 (Pattern ID to Pulse Group Mapping)
# ═══════════════════════════════════════════════════════════════════════════════

PATTERN_PULSE_MAP = {
    # 감기 변증
    "Cold_WC": COLD_WIND_COLD_PULSES,  # 풍한형
    "Cold_WH": COLD_WIND_HEAT_PULSES,  # 풍열형
    
    # 알레르기비염 - 풍한 계열 (모두 풍한 위주)
    "R_WBG": COLD_WIND_COLD_PULSES,    # 월비가반하탕
    "R_SGM": COLD_WIND_COLD_PULSES,    # 사간마황탕
    "R_SCY": COLD_WIND_COLD_PULSES,    # 소청룡탕
    "R_YGG": COLD_WIND_COLD_PULSES,    # 영감강미신하인탕
    "R_MHB": COLD_WIND_COLD_PULSES,    # 마황부자세신탕
    
    # 요통/소화불량 - 허증
    "BP_QiDef": DEFICIENCY_PATTERN_PULSES,     # 기허형
    "BP_YangDef": DEFICIENCY_PATTERN_PULSES,   # 양허형
    "BP_YinDef": DEFICIENCY_PATTERN_PULSES,    # 음허형
    "DY_QiDef": DEFICIENCY_PATTERN_PULSES,     # 기허형
    "DY_YangDef": DEFICIENCY_PATTERN_PULSES,   # 양허형
    "DY_YinDef": DEFICIENCY_PATTERN_PULSES,    # 음허형
    
    # 요통/소화불량 - 기체/어혈 (실증)
    "BP_QiStag": QI_STAG_BLOOD_STASIS_PULSES,      # 기체형
    "BP_BloodStasis": QI_STAG_BLOOD_STASIS_PULSES, # 어혈형
    "DY_QiStag": QI_STAG_BLOOD_STASIS_PULSES,      # 기체형
    "DY_BloodStasis": QI_STAG_BLOOD_STASIS_PULSES, # 어혈형
    
    # 요통/소화불량 - 담음/식적 (실증)
    "BP_Phlegm": PHLEGM_FOOD_STAG_PULSES,     # 담음형
    "BP_FoodStag": PHLEGM_FOOD_STAG_PULSES,   # 식적형
    "DY_Phlegm": PHLEGM_FOOD_STAG_PULSES,     # 담음형
    "DY_FoodStag": PHLEGM_FOOD_STAG_PULSES,   # 식적형
    
    # 요통/소화불량 - 한증
    "BP_Cold": COLD_PATTERN_PULSES,   # 한증형
    "DY_Cold": COLD_PATTERN_PULSES,   # 한증형
    
    # 요통/소화불량 - 열증
    "BP_Heat": HEAT_PATTERN_PULSES,   # 열증형
    "DY_Heat": HEAT_PATTERN_PULSES,   # 열증형
}


# ═══════════════════════════════════════════════════════════════════════════════
# 복합맥 정의 (Compound Pulse Definitions)
# 단일 맥을 조합하여 출력용 복합맥 생성
# ═══════════════════════════════════════════════════════════════════════════════

# 복합맥 → 구성 단일맥 매핑
COMPOUND_PULSE_COMPONENTS = {
    "완맥": ["완맥"],
    "부맥": ["부맥"],
    "침맥": ["침맥"],
    "지맥": ["지맥"],
    "삭맥": ["삭맥"],
    "허맥": ["허맥"],
    "실맥": ["실맥"],
    "세맥": ["세맥"],
    "홍맥": ["홍맥"],
    "긴맥": ["긴맥"],
    "활맥": ["활맥"],
    "삽맥": ["삽맥"],
    "현맥": ["현맥"],
    "단맥": ["단맥"],
    "장맥": ["장맥"],
    # 복합맥 조합
    "부삭": ["부맥", "삭맥"],
    "부긴": ["부맥", "긴맥"],
    "부허": ["부맥", "허맥"],
    "홍삭": ["홍맥", "삭맥"],
    "침세": ["침맥", "세맥"],
    "침긴": ["침맥", "긴맥"],
    "현긴": ["현맥", "긴맥"],
    "세삽": ["세맥", "삽맥"],
    "허세": ["허맥", "세맥"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# 맥 조합 검증 함수 (Pulse Combination Validation)
# ═══════════════════════════════════════════════════════════════════════════════

def is_valid_pulse_combination(pulse1: str, pulse2: str) -> bool:
    """
    두 맥이 함께 나타날 수 있는지 검증합니다.
    
    Rules (Prof. Lee):
    1. 부맥류(부, 홍) ↔ 침맥류(침, 복) 겹침 불가
    2. 지맥류(지, 완, 삽) ↔ 삭맥류(삭) 겹침 불가
    3. 허맥류(허, 세, 단) ↔ 실맥류(실, 활, 긴, 장, 현) 겹침 불가
    6. 홍맥, 완맥 ↔ 허맥류 겹침 불가
    7. 허맥(무력) ↔ 실맥(유력) 겹침 불가
    """
    # Rule 1: 부맥류 + 침맥류 충돌
    if (pulse1 in FLOATING_GROUP and pulse2 in DEEP_GROUP) or \
       (pulse1 in DEEP_GROUP and pulse2 in FLOATING_GROUP):
        return False
    
    # Rule 2: 지맥류 + 삭맥류 충돌
    if (pulse1 in SLOW_GROUP and pulse2 in RAPID_GROUP) or \
       (pulse1 in RAPID_GROUP and pulse2 in SLOW_GROUP):
        return False
    
    # Rule 3 & 7: 허맥류 + 실맥류 충돌
    if (pulse1 in DEFICIENT_GROUP and pulse2 in EXCESS_GROUP) or \
       (pulse1 in EXCESS_GROUP and pulse2 in DEFICIENT_GROUP):
        return False
    
    # Rule 6: 홍맥, 완맥 + 허맥류 충돌
    if (pulse1 in ["홍맥", "완맥"] and pulse2 in DEFICIENT_GROUP) or \
       (pulse1 in DEFICIENT_GROUP and pulse2 in ["홍맥", "완맥"]):
        # 완맥+허맥류는 허용할 수 있으나, 홍맥+허맥류는 불가
        if pulse1 == "홍맥" or pulse2 == "홍맥":
            return False
    
    return True


def get_valid_compound_pulses(allowed_single_pulses: list) -> list:
    """
    허용된 단일맥 목록에서 유효한 복합맥 목록을 생성합니다.
    
    Args:
        allowed_single_pulses: 허용된 단일맥 목록
    
    Returns:
        유효한 복합맥 목록 (단일맥 포함)
    """
    valid_compounds = []
    
    for compound, components in COMPOUND_PULSE_COMPONENTS.items():
        # 모든 구성 맥이 허용된 목록에 있어야 함
        if all(comp in allowed_single_pulses for comp in components):
            # 복합맥의 경우 조합 규칙도 확인
            if len(components) == 2:
                if is_valid_pulse_combination(components[0], components[1]):
                    valid_compounds.append(compound)
            else:
                valid_compounds.append(compound)
    
    return valid_compounds if valid_compounds else ["완맥"]


# ═══════════════════════════════════════════════════════════════════════════════
# 변증 ID 추출 함수 (Pattern ID Extraction)
# ═══════════════════════════════════════════════════════════════════════════════

def get_pattern_id(session) -> str:
    """
    세션에서 현재 선택된 변증 ID를 추출합니다.
    
    Args:
        session: Streamlit session_state
    
    Returns:
        변증 ID (예: "Cold_WC", "BP_QiDef")
    """
    from constants import DISEASE_PATTERNS
    
    disease = session.get('disease', '감기')
    pattern_idx = session.get('pattern_idx', 0)
    
    # 질환명 정규화
    if "감기" in disease:
        disease_key = "감기"
    elif "비염" in disease:
        disease_key = "알레르기비염"
    elif "소화불량" in disease:
        disease_key = "기능성소화불량"
    elif "요통" in disease:
        disease_key = "요통"
    else:
        disease_key = "감기"
    
    if disease_key in DISEASE_PATTERNS:
        patterns = DISEASE_PATTERNS[disease_key]["patterns"]
        if 0 <= pattern_idx < len(patterns):
            return patterns[pattern_idx].get("id", "")
    
    return ""


# ═══════════════════════════════════════════════════════════════════════════════
# 메인 함수들 (Main Functions)
# ═══════════════════════════════════════════════════════════════════════════════

def get_allowed_pulses(disease: str, pattern_id: str = None) -> list:
    """
    질환과 변증에 따라 허용되는 맥 목록을 반환합니다.
    
    Args:
        disease: 질환명 (감기, 알레르기비염, 요통, 기능성소화불량)
        pattern_id: 변증 ID (선택사항)
    
    Returns:
        허용되는 단일맥 목록
    """
    # 변증 ID가 있으면 변증별 규칙 우선
    if pattern_id and pattern_id in PATTERN_PULSE_MAP:
        return PATTERN_PULSE_MAP[pattern_id]
    
    # 변증 ID가 없으면 질환별 기본 규칙
    if "감기" in disease:
        # 감기는 기본적으로 풍한형 규칙 사용
        return COLD_WIND_COLD_PULSES
    elif "비염" in disease:
        return COLD_WIND_COLD_PULSES
    elif "소화불량" in disease or "요통" in disease:
        # 기본값: 완맥
        return ["완맥", "부맥", "침맥", "실맥", "허맥"]
    
    return ALL_SINGLE_PULSES


def select_pulse_for_pattern(session) -> str:
    """
    변증에 맞는 적절한 맥을 선택합니다.
    
    Args:
        session: Streamlit session_state
    
    Returns:
        선택된 맥명 (단일맥 또는 복합맥)
    """
    disease = session.get('disease', '감기')
    pattern_id = get_pattern_id(session)
    
    # 허용된 단일맥 목록 가져오기
    allowed_pulses = get_allowed_pulses(disease, pattern_id)
    
    # 유효한 복합맥 목록 생성
    valid_compounds = get_valid_compound_pulses(allowed_pulses)
    
    # 랜덤 선택 (단일맥 우선, 일부 확률로 복합맥)
    if random.random() < 0.3 and len(valid_compounds) > len(allowed_pulses):
        # 30% 확률로 복합맥 선택 (복합맥이 있는 경우)
        compound_only = [c for c in valid_compounds if c not in allowed_pulses]
        if compound_only:
            return random.choice(compound_only)
    
    return random.choice(allowed_pulses)


def apply_pulse_rules(session):
    """
    맥진 규칙을 적용합니다.
    - 질환/변증에 맞는 맥을 선택
    - 조합 규칙 검증
    - 맥박수 조정 (삭맥 = 빠름, 지맥 = 느림)
    
    Args:
        session: Streamlit session_state 객체
    """
    # 변증에 맞는 맥 선택
    selected_pulse = select_pulse_for_pattern(session)
    
    # 복합맥 저장 (출력용)
    session.compound_pulse = selected_pulse
    
    # 맥 특성에 따른 맥박수 조정
    pulse_components = COMPOUND_PULSE_COMPONENTS.get(selected_pulse, [selected_pulse])
    
    # 삭맥 포함 시 빠른 맥박 (90-110)
    if "삭맥" in pulse_components or "홍맥" in pulse_components:
        session.pulse_rate = random.randint(90, 110)
    # 지맥/완맥 포함 시 느린 맥박 (50-65)
    elif "지맥" in pulse_components:
        session.pulse_rate = random.randint(50, 65)
    elif "완맥" in pulse_components and "삭맥" not in pulse_components:
        session.pulse_rate = random.randint(60, 75)
    # 그 외 정상 범위
    else:
        session.pulse_rate = random.randint(65, 85)


def get_pulse_description(pulse: str) -> str:
    """
    맥의 한글 설명을 반환합니다.
    
    Args:
        pulse: 맥명
    
    Returns:
        맥의 설명 문자열
    """
    descriptions = {
        "완맥": "완맥(緩脈) - 정상 맥",
        "부맥": "부맥(浮脈) - 가볍게 눌러도 느껴지는 맥",
        "침맥": "침맥(沈脈) - 깊이 눌러야 느껴지는 맥",
        "지맥": "지맥(遲脈) - 느린 맥 (60회/분 이하)",
        "삭맥": "삭맥(數脈) - 빠른 맥 (90회/분 이상)",
        "허맥": "허맥(虛脈) - 무력한 맥",
        "실맥": "실맥(實脈) - 유력한 맥",
        "세맥": "세맥(細脈) - 가는 맥",
        "홍맥": "홍맥(洪脈) - 크고 힘찬 맥",
        "긴맥": "긴맥(緊脈) - 팽팽한 맥",
        "활맥": "활맥(滑脈) - 미끄러운 맥",
        "삽맥": "삽맥(澀脈) - 거친 맥",
        "현맥": "현맥(弦脈) - 팽팽하고 긴 맥",
        "단맥": "단맥(短脈) - 짧은 맥",
        "장맥": "장맥(長脈) - 긴 맥",
        "복맥": "복맥(伏脈) - 매우 깊은 맥",
        # 복합맥
        "부삭": "부삭맥(浮數脈) - 뜨고 빠른 맥",
        "부긴": "부긴맥(浮緊脈) - 뜨고 팽팽한 맥",
        "부허": "부허맥(浮虛脈) - 뜨고 무력한 맥",
        "홍삭": "홍삭맥(洪數脈) - 크고 빠른 맥",
        "침세": "침세맥(沈細脈) - 가라앉고 가는 맥",
        "침긴": "침긴맥(沈緊脈) - 가라앉고 팽팽한 맥",
        "현긴": "현긴맥(弦緊脈) - 팽팽하고 긴 맥",
        "세삽": "세삽맥(細澀脈) - 가늘고 거친 맥",
        "허세": "허세맥(虛細脈) - 무력하고 가는 맥",
    }
    return descriptions.get(pulse, pulse)


# ═══════════════════════════════════════════════════════════════════════════════
# 하위 호환성을 위한 기존 변수 (Legacy Support)
# ═══════════════════════════════════════════════════════════════════════════════

# 기존 코드와의 호환성을 위해 유지
DISEASE_PULSE_MAP = {
    "감기": COLD_WIND_COLD_PULSES,
    "알레르기비염": COLD_WIND_COLD_PULSES,
    "요통": ALL_SINGLE_PULSES,
    "기능성소화불량": ALL_SINGLE_PULSES,
    "기능성 소화불량": ALL_SINGLE_PULSES,
}

# 기존 복합맥 목록 (하위 호환성)
ALL_COMPOUND_PULSES = list(COMPOUND_PULSE_COMPONENTS.keys())
FLOATING_PULSES = ["부맥", "부삭", "부긴", "부허", "홍맥", "홍삭"]
DEEP_PULSES = ["침맥", "침세", "침긴"]
DEFICIENT_PULSES = ["허맥", "세맥", "단맥", "허세"]
EXCESS_PULSES = ["실맥", "현맥", "현긴", "긴맥"]
