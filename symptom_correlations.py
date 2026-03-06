"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Symptom Correlation Rules (Pages 36-38)
Based on 400 patient chart review correlation analysis
═══════════════════════════════════════════════════════════════════════════════

This module implements symptom correlation rules derived from the 400-patient
chart review analysis documented in pages 36-38 of the clinical guidelines.

Key Correlation Clusters (51 total correlations):
1. 식욕-소화 클러스터 (Appetite-Digestion Cluster)
2. 비만 클러스터 (Obesity Cluster)
3. 당뇨-고혈압-이상지질혈증 패턴 (Metabolic Syndrome Cluster)
4. 피로-통증-허약 패턴 (Fatigue-Pain-Weakness)
5. 흉민-스트레스-수면 클러스터 (Chest Tightness-Stress-Sleep)
6. 이명-난청 패턴 (Tinnitus-Hearing Loss)
7. 기침-가래-매핵기 패턴 (Cough-Phlegm-Throat Obstruction)
8. 땀양-열 (Sweat-Heat) - Negative correlation

Correlation Coefficients from Page 37-38 (All from attached images):

식욕-소화 클러스터:
- 식욕좋음 ↔ 비만: r=0.687
- 식욕좋음 ↔ 복부비만: r=0.373
- 식욕좋음 ↔ 식사량: r=0.349
- 식욕좋음 ↔ 음수량: r=0.311
- 식욕좋음 ↔ 소화양호: r=0.374
- 강박 ↔ 식욕좋음: r=-0.404 (negative)
- 소화양호 ↔ 소화불량: r=-0.537 (negative)
- 소화양호 ↔ 속쓰림: r=-0.325 (negative)
- 소화양호 ↔ 구역구토: r=-0.345 (negative)
- 소화불량 ↔ 상복통증: r=0.372
- 소화불량 ↔ 하복통증: r=0.310
- 구역구토 ↔ 소화불량: r=0.349
- 구역구토 ↔ 트림: r=0.309
- 구역구토 ↔ 상복통증: r=0.332
- 트림 ↔ 가스참: r=0.325
- 트림 ↔ 상복통증: r=0.455
- 트림 ↔ 하복통증: r=0.300
- 속쓰림 ↔ 소화불량: r=0.329
- 속쓰림 ↔ 구역구토: r=0.326
- 복부비만 ↔ 비만: r=0.689
- 복부비만 ↔ 식사량: r=0.359

호흡기 클러스터:
- 숨참 ↔ 흉통: r=0.431
- 숨참 ↔ 기침: r=0.319
- 숨참 ↔ 갈증: r=0.307
- 기침 ↔ 가래: r=0.438
- 기침 ↔ 매핵기: r=0.351
- 가래 ↔ 매핵기: r=0.443

흉민-스트레스-수면 클러스터:
- 흉민 ↔ 흉통: r=0.359
- 흉민 ↔ 스트레스: r=0.322
- 흉민 ↔ 두통: r=0.356
- 흉민 ↔ 상복통증: r=0.385
- 흉민 ↔ 수면질: r=0.373
- 흉민 ↔ 숨참: r=0.431
- 흉통 ↔ 다몽: r=0.301
- 스트레스 ↔ 수면질: r=0.430
- 스트레스 ↔ 트림: r=0.323
- 스트레스 ↔ 활동량: r=0.323
- 수면질 ↔ 수면장애: r=0.695
- 다몽 ↔ 수면장애: r=0.327
- 다몽 ↔ 경계긴장: r=0.481
- 다몽 ↔ 우울: r=0.358
- 경계긴장 ↔ 우울: r=0.312
- 경계긴장 ↔ 흉통: r=0.326

