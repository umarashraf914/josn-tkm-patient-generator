"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Batch Prompt Builder
LLM prompt construction and Gemini API integration for batch generation
═══════════════════════════════════════════════════════════════════════════════
"""

import json
from google import genai
from data_mappings import get_desc
from constants import DISEASE_PATTERNS

GEMINI_MODEL = "gemini-2.5-flash"


def generate_scenario_with_gemini(client, session) -> tuple[str, str]:
    """Generate patient scenario using Gemini API."""
    
    # Build prompt using same logic as patient_generator.py
    fever_desc = get_desc("fever_sev", session.fever_sev) or f"레벨 {session.fever_sev}"
    chills_desc = get_desc("chills_sev", session.chills_sev) or f"레벨 {session.chills_sev}"
    snot_desc = get_desc("snot_sev", session.snot_sev) or f"레벨 {session.snot_sev}"
    cough_desc = get_desc("cough_sev", session.cough_sev) or f"레벨 {session.cough_sev}"
    sneeze_desc = get_desc("rhinitis_sneeze", session.sneeze_sev) or f"레벨 {session.sneeze_sev}"
    nose_block_desc = get_desc("rhinitis_block", session.nose_block_sev) or f"레벨 {session.nose_block_sev}"
    nose_itch_desc = get_desc("rhinitis_itch", session.nose_itch_sev) or f"레벨 {session.nose_itch_sev}"
    rhinitis_snot_desc = get_desc("rhinitis_snot_sev", session.snot_sev) or f"레벨 {session.snot_sev}"
    
    # Calculate BMI
    bmi_str = "N/A"
    if session.get("height", 0) > 0:
        bmi = session.weight / ((session.height / 100) ** 2)
        bmi_str = f"{bmi:.1f}"
    
    # Build pattern info
    selected_pattern = "N/A"
    disease_key = None
    if "감기" in session.disease:
        disease_key = "감기"
    elif "비염" in session.disease:
        disease_key = "알레르기비염"
    elif "요통" in session.disease:
        disease_key = "요통"
    elif "소화불량" in session.disease:
        disease_key = "기능성소화불량"
    
    if disease_key and disease_key in DISEASE_PATTERNS:
        patterns = DISEASE_PATTERNS[disease_key]["patterns"]
        idx = session.get("pattern_idx", 0)
        if 0 <= idx < len(patterns):
            p = patterns[idx]
            # For 알레르기비염, prescription name IS the pattern name
            if disease_key == "알레르기비염":
                selected_pattern = p['name']
            else:
                selected_pattern = f"{p['name']} → {', '.join(p['prescriptions'])}"
    
    # Store pattern name for PDF
    session.pattern_name = selected_pattern
    
    system_prompt = build_batch_prompt(session, selected_pattern,
                                        fever_desc, chills_desc, snot_desc, cough_desc,
                                        sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc,
                                        bmi_str)
    
    # Call Gemini
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=system_prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        
        summary = data.get('요약', '환자 시나리오')
        scenario = data.get('환자시나리오', data.get('초진기록', response.text))
        
        return summary, scenario
        
    except Exception as e:
        print(f"  ❌ Gemini API error: {e}")
        return None, None


def get_menstrual_info(session):
    """폐경 여부에 따라 여성력 정보 반환"""
    if session.sex != "여":
        return "해당없음 (남성)"
    
    if session.get('mens_regular', '') == "폐경":
        return "폐경"
    else:
        return f"생리주기 {session.get('mens_cycle', 'N/A')}일, 규칙성 {session.get('mens_regular', 'N/A')}, 기간 {session.get('mens_duration', 'N/A')}일, 생리통 {session.get('mens_pain_score', 0)}/10"


def build_batch_prompt(session, selected_pattern,
                        fever_desc, chills_desc, snot_desc, cough_desc,
                        sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc,
                        bmi_str="N/A"):
    """Build the LLM prompt for batch patient generation (same as patient_generator.py)."""
    
    return f"""
    당신은 한의 임상 가상환자 시나리오 생성 전문가입니다.
    
    ## 역할
    한의사의 관점에서 환자 정보를 진료기록부 형식으로 정리하세요.
    ❌ 환자 시점 (예: "저는 열이 나고...")이 아닌
    ✅ 의사 시점 (예: "상기 환자는 발열을 호소하며...")으로 작성하세요.
    
    ⚠️ 중요: 변증(辨證), 치법(治法), 처방(處方)은 절대 생성하지 마세요!
    ⚠️ 중요: 모든 출력은 100% 한국어로만 작성하세요! 영어 금지!
    
    ## 환자 정보 (Patient Data)
    
    ### 1. 인구학적정보 및 활력징후
    - 나이/성별: {session.age}세 {session.sex}
    - 직업: {session.job}
    - 신장/체중/BMI: {session.height}cm / {session.weight}kg / BMI {bmi_str}
    - 발현시점: {session.onset}
    - 경과: {session.course}
    - 발병 에피소드: {session.get('episode', '특별한 계기 없이 발생')}
    - 활력징후: BP {session.sbp}/{session.dbp} mmHg, 맥박 {session.pulse_rate}회/분, 체온 {session.temp}°C, 호흡 {session.resp}회/분

    ### 2. 병력 및 생활습관
    - 현병력: {session.history_conditions}
    - 약물력: {session.meds_specific}
    - 가족력: {session.family_hx}
    - 악화요인: {session.get('aggravating_factors', [])}
    - 완화요인: {session.get('relieving_factors', [])}
    - 음주: {session.social_alcohol_freq}
    - 흡연: {session.social_smoke_daily}개피/일
    - 운동강도: {session.social_exercise_int}
    - 여성력: {get_menstrual_info(session)}
    
    ### 3. 배설 및 식사
    - 식사횟수: {session.diet_freq}회/일, {session.diet_regular}
    - 음수량: {session.water_intake}
    - 대변: {session.stool_freq}, {session.stool_color}, {session.stool_form}
    - 소변: {session.urine_color}, 주간 {session.urine_freq_day}회, 야간 {session.urine_freq_night}회
    
    ### 4. 수면, 땀, 한열
    - 수면: {session.sleep_hours}시간, {session.sleep_depth}, 기상시 {session.sleep_waking_state}
    - 입면장애: {session.insomnia_onset}/5, 중도각성: {session.insomnia_maintain}/5
    - 땀: {session.sweat_amt}, {session.sweat_area}, 땀흘린후 {session.get('sweat_feeling', 'N/A')}
    - 한열경향: {session.cold_heat_pref}
    - 음료온도선호: {session.drink_temp}
    - 수족냉증: {session.get('cold_hands_feet', False)}
    
    ### 5. 정신상태 및 신체검진
    - 기억력: {session.memory}, 의욕: {session.motivation}
    - 스트레스대처력: {session.stress_coping}
    - 부종: {session.edema}, 멍듦: {session.bruising}
    - 사지무력감: {session.limb_weakness}
    - 피부건조도: {session.skin_dry}, 가려움: {session.skin_itch}
    - 이명강도: {session.tinnitus_sev}/5, 난청: {session.hearing_sev}/5
    - 어지러움: {session.dizziness_sev}/5
    - 면색: {session.face_color}
    
    ### 6. 맥진 및 설진
    - 맥위(부침): {session.pulse_depth}
    - 맥폭(대세): {session.pulse_width}
    - 맥력: {session.pulse_strength}
    - 맥상: {session.pulse_smooth}
    - 복합맥상: {session.get('compound_pulse', '완맥')}
    - 설질: {session.tongue_color}, {session.tongue_size}
    - 설태: {session.tongue_coat_color}, {session.tongue_coat_thick}
    
    ### 7. 주소증 (Chief Complaint)
    - 질환명: {session.disease}
    
    **감기 증상:** 발열 {fever_desc}, 오한 {chills_desc}, 콧물 {snot_desc}, 기침 {cough_desc}
    **비염 증상:** 재채기 {sneeze_desc}, 코막힘 {nose_block_desc}, 코가려움 {nose_itch_desc}
    **요통 증상:** 통증강도 {session.pain_sev}/10, 통증양상 {session.get('pain_nature', [])}
    **소화불량 증상:** 복만/복통 {session.pain_sev}/5, 증상 {session.get('dyspepsia_spec', [])}

    ## 출력 형식 (JSON)
    반드시 아래 형식으로 JSON을 생성하세요:
    
    {{
      "요약": "환자 요약 (예: 45세 남성, 3일전부터 오한, 발열, 두통 호소)",
      
      "환자시나리오": "한의사 관점의 상세 환자 기록. 반드시 다음 형식으로 작성:
        
        【환자정보】
        상기 환자는 XX세 XX 환자로 [직업] 종사자이다. 신장은 XXcm, 체중은 XXkg, BMI는 XX이다.
        
        【주소증】
        [발현시점]부터 [주요증상]을 주소로 내원하였다.
        
        【발병 에피소드】
        [발병 전 상황을 구체적으로 기술]
        
        【현병력】
        [증상의 발생, 경과, 양상, 악화/완화 요인을 상세히 기술]
        
        【과거력】
        [기존 질환, 수술력, 약물력]
        
        【가족력】
        [가족 질환력]
        
        【사회력】
        [직업, 음주, 흡연, 운동 습관]
        
        【계통적 문진 (Review of Systems)】
        - 식욕/소화: [식욕, 소화 상태, 오심/구토]
        - 대변: [횟수, 성상, 색깔]
        - 소변: [횟수, 색깔, 야간뇨]
        - 수면: [수면시간, 질, 입면장애(X/5), 중도각성(X/5)]
        - 한열: [오한/발열 경향, 수족냉증, 온도 선호]
        - 땀: [발한 정도, 부위, 야간 발한]
        - 통증: [부위, 성질, 강도, 빈도]
        - 정신/정서: [스트레스, 기억력, 의욕]
        
        【신체검진 소견】
        - 활력징후: BP XXX/XX mmHg, 맥박 XX회/분, 체온 XX.X°C, 호흡 XX회/분
        - 전신 상태: [피로감, 부종, 피부 상태]
        - 면색: [창백/홍조/황색/정상 등]
        
        【설진 소견】
        - 설질: [색깔, 크기]
        - 설태: [색깔, 두께]
        
        【맥진 소견】
        - 맥위(부침): [부/중/침]
        - 맥폭(대세): [세/대/홍]
        - 맥력: [유력/무력]
        - 맥상: [활/삽/긴/완 등]"
    }}
    
    ## 중요 지침
    1. 모든 출력은 한국어로 작성
    2. 의사 관점으로 작성 (환자 시점 ❌)
    3. 한의학 전문용어 적극 사용 (惡寒, 發熱, 無汗 등)
    4. ⚠️ 변증, 치법, 처방은 절대 생성하지 마세요!
    5. 객관적인 환자 소견만 기술하세요
    6. 각 【섹션】 사이에는 반드시 줄바꿈을 넣어 구분하세요
    """
