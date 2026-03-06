"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Disease Pattern-Specific Constraints
Based on Clinical Guidelines Pages 15-16, 23

[교수님 피드백 2025-01 반영]
- 감기: 목감기(인후통), 몸살(신체통)이 주소증으로 항상 가능하도록 설정
- 알레르기비염: 청수양 콧물(맑은 콧물) 위주로, 황농성(누런 콧물) 제외
- 요통: 고령자 열증 제외, 어혈형에 외상력 추가
- 소화불량: 식적형에서 과식 관련 원인 제외
═══════════════════════════════════════════════════════════════════════════════

This module contains pattern-specific constraints for each disease type:
- 감기 (Cold) - Wind-Cold, Wind-Heat patterns
- 비염 (Rhinitis) - Various water retention patterns
- 요통 (Back Pain) - 한열허실 based patterns
- 소화불량 (Dyspepsia) - Spleen-stomach patterns
"""

import random


# ═══════════════════════════════════════════════════════════════════════════════
# COLD (감기) CONSTRAINTS - Page 15
# [교수님 피드백] 감기 일반 증상으로 목감기(인후통), 몸살(신체통) 포함 필수
# ═══════════════════════════════════════════════════════════════════════════════

def apply_cold_constraints(session):
    """
    Apply cold (감기) pattern-specific constraints (Page 15).
    
    Patterns:
    - 0: Wind-Cold (풍한형) - 惡寒重, 無汗
    - 1: Wind-Heat (풍열형) - 身熱, 有汗
    - 2: Wind-Dryness (풍조형) - Dry symptoms
    
    [교수님 피드백]
    - 모든 감기 환자에서 인후통/몸살이 주소증으로 가능해야 함
    """
    if "Cold" not in session.disease and "감기" not in session.disease:
        return
    
    current_pattern = session.pattern_idx
    
    # [교수님 피드백] 일반 감기 증상 보장 - 인후통, 몸살 가능성 확보
    _ensure_cold_general_symptoms(session)
    
    if current_pattern == 0:
        _apply_wind_cold_pattern(session)
    elif current_pattern == 1:
        _apply_wind_heat_pattern(session)
    elif current_pattern == 2:
        _apply_wind_dryness_pattern(session)


def _ensure_cold_general_symptoms(session):
    """
    [교수님 피드백] 감기 일반 증상 보장
    - 인후통(목감기)과 몸살(신체통)이 주소증으로 가능해야 함
    - 현재 증상 수준이 너무 낮으면 일부 증상을 높여 현실성 부여
    """
    # 인후통이 전혀 없는 경우 일정 확률로 경미한 인후통 추가
    if hasattr(session, 'sore_throat') and not session.sore_throat:
        if random.random() < 0.3:  # 30% 확률로 인후통 추가
            session.sore_throat = True
            if hasattr(session, 'throat_redness'):
                session.throat_redness = random.randint(2, 3)
    
    # 몸살(신체통)이 전혀 없는 경우 일정 확률로 경미한 몸살 추가
    if hasattr(session, 'body_ache_cold') and not session.body_ache_cold:
        if random.random() < 0.25:  # 25% 확률로 몸살 추가
            session.body_ache_cold = True
            if hasattr(session, 'body_ache'):
                session.body_ache = random.randint(2, 3)


def _apply_wind_cold_pattern(session):
    """
    Apply Wind-Cold (풍한) pattern constraints.
    
    Page 15: 오한이 심하고 땀이 없다 (惡寒重, 無汗)
    - Chills dominant over fever
    - No sweating
    - White/clear phlegm
    - Prefers warm drinks
    - Joint pain common (骨節疼痛)
    """
    # Chills should be more severe than fever
    if session.fever_sev > session.chills_sev:
        session.chills_sev, session.fever_sev = session.fever_sev, session.chills_sev
    
    # Tongue and phlegm characteristics
    session.tongue_coat_color = "백태"
    session.phlegm_color = "희박/맑음"
    
    # No sweating (無汗)
    session.sweating = False
    session.sweat_amt = "무한"
    
    # Joint pain correlation (骨節疼痛)
    if random.random() < 0.6:
        if "골절동통 (骨節疼痛) - 풍한" not in session.cold_symptoms_spec:
            session.cold_symptoms_spec.append("골절동통 (骨節疼痛) - 풍한")
    
    # Prefers warm/hot drinks (avoids cold)
    # Use Korean values to match UI options
    if session.drink_temp == "냉수":
        session.drink_temp = random.choice(["온수", "열수"])


def _apply_wind_heat_pattern(session):
    """
    Apply Wind-Heat (풍열) pattern constraints.
    
    Page 15: 身熱 (body heat/fever dominant)
    - Fever dominant over chills
    - Sweating present
    - Yellow/sticky phlegm
    - May prefer cool drinks
    """
    # Fever should be more severe than chills
    if session.chills_sev > session.fever_sev:
        session.chills_sev, session.fever_sev = session.fever_sev, session.chills_sev
    
    # Tongue and phlegm characteristics
    session.tongue_coat_color = random.choice(["백태", "황태"])
    session.phlegm_color = "황담/끈적"
    
    # Sweating present (有汗)
    session.sweating = True
    if session.sweat_amt == "무한":
        session.sweat_amt = "보통"
    
    # May prefer cool drinks
    # Use Korean values to match UI options
    if session.drink_temp == "열수":
        session.drink_temp = random.choice(["온수", "냉수"])


def _apply_wind_dryness_pattern(session):
    """
    Apply Wind-Dryness (풍조/온燥) pattern constraints.
    
    Page 15: Dry cough, little phlegm, dry/painful throat
    - Mild or no fever/chills
    - Dry throat and lips
    - Dry skin
    - Increased mouth dryness
    """
    # Mild fever/chills
    session.fever_sev = random.randint(1, 2)
    session.chills_sev = random.randint(1, 2)
    
    # Little phlegm, dry symptoms
    session.phlegm_amt = random.randint(0, 1)
    session.throat_dry = True
    session.lip_dry = True
    
    # Dry skin
    if session.skin_dry == "Normal (정상)":
        session.skin_dry = random.choice(["Dry (건조)", "Scaly (각질)"])
    
    # Increased mouth dryness
    session.mouth_dry = random.randint(2, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# RHINITIS (비염) CONSTRAINTS - Page 23
# [교수님 피드백] 알레르기비염은 청수양(맑은 콧물) 위주, 황농성(누런 콧물) 제외
# ═══════════════════════════════════════════════════════════════════════════════

def apply_rhinitis_constraints(session):
    """
    Apply rhinitis (비염) pattern-specific constraints.
    
    [교수님 피드백] 알레르기비염은 수체형이므로:
    - 청수양 (맑은 콧물) 위주로 생성
    - 황농성 (누렇고 찐득한 콧물)은 제외하거나 매우 드물게
    
    Patterns (수체형 variations):
    - 0: Yuebi (월비가반하탕) - 유일하게 열증/점액 가능
    - 1: Shegan (사간마황탕) - Cold/asthma
    - 2: Minor Blue Dragon (소청룡탕) - Cold/watery ★핵심
    - 3: Ling-Gan (영감강미신하인탕) - Cold/deficiency
    - 4: Mahuang-Fuzi (마황부자세신탕) - Kidney Yang deficiency
    """
    if "Rhinitis" not in session.disease and "비염" not in session.disease:
        return
    
    # [교수님 피드백] 기본적으로 알레르기비염은 맑은 콧물 위주
    _ensure_rhinitis_watery_discharge(session)
    
    pattern_handlers = {
        0: _apply_yuebi_pattern,
        1: _apply_shegan_pattern,
        2: _apply_minor_blue_dragon_pattern,
        3: _apply_linggan_pattern,
        4: _apply_mahuang_fuzi_pattern
    }
    
    handler = pattern_handlers.get(session.pattern_idx)
    if handler:
        handler(session)


def _ensure_rhinitis_watery_discharge(session):
    """
    [교수님 피드백] 알레르기비염 콧물 특성 보장
    - 청수양 (맑은 콧물)이 기본
    - 황농성 (누런 콧물)은 월비가반하탕 패턴에서만 허용
    """
    # 콧물 색상이 황색/녹색이면 맑은 콧물로 변경 (월비가반하탕 제외)
    if hasattr(session, 'snot_type'):
        yellow_keywords = ["황", "yellow", "Yellow", "녹", "green", "Green", "찐득", "sticky", "Sticky"]
        if any(kw in str(session.snot_type) for kw in yellow_keywords):
            # 월비가반하탕(열증) 패턴이 아니면 맑은 콧물로 강제 변경
            if session.pattern_idx != 0:
                session.snot_type = "청수양 (淸水樣) - 맑은 콧물"
    
    if hasattr(session, 'snot_color'):
        if session.snot_color in ["황색", "녹색", "Yellow", "Green"]:
            if session.pattern_idx != 0:
                session.snot_color = "맑음/투명"


def _apply_yuebi_pattern(session):
    """
    Yuebi (월비가반하탕) - Heat/sticky pattern.
    [교수님 피드백] 이 패턴만 황농성(누런 콧물) 허용
    """
    # 월비가반하탕은 열증이므로 누런 콧물 가능
    session.snot_type = "백점액 (白粘) - 희고 끈적"  # 황농성보다는 백점액 권장
    if session.tongue_coat_color == "백태":
        session.tongue_coat_color = "황태"


def _apply_shegan_pattern(session):
    """Shegan (사간마황탕) - Cold/asthma pattern."""
    session.snot_type = random.choice(["청수양 (清水樣) - 맑고 물같음", "백점액 (白粘) - 희고 끈적"])


def _apply_minor_blue_dragon_pattern(session):
    """
    Minor Blue Dragon (소청룡탕) - Cold/watery pattern.
    Key sign: 맑은 콧물이 줄줄 (profuse clear discharge)
    """
    session.snot_type = "청수양 (清水樣) - 맑고 물같음"
    session.tongue_coat_color = "백태"
    if session.cold_heat_pref == "열감/더위탐":
        session.cold_heat_pref = random.choice(["오한/추위탐", "보통"])


def _apply_linggan_pattern(session):
    """Ling-Gan (영감강미신하인탕) - Cold/deficiency pattern."""
    session.snot_type = "청수양 (清水樣) - 맑고 물같음"
    session.cold_heat_pref = "오한/추위탐"
    session.fatigue_level = random.choice(["중등도", "심함"])


def _apply_mahuang_fuzi_pattern(session):
    """
    Mahuang-Fuzi (마황부자세신탕) - Kidney Yang deficiency pattern.
    신양허: 수족냉, 피로
    """
    session.cold_hands_feet = True
    session.cold_heat_pref = "오한/추위탐"
    session.fatigue_level = random.choice(["중등도", "심함"])


# ═══════════════════════════════════════════════════════════════════════════════
# BACK PAIN (요통) CONSTRAINTS - Pages 15-16
# [교수님 피드백] 고령자 열증 제외, 어혈형에 외상력 추가
# ═══════════════════════════════════════════════════════════════════════════════

def apply_back_pain_constraints(session):
    """
    Apply back pain (요통) pattern-specific constraints (Pages 15-16).
    
    [교수님 피드백]
    - 고령자(65세 이상)에게 열증형(습열) 배제
    - 어혈형에는 반드시 외상력(낙상, 타박 등) 포함
    
    Patterns (한열허실 based):
    - 0: 신허 (Kidney Deficiency)
    - 1: 담음 (Phlegm)
    - 2: 식적 (Food Stagnation)
    - 3: 기 (Qi)
    - 4: 좌섬 (Sprain)
    - 5: 어혈 (Blood Stasis) ★외상력 필수
    - 6: 풍 (Wind)
    - 7: 한 (Cold)
    - 8: 습 (Dampness)
    - 9: 습열 (Damp-Heat) ★고령자 제외
    """
    if "Back Pain" not in session.disease and "요통" not in session.disease:
        return
    
    # [교수님 피드백] 고령자(65세 이상)에게 열증(습열) 패턴 배제
    _exclude_heat_pattern_for_elderly(session)
    
    # Ensure pain severity is capped at 7 per KTAS rules
    if session.pain_sev >= 7:
        session.pain_sev = 7
    
    # Ensure back pain is present for back pain diagnosis
    if session.pain_back[0] < 3:
        session.pain_back = [random.randint(3, 5), session.pain_sev]
        session.pain_back_f = session.pain_back[0]
        session.pain_back_i = session.pain_back[1]
    
    pain_nature_list = session.get("pain_nature", [])
    
    # Pattern-specific handler mapping
    pattern_handlers = {
        0: _apply_kidney_deficiency_pattern,
        1: _apply_phlegm_pattern,
        2: _apply_food_stagnation_pattern,
        3: _apply_qi_pattern,
        4: _apply_sprain_pattern,
        5: _apply_blood_stasis_pattern,
        6: _apply_wind_pattern,
        7: _apply_cold_pattern,
        8: _apply_dampness_pattern,
        9: _apply_damp_heat_pattern
    }
    
    handler = pattern_handlers.get(session.pattern_idx)
    if handler:
        handler(session, pain_nature_list)


def _exclude_heat_pattern_for_elderly(session):
    """
    [교수님 피드백] 고령자(65세 이상)에게 열증(습열) 패턴 배제
    - 습열형(pattern_idx=9)인 경우 한증형(pattern_idx=7)으로 변경
    """
    age = getattr(session, 'age', 40)
    if age >= 65 and session.pattern_idx == 9:  # 습열형(Damp-Heat)
        # 고령자에게 습열 대신 한증으로 변경
        session.pattern_idx = 7  # 한증형(Cold)
        # 로그 출력 (디버깅용)
        if hasattr(session, 'pattern_change_log'):
            session.pattern_change_log = "고령자(65+) 열증 → 한증 변경"


def _apply_kidney_deficiency_pattern(session, pain_nature_list):
    """
    신허 (Kidney Deficiency) pattern.
    Page 15: Continuous ache, hard to move, sexual overexertion cause
    舌大 (large tongue), 맥세 (thin pulse)
    """
    session.back_pain_cause = "신허 (Kidney Deficiency)"
    session.tongue_size = "대 (Enlarged)"
    session.pulse_width = "세맥"
    session.fatigue_level = random.choice(["중등도", "심함"])


def _apply_phlegm_pattern(session, pain_nature_list):
    """
    담음 (Phlegm) pattern.
    Page 15: Pain radiates up/down along meridians
    맥滑 또는 伏 (slippery or hidden pulse)
    """
    session.back_pain_cause = "발병 요인 없음"
    if "유주통 (Moving) - 담음" not in pain_nature_list:
        session.pain_nature.append("유주통 (Moving) - 담음")
    session.pulse_smooth = "활맥"


def _apply_food_stagnation_pattern(session, pain_nature_list):
    """
    식적 (Food Stagnation) pattern.
    Page 15: Caused by overeating/alcohol
    Difficulty bending/straightening, 맥滑 (slippery pulse)
    
    [교수님 피드백] 과식 관련 원인 제외
    - "과식" 대신 "음주", "소화 불량" 등으로 대체
    """
    # [교수님 피드백] 과식 제외 - 대체 원인 사용
    non_overeating_causes = [
        "음주 (Alcohol)",
        "소화기능 저하 (Digestive Weakness)",
        "불규칙한 식사 (Irregular Meals)",
        "기름진 음식 (Greasy Food)"
    ]
    session.back_pain_cause = random.choice(non_overeating_causes)
    session.pulse_smooth = "활맥"
    session.appetite = random.choice(["없음", "적음"])
    session.bloating = random.randint(2, 4)


def _apply_qi_pattern(session, pain_nature_list):
    """
    기 (Qi) pattern.
    Page 15: Frustration cause, worse with standing/walking
    맥沈伏 또는 弦 (sinking-hidden or wiry pulse)
    """
    session.back_pain_cause = "울체/스트레스 (Frustration)"
    if "오래 서있으면 악화 - 기" not in pain_nature_list:
        session.pain_nature.append("오래 서있으면 악화 - 기")
    session.pulse_depth = "침맥"
    session.pulse_tension = random.choice(["긴맥", "보통"])


def _apply_sprain_pattern(session, pain_nature_list):
    """
    좌섬 (Sprain) pattern.
    Page 15: Lifting heavy things, injury - sudden onset
    맥沈伏 實 (sinking-hidden, replete pulse)
    """
    session.back_pain_cause = "좌섬/외상 (Sprain/Injury)"
    session.onset = random.choice(["1일 전", "2-3일 전"])
    session.pulse_depth = "침맥"
    session.pulse_strength = "강력"


def _apply_blood_stasis_pattern(session, pain_nature_list):
    """
    어혈 (Blood Stasis) pattern.
    Page 15: Fall, hit, or chronic injury
    Less pain during day, worse at night; stabbing pain
    맥澀 (choppy pulse)
    
    [교수님 피드백] 어혈형에는 반드시 외상력(낙상, 타박 등) 포함
    """
    # [교수님 피드백] 외상력 필수 - 구체적인 외상 사유 추가
    injury_causes = [
        "낙상 (Fall)",
        "타박상 (Bruise/Contusion)",
        "교통사고 (Traffic Accident)",
        "운동 중 부상 (Sports Injury)",
        "무거운 물건 들다 삐끗 (Lifting Injury)"
    ]
    session.back_pain_cause = random.choice(injury_causes)
    
    # 외상력 명시적 기록
    session.trauma_history = True
    session.trauma_detail = session.back_pain_cause
    
    session.back_pain_timing = "야간 악화 (Worse at Night)"
    
    if "자통 (Stabbing) - 어혈" not in pain_nature_list:
        session.pain_nature.append("자통 (Stabbing) - 어혈")
    if "야간통 (Worse at Night) - 어혈" not in pain_nature_list:
        session.pain_nature.append("야간통 (Worse at Night) - 어혈")
    
    session.pulse_smooth = "삽맥"
    session.tongue_color = random.choice(["강홍/자설", "담홍"])


def _apply_wind_pattern(session, pain_nature_list):
    """
    풍 (Wind) pattern.
    Page 16: Pain moves around, may radiate to legs
    맥浮 (floating pulse)
    """
    session.back_pain_cause = "발병 요인 없음"
    if "유주통 (Moving) - 담음" not in pain_nature_list:
        session.pain_nature.append("유주통 (Moving) - 담음")
    session.back_radiation = True
    session.pulse_depth = "부맥"


def _apply_cold_pattern(session, pain_nature_list):
    """
    한 (Cold) pattern.
    Page 16: Hard to turn body, warmth helps
    맥沈緊 (sinking-tight pulse)
    """
    session.back_pain_cause = "발병 요인 없음"
    
    if "한통 (Cold Pain) - 한" not in pain_nature_list:
        session.pain_nature.append("한통 (Cold Pain) - 한")
    if "득온즉감 (Better w/ Warmth) - 한" not in pain_nature_list:
        session.pain_nature.append("득온즉감 (Better w/ Warmth) - 한")
    
    session.pulse_depth = "침맥"
    session.pulse_tension = "긴맥"
    session.cold_heat_pref = "오한/추위탐"
    session.cold_hands_feet = True


def _apply_dampness_pattern(session, pain_nature_list):
    """
    습 (Dampness) pattern.
    Page 16: Damp environment, heavy like a stone, cold feeling
    맥緩 (slow pulse)
    """
    session.back_pain_cause = "습한 환경 (Damp Environment)"
    
    if "중통 (Heavy) - 습" not in pain_nature_list:
        session.pain_nature.append("중통 (Heavy) - 습")
    
    session.cold_heat_pref = "오한/추위탐"
    session.pulse_tension = "유맥"
    session.tongue_coat_thick = random.choice(["후태", "니태"])


def _apply_damp_heat_pattern(session, pain_nature_list):
    """
    습열 (Damp-Heat) pattern.
    Page 16: Greasy food, sitting long worsens it
    맥緩 또는 沈 (slow or sinking pulse)
    """
    session.back_pain_cause = "기름진 음식/오래 앉음"
    session.pulse_depth = random.choice(["중맥", "침맥"])
    session.pulse_tension = "유맥"
    session.tongue_coat_color = "황태"
    session.tongue_coat_thick = "니태"


# ═══════════════════════════════════════════════════════════════════════════════
# DYSPEPSIA (소화불량) CONSTRAINTS - Page 16
# [교수님 피드백] 식적형에서 과식 관련 원인 제외
# ═══════════════════════════════════════════════════════════════════════════════

def apply_dyspepsia_constraints(session):
    """
    Apply dyspepsia (소화불량) pattern-specific constraints (Page 16).
    
    [교수님 피드백]
    - 식적형에서 "과식" 또는 "폭식" 관련 원인 제외
    - 대신 소화기능 저하, 스트레스 등으로 대체
    
    Patterns:
    - 0: 비위허약/위허기허 (Spleen-Stomach Weakness)
    - 1: 비위기허 (Spleen-Stomach Qi Deficiency)
    - 2: 간위불화 (Liver-Stomach Disharmony)
    - 3: 비위습열 (Spleen-Stomach Damp-Heat)
    - 4: 한열착잡 (Cold-Heat Complex)
    - 5: 음식정체/식적 (Food Stagnation) ★과식 제외
    """
    if "Dyspepsia" not in session.disease and "소화불량" not in session.disease:
        return
    
    dyspepsia_specs = session.get("dyspepsia_spec", [])
    
    pattern_handlers = {
        0: _apply_spleen_stomach_weakness_pattern,
        1: _apply_spleen_stomach_qi_def_pattern,
        2: _apply_liver_stomach_disharmony_pattern,
        3: _apply_spleen_stomach_damp_heat_pattern,
        4: _apply_cold_heat_complex_pattern,
        5: _apply_dyspepsia_food_stagnation_pattern
    }
    
    handler = pattern_handlers.get(session.pattern_idx)
    if handler:
        handler(session, dyspepsia_specs)


def _apply_spleen_stomach_weakness_pattern(session, dyspepsia_specs):
    """
    비위허약/위허기허 (Spleen-Stomach Weakness) pattern.
    Page 16: No appetite, eats little, bloating after eating
    舌苔淡白 薄潤, 脈細弱
    """
    session.appetite = random.choice(["없음", "적음"])
    session.diet_amt = "적음"
    session.bloating = random.randint(2, 4)
    session.fatigue_level = random.choice(["중등도", "심함"])
    session.limb_weakness = True
    
    # Tongue: Pale with thin white coat
    session.tongue_color = "담백"
    session.tongue_coat_color = "백태"
    session.tongue_coat_thick = "박태"
    
    # Pulse: Thin-weak
    session.pulse_width = "세맥"
    session.pulse_strength = "무력"


def _apply_spleen_stomach_qi_def_pattern(session, dyspepsia_specs):
    """
    비위기허 (Spleen-Stomach Qi Deficiency) pattern.
    Page 16: Stomach pain, sighing, easily tired
    舌淡苔白, 脈細弱
    """
    session.epigastric_pain = random.randint(2, 4)
    session.sighing_freq = random.randint(2, 4)
    session.fatigue_level = random.choice(["중등도", "심함"])
    session.mental_clarity = "흐릿"
    session.emot_anger = random.randint(3, 5)
    
    # Tongue: Pale white
    session.tongue_color = "담백"
    session.tongue_coat_color = "백태"
    
    # Pulse: Thin-weak
    session.pulse_width = "세맥"
    session.pulse_strength = "무력"


def _apply_liver_stomach_disharmony_pattern(session, dyspepsia_specs):
    """
    간위불화 (Liver-Stomach Disharmony) pattern.
    Page 16: Acid reflux, frequent belching, easily angered
    舌淡紅 苔薄白, 脈弦
    """
    session.acid_reflux = True
    session.belching = random.randint(3, 5)
    
    if "신물 (Acid Reflux) - 간/식" not in dyspepsia_specs:
        session.dyspepsia_spec.append("신물 (Acid Reflux) - 간/식")
    
    session.emot_anger = random.randint(3, 5)
    session.bitter_taste = True
    session.mouth_dry = random.randint(2, 4)
    
    if "구고 (Bitter Taste) - 열" not in dyspepsia_specs:
        session.dyspepsia_spec.append("구고 (Bitter Taste) - 열")
    
    # Tongue: Red with thin white coat
    session.tongue_color = "담홍"
    session.tongue_coat_color = "백태"
    session.tongue_coat_thick = "박태"
    
    # Pulse: Wiry
    session.pulse_tension = "긴맥"


def _apply_spleen_stomach_damp_heat_pattern(session, dyspepsia_specs):
    """
    비위습열 (Spleen-Stomach Damp-Heat) pattern.
    Page 16: Acid reflux, nausea, vomiting, body heat
    舌紅 苔黃膩, 脈滑數
    """
    session.acid_reflux = True
    session.nausea = random.randint(3, 5)
    session.nausea_sev = random.randint(3, 5)
    
    if "구역/구토 (Nausea) - 습열" not in dyspepsia_specs:
        session.dyspepsia_spec.append("구역/구토 (Nausea) - 습열")
    
    session.cold_heat_body = "열"
    session.bitter_taste = True
    session.mouth_dry = random.randint(2, 4)
    
    # Tongue: Red with yellow greasy coat
    session.tongue_color = "홍설"
    session.tongue_coat_color = "황태"
    session.tongue_coat_thick = "니태"
    
    # Pulse: Slippery-rapid
    session.pulse_smooth = "활맥"


def _apply_cold_heat_complex_pattern(session, dyspepsia_specs):
    """
    한열착잡 (Cold-Heat Complex) pattern.
    Page 16: Acid reflux, nausea, cold limbs
    舌淡 苔黃, 脈弦
    """
    session.acid_reflux = True
    session.epigastric_pain = random.randint(2, 4)
    session.cold_limbs_dyspepsia = True
    session.cold_hands_feet = True
    
    if "수족냉증 (Cold Limbs) - 허" not in dyspepsia_specs:
        session.dyspepsia_spec.append("수족냉증 (Cold Limbs) - 허")
    
    # Tongue: Pale with yellow coat
    session.tongue_color = "담백"
    session.tongue_coat_color = "황태"
    
    # Pulse: Wiry
    session.pulse_tension = "긴맥"


def _apply_dyspepsia_food_stagnation_pattern(session, dyspepsia_specs):
    """
    음식정체/식적 (Food Stagnation) pattern.
    Page 16-17: Acid reflux with foul smell, no appetite
    苔厚膩, 脈滑
    
    [교수님 피드백] 과식/폭식 관련 원인 제외
    - "과식" 대신 "소화기능 저하", "스트레스", "찬음식" 등으로 대체
    """
    session.acid_reflux = True
    session.foul_belch = True
    session.belching = random.randint(3, 5)
    session.belching_smell = "부패취"
    
    if "부패취 (Foul Belching) - 식적" not in dyspepsia_specs:
        session.dyspepsia_spec.append("부패취 (Foul Belching) - 식적")
    
    session.nausea = random.randint(2, 4)
    session.appetite = "없음"
    
    # [교수님 피드백] 과식 원인 제외 - 대체 원인 사용
    # 기존: "과식", "폭식", "많이 먹음" 등 제외
    # 대체: 소화기능 저하, 스트레스, 찬음식, 불규칙한 식사 등
    non_overeating_causes = [
        "소화기능 저하",
        "스트레스/정서적 요인",
        "찬음식 섭취",
        "불규칙한 식사",
        "기름진 음식",
        "급하게 먹음"
    ]
    session.dyspepsia_cause = random.choice(non_overeating_causes)
    
    # Tongue: Thick greasy coat
    session.tongue_coat_thick = "니태"
    
    # Pulse: Slippery
    session.pulse_smooth = "활맥"
