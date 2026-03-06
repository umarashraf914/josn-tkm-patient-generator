"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - General Consistency Rules
Clinical Logic Constraints for Realistic Patient Data
═══════════════════════════════════════════════════════════════════════════════

This module ensures clinical consistency across various data points:
- Fever-Temperature consistency
- Women's health constraints
- Mental/Appetite constraints
- BMI/Body composition constraints
- Sleep constraints
- Excretion constraints
- Pulse-Tongue consistency
"""

import random


def apply_consistency_rules(session):
    """
    Apply general clinical consistency rules.
    
    Args:
        session: Streamlit session_state object
    """
    _apply_age_height_weight_constraints(session)  # Apply first!
    _apply_fever_temperature_consistency(session)
    _apply_womens_health_constraints(session)
    _apply_snot_rhinitis_constraints(session)
    _apply_mental_appetite_constraints(session)
    _apply_bmi_body_constraints(session)
    _apply_sleep_constraints(session)
    _apply_excretion_constraints(session)
    _apply_pulse_tongue_constraints(session)


def _apply_age_height_weight_constraints(session):
    """
    Ensure height, weight, job, alcohol, and smoking are appropriate for the patient's age and sex.
    
    Age-appropriate ranges (approximate Korean averages):
    - Minimum age is 10 (to match CSV rule categories)
    - Korean Male average height: ~172cm
    - Korean Female average height: ~159cm
    
    Sex-specific height ranges:
    - Male: Generally 160-185cm for adults
    - Female: Generally 150-168cm for adults
    
    Age ranges:
    - Adolescents (10-17): Growing, height varies by age
    - Young Adults (18-19): Near adult height
    - Adults (20-64): Full adult height
    - Elderly (65+): May be slightly shorter
    """
    age = session.age
    sex = session.sex  # "남" or "여"
    
    # Enforce minimum age = 10 (CSV rules start at age category 1 = 10-19)
    if age < 10:
        session.age = 10
        age = 10
    
    # ===========================================
    # MINORS (10-17): Strict constraints (sex-specific)
    # ===========================================
    if age <= 17:
        # Height: grows with age, boys grow faster after ~13
        if sex == "남":
            min_height = max(130, 130 + (age - 10) * 4)  # Boys grow faster
            max_height = 145 + (age - 10) * 5
        else:
            # Girls: earlier growth spurt, slower after ~14, max 170cm
            min_height = max(130, 132 + (age - 10) * 3)
            max_height = min(140 + (age - 10) * 4, 170)  # Cap at 170cm
        
        if session.height > max_height:
            session.height = random.randint(min_height, max_height)
        if session.height < min_height:
            session.height = random.randint(min_height, min(max_height, min_height + 15))
        
        # Weight: proportional to height/age
        # UI minimum is 30kg, so ensure weight is at least 30
        min_weight = max(30, 28 + (age - 10) * 4)   # ~30kg at 10 (UI min), grows with age
        max_weight = 40 + (age - 10) * 5   # ~40kg at 10, ~75kg at 17
        if session.weight > max_weight:
            session.weight = random.randint(min_weight, max_weight)
        if session.weight < min_weight:
            session.weight = random.randint(min_weight, min(max_weight, min_weight + 10))
        
        # Job: Minors can ONLY be students
        session.job = "학생"
        
        # Alcohol: Minors cannot drink
        session.social_alcohol_freq = "비음주"
        
        # Smoking: Minors should not smoke (or very minimal if > 15)
        if age < 16:
            session.social_smoke_daily = 0.0
        elif session.social_smoke_daily > 5:
            session.social_smoke_daily = random.uniform(0, 3)
    
    # ===========================================
    # YOUNG ADULTS (18-19): Some restrictions (sex-specific)
    # ===========================================
    elif age <= 19:
        if sex == "남":
            if session.height > 190:
                session.height = random.randint(165, 182)
            if session.height < 160:
                session.height = random.randint(162, 175)
        else:
            # Female young adults - max 170cm
            if session.height > 170:
                session.height = random.randint(155, 168)
            if session.height < 150:
                session.height = random.randint(152, 163)
        
        if session.weight > 90:
            session.weight = random.randint(50, 80)
        if session.weight < 45:
            session.weight = random.randint(48, 65)
        
        # Job: Young adults typically students or entry-level
        if session.job in ["관리직", "전문직"]:
            session.job = random.choice(["학생", "사무직"])
    
    # ===========================================
    # ADULTS (20-64): Normal ranges (sex-specific)
    # ===========================================
    elif age <= 64:
        if sex == "남":
            if session.height < 155:
                session.height = random.randint(165, 178)
            if session.height > 195:
                session.height = random.randint(170, 185)
        else:
            # Female adults - max 170cm
            if session.height > 170:
                session.height = random.randint(155, 168)
            if session.height < 148:
                session.height = random.randint(152, 162)
        
        if session.weight < 40:
            session.weight = random.randint(50, 70)
    
    # ===========================================
    # ELDERLY (65+): Adjusted ranges (sex-specific, slight height decrease with age)
    # ===========================================
    else:
        if sex == "남":
            if session.height > 182:
                session.height = random.randint(160, 175)
            if session.height < 155:
                session.height = random.randint(158, 170)
        else:
            # Female elderly - max 170cm
            if session.height > 170:
                session.height = random.randint(150, 163)
            if session.height < 145:
                session.height = random.randint(148, 158)
        
        if session.weight > 95:
            session.weight = random.randint(55, 80)
        if session.weight < 40:
            session.weight = random.randint(45, 65)
        
        # Elderly typically retired
        if session.job == "학생":
            session.job = random.choice(["사무직", "가사"])


def _apply_fever_temperature_consistency(session):
    """
    Ensure fever severity matches actual temperature reading.
    
    Rules:
    - High Fever (level 4-5) must have elevated temp (≥38.0°C)
    - Low/No Fever (level 1-2) should have normal temperature (<38.5°C)
    - Medium fever (level 3) = mild temp elevation (37.4-38.4°C)
    """
    if session.fever_sev >= 4 and session.temp < 38.0:
        session.temp = round(random.uniform(38.0, 39.5), 1)
    
    if session.fever_sev <= 2 and session.temp >= 38.5:
        session.temp = round(random.uniform(36.0, 37.3), 1)
    
    if session.fever_sev == 3 and (session.temp < 37.4 or session.temp >= 38.5):
        session.temp = round(random.uniform(37.4, 38.4), 1)


def _apply_womens_health_constraints(session):
    """
    Apply women's health constraints based on age and sex.
    
    Rules:
    - Women's health only applies to females aged 14-50
    - Males have no menstrual data
    - Women >50 marked as menopause
    """
    if session.sex == "여":
        if session.age < 14 or session.age > 50:
            session.mens_regular = "Menopause" if session.age > 50 else "N/A"
            session.mens_pain_score = 0
            session.mens_duration = 0
        else:
            if session.mens_regular == "Menopause":
                session.mens_regular = random.choice(["Regular", "Irregular"])
    else:
        # Male patients - reset all women's health variables
        session.mens_pain_score = 0
        session.mens_duration = 0


def _apply_snot_rhinitis_constraints(session):
    """
    Apply snot/rhinitis consistency rules.
    
    Rules:
    - No snot (severity ≤1) means clear/none type
    """
    if session.snot_sev <= 1:
        session.snot_type = "Clear/Watery (맑음/물)"


def _apply_mental_appetite_constraints(session):
    """
    Apply mental state and appetite consistency rules.
    
    Rules:
    - No appetite + High motivation is impossible
    - Severe fatigue should lower motivation
    - Poor memory + High stress coping is inconsistent
    """
    if session.appetite == "없음" and session.motivation == "높음":
        session.motivation = "낮음"
    
    if session.fatigue_level == "심함" and session.motivation == "높음":
        session.motivation = random.choice(["보통", "낮음"])
    
    if session.memory == "나쁨" and session.stress_coping == "좋음":
        session.stress_coping = random.choice(["보통", "나쁨"])


def _apply_bmi_body_constraints(session):
    """
    Apply BMI and body composition consistency rules.
    
    Rules:
    - Low BMI (<18.5) + Solid body is inconsistent
    - High BMI (>30) + Soft body is inconsistent
    """
    height_m = session.height / 100
    bmi = session.weight / (height_m * height_m)
    
    if bmi < 18.5 and session.body_solidity == "단단":
        session.body_solidity = "물렁"
    if bmi > 30 and session.body_solidity == "물렁":
        session.body_solidity = random.choice(["보통", "단단"])


def _apply_sleep_constraints(session):
    """
    Apply sleep-related consistency rules.
    
    Rules:
    - Very short sleep (≤4 hours) affects waking state
    - Good sleep (≥8 hours, deep) should feel refreshed
    - Insomnia = shallow sleep
    - Frequent night urination = poor sleep
    - Frequent dreams/nightmares = shallow sleep
    """
    if session.sleep_hours <= 4:
        session.sleep_waking_state = random.choice(["피곤함", "무거움"])
    
    if session.sleep_hours >= 8 and session.sleep_depth == "깊음":
        session.sleep_waking_state = "개운함"
    
    if session.insomnia_onset or session.insomnia_maintain:
        session.sleep_depth = "얕음"
    
    if session.urine_freq_night >= 3:
        session.sleep_depth = "얕음"
        if session.sleep_waking_state == "개운함":
            session.sleep_waking_state = "피곤함"
    
    if session.dreams in ["자주", "악몽"]:
        session.sleep_depth = "얕음"


def _apply_excretion_constraints(session):
    """
    Apply excretion-related consistency rules.
    
    Rules:
    - Constipation + Loose stool is inconsistent
    - Frequent stool (2-3/day) shouldn't be hard
    """
    if session.stool_freq == "변비" and session.stool_form == "묽음/연변":
        session.stool_form = "굳음/경변"
    
    if session.stool_freq == "2-3회/일" and session.stool_form == "굳음/경변":
        session.stool_form = random.choice(["보통", "묽음/연변"])


def _apply_pulse_tongue_constraints(session):
    """
    Apply pulse-tongue TKM diagnostic consistency rules.
    
    Rules:
    - Strong pulse + Pale tongue (deficiency sign) is rare
    - Weak pulse + Red tongue (heat sign) is inconsistent
    """
    if session.pulse_strength == "강력" and session.tongue_color == "담백":
        session.tongue_color = random.choice(["담홍", "홍설"])
    
    if session.pulse_strength == "무력" and session.tongue_color == "홍설":
        session.tongue_color = random.choice(["담백", "담홍"])
