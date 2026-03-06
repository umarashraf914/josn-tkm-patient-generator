"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - CSV Symptom Mappers
Disease-specific functions that map CSV-generated patient data to session state
═══════════════════════════════════════════════════════════════════════════════
"""

import random
import logging
from clinical_lists import (
    PAST_COLD_PROBLEM_AREAS, AGGRAVATING_FACTORS, RELIEVING_FACTORS,
    get_random_additional_symptoms, get_random_comorbidities
)
from cold_constants import COLD_CHIEF_TYPES

logger = logging.getLogger("randomizer")

# ─── Logging helpers (mirrored from randomizer.py) ───────────────────────────
ENABLE_RANDOMIZER_LOGGING = False

def log_value_set(field_name: str, value, source: str):
    """Log when a session state value is set."""
    if ENABLE_RANDOMIZER_LOGGING:
        logger.debug(f"SET {field_name} = {value} [Source: {source}]")

def log_layer_start(layer_name: str):
    """Log when a layer starts."""
    if ENABLE_RANDOMIZER_LOGGING:
        logger.info(f"{'='*50}")
        logger.info(f"STARTING: {layer_name}")
        logger.info(f"{'='*50}")


def apply_cold_symptoms(session, patient_data):
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


def apply_rhinitis_symptoms(session, patient_data):
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


def apply_common_symptoms(session, patient_data):
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


def apply_dyspepsia_symptoms(session, patient_data):
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


def apply_backpain_symptoms(session, patient_data):
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