기타 클러스터:
- 피로 ↔ 통증: r=0.435
- 피로 ↔ 허약: r=0.320
- 난청 ↔ 이명: r=0.329
- 땀양 ↔ 열: r=-0.372 (negative)
- 고혈압 ↔ 당뇨: r=0.340
- 고혈압 ↔ 이상지질: r=0.447
- 당뇨 ↔ 이상지질: r=0.414
"""

import random

# ═══════════════════════════════════════════════════════════════════════════════
# CORRELATION COEFFICIENTS DICTIONARY (Pages 37-38)
# Extracted from 400-patient chart review correlation analysis
# ═══════════════════════════════════════════════════════════════════════════════

CORRELATION_COEFFICIENTS = {
    # Appetite-Related (식욕 관련) - Image (22 correlations verified)
    ("appetite_good", "obesity"): 0.364,  # #2: 비만 ↔ 식욕좋음 (corrected from 0.687)
    ("appetite_good", "abdominal_obesity"): 0.373,  # #4: 식욕좋음 ↔ 복부비만
    ("appetite_good", "food_amount"): 0.689,  # #6: 식욕좋음 ↔ 식사량 (corrected from 0.349)
    ("appetite_good", "water_intake"): 0.311,  # #5: 음수량 ↔ 식욕좋음
    ("appetite_good", "ocd"): -0.404,  # #1: 강박 ↔ 식욕좋음 (Negative)
    ("appetite_good", "digestion_good"): 0.374,  # #7: 식욕좋음 ↔ 소화양호
    
    # Obesity Cluster (비만 클러스터) - Image
    ("abdominal_obesity", "obesity"): 0.687,  # #3: 비만 ↔ 복부비만 (corrected from 0.689)
    ("abdominal_obesity", "food_amount"): 0.359,  # #8: 식사량 ↔ 복부비만
    
    # Digestion-Related (소화 관련) - Image
    ("digestion_good", "dyspepsia"): -0.537,  # #10: 소화양호 ↔ 소화불량 (Negative)
    ("digestion_good", "heartburn"): 0.329,  # #11: 속쓰림 ↔ 소화양호 (corrected: was -0.325, image shows +0.329)
    ("digestion_good", "nausea_vomit"): -0.325,  # #13/#22: 소화양호 ↔ 구역구토 (Negative, corrected from -0.345)
    ("digestion_good", "food_amount"): 0.349,  # #9: 소화양호 ↔ 식사량 (NEW - was missing)
    ("dyspepsia", "upper_abd_pain"): 0.372,  # 소화불량 ↔ 상복통증
    ("dyspepsia", "lower_abd_pain"): 0.310,  # 소화불량 ↔ 하복통증
    ("nausea_vomit", "dyspepsia"): 0.349,  # 구역구토 ↔ 소화불량
    ("nausea_vomit", "belching"): 0.309,  # 구역구토 ↔ 트림
    ("nausea_vomit", "upper_abd_pain"): 0.332,  # 구역구토 ↔ 상복통증
    ("belching", "gas_bloating"): 0.325,  # 트림 ↔ 가스참
    ("belching", "upper_abd_pain"): 0.455,  # 트림 ↔ 상복통증 (updated from 0.309)
    ("belching", "lower_abd_pain"): 0.300,  # 트림 ↔ 하복통증
    ("heartburn", "dyspepsia"): 0.329,  # 속쓰림 ↔ 소화불량
    ("heartburn", "nausea_vomit"): 0.326,  # 속쓰림 ↔ 구역구토
    
    # Respiratory-Related (호흡기 관련) - Image 3
    ("dyspnea", "chest_pain"): 0.431,  # 숨참 ↔ 흉통
    ("dyspnea", "cough"): 0.319,  # 숨참 ↔ 기침
    ("dyspnea", "thirst"): 0.307,  # 숨참 ↔ 갈증
    ("cough", "phlegm"): 0.438,  # 기침 ↔ 가래
    ("cough", "throat_obstruction"): 0.351,  # 기침 ↔ 매핵기
    ("phlegm", "throat_obstruction"): 0.443,  # 가래 ↔ 매핵기
    
    # Chest Tightness Cluster (흉민 클러스터) - Image 4
    ("chest_tight", "chest_pain"): 0.359,  # 흉민 ↔ 흉통
    ("chest_tight", "stress"): 0.322,  # 흉민 ↔ 스트레스
    ("chest_tight", "headache"): 0.356,  # 흉민 ↔ 두통
    ("chest_tight", "upper_abd_pain"): 0.385,  # 흉민 ↔ 상복통증
    ("chest_tight", "sleep_quality"): 0.373,  # 흉민 ↔ 수면질
    ("chest_tight", "dyspnea"): 0.431,  # 흉민 ↔ 숨참
    
    # Stress-Sleep Cluster (스트레스-수면 클러스터) - Image 4
    ("stress", "sleep_quality"): 0.430,  # 스트레스 ↔ 수면질
    ("stress", "belching"): 0.323,  # 스트레스 ↔ 트림
    ("stress", "activity_level"): 0.323,  # 스트레스 ↔ 활동량
    ("sleep_quality", "sleep_disorder"): 0.695,  # 수면질 ↔ 수면장애
    ("dreams", "sleep_disorder"): 0.327,  # 다몽 ↔ 수면장애
    ("dreams", "anxiety"): 0.481,  # 다몽 ↔ 경계긴장
    ("dreams", "depression"): 0.358,  # 다몽 ↔ 우울
    ("dreams", "sleep_quality"): 0.430,  # 다몽 ↔ 수면질 (NEW)
    ("dreams", "chest_tight"): 0.332,  # 다몽 ↔ 흉민
    ("chest_pain", "dreams"): 0.301,  # 흉통 ↔ 다몽
    ("anxiety", "depression"): 0.312,  # 경계긴장 ↔ 우울
    ("anxiety", "chest_pain"): 0.326,  # 경계긴장 ↔ 흉통
    
    # Fatigue Cluster (피로 클러스터)
    ("fatigue", "pain"): 0.435,
    ("fatigue", "weakness"): 0.320,
    
    # Ear-Related (귀 관련)
    ("hearing_loss", "tinnitus"): 0.329,
    
    # Sweat-Heat (땀-열)
    ("sweat_amount", "heat"): -0.372,  # Negative
    
    # Metabolic Syndrome (대사증후군)
    ("hypertension", "diabetes"): 0.340,
    ("hypertension", "dyslipidemia"): 0.447,
    ("diabetes", "dyslipidemia"): 0.414,
}


def apply_correlation_probability(correlation_coefficient):
    """
    Convert correlation coefficient to probability for symptom co-occurrence.
    Uses a scaled probability based on the absolute value of correlation.
    
    Args:
        correlation_coefficient: r value from -1 to 1
    
    Returns:
        Probability value from 0 to 1
    """
    # Scale correlation to probability (r of 0.5 = 50% chance)
    # For negative correlations, we return the inverse probability
    abs_r = abs(correlation_coefficient)
    base_prob = 0.3 + (abs_r * 0.5)  # Scale from 0.3 to 0.8
    return min(base_prob, 0.85)  # Cap at 85%


def should_apply_correlation(correlation_coefficient):
    """
    Determine if a correlation should be applied based on random chance.
    
    Args:
        correlation_coefficient: r value from -1 to 1
    
    Returns:
        True if correlation should be applied, False otherwise
    """
    prob = apply_correlation_probability(correlation_coefficient)
    return random.random() < prob


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 36: MAIN CORRELATION PATTERNS
# 400명 차트리뷰 결과 증상간 상관관계 전체 참고자료
# ═══════════════════════════════════════════════════════════════════════════════

def apply_appetite_digestion_correlations(session_state):
    """
    Page 36-37: 식욕-소화 상관관계
    - 식욕이 좋으면 소화가 양호하고 비만, 음수량, 식사량이 많아지는 경향으로 생성
    - 소화불량은 상복부통증, 구토, 구역, 트림, 속쓰림 등 소화기 불편증상과 양의 상관성을 가짐
    """
    # Calculate BMI for obesity check
    height_m = session_state.height / 100
    bmi = session_state.weight / (height_m * height_m)
    is_obese = bmi >= 25
    
    # RULE 1: 식욕좋음 → 비만 경향 (r=0.687)
    if session_state.appetite in ["항진", "보통"]:
        if should_apply_correlation(0.687):
            # Good appetite correlates with better digestion
            if session_state.digestion in ["나쁨", "매우 나쁨"]:
                session_state.digestion = random.choice(["보통", "좋음"])
            
            # Correlates with higher food/water intake
            if should_apply_correlation(0.349):  # food_amount
                session_state.diet_amt = random.choice(["보통", "많음"])
            
            if should_apply_correlation(0.311):  # water_intake
                session_state.water_intake = random.choice(["1-2L", "2L 이상"])
    
    # RULE 2: 소화불량 → GI 증상들 (r=0.329-0.372)
    if session_state.digestion in ["나쁨", "매우 나쁨"]:
        # Upper abdominal pain (r=0.372)
        if should_apply_correlation(0.372):
            if hasattr(session_state, 'abd_pain_sev') and session_state.abd_pain_sev < 2:
                session_state.abd_pain_sev = random.randint(2, 4)
        
        # Nausea/vomiting (r=0.349)
        if should_apply_correlation(0.349):
            if session_state.nausea < 2:
                session_state.nausea = random.randint(2, 4)
        
        # Bloating (r=0.325 via belching-gas connection)
        if should_apply_correlation(0.325):
            if session_state.bloating < 2:
                session_state.bloating = random.randint(2, 4)
        
        # Heartburn/속쓰림 (r=0.329)
        if should_apply_correlation(0.329):
            if hasattr(session_state, 'acid_reflux'):
                session_state.acid_reflux = True
    
    # RULE 3: 트림 → 가스참 (r=0.325)
    if hasattr(session_state, 'belching') and session_state.belching >= 3:
        if should_apply_correlation(0.325):
            if session_state.bloating < 2:
                session_state.bloating = random.randint(2, 4)
            session_state.flatulence = random.choice(["보통", "잦음"])
    
    return session_state


def apply_ocd_appetite_negative_correlation(session_state):
    """
    Page 36-37: 강박증상은 '식욕좋음', '소화잘됨' 증상과 음의 상관관계로 가급적 배제
    강박 ↔ 식욕좋음: r=-0.404 (negative)
    """
    # High anxiety/OCD symptoms negatively correlate with good appetite/digestion
    if session_state.emot_anxiety >= 4 or session_state.emot_thought >= 4:
        if should_apply_correlation(0.404):  # Use absolute value
            # Reduce appetite
            if session_state.appetite in ["항진"]:
                session_state.appetite = random.choice(["보통", "저하"])
            
            # Reduce digestion quality
            if session_state.digestion in ["좋음"]:
                session_state.digestion = random.choice(["보통", "나쁨"])
    
    return session_state


def apply_respiratory_correlations(session_state):
    """
    Page 36-37: 호흡기 증상 상관관계
    - 숨참(천증) 등은 흉통, 갈증, 기침과 양의 상관관계를 가짐
    - 기침은 가래, 매핵기와 양의 상관성을 가짐
    """
    # RULE 1: 숨참/천증 → 흉통 (r=0.431)
    dyspnea_present = session_state.resp >= 22 or (hasattr(session_state, 'cold_dyspnea') and session_state.cold_dyspnea)
    
    if dyspnea_present:
        # Chest pain correlation (r=0.431)
        if should_apply_correlation(0.431):
            if session_state.chest_pain_sev < 2:
                session_state.chest_pain_sev = random.randint(2, 4)
        
        # Cough correlation (r=0.319)
        if should_apply_correlation(0.319):
            if session_state.cough_sev < 2:
                session_state.cough_sev = random.randint(2, 4)
        
        # Thirst/갈증 correlation (r=0.307)
        if should_apply_correlation(0.307):
            if session_state.mouth_dry < 2:
                session_state.mouth_dry = random.randint(2, 4)
    
    # RULE 2: 기침 → 가래 (r=0.438)
    if session_state.cough_sev >= 3:
        if should_apply_correlation(0.438):
            if hasattr(session_state, 'phlegm_amt') and session_state.phlegm_amt < 2:
                session_state.phlegm_amt = random.randint(2, 4)
        
        # 기침 → 매핵기/throat obstruction (r=0.351)
        if should_apply_correlation(0.351):
            if hasattr(session_state, 'throat_dry'):
                session_state.throat_dry = True
    
    # RULE 3: 가래 → 매핵기 (r=0.443)
    if hasattr(session_state, 'phlegm_amt') and session_state.phlegm_amt >= 3:
        if should_apply_correlation(0.443):
            session_state.throat_dry = True
    
    return session_state


def apply_chest_tightness_cluster(session_state):
    """
    Page 36-38: 가슴답답함(흉민) 상관 클러스터
    - 흉민은 흉통, 스트레스, 우울, 경계, 두통, 수면, 꿈 등과 양의 상관관계를 가짐
    """
    if session_state.chest_tight_sev >= 3:
        # 흉민 → 흉통 (r=0.359)
        if should_apply_correlation(0.359):
            if session_state.chest_pain_sev < 2:
                session_state.chest_pain_sev = random.randint(2, 3)
        
        # 흉민 → 스트레스/불안 (r=0.322)
        if should_apply_correlation(0.322):
            if session_state.emot_anxiety < 2:
                session_state.emot_anxiety = random.randint(2, 4)
        
        # 흉민 → 두통 (r=0.356)
        if should_apply_correlation(0.356):
            if session_state.neck_nape_sev < 2:
                session_state.neck_nape_sev = random.randint(2, 3)
            if hasattr(session_state, 'headache_cold'):
                session_state.headache_cold = True
        
        # 흉민 → 상복통증 (r=0.385)
        if should_apply_correlation(0.385):
            if hasattr(session_state, 'abd_pain_sev') and session_state.abd_pain_sev < 2:
                session_state.abd_pain_sev = random.randint(2, 3)
    
    return session_state


def apply_stress_sleep_cluster(session_state):
    """
    Page 38: 스트레스-수면질-수면장애 상관 클러스터
    - 스트레스 ↔ 수면질: r=0.430
    - 수면질 ↔ 수면장애: r=0.695
    - 다몽 ↔ 수면장애: r=0.327
    - 다몽 ↔ 경계긴장: r=0.481
    - 다몽 ↔ 우울: r=0.358
    """
    # RULE 1: High stress → Poor sleep quality (r=0.430)
    if session_state.emot_anxiety >= 3 or (hasattr(session_state, 'stress_coping') and session_state.stress_coping == "나쁨"):
        if should_apply_correlation(0.430):
            if session_state.sleep_waking_state == "개운함":
                session_state.sleep_waking_state = random.choice(["피곤함", "무거움"])
            if session_state.sleep_depth == "깊음":
                session_state.sleep_depth = "얕음"
        
        # 스트레스 → 트림 (r=0.323)
        if should_apply_correlation(0.323):
            if hasattr(session_state, 'belching') and session_state.belching < 2:
                session_state.belching = random.randint(2, 3)
    
    # RULE 2: Poor sleep quality → Sleep disorder (r=0.695)
    if session_state.sleep_depth == "얕음" or session_state.sleep_waking_state in ["피곤함", "무거움"]:
        if should_apply_correlation(0.695):
            # High correlation - likely to have insomnia
            if not session_state.insomnia_onset and random.random() < 0.5:
                session_state.insomnia_onset = True
            if not session_state.insomnia_maintain and random.random() < 0.4:
                session_state.insomnia_maintain = True
    
    # RULE 3: 다몽/Frequent dreams correlations
    if session_state.dreams in ["자주", "악몽"]:
        # 다몽 → 수면장애 (r=0.327)
        if should_apply_correlation(0.327):
            session_state.sleep_depth = "얕음"
            session_state.insomnia_maintain = True
        
        # 다몽 → 경계긴장/불안 (r=0.481)
        if should_apply_correlation(0.481):
            if session_state.emot_anxiety < 3:
                session_state.emot_anxiety = random.randint(3, 4)
            if session_state.emot_startle < 3:
                session_state.emot_startle = random.randint(3, 4)
        
        # 다몽 → 우울 (r=0.358)
        if should_apply_correlation(0.358):
            if session_state.emot_depress < 2:
                session_state.emot_depress = random.randint(2, 3)
    
    # RULE 4: 경계긴장/불안 → 우울 (r=0.312)
    if session_state.emot_anxiety >= 3:
        if should_apply_correlation(0.312):
            if session_state.emot_depress < 2:
                session_state.emot_depress = random.randint(2, 3)
    
    return session_state


def apply_fatigue_pain_cluster(session_state):
    """
    Page 38: 피로-통증-허약 상관 클러스터
    - 피로 ↔ 통증: r=0.435
    - 피로 ↔ 허약: r=0.320
    """
    # RULE 1: 피로 → 통증 (r=0.435)
    if session_state.fatigue_level in ["심함", "중등도"]:
        if should_apply_correlation(0.435):
            # General pain increases with fatigue
            if session_state.pain_sev < 2:
                session_state.pain_sev = random.randint(2, 4)
            
            # Body aches more likely
            if hasattr(session_state, 'body_ache_cold'):
                session_state.body_ache_cold = True
        
        # 피로 → 허약 (r=0.320)
        if should_apply_correlation(0.320):
            if session_state.physical_strength == "강건":
                session_state.physical_strength = random.choice(["보통", "허약"])
            session_state.limb_weakness = True
    
    # Reverse: Pain → Fatigue
    if session_state.pain_sev >= 4:
        if should_apply_correlation(0.435):
            if session_state.fatigue_level in ["없음", "약함"]:
                session_state.fatigue_level = random.choice(["중등도", "심함"])
    
    return session_state


def apply_hearing_tinnitus_correlation(session_state):
    """
    Page 38: 난청-이명 상관관계
    - 난청 ↔ 이명: r=0.329
    """
    # RULE 1: 난청 → 이명 (r=0.329)
    if session_state.hearing_sev >= 3:
        if should_apply_correlation(0.329):
            if session_state.tinnitus_sev < 2:
                session_state.tinnitus_sev = random.randint(2, 4)
                session_state.tinnitus_freq = random.randint(2, 4)
    
    # RULE 2: 이명 → 난청 (bidirectional)
    if session_state.tinnitus_sev >= 3:
        if should_apply_correlation(0.329):
            if session_state.hearing_sev < 1:
                session_state.hearing_sev = random.randint(1, 3)
    
    return session_state


def apply_sweat_heat_negative_correlation(session_state):
    """
    Page 38: 땀 양-열 음의 상관관계
    - 땀양 ↔ 열: r=-0.372 (negative)
    - 땀 양이 많아지면 체온이 높아지는 것 배제 (땀이 체온을 낮춤)
    """
    # RULE: High sweat → body should NOT feel excessively hot
    if session_state.sweat_amt in ["다한", "많음"]:
        if should_apply_correlation(0.372):  # Use absolute value
            # Body heat feeling should decrease (sweating cools the body)
            if session_state.cold_heat_body in ["열"]:
                session_state.cold_heat_body = random.choice(["보통", "한"])
            
            # Heat sensitivity should decrease
            if session_state.heat_sensitivity >= 4:
                session_state.heat_sensitivity = random.randint(2, 3)
    
    # Reverse: If body feels hot, sweating should not be excessive (exclusion rule)
    if session_state.cold_heat_body in ["열"] and session_state.heat_sensitivity >= 4:
        if session_state.sweat_amt in ["다한"]:
            session_state.sweat_amt = random.choice(["보통", "무한"])
    
    return session_state


def apply_metabolic_syndrome_correlations(session_state):
    """
    Page 38: 고혈압-당뇨-이상지질혈증 상호 양의 상관성
    - 고혈압 ↔ 당뇨: r=0.340
    - 고혈압 ↔ 이상지질: r=0.447
    - 당뇨 ↔ 이상지질: r=0.414
    """
    metabolic_conditions = {
        "고혈압": 0.447,  # Highest correlation with others
        "당뇨": 0.340,
        "이상지질혈증": 0.414
    }
    
    history = session_state.history_conditions if hasattr(session_state, 'history_conditions') else []
    
    # Only apply for patients aged 40+
    if session_state.age >= 40:
        # Check each metabolic condition
        for cond, r_value in metabolic_conditions.items():
            if cond in history:
                # This condition exists, check correlations with others
                for other_cond, other_r in metabolic_conditions.items():
                    if other_cond != cond and other_cond not in history:
                        # Calculate combined probability
                        combined_r = (r_value + other_r) / 2
                        if should_apply_correlation(combined_r):
                            history.append(other_cond)
        
        session_state.history_conditions = list(set(history))  # Remove duplicates
    
    return session_state


# ═══════════════════════════════════════════════════════════════════════════════
# MASTER CORRELATION FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def apply_all_page36_38_correlations(session_state):
    """
    Master function to apply all correlation rules from Pages 36-38.
    Call this after randomization to ensure realistic symptom combinations.
    
    Returns:
        Modified session_state with correlation rules applied
    """
    # 1. Appetite-Digestion correlations (식욕-소화)
    session_state = apply_appetite_digestion_correlations(session_state)
    
    # 2. OCD-Appetite negative correlation (강박-식욕 음의 상관)
    session_state = apply_ocd_appetite_negative_correlation(session_state)
    
    # 3. Respiratory correlations (호흡기)
    session_state = apply_respiratory_correlations(session_state)
    
    # 4. Chest tightness cluster (흉민 클러스터)
    session_state = apply_chest_tightness_cluster(session_state)
    
    # 5. Stress-Sleep cluster (스트레스-수면 클러스터)
    session_state = apply_stress_sleep_cluster(session_state)
    
    # 6. Fatigue-Pain cluster (피로-통증 클러스터)
    session_state = apply_fatigue_pain_cluster(session_state)
    
    # 7. Hearing-Tinnitus correlation (난청-이명)
    session_state = apply_hearing_tinnitus_correlation(session_state)
    
    # 8. Sweat-Heat negative correlation (땀-열 음의 상관)
    session_state = apply_sweat_heat_negative_correlation(session_state)
    
    # 9. Metabolic syndrome correlations (대사증후군)
    session_state = apply_metabolic_syndrome_correlations(session_state)
    
    return session_state


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_correlation_consistency(session_state):
    """
    Validate that symptom correlations are consistent with Pages 36-38 rules.
    Returns list of any inconsistencies found.
    """
    issues = []
    
    # Check 1: Good appetite should not have severe digestion issues
    if session_state.appetite in ["항진"] and session_state.digestion in ["나쁨", "매우 나쁨"]:
        issues.append("Inconsistent: High appetite with poor digestion (강박 패턴 아니면 부적절)")
    
    # Check 2: High sweat with high heat feeling
    if session_state.sweat_amt in ["다한"] and session_state.cold_heat_body in ["열"]:
        issues.append("Warning: Excessive sweat with hot feeling (땀양-열 음의 상관 위반)")
    
    # Check 3: Severe fatigue without weakness
    if session_state.fatigue_level == "심함" and session_state.physical_strength == "강건":
        issues.append("Inconsistent: Severe fatigue with strong physical strength")
    
    # Check 4: Hearing loss without tinnitus correlation
    if session_state.hearing_sev >= 4 and session_state.tinnitus_sev == 0:
        issues.append("Warning: Severe hearing loss without any tinnitus (난청-이명 상관 누락)")
    
    return issues


def get_correlation_summary():
    """
    Return a summary of all correlation rules for documentation/display.
    """
    return {
        "positive_correlations": [
            "식욕좋음 → 비만, 음수량, 식사량 증가",
            "소화불량 → 상복부통증, 구역, 구토, 트림, 속쓰림",
            "숨참 → 흉통, 기침, 갈증",
            "기침 → 가래, 매핵기",
            "흉민 → 흉통, 스트레스, 두통, 수면장애",
            "스트레스 → 수면질 저하, 트림",
            "수면질 저하 → 수면장애",
            "다몽 → 경계긴장, 우울",
            "피로 → 통증, 허약",
            "난청 ↔ 이명",
            "고혈압 ↔ 당뇨 ↔ 이상지질혈증"
        ],
        "negative_correlations": [
            "강박/불안 → 식욕좋음 감소, 소화잘됨 감소",
            "땀양 많음 → 열감 감소 (땀이 체온 낮춤)"
        ],
        "source": "400명 임상한의사 차트리뷰 결과 (Pages 36-38)"
    }
