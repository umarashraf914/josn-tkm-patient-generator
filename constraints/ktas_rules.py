"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - KTAS Emergency Exclusion Rules
Based on Page 25 of Clinical Guidelines
═══════════════════════════════════════════════════════════════════════════════

CRITICAL: These rules ensure patient safety by excluding emergency cases.
Only generate KTAS Level 4-5 (준응급, 비응급) patients for 한의원 setting.

응급상황 배제 기준 (KTAS Level 1-2 Exclusion Criteria):
═══════════════════════════════════════════════════════════════════════════════
| 임상지표     | 응급상황 (KTAS 1~2등급) 기준 [배제 기준]           |
|-------------|---------------------------------------------------|
| 의식 상태   | 통증에만 반응(P) 혹은 무반응(U), 혼돈(Confusion)  |
| 혈압 (SBP)  | <90 mmHg (저혈압/쇼크), >180mmHg (보수적 200mmHg) |
| 맥박 (HR)   | <50회 또는 >130회/분 (서맥/빈맥)                   |
| 호흡 (RR)   | <10회 또는 >30회/분 (호흡부전)                     |
| 체온 (BT)   | <35.0°C (저체온) 또는 >40.5°C (고체온)            |
| 산소포화도  | SpO2 < 92% (저산소증)                             |
| 통증 (NRS)  | 8점 이상 (극심한 통증)                             |
═══════════════════════════════════════════════════════════════════════════════
"""

import random


# KTAS Safe Ranges
KTAS_LIMITS = {
    'sbp': {'min': 90, 'max': 200, 'safe_range': (95, 170)},
    'dbp': {'min': 60, 'max': 110, 'safe_range': (65, 100)},
    'pulse_rate': {'min': 50, 'max': 130, 'safe_range': (55, 120)},
    'resp': {'min': 10, 'max': 30, 'safe_range': (12, 24)},
    'temp': {'min': 35.0, 'max': 40.5, 'safe_range': (36.0, 39.5)},
    'pain_sev': {'max': 7},  # NRS < 8
    'dizziness_sev': {'max': 4},  # With vision blackout
    'consciousness': {'allowed': ['A', 'V']},  # AVPU: only Alert/Voice allowed
    'spo2': {'min': 92, 'safe_range': (95, 100)},  # SpO2 < 92% = hypoxemia
}


def apply_ktas_rules(session):
    """
    Apply KTAS Level 1-2 exclusion rules for patient safety.
    
    Args:
        session: Streamlit session_state object
    """
    _apply_consciousness_rules(session)
    _apply_spo2_rules(session)
    _apply_blood_pressure_rules(session)
    _apply_heart_rate_rules(session)
    _apply_respiratory_rules(session)
    _apply_temperature_rules(session)
    _apply_pain_rules(session)
    _apply_neurological_rules(session)


def _apply_consciousness_rules(session):
    """
    Apply consciousness level (AVPU) safety rules.
    
    Rules:
    - Only Alert (A) and Voice-responsive (V) are allowed for KTAS 4-5
    - Pain-responsive (P), Unresponsive (U), Confusion are KTAS 1-2 → excluded
    """
    allowed = KTAS_LIMITS['consciousness']['allowed']
    if session.consciousness not in allowed:
        session.consciousness = 'A'  # Default to Alert


def _apply_spo2_rules(session):
    """
    Apply oxygen saturation (SpO2) safety rules.
    
    Rules:
    - SpO2 must be ≥92% (exclude <92% hypoxemia which is KTAS Level 1-2)
    """
    if session.spo2 < KTAS_LIMITS['spo2']['min']:
        session.spo2 = random.randint(
            KTAS_LIMITS['spo2']['safe_range'][0],
            KTAS_LIMITS['spo2']['safe_range'][1]
        )


def _apply_blood_pressure_rules(session):
    """
    Apply blood pressure safety rules.
    
    Rules:
    - SBP must be 90-200 mmHg (exclude <90 hypotension/shock, >200 hypertensive crisis)
    - DBP must be 60-110 mmHg
    - DBP must be less than SBP by at least 20 mmHg (pulse pressure)
    """
    # SBP Rules
    if session.sbp < KTAS_LIMITS['sbp']['min']:
        session.sbp = random.randint(95, 130)
    if session.sbp > KTAS_LIMITS['sbp']['max']:
        session.sbp = random.randint(130, 190)
    
    # DBP Rules
    if session.dbp < KTAS_LIMITS['dbp']['min']:
        session.dbp = random.randint(65, 85)
    if session.dbp > KTAS_LIMITS['dbp']['max']:
        session.dbp = random.randint(70, 100)
    
    # Pulse Pressure Rule: DBP must be less than SBP (by at least 20)
    if session.dbp >= session.sbp:
        session.dbp = session.sbp - random.randint(20, 40)


def _apply_heart_rate_rules(session):
    """
    Apply heart rate safety rules.
    
    Rules:
    - HR must be 50-130 bpm (exclude <50 bradycardia, >130 tachycardia)
    """
    if session.pulse_rate < KTAS_LIMITS['pulse_rate']['min']:
        session.pulse_rate = random.randint(55, 75)
    if session.pulse_rate > KTAS_LIMITS['pulse_rate']['max']:
        session.pulse_rate = random.randint(70, 120)


def _apply_respiratory_rules(session):
    """
    Apply respiratory rate safety rules.
    
    Rules:
    - RR must be 10-30/min (exclude <10 or >30 respiratory failure)
    """
    if session.resp < KTAS_LIMITS['resp']['min']:
        session.resp = random.randint(12, 18)
    if session.resp > KTAS_LIMITS['resp']['max']:
        session.resp = random.randint(16, 24)


def _apply_temperature_rules(session):
    """
    Apply temperature safety rules.
    
    Rules:
    - Temperature must be 35.0-40.5°C (exclude hypothermia <35, hyperthermia >40.5)
    """
    if session.temp < KTAS_LIMITS['temp']['min']:
        session.temp = round(random.uniform(36.0, 37.0), 1)
    if session.temp > KTAS_LIMITS['temp']['max']:
        session.temp = round(random.uniform(37.5, 39.5), 1)


def _apply_pain_rules(session):
    """
    Apply pain severity safety rules.
    
    Rules:
    - Pain NRS must be < 8 (exclude severe pain ≥8 which is KTAS Level 3+)
    """
    if session.pain_sev >= 8:
        session.pain_sev = random.randint(3, 7)


def _apply_neurological_rules(session):
    """
    Apply neurological symptom safety rules.
    
    Rules:
    - Exclude severe dizziness with vision blackout (KTAS emergency)
    """
    if session.dizziness_sev >= 5 and session.vision_blackout:
        session.dizziness_sev = random.randint(2, 4)
        session.vision_blackout = False
