"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Symptom Correlation Rules
Based on 400 Patient Chart Reviews (Pages 36-40)
═══════════════════════════════════════════════════════════════════════════════

This module contains correlation rules derived from 400-patient chart reviews:
- Positive correlations (symptoms that tend to occur together)
- Negative correlations (symptoms that exclude each other)
- Disease-specific correlations (e.g., cold symptoms)
"""

import random
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from symptom_correlations import apply_all_page36_38_correlations


def apply_symptom_correlation_rules(session):
    """
    Apply correlation rules based on 400 patient chart reviews (Pages 36-40).
    These rules adjust symptom severity and presence based on identified correlations.
    
    Args:
        session: Streamlit session_state object
    """
    _apply_appetite_digestion_correlations(session)
    _apply_anxiety_correlations(session)
    _apply_chest_correlations(session)
    _apply_respiratory_correlations(session)
    _apply_fatigue_correlations(session)
    _apply_hearing_tinnitus_correlations(session)
    _apply_sweat_heat_correlations(session)
    _apply_metabolic_correlations(session)
    _apply_stress_sleep_correlations(session)
    _apply_cold_specific_correlations(session)
    
    # Apply detailed correlations from external module
    apply_all_page36_38_correlations(session)


# ═══════════════════════════════════════════════════════════════════════════════
# APPETITE-DIGESTION CORRELATIONS (Pages 36-37)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_appetite_digestion_correlations(session):
    """
    Apply appetite-digestion correlation rules.
    
    Rules:
    - Good appetite correlates with good digestion (positive)
    - Dyspepsia correlates with upper abdominal symptoms (positive)
    """
    # Good appetite → better digestion
    if session.appetite in ["항진", "보통"]:
        if session.digestion in ["나쁨", "매우 나쁨"]:
            if random.random() < 0.7:  # 70% correlation strength
                session.digestion = random.choice(["보통", "좋음"])
    
    # Poor digestion → GI symptoms
    if session.digestion in ["나쁨", "매우 나쁨"]:
        if session.bloating < 2:
            session.bloating = random.randint(2, 4)
        if session.nausea < 2:
            session.nausea = random.randint(1, 3)


# ═══════════════════════════════════════════════════════════════════════════════
# ANXIETY CORRELATIONS (Pages 36-37)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_anxiety_correlations(session):
    """
    Apply anxiety-related correlation rules.
    
    Rules:
    - OCD/Anxiety negatively correlates with good appetite/digestion
    """
    if session.emot_anxiety >= 4:
        if session.appetite == "항진":
            session.appetite = random.choice(["보통", "저하"])
        if session.digestion == "좋음":
            session.digestion = random.choice(["보통", "나쁨"])


# ═══════════════════════════════════════════════════════════════════════════════
# CHEST SYMPTOM CORRELATIONS (Pages 36-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_chest_correlations(session):
    """
    Apply chest tightness correlation cluster.
    
    Rules:
    - Chest tightness correlates with stress, depression, anxiety
    - Chest tightness correlates with poor sleep quality
    """
    if session.chest_tight_sev >= 3:
        if session.emot_anxiety < 2:
            session.emot_anxiety = random.randint(2, 4)
        if session.emot_depress < 2:
            session.emot_depress = random.randint(2, 3)
        if session.sleep_depth == "깊음":
            session.sleep_depth = "얕음"


# ═══════════════════════════════════════════════════════════════════════════════
# RESPIRATORY CORRELATIONS (Pages 36-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_respiratory_correlations(session):
    """
    Apply respiratory-related correlations.
    
    Rules:
    - Dyspnea (elevated RR) correlates with cough and thirst
    - Cough correlates with phlegm
    """
    # Elevated respiratory rate → cough and dry mouth
    if session.resp >= 22:
        if session.cough_sev < 2:
            session.cough_sev = random.randint(2, 4)
        if session.mouth_dry < 2:
            session.mouth_dry = random.randint(2, 3)
    
    # Cough → phlegm
    if session.cough_sev >= 3:
        if session.phlegm_amt < 2:
            session.phlegm_amt = random.randint(2, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# FATIGUE CORRELATIONS (Pages 36-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_fatigue_correlations(session):
    """
    Apply fatigue-related correlations.
    
    Rules:
    - Fatigue-Pain positive correlation (r=0.435)
    - Fatigue-Weakness positive correlation (r=0.320)
    """
    if session.fatigue_level in ["심함", "중등도"]:
        # Weakness should be present
        if session.physical_strength == "강건":
            session.physical_strength = random.choice(["보통", "허약"])
        # General pain tends to be present
        if session.pain_sev < 2 and random.random() < 0.4:
            session.pain_sev = random.randint(2, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# HEARING-TINNITUS CORRELATIONS (Pages 36-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_hearing_tinnitus_correlations(session):
    """
    Apply hearing-tinnitus correlations.
    
    Rules:
    - Hearing loss and tinnitus have positive correlation (r=0.329)
    """
    if session.hearing_sev >= 3:
        if session.tinnitus_sev < 2:
            session.tinnitus_sev = random.randint(2, 4)
            session.tinnitus_freq = random.randint(2, 4)
    
    if session.tinnitus_sev >= 3:
        if session.hearing_sev < 1 and random.random() < 0.3:
            session.hearing_sev = random.randint(1, 2)


# ═══════════════════════════════════════════════════════════════════════════════
# SWEAT-HEAT CORRELATIONS (Pages 37-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_sweat_heat_correlations(session):
    """
    Apply sweat-heat negative correlation.
    
    Rules:
    - Sweat amount and heat have NEGATIVE correlation (r=-0.372)
    - High sweat → body should NOT feel excessively hot (sweat cools body)
    """
    if session.sweat_amt in ["다한", "많음"]:
        if session.cold_heat_body in ["열"]:
            if session.heat_sensitivity >= 5:
                session.heat_sensitivity = random.randint(2, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# METABOLIC SYNDROME CORRELATIONS (Pages 37-38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_metabolic_correlations(session):
    """
    Apply metabolic syndrome correlations.
    
    Rules:
    - Hypertension, Dyslipidemia, Diabetes have positive correlations (r=0.340-0.447)
    - If one metabolic condition exists, others are more likely
    """
    metabolic_conditions = ["고혈압", "당뇨", "이상지질혈증"]
    existing_metabolic = [c for c in metabolic_conditions if c in session.history_conditions]
    
    if len(existing_metabolic) >= 1 and session.age >= 40:
        for cond in metabolic_conditions:
            if cond not in session.history_conditions:
                if random.random() < 0.35:  # 35% correlation probability
                    session.history_conditions.append(cond)


# ═══════════════════════════════════════════════════════════════════════════════
# STRESS-SLEEP CLUSTER CORRELATIONS (Page 38)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_stress_sleep_correlations(session):
    """
    Apply stress-sleep cluster correlations.
    
    Rules:
    - Chest tightness/anxiety correlates with poor sleep
    - Sleep quality tends to decrease with stress
    """
    if session.chest_tight_sev >= 3 or session.emot_anxiety >= 4:
        if session.sleep_waking_state == "개운함":
            session.sleep_waking_state = random.choice(["피곤함", "무거움"])
        if not session.insomnia_onset and random.random() < 0.4:
            session.insomnia_onset = True


# ═══════════════════════════════════════════════════════════════════════════════
# COLD-SPECIFIC CORRELATIONS (Pages 39-40)
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_cold_specific_correlations(session):
    """
    Apply cold-specific correlation rules (Pages 39-40).
    """
    # Use Korean keyword for disease check
    if "감기" not in session.disease:
        return
    
    _apply_fever_respiratory_correlation(session)
    _apply_smoker_phlegm_correlation(session)
    _apply_snot_consistency_rules(session)
    _apply_alternating_fever_chills_rules(session)
    _apply_nasal_smell_correlation(session)
    _apply_phlegm_consistency_rules(session)
    _ensure_prominent_cold_symptom(session)
    
    # Additional Page 39-40 rules
    _apply_cold_chief_type_consistency(session)
    _apply_cold_exam_findings_correlation(session)
    _apply_cough_throat_correlation(session)
    _apply_body_ache_heaviness_correlation(session)


def _apply_fever_respiratory_correlation(session):
    """
    Page 40: High fever tends to cause shortness of breath.
    """
    if session.fever_sev >= 4:
        if session.resp < 18:
            session.resp = random.randint(18, 24)


def _apply_smoker_phlegm_correlation(session):
    """
    Page 40: Smokers have higher correlation with phlegm amount and color.
    """
    if session.social_smoke_daily > 0:
        if session.phlegm_amt < 2:
            session.phlegm_amt = random.randint(2, 4)
        if session.phlegm_color in ["맑음", "없음"]:
            session.phlegm_color = random.choice(["백색", "황색"])


def _apply_snot_consistency_rules(session):
    """
    Page 40: No snot = no snot color (NEGATIVE correlation).
    콧물이 없을 때 콧물색도 없어야 함
    """
    if session.snot_sev <= 1:
        session.snot_type = "없음"
        if hasattr(session, 'snot_color'):
            session.snot_color = "없음"


def _apply_alternating_fever_chills_rules(session):
    """
    Page 40: Alternating chills-fever AND (fever OR chills) simultaneously is IMPOSSIBLE.
    한열왕래하면서 발열, 오한이 심한 경우는 없음
    """
    alternating_present = False
    if hasattr(session, 'alternating_chills_fever'):
        if session.alternating_chills_fever >= 3:
            alternating_present = True
    
    if alternating_present:
        if session.fever_sev >= 4:
            session.fever_sev = random.randint(2, 3)
        if session.chills_sev >= 4:
            session.chills_sev = random.randint(2, 3)


def _apply_nasal_smell_correlation(session):
    """
    Page 40: Nasal congestion can be accompanied by smell reduction.
    코막힘이 있을 때 후각감퇴 동반 가능
    """
    if session.nose_block_sev >= 3:
        if hasattr(session, 'smell_reduction'):
            if session.smell_reduction < 2:
                session.smell_reduction = random.randint(2, 4)


def _apply_phlegm_consistency_rules(session):
    """
    Page 39: Phlegm color only specified if phlegm exists.
    가래가 없으면 가래색도 없음
    """
    if session.phlegm_amt <= 1:
        session.phlegm_color = "None"


def _ensure_prominent_cold_symptom(session):
    """
    Page 39-40: Ensure at least one prominent cold symptom exists.
    감기 주소증 유형별 생성 (최소 1개 이상)
    """
    cold_prominent_symptoms = []
    
    if session.fever_sev >= 3:
        cold_prominent_symptoms.append("fever")
    if session.chills_sev >= 3:
        cold_prominent_symptoms.append("chills")
    if session.snot_sev >= 3:
        cold_prominent_symptoms.append("snot")
    if session.nose_block_sev >= 3:
        cold_prominent_symptoms.append("nasal_congestion")
    if session.cough_sev >= 3:
        cold_prominent_symptoms.append("cough")
    
    # If no prominent symptom, make at least one prominent
    if len(cold_prominent_symptoms) == 0:
        symptom_to_raise = random.choice(["fever_sev", "chills_sev", "snot_sev", "cough_sev"])
        setattr(session, symptom_to_raise, random.randint(3, 5))


# ═══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL PAGE 39-40 RULES
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_cold_chief_type_consistency(session):
    """
    Page 39: Cold chief type must match prominent symptoms.
    감기주소증 유형이 실제 증상과 일치해야 함
    
    [교수님 피드백] 인후통(목감기), 몸살(신체통) 포함
    """
    if not hasattr(session, 'cold_chief_type') or not session.cold_chief_type:
        return
    
    # Map chief types to their corresponding symptom variables
    # [교수님 피드백] 인후통, 몸살 명시
    chief_type_symptom_map = {
        "발열증상 위주": ("fever_sev", 3),
        "오한증상 위주": ("chills_sev", 3),
        "콧물 위주": ("snot_sev", 3),
        "코막힘 위주": ("nose_block_sev", 3),
        "인후통 위주": ("sore_throat", True),  # 목감기
        "재채기 위주": ("sneeze_sev", 3),
        "기침증상 위주": ("cough_sev", 3),
        "가래 위주": ("phlegm_amt", 3),
        "몸살 위주": ("body_ache_cold", True),  # 신체통
        "신중 위주": ("body_heaviness_cold", True),
        "두통/경항통 위주": ("headache_cold", True),
    }
    
    for chief_type in session.cold_chief_type:
        for type_name, (attr, threshold) in chief_type_symptom_map.items():
            if type_name in chief_type:
                if hasattr(session, attr):
                    current_value = getattr(session, attr)
                    # If boolean attribute
                    if isinstance(threshold, bool):
                        if not current_value:
                            setattr(session, attr, True)
                    # If numeric attribute
                    elif isinstance(current_value, (int, float)):
                        if current_value < threshold:
                            setattr(session, attr, random.randint(threshold, 5))
                break


def _apply_cold_exam_findings_correlation(session):
    """
    Page 40: Examination findings should correlate with symptoms.
    진찰소견이 증상과 일치해야 함
    """
    # Stethoscope findings correlation with respiratory symptoms
    if hasattr(session, 'exam_stethoscope'):
        # High cough or phlegm → abnormal lung sounds
        if session.cough_sev >= 4 or (hasattr(session, 'phlegm_amt') and session.phlegm_amt >= 4):
            if session.exam_stethoscope == "정상":
                session.exam_stethoscope = random.choice(["수포음", "천명음"])
        
        # Dyspnea present → may have abnormal sounds
        if hasattr(session, 'cold_dyspnea') and session.cold_dyspnea:
            if session.exam_stethoscope == "정상" and random.random() < 0.5:
                session.exam_stethoscope = random.choice(["감소", "천명음"])
    
    # Throat visual exam correlation with sore throat
    if hasattr(session, 'exam_throat_visual'):
        if hasattr(session, 'sore_throat') and session.sore_throat:
            if session.exam_throat_visual == "정상":
                session.exam_throat_visual = random.choice(["발적", "부종"])
    
    # Rhinoscope findings correlation with nasal symptoms
    if hasattr(session, 'exam_rhinoscope_finding'):
        # Severe nasal congestion → congestion finding
        if session.nose_block_sev >= 3:
            if session.exam_rhinoscope_finding == "정상":
                session.exam_rhinoscope_finding = random.choice(["충혈", "분비물"])
        
        # High snot → discharge finding
        if session.snot_sev >= 3:
            if session.exam_rhinoscope_finding == "정상" and random.random() < 0.6:
                session.exam_rhinoscope_finding = "분비물"


def _apply_cough_throat_correlation(session):
    """
    Page 39-40: Cough correlates with throat symptoms.
    기침이 심하면 인후통/인후부 증상 동반 가능
    """
    # Severe cough → may have throat symptoms
    if session.cough_sev >= 4:
        if hasattr(session, 'sore_throat') and not session.sore_throat:
            if random.random() < 0.4:  # 40% chance
                session.sore_throat = True
        
        # Throat dryness with dry cough
        if hasattr(session, 'throat_dry') and not session.throat_dry:
            if session.phlegm_amt <= 1:  # Dry cough (little phlegm)
                if random.random() < 0.6:
                    session.throat_dry = True


def _apply_body_ache_heaviness_correlation(session):
    """
    Page 39-40: Body ache and heaviness correlations.
    몸살과 신중(몸이 무거움) 증상 상관관계
    """
    # Severe fever/chills often accompanied by body ache
    if session.fever_sev >= 3 or session.chills_sev >= 3:
        if hasattr(session, 'body_ache_cold') and not session.body_ache_cold:
            if random.random() < 0.5:  # 50% chance
                session.body_ache_cold = True
    
    # Body ache → body heaviness correlation
    if hasattr(session, 'body_ache_cold') and session.body_ache_cold:
        if hasattr(session, 'body_heaviness_cold') and not session.body_heaviness_cold:
            if random.random() < 0.4:  # 40% chance
                session.body_heaviness_cold = True
    
    # Fatigue correlation with body symptoms
    if session.fatigue_level in ["심함", "중등도"]:
        if hasattr(session, 'body_heaviness_cold') and not session.body_heaviness_cold:
            if random.random() < 0.5:
                session.body_heaviness_cold = True
