"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - System Prompt Template
Main LLM prompt for patient scenario generation
═══════════════════════════════════════════════════════════════════════════════
"""

from .disease_prompts import (
    get_cold_symptoms_section,
    get_rhinitis_symptoms_section,
    get_back_pain_symptoms_section,
    get_dyspepsia_symptoms_section
)


def build_system_prompt(session, symptom_descriptions, selected_pattern=None):
    """
    Build the complete system prompt for LLM patient generation.
    
    This generates PATIENT PRESENTATION DATA ONLY.
    The doctor will determine the diagnosis (변증), treatment (치법), and prescription (처방).
    
    Args:
        session: Streamlit session_state object
        symptom_descriptions: Dictionary of symptom descriptions
        selected_pattern: (DEPRECATED - not used, kept for backward compatibility)
    
    Returns:
        Complete system prompt string
    """
    # Unpack symptom descriptions
    fever_desc = symptom_descriptions.get('fever', '')
    chills_desc = symptom_descriptions.get('chills', '')
    snot_desc = symptom_descriptions.get('snot', '')
    cough_desc = symptom_descriptions.get('cough', '')
    sneeze_desc = symptom_descriptions.get('sneeze', '')
    nose_block_desc = symptom_descriptions.get('nose_block', '')
    nose_itch_desc = symptom_descriptions.get('nose_itch', '')
    rhinitis_snot_desc = symptom_descriptions.get('rhinitis_snot', '')
    
    # Build disease-specific symptoms section
    disease_symptoms = _get_disease_symptoms_section(
        session, fever_desc, chills_desc, snot_desc, cough_desc,
        sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc
    )
    
    prompt = f"""
    당신은 한의 임상 가상환자 시나리오 생성 전문가입니다.
    
    ## 역할
    한의사의 관점에서 진료기록부 형식으로 가상환자 시나리오를 생성하세요.
    ❌ 환자 시점 (예: "저는 열이 나고...")이 아닌
    ✅ 의사 시점 (예: "상기 환자는 발열을 호소하며...")으로 작성하세요.
    
    ## 환자 정보 (Patient Data)
    
    ### 1. 인구학적정보 및 활력징후
    - 나이/성별: {session.age}세 {session.sex}
    - 직업: {session.job}
    - 발현시점: {session.onset}
    - 경과: {session.course}
    - 활력징후: BP {session.sbp}/{session.dbp} mmHg, 맥박 {session.pulse_rate}회/분, 체온 {session.temp}°C
    
    ### 2. 병력 및 생활습관 (Page 18)
    - 현병력: {session.history_conditions}
    - 약물력: {session.meds_specific}
    - 가족력: {session.family_hx}
    - 악화요인: {getattr(session, 'aggravating_factors', [])}
    - 완화요인: {getattr(session, 'relieving_factors', [])}
    - 음주: {session.social_alcohol_freq}
    - 흡연: {session.social_smoke_daily}개피/일
    - 운동강도: {session.social_exercise_int}
    
    ### 3. 배설 및 식사
    - 식사횟수: {session.diet_freq}회/일, {session.diet_regular}
    - 음수량: {session.water_intake}
    - 대변: {session.stool_freq}, {session.stool_color}, {session.stool_form}
    - 소변: {session.urine_color}, 주간 {session.urine_freq_day}회, 야간 {session.urine_freq_night}회
    
    ### 4. 수면, 땀, 한열
    - 수면: {session.sleep_hours}시간, {session.sleep_depth}, 기상시 {session.sleep_waking_state}
    - 입면장애: {session.insomnia_onset}/5, 중도각성: {session.insomnia_maintain}/5
    - 땀: {session.sweat_amt}, {session.sweat_area}
    - 한열경향: {session.cold_heat_pref}
    - 음료온도선호: {session.drink_temp}
    
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
    - 맥상: {session.get('compound_pulse', '완맥')}
    - 설질: {session.tongue_color}, {session.tongue_size}
    - 설태: {session.tongue_coat_color}, {session.tongue_coat_thick}
    
    ### 7. 주소증
    - 질환명: {session.disease}
    
    {disease_symptoms}
    
    ### 8. 추가 증상 및 동반질환 (Pages 24-25)
    - 추가 증상 (한의원 다빈도): {getattr(session, 'additional_symptoms', [])}
    - 추가 동반질환: {getattr(session, 'additional_comorbidities', [])}
    
    {get_output_format_instructions()}
    
    ## 중요 지침
    1. 모든 출력은 한국어로 작성
    2. 의사 관점으로 작성 (환자 시점 ❌)
    3. 한의학 전문용어 적극 사용 (예: 惡寒, 發熱, 無汗 등)
    4. ⚠️ 변증(辨證), 치법(治法), 처방(處方)은 절대 생성하지 마세요!
       - 이 앱은 환자 시나리오만 생성합니다
       - 진단과 처방은 의사가 직접 결정합니다
    5. 객관적인 환자 소견만 기술하세요
    """
    
    return prompt


def _get_disease_symptoms_section(session, fever_desc, chills_desc, snot_desc, cough_desc,
                                   sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc):
    """Build disease-specific symptoms section of prompt."""
    
    sections = []
    
    # Cold symptoms
    cold_section = get_cold_symptoms_section(
        session, fever_desc, chills_desc, snot_desc, cough_desc
    )
    if cold_section:
        sections.append(cold_section)
    
    # Rhinitis symptoms
    rhinitis_section = get_rhinitis_symptoms_section(
        session, sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc
    )
    if rhinitis_section:
        sections.append(rhinitis_section)
    
    # Back pain symptoms
    back_pain_section = get_back_pain_symptoms_section(session)
    if back_pain_section:
        sections.append(back_pain_section)
    
    # Dyspepsia symptoms
    dyspepsia_section = get_dyspepsia_symptoms_section(session)
    if dyspepsia_section:
        sections.append(dyspepsia_section)
    
    return "\n".join(sections)


def get_output_format_instructions():
    """
    Get the JSON output format instructions.
    
    NOTE: This generates PATIENT PRESENTATION DATA ONLY.
    The doctor will determine 변증 (pattern diagnosis), 치법, and 처방.
    """
    return '''
    ## 출력 형식 (JSON)
    반드시 아래 형식으로 JSON을 생성하세요:
    
    ⚠️ 중요: 변증, 치법, 처방은 생성하지 마세요! 
    의사가 이 환자 데이터를 보고 직접 진단을 내립니다.
    환자의 증상과 소견만 객관적으로 기술하세요.
    
    {
      "요약": "환자 요약 (예: 45세 남성, 3일 전부터 오한, 발열, 두통 호소)",
      
      "환자시나리오": "한의사 관점의 상세 환자 기록. 반드시 다음 형식으로 작성:
        
        【환자정보】
        상기 환자는 XX세 XX 환자로 [직업] 종사자이다.
        
        【주소증】
        [발현시점]부터 [주요증상]을 주소로 내원하였다.
        
        【현병력】
        [증상의 발생, 경과, 양상을 상세히 기술. 악화/완화 요인 포함]
        
        【과거력】
        [기존 질환, 수술력, 약물력 등]
        
        【가족력】
        [가족 질환력]
        
        【사회력】
        [직업, 음주, 흡연, 운동 습관]
        
        【계통적 문진 (Review of Systems)】
        - 식욕/소화: [식욕 상태, 소화 양호/불량, 오심/구토 유무]
        - 대변: [횟수, 성상, 색깔]
        - 소변: [횟수, 색깔, 야간뇨]
        - 수면: [수면시간, 질, 입면/각성 장애]
        - 한열: [오한/발열 경향, 수족냉증, 온도 선호]
        - 땀: [발한 정도, 부위, 야간 발한]
        - 통증: [부위, 성질, 강도, 빈도]
        - 정신/정서: [스트레스, 불안, 우울, 기억력]
        
        【신체검진 소견】
        - 활력징후: BP, 맥박, 체온, 호흡
        - 전신 상태: [피로감, 체력, 부종, 피부 상태]
        - 면색: [창백/홍조/황색/정상]
        
        【설진 소견】
        - 설질: [색깔, 크기, 형태]
        - 설태: [색깔, 두께, 분포]
        
        【맥진 소견】
        - 맥위(부침): [부맥/중맥/침맥]
        - 맥폭(대세): [세맥/대맥/홍맥]  
        - 맥력: [유력/무력]
        - 맥상: [활/삽/긴/완 등]
        "
    }
    '''
