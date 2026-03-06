"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Negative Correlation Rules (Page 26)
음의 상관성 규칙 - 서로 적게 생성하거나 생성하지 않음
═══════════════════════════════════════════════════════════════════════════════

This module implements negative correlation rules from Page 26 of the clinical
guidelines. These rules prevent illogical or clinically impossible combinations
of symptoms and conditions.

Categories:
1. Appetite-Motivation constraints (식욕-의욕)
2. Age-related constraints (나이 관련)
3. Social history constraints (음주/흡연/운동)
4. Pain-related constraints (통증 관련)
5. Excretion constraints (배변/배뇨)
6. Physical-Mental constraints (체력/정신)
7. Sensory constraints (감각 - 이명, 후각)
8. Cold-Heat consistency (한열 민감성)
"""

import random


def apply_negative_correlation_rules(session):
    """
    Apply all negative correlation rules from Page 26.
    
    These rules PREVENT illogical combinations by adjusting values
    when contradictory states are detected.
    
    Args:
        session: Streamlit session_state object
    """
    # 0. Sex-Specific Rules (성별 관련) - 남성에게 월경 증상 배제
    _apply_sex_specific_rules(session)
    
    # 1. Appetite-Motivation Rules (식욕-의욕)
    _apply_appetite_motivation_rules(session)
    
    # 2. Age-Related Rules (나이 관련)
    _apply_age_related_rules(session)
    
    # 3. Social History Rules (사회력 - 음주/흡연/운동)
    _apply_social_history_rules(session)
    
    # 4. Pain-Related Rules (통증 관련)
    _apply_pain_related_rules(session)
    
    # 5. Excretion Rules (배변/배뇨)
    _apply_excretion_rules(session)
    
    # 6. Physical-Mental Rules (체력/정신)
    _apply_physical_mental_rules(session)
    
    # 7. Sensory Rules (감각 - 이명)
    _apply_sensory_rules(session)
    
    # 8. Cold-Heat Consistency (한열 민감성)
    _apply_cold_heat_consistency_rules(session)
    
    # 9. Skin-Face Consistency (피부-얼굴 광택)
    _apply_skin_face_consistency_rules(session)


# ═══════════════════════════════════════════════════════════════════════════════
# 0. SEX-SPECIFIC RULES (성별 관련)
# 남성 환자 및 어린 아이에게 월경 관련 증상 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_sex_specific_rules(session):
    """
    Apply sex-specific rules to exclude gender-inappropriate symptoms.
    
    Rules:
    - 남성 환자에게 월경통, 월경불순 등 여성 전용 증상 배제
      (Male patients should not have menstrual symptoms)
    - 12세 미만 어린이에게 월경 관련 증상 배제
      (Children under 12 should not have menstrual symptoms)
    """
    # Female-only symptoms that should be excluded for male patients and young children
    female_only_keywords = ["월경", "月經", "생리통", "생리불순"]
    
    # Check if patient is male
    is_male = getattr(session, 'sex', None) in ["남", "남자", "Male", "M"]
    
    # Check if patient is a young child (under 12)
    age = getattr(session, 'age', 20)
    is_young_child = age < 12
    
    # Exclude menstrual symptoms for males OR young children
    if is_male or is_young_child:
        # Filter out female-only symptoms from additional_symptoms
        if hasattr(session, 'additional_symptoms') and session.additional_symptoms:
            session.additional_symptoms = [
                symptom for symptom in session.additional_symptoms
                if not any(female_kw in symptom for female_kw in female_only_keywords)
            ]
        
        # Clear any menstrual-related fields
        if hasattr(session, 'mens_cycle'):
            delattr(session, 'mens_cycle')
        if hasattr(session, 'mens_regular'):
            delattr(session, 'mens_regular')
        if hasattr(session, 'mens_pain'):
            delattr(session, 'mens_pain')


# ═══════════════════════════════════════════════════════════════════════════════
# 1. APPETITE-MOTIVATION RULES (식욕-의욕)
# Page 26: 식욕이 없는데 의욕이 넘치는 상황배제
# Page 26: 입맛(식욕)이 없는데 의욕이 매우 높고 능동적인 성향은 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_appetite_motivation_rules(session):
    """
    Apply appetite-motivation negative correlation rules.
    
    Rules:
    - 식욕이 없는데 의욕이 넘치는 상황배제
      (No appetite + High motivation = EXCLUDE)
    - 입맛(식욕)이 없는데 의욕이 매우 높고 능동적인 성향은 배제
      (No appetite + Very high motivation/active tendency = EXCLUDE)
    """
    # Check for no appetite conditions
    no_appetite = session.appetite in ["없음", "저하"]
    
    # Check for high motivation conditions
    high_motivation = session.motivation in ["높음"]
    
    if no_appetite and high_motivation:
        # Rule: No appetite cannot coexist with high motivation
        # Resolution: Lower motivation to match poor appetite
        session.motivation = random.choice(["보통", "낮음", "무기력"])
    
    # Additional check: Very low appetite (None) should not have normal+ motivation
    if session.appetite == "없음" and session.motivation == "보통":
        # Severe appetite loss usually accompanies motivation loss
        if random.random() < 0.7:  # 70% probability to enforce
            session.motivation = random.choice(["낮음", "무기력"])


# ═══════════════════════════════════════════════════════════════════════════════
# 2. AGE-RELATED RULES (나이 관련)
# Page 26: 미성년자가 직업을 갖는 경우 배제
# Page 26: 미성년자가 만성병이나 그로 인한 복약을 하는 경우 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_age_related_rules(session):
    """
    Apply age-related negative correlation rules.
    
    Rules:
    - 미성년자가 직업을 갖는 경우 배제
      (Minor with job = EXCLUDE, except student)
    - 미성년자가 만성병이나 그로 인한 복약을 하는 경우 배제
      (Minor with chronic disease/medications = EXCLUDE)
    """
    is_minor = session.age < 19  # Korean legal adult age is 19
    
    if is_minor:
        # Rule 1: Minors should be students, not have professional jobs
        professional_jobs = [
            "사무직", 
            "현장직", 
            "가사",
            "관리직",
            "전문직",
            "서비스직",
            "판매직",
            "기능직"
        ]
        if session.job in professional_jobs:
            session.job = "학생"
        
        # Rule 2: Minors should not have chronic disease history
        chronic_conditions = ["고혈압", "당뇨", "이상지질혈증"]
        if hasattr(session, 'history_conditions') and session.history_conditions:
            # Remove chronic conditions from minor's history
            session.history_conditions = [
                c for c in session.history_conditions 
                if c not in chronic_conditions
            ]
        
        # Rule 3: Minors should not take chronic disease medications
        chronic_meds = ["혈압약", "당뇨약", "이상지질혈증약"]
        if hasattr(session, 'meds_specific') and session.meds_specific:
            session.meds_specific = [
                m for m in session.meds_specific 
                if m not in chronic_meds
            ]


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SOCIAL HISTORY RULES (사회력 - 음주/흡연/운동)
# Page 26: 술을 안마신다고 하면 잔 수 산정을 배제
# Page 26: 담배를 안피운다고 하면 흡연기간 산정을 배제
# Page 26: 주간운동시간이 있으면 평균운동시간이 0시간이 되는 것 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_social_history_rules(session):
    """
    Apply social history negative correlation rules.
    
    Rules:
    - 술을 안마신다고 하면 잔 수 산정을 배제
      (No alcohol → alcohol amount must be 0)
    - 담배를 안피운다고 하면 흡연기간 산정을 배제
      (No smoking → smoking duration must be 0)
    - 주간운동시간이 있으면 평균운동시간이 0시간이 되는 것 배제
      (Exercise frequency > 0 → exercise time must be > 0)
    """
    # Rule 1: No alcohol → no drink amount
    if session.social_alcohol_freq in ["비음주", "None (비음주)"]:
        session.social_alcohol_amt = 0.0
        session.social_alcohol_freq = "비음주"  # Normalize to Korean only
        # Also reset any alcohol-related variables
        if hasattr(session, 'social_alcohol_glasses'):
            session.social_alcohol_glasses = 0
    else:
        # If drinking, must have some amount
        if session.social_alcohol_amt <= 0:
            session.social_alcohol_amt = round(random.uniform(1.0, 3.0), 1)
    
    # Rule 2: No smoking → no smoking duration
    if session.social_smoke_daily <= 0:
        # Non-smoker: reset all smoking-related fields
        session.social_smoke_daily = 0.0
        if hasattr(session, 'social_smoke_years'):
            session.social_smoke_years = 0
    else:
        # Smoker: must have smoking duration
        if hasattr(session, 'social_smoke_years') and session.social_smoke_years <= 0:
            # Estimate years based on age (minimum 1 year)
            max_years = max(1, session.age - 18)
            session.social_smoke_years = random.randint(1, min(max_years, 30))
    
    # Rule 3: Exercise frequency > 0 → exercise time > 0
    # Check if there's exercise frequency/intensity
    has_exercise_activity = False
    
    if hasattr(session, 'social_exercise_freq') and session.social_exercise_freq > 0:
        has_exercise_activity = True
    
    if session.social_exercise_int in ["중", "고"]:
        has_exercise_activity = True
    
    if has_exercise_activity and session.social_exercise_time <= 0:
        # Has exercise activity but 0 time → set minimum time
        session.social_exercise_time = random.randint(15, 60)
    
    # Inverse: If exercise time > 0 but intensity is 0, set appropriate intensity
    if session.social_exercise_time > 0:
        if hasattr(session, 'social_exercise_freq') and session.social_exercise_freq <= 0:
            session.social_exercise_freq = random.randint(1, 3)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PAIN-RELATED RULES (통증 관련)
# Page 26: 복통이 없는데 복통의 양상이 나오는 것 배제
# Page 26: 통증이 없는데 통증의 양상이 나타나면 안됨
# Page 26: 신체통이 없는데, 몸이 신중(예-몸이 무겁다) 증상이 중등도 이상이 나오는 것 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_pain_related_rules(session):
    """
    Apply pain-related negative correlation rules.
    
    Rules:
    - 복통이 없는데 복통의 양상이 나오는 것 배제
      (No abdominal pain → no pain type/nature)
    - 통증이 없는데 통증의 양상이 나타나면 안됨
      (No pain → no pain characteristics)
    - 신체통이 없는데, 몸이 신중(예-몸이 무겁다) 증상이 중등도 이상이 나오는 것 배제
      (No body pain + Moderate body heaviness = EXCLUDE)
    """
    # Rule 1: No abdominal pain → no abdominal pain type
    no_abd_pain = session.abd_pain_sev <= 1
    
    if no_abd_pain:
        session.abd_pain_type = "없음"
        # Also reset related abdominal symptoms
        session.abd_tenderness = False
    else:
        # If there IS abdominal pain, must have a pain type
        if session.abd_pain_type in ["없음", "None (없음)"]:
            session.abd_pain_type = random.choice([
                "둔통", 
                "예리통", 
                "산통/경련통"
            ])
    
    # Rule 2: Check all pain grid items - no frequency → no intensity
    pain_parts = [
        "pain_neck", "pain_shoulder", "pain_back", "pain_knee", 
        "pain_hand", "pain_elbow", "pain_flank", "pain_pelvis", "pain_hip"
    ]
    
    for part in pain_parts:
        freq_key = f"{part}_f"
        intensity_key = f"{part}_i"
        
        if hasattr(session, freq_key):
            freq = getattr(session, freq_key, 0)
            
            if freq <= 0:
                # No frequency → no intensity
                setattr(session, intensity_key, 0)
                if hasattr(session, part):
                    session[part] = [0, 0]
            else:
                # Has frequency → must have some intensity
                intensity = getattr(session, intensity_key, 0)
                if intensity <= 0:
                    new_intensity = random.randint(2, 6)
                    setattr(session, intensity_key, new_intensity)
                    if hasattr(session, part):
                        session[part] = [freq, new_intensity]
    
    # Rule 3: No body pain + moderate body heaviness = EXCLUDE
    # Check if there's no body pain (all pain frequencies are 0 or low)
    total_pain_freq = sum([
        getattr(session, f"{p}_f", 0) for p in pain_parts
    ])
    
    no_body_pain = total_pain_freq <= 2  # Very low overall pain
    
    if no_body_pain and hasattr(session, 'body_heaviness_cold'):
        # Body heaviness should be low if no body pain
        if session.body_heaviness_cold:
            if random.random() < 0.7:  # 70% enforce
                session.body_heaviness_cold = False


# ═══════════════════════════════════════════════════════════════════════════════
# 5. EXCRETION RULES (배변/배뇨)
# Page 26: 배변후 느낌이 상쾌하다는 것과 배변 후 잔변감(강도)이 중등도 이상인 것 배제
# Page 26: 1일 소변횟수가 0-2회 사이에 야간뇨가 중등도 이상이면 안됨
# Page 26: 소변후 느낌이 상쾌하다는 것과 소변 후 잔뇨감(강도)이 중등도 이상인 것 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_excretion_rules(session):
    """
    Apply excretion-related negative correlation rules.
    
    Rules:
    - 배변후 느낌이 상쾌하다는 것과 배변 후 잔변감(강도)이 중등도 이상인 것 배제
      (Refreshed after defecation + Moderate residual feeling = EXCLUDE)
    - 1일 소변횟수가 0-2회 사이에 야간뇨가 중등도 이상이면 안됨
      (0-2 urinations/day → nocturia cannot be moderate+)
    - 소변후 느낌이 상쾌하다는 것과 소변 후 잔뇨감(강도)이 중등도 이상인 것 배제
      (Refreshed after urination + Moderate residual = EXCLUDE)
    """
    # Rule 1: Defecation - refreshed feeling vs residual feeling
    # stool_discomfort: True = discomfort, False = no discomfort (comfortable)
    if not session.stool_discomfort:
        # Feeling comfortable/refreshed after defecation
        # Cannot have moderate+ residual feeling
        # stool_form affects this - if hard stool, likely some discomfort
        if session.stool_form == "Hard (굳음/경변)":
            # Hard stool usually causes some discomfort
            session.stool_discomfort = True
    
    # Rule 2: Low daily urination (0-2) → nocturia cannot be moderate+
    # urine_freq_day: daily urination count
    # urine_freq_night: nocturia count (0-5 scale, 3+ is moderate)
    if session.urine_freq_day <= 2:
        # Very low daily urination
        if session.urine_freq_night >= 3:
            # Nocturia is moderate+ (3-4 times or 5+ times)
            # This is illogical: can't have frequent night urination 
            # but very low overall daily urination
            session.urine_freq_night = random.randint(0, 2)
    
    # Additional logic: If total urination is very low, nocturia should be low
    total_urination = session.urine_freq_day + session.urine_freq_night
    if total_urination <= 3:
        if session.urine_freq_night > session.urine_freq_day:
            # Night frequency shouldn't exceed day frequency in low total
            session.urine_freq_night = min(session.urine_freq_night, session.urine_freq_day)
    
    # Rule 3: Refreshed after urination vs residual urine feeling
    # urine_residual: True = has residual feeling, False = no residual
    if session.urine_stream == "Normal (정상)" and not session.urine_residual:
        # Normal stream and no residual = comfortable urination
        # Consistent state - no changes needed
        pass
    elif session.urine_stream == "정상" and session.urine_residual:
        # Normal stream but residual feeling - somewhat inconsistent
        # Allow with low probability
        if random.random() < 0.3:
            session.urine_residual = False
    
    # If weak stream, should have residual feeling
    if session.urine_stream in ["약함", "끊김"]:
        if not session.urine_residual:
            if random.random() < 0.6:  # 60% should have residual
                session.urine_residual = True


# ═══════════════════════════════════════════════════════════════════════════════
# 6. PHYSICAL-MENTAL RULES (체력/정신)
# Page 26: 체력이 매우 약한데 피로가 거의 없다는 것은 배제
# Page 26: 정신이 맑은데 기억력이 매우 나빠지면 안됨
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_physical_mental_rules(session):
    """
    Apply physical-mental state negative correlation rules.
    
    Rules:
    - 체력이 매우 약한데 피로가 거의 없다는 것은 배제
      (Very weak physical strength + No fatigue = EXCLUDE)
    - 정신이 맑은데 기억력이 매우 나빠지면 안됨
      (Clear mind + Very bad memory = EXCLUDE)
    """
    # Rule 1: Very weak → must have fatigue
    if session.physical_strength == "허약":
        if session.fatigue_level in ["없음", "약함"]:
            # Weak strength but no/low fatigue is illogical
            session.fatigue_level = random.choice(["중등도", "심함"])
    
    # Inverse: Strong strength should not have severe fatigue typically
    if session.physical_strength == "강건":
        if session.fatigue_level == "심함":
            # Strong but severely fatigued - possible but reduce probability
            if random.random() < 0.5:
                session.fatigue_level = random.choice(["없음", "약함", "중등도"])
    
    # Rule 2: Clear mind → cannot have very bad memory
    if session.mental_clarity == "맑음":
        if session.memory == "나쁨":
            # Clear mind but bad memory is illogical
            session.memory = random.choice(["좋음", "건망"])
    
    # Inverse: Confused/Foggy mind should not have good memory
    if session.mental_clarity in ["흐릿", "혼란"]:
        if session.memory == "좋음":
            if random.random() < 0.7:  # 70% enforce
                session.memory = random.choice(["건망", "나쁨"])


# ═══════════════════════════════════════════════════════════════════════════════
# 7. SENSORY RULES (감각 - 이명)
# Page 26: 이명을 느끼지 않는데, 이명의 강도가 높은 것 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_sensory_rules(session):
    """
    Apply sensory-related negative correlation rules.
    
    Rules:
    - 이명을 느끼지 않는데, 이명의 강도가 높은 것 배제
      (No tinnitus frequency + High tinnitus intensity = EXCLUDE)
    """
    # Rule: Tinnitus frequency and intensity must be consistent
    # tinnitus_freq: 0-5 scale (0 = none, 5 = constant)
    # tinnitus_sev: 0-5 scale (0 = none, 5 = severe)
    
    if session.tinnitus_freq == 0:
        # No tinnitus frequency → intensity must be 0
        session.tinnitus_sev = 0
    elif session.tinnitus_freq <= 1:
        # Very rare tinnitus → intensity should be low
        if session.tinnitus_sev >= 3:
            session.tinnitus_sev = random.randint(0, 2)
    else:
        # Has tinnitus → should have some intensity
        if session.tinnitus_sev == 0:
            session.tinnitus_sev = random.randint(1, session.tinnitus_freq)
    
    # Intensity should not exceed frequency level significantly
    if session.tinnitus_sev > session.tinnitus_freq + 1:
        session.tinnitus_sev = min(session.tinnitus_sev, session.tinnitus_freq + 1)


# ═══════════════════════════════════════════════════════════════════════════════
# 8. COLD-HEAT CONSISTENCY RULES (한열 민감성)
# Page 26: 한열 민감성 관계에서 모순적 지표 배제
#          (예-열이 매우 높은데(신열) 체온이 낮다 등)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_cold_heat_consistency_rules(session):
    """
    Apply cold-heat sensitivity consistency rules.
    
    Rules:
    - 한열 민감성 관계에서 모순적 지표 배제
      (Contradictory cold-heat indicators = EXCLUDE)
    - 예: 열이 매우 높은데(신열) 체온이 낮다
      (High fever sensation + Low body temperature = EXCLUDE)
    """
    # Rule 1: Heat sensitivity vs actual temperature
    # heat_sensitivity: 1-5 scale (5 = very heat sensitive)
    # temp: actual body temperature
    
    if session.heat_sensitivity >= 4:
        # Very heat sensitive → should have elevated or normal temp, not low
        if session.temp < 36.0:
            session.temp = round(random.uniform(36.5, 37.5), 1)
    
    # Rule 2: Cold sensitivity vs actual temperature
    # cold_sensitivity: 1-5 scale (5 = very cold sensitive)
    if session.cold_sensitivity >= 4:
        # Very cold sensitive → should not have high fever
        if session.temp >= 39.0:
            # Reduce temperature or reduce cold sensitivity
            if random.random() < 0.5:
                session.temp = round(random.uniform(37.0, 38.5), 1)
            else:
                session.cold_sensitivity = random.randint(1, 3)
    
    # Rule 3: Cold-heat body sensation vs cold-heat preference
    # cold_heat_body: "Cold (한 寒)", "Balanced (보통)", "Hot (열 熱)"
    # cold_heat_pref: "Cold Sens (오한/추위탐)", "Balanced (보통)", "Heat Sens (열감/더위탐)"
    
    # If body feels hot, shouldn't prefer cold/have cold sensitivity
    if session.cold_heat_body == "Hot (열 熱)":
        if session.cold_heat_pref == "Cold Sens (오한/추위탐)":
            # Body feels hot but prefers cold? This is inconsistent
            session.cold_heat_pref = random.choice(["Balanced (보통)", "Heat Sens (열감/더위탐)"])
    
    # If body feels cold, shouldn't have heat preference
    if session.cold_heat_body == "Cold (한 寒)":
        if session.cold_heat_pref == "Heat Sens (열감/더위탐)":
            # Body feels cold but heat sensitive? Inconsistent
            session.cold_heat_pref = random.choice(["Cold Sens (오한/추위탐)", "Balanced (보통)"])
    
    # Rule 4: Fever severity vs cold-heat body
    # If high fever, body should feel hot
    if hasattr(session, 'fever_sev') and session.fever_sev >= 4:
        if session.cold_heat_body == "Cold (한 寒)":
            # High fever but body feels cold is rare (except in 한열왕래)
            if random.random() < 0.7:
                session.cold_heat_body = random.choice(["Balanced (보통)", "Hot (열 熱)"])
    
    # Rule 5: Drink temperature preference consistency
    # Cold body → should prefer warm/hot drinks
    # Use Korean values to match UI options
    if session.cold_heat_body == "Cold (한 寒)":
        if session.drink_temp == "냉수":
            session.drink_temp = random.choice(["온수", "열수"])
    
    # Hot body → may prefer cold drinks
    if session.cold_heat_body == "Hot (열 熱)":
        if session.drink_temp == "열수":
            if random.random() < 0.6:
                session.drink_temp = random.choice(["냉수", "온수"])


# ═══════════════════════════════════════════════════════════════════════════════
# 9. SKIN-FACE CONSISTENCY RULES (피부-얼굴 광택)
# Page 26: 피부건조도가 매우 심한데 얼굴 광택이 윤기가 충만한 것은 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_skin_face_consistency_rules(session):
    """
    Apply skin-face consistency rules.
    
    Rules:
    - 피부건조도가 매우 심한데 얼굴 광택이 윤기가 충만한 것은 배제
      (Very dry skin + Shiny/glossy face = EXCLUDE)
    """
    # Rule: Very dry skin → face should not be shiny
    # skin_dry: "Normal (정상)", "Dry (건조)", "Scaly (각질)"
    # face_gloss: "Dull (칙칙)", "Normal (보통)", "Shiny (윤기)"
    
    if session.skin_dry == "Scaly (각질)":
        # Very dry skin with scaling
        if session.face_gloss == "Shiny (윤기)":
            # Cannot have very dry skin but shiny face
            session.face_gloss = random.choice(["Dull (칙칙)", "Normal (보통)"])
    
    if session.skin_dry == "Dry (건조)":
        # Moderately dry skin
        if session.face_gloss == "Shiny (윤기)":
            # Less strict - allow with lower probability
            if random.random() < 0.6:
                session.face_gloss = "Normal (보통)"
    
    # Inverse: Very shiny face → skin should not be very dry
    if session.face_gloss == "Shiny (윤기)":
        if session.skin_dry == "Scaly (각질)":
            session.skin_dry = random.choice(["Normal (정상)", "Dry (건조)"])
    
    # Consistency with lip dryness
    if session.skin_dry == "Scaly (각질)":
        # Very dry skin → lips should also be dry
        if not session.lip_dry:
            if random.random() < 0.7:
                session.lip_dry = True


# ═══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL MENSTRUAL RULES
# Page 26: 생리주기가 제시되면 생리규칙성에서 3개월 이상 생리가 없다는 항목은 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_menstrual_consistency_rules(session):
    """
    Apply menstrual cycle consistency rules.
    
    Rules:
    - 생리주기가 제시되면 생리규칙성에서 3개월 이상 생리가 없다는 항목은 배제
      (If menstrual cycle is given → "no period 3+ months" is excluded)
    """
    # Only applies to females
    if session.sex != "여":
        return
    
    # Check if menstrual cycle is specified
    has_cycle = hasattr(session, 'mens_cycle') and session.mens_cycle > 0
    
    # 폐경인 경우 생리 관련 정보 모두 초기화
    if session.mens_regular == "폐경":
        session.mens_cycle = 0
        session.mens_duration = 0
        session.mens_pain_score = 0
        session.mens_color = "N/A"
    elif has_cycle and session.mens_cycle > 0:
        # Cycle is specified and not menopause
        # Keep the existing cycle data
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# MEAL FREQUENCY-REGULARITY RULES
# Page 26: 하루 식사횟수가 1회 미만인 경우 매우 규칙적이라는 것은 배제
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_meal_consistency_rules(session):
    """
    Apply meal frequency-regularity consistency rules.
    
    Rules:
    - 하루 식사횟수가 1회 미만인 경우 매우 규칙적이라는 것은 배제
      (<1 meal/day → cannot be "very regular")
    """
    # diet_freq: meal frequency per day (1, 2, 3, 4)
    # diet_regular: "Regular (규칙적)", "Irregular (불규칙)"
    
    if session.diet_freq <= 1:
        # 1 or fewer meals per day
        if session.diet_regular in ["Regular (규칙적)", "규칙적"]:
            # Cannot be regular with such low meal frequency
            session.diet_regular = "불규칙"
    
    # Also check appetite correlation
    if session.diet_freq <= 1 and session.appetite in ["항진", "보통", "High (항진)", "Normal (보통)"]:
        # Low meal frequency should correlate with low appetite
        if random.random() < 0.6:
            session.appetite = random.choice(["없음", "저하"])
