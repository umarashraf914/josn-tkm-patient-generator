"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Patient Generation & LLM Integration
═══════════════════════════════════════════════════════════════════════════════
"""

import json
from data_mappings import get_desc
from constants import DISEASE_PATTERNS


def generate_patient(st, client):
    """
    Generate a virtual patient scenario using LLM.
    
    Args:
        st: Streamlit module
        client: Google GenAI Client instance
    
    All 4 diseases are now supported:
    - 감기 (Common Cold)
    - 알레르기비염 (Allergic Rhinitis)
    - 기능성소화불량 (Functional Dyspepsia)
    - 요통 (Low Back Pain)
    """
    session = st.session_state
    
    # ═══════════════════════════════════════════════════════════════════
    # All 4 diseases are now supported with CSV generation rules
    # ═══════════════════════════════════════════════════════════════════
    
    # ═══════════════════════════════════════════════════════════════════
    # NOTE: Constraints are applied during randomization, not here
    # Streamlit prevents modifying widget-bound session state after render
    # ═══════════════════════════════════════════════════════════════════
    
    if not client:
        st.error("API 키 오류. Streamlit Secrets에서 확인하세요.")
        return
    
    session = st.session_state
    
    # --- GET RICH KOREAN DESCRIPTIONS FOR LLM ---
    fever_desc = get_desc("fever_sev", session.fever_sev) or f"레벨 {session.fever_sev}"
    chills_desc = get_desc("chills_sev", session.chills_sev) or f"레벨 {session.chills_sev}"
    snot_desc = get_desc("snot_sev", session.snot_sev) or f"레벨 {session.snot_sev}"
    cough_desc = get_desc("cough_sev", session.cough_sev) or f"레벨 {session.cough_sev}"
    
    # Rhinitis descriptions
    sneeze_desc = get_desc("rhinitis_sneeze", session.sneeze_sev) or f"레벨 {session.sneeze_sev}"
    nose_block_desc = get_desc("rhinitis_block", session.nose_block_sev) or f"레벨 {session.nose_block_sev}"
    nose_itch_desc = get_desc("rhinitis_itch", session.nose_itch_sev) or f"레벨 {session.nose_itch_sev}"
    rhinitis_snot_desc = get_desc("rhinitis_snot_sev", session.snot_sev) or f"레벨 {session.snot_sev}"
    
    # Other descriptors from data_mappings
    fatigue_desc = get_desc("fatigue", session.get("fatigue_sev", 2)) or "보통"
    sweat_desc = get_desc("sweat_amt", 3) or "적당히 흘림"
    sleep_desc = get_desc("sleep_quality", 3) or "보통"
    
    # Get selected pattern name based on current disease and pattern index
    # Use Korean keywords to match UI dropdown options
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
    
    # Build the prompt
    # Calculate BMI for prompt
    bmi_str = "N/A"
    if session.get("height", 0) > 0:
        bmi = session.weight / ((session.height / 100) ** 2)
        bmi_str = f"{bmi:.1f}"
    
    system_prompt = _build_generation_prompt(session, selected_pattern, 
                                              fever_desc, chills_desc, snot_desc, cough_desc,
                                              sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc,
                                              bmi_str)
    
    with st.spinner('가상환자 시나리오 생성 중...'):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=system_prompt,
                config={'response_mime_type': 'application/json'}
            )
            data = json.loads(response.text)
            st.success("✅ 환자 시나리오 생성 완료")
            
            # Store generated data in session state for PDF export
            session.generated_summary = data.get('요약', '요약 없음')
            session.generated_scenario = data.get('환자시나리오', data.get('초진기록', '기록 없음'))
            session.generated_patient_info = {
                'disease': session.disease,
                'pattern': selected_pattern,
                'age': session.age,
                'sex': session.sex,
                'height': session.height,
                'weight': session.weight,
                'sbp': session.sbp,
                'dbp': session.dbp,
                'pulse_rate': session.pulse_rate,
                'temp': session.temp,
            }
            session.scenario_generated = True
            
            # Display summary
            st.subheader(session.generated_summary)
            
            # Display patient scenario (no tabs needed - single output)
            st.markdown("---")
            st.markdown("### 📋 가상환자 시나리오")
            st.markdown(session.generated_scenario)
                
        except Exception as e:
            st.error(f"오류 발생: {e}")
            session.scenario_generated = False


def _get_menstrual_info(session):
    """폐경 여부에 따라 여성력 정보 반환"""
    if session.sex != "여":
        return "해당없음 (남성)"
    
    if session.get('mens_regular', '') == "폐경":
        return "폐경"
    else:
        return f"생리주기 {session.get('mens_cycle', 'N/A')}일, 규칙성 {session.get('mens_regular', 'N/A')}, 기간 {session.get('mens_duration', 'N/A')}일, 생리통 {session.get('mens_pain_score', 0)}/10, 생리혈색 {session.get('mens_color', 'N/A')}"


def _build_generation_prompt(session, selected_pattern,
                             fever_desc, chills_desc, snot_desc, cough_desc,
                             sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc,
                             bmi_str="N/A"):
    """Build the LLM prompt for patient generation.
    
    NOTE: This generates PATIENT PRESENTATION DATA ONLY.
    변증 (diagnosis), 치법 (treatment), 처방 (prescription) are NOT generated.
    The doctor will determine these based on the patient scenario.
    """
    
    return f"""
    당신은 한의 임상 가상환자 시나리오 생성 전문가입니다.
    
    ## 역할
    한의사의 관점에서 환자 정보를 진료기록부 형식으로 정리하세요.
    ❌ 환자 시점 (예: "저는 열이 나고...")이 아닌
    ✅ 의사 시점 (예: "상기 환자는 발열을 호소하며...")으로 작성하세요.
    
    ⚠️ 중요: 변증(辨證), 치법(治法), 처방(處方)은 절대 생성하지 마세요!
    이 시나리오는 의사 교육용입니다. 의사가 직접 진단을 내립니다.
    
    ⚠️ 중요: 모든 출력은 100% 한국어로만 작성하세요!
    영어 번역이나 영어 단어를 절대 포함하지 마세요.
    
    ❌ 금지 예시 (영어 포함):
    - "70세 Female 환자" → ✅ "70세 여 환자"
    - "사무직(Office)" → ✅ "사무직"
    - "요통(Back Pain)" → ✅ "요통"
    - "암색(Dark)" → ✅ "암색"
    - "오한 경향(Cold Sens)" → ✅ "오한 경향"
    - "야간도한(Night Sweat)" → ✅ "야간도한"
    - "의욕(Motivation)" → ✅ "의욕"
    - "고혈압(HTN)" → ✅ "고혈압"
    - "당뇨(DM)" → ✅ "당뇨"
    - "냉수(Icy)" → ✅ "냉수"
    
    모든 괄호 안의 영어 번역을 삭제하세요!
    
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
    - 여성력: {_get_menstrual_info(session)}
    
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
    - 사지무력감: {session.limb_weakness}, 눈앞캄캄함: {session.get('vision_blackout', False)}
    - 피부건조도: {session.skin_dry}, 가려움: {session.skin_itch}
    - 이명강도: {session.tinnitus_sev}/5, 난청: {session.hearing_sev}/5
    - 어지러움: {session.dizziness_sev}/5
    - 면색: {session.face_color}
    
    ### 6. 맥진 및 설진 소견
    【맥진소견】
    - 맥상: {session.get('compound_pulse', '완맥')}
    【설진소견】
    - 설질: {session.tongue_color}, {session.tongue_size}
    - 설태: {session.tongue_coat_color}, {session.tongue_coat_thick}
    
    ### 7. 주소증
    - 질환명: {session.disease}
    
    **감기 증상 (해당시):**
    - 발열: {fever_desc} ({session.fever_sev}/5)
    - 오한: {chills_desc} ({session.chills_sev}/5)
    - 콧물: {snot_desc} ({session.snot_sev}/5), 색: {session.get('snot_color', 'N/A')}
    - 기침: {cough_desc} ({session.cough_sev}/5)
    - 가래: 양 {session.get('phlegm_amt', 0)}/5, 색 {session.get('phlegm_color', '없음')}
    - 기타 증상: {session.cold_symptoms_spec}
    - 감기주소증 유형: {session.get('cold_chief_type', [])}
    - 발병일: {session.get('cold_onset_specific', 'N/A')}
    - 인후통: {session.get('sore_throat', False)}
    - 몸살(신체통): {session.get('body_ache_cold', False)}
    - 몸무거움(신중): {session.get('body_heaviness_cold', False)}
    - 두통: {session.get('headache_cold', False)}
    - 경항통: {session.get('neck_pain_cold', False)}
    - 호흡곤란: {session.get('cold_dyspnea', False)}
    - 땀유무: {session.get('cold_sweating_check', False)}
    - 후각감퇴: {session.get('smell_reduction', 0)}/5
    - 한열왕래: {session.get('alternating_chills_fever', 0)}/5
    
    **감기 진찰소견 (해당시):**
    - 청진기 호흡음: {session.get('exam_stethoscope', '정상')}
    - 인후부 망진/촉진: {session.get('exam_throat_visual', '정상')}
    - 설압자 편도소견: {session.get('exam_tongue_depressor', '정상')}
    - 비경 소견: {session.get('exam_rhinoscope_finding', '정상')}
    
    **비염 증상 (해당시):**
    - 재채기: {sneeze_desc} ({session.sneeze_sev}/5)
    - 코막힘: {nose_block_desc} ({session.nose_block_sev}/5)
    - 코가려움: {nose_itch_desc} ({session.nose_itch_sev}/5)
    - 콧물양: {rhinitis_snot_desc} ({session.snot_sev}/5)
    - 콧물성상: {session.get('snot_type', 'N/A')}
    
    **요통 증상 (해당시):**
    - 통증강도: {session.pain_sev}/10
    - 통증양상: {session.get('pain_nature', [])}
    
    **소화불량 증상 (해당시):**
    - 복만/복통: {session.pain_sev}/5
    - 증상: {session.get('dyspepsia_spec', [])}
    
    ### 8. 추가 증상 및 동반질환
    - 추가 증상: {session.get('additional_symptoms', [])}
    - 추가 동반질환: {session.get('additional_comorbidities', [])}
    
    ## 출력 형식 (JSON)
    반드시 아래 형식으로 JSON을 생성하세요:
    
    {{
      "요약": "환자 요약 (예: 45세 남성, 3일전부터 오한, 발열, 두통 호소)",
      
      "환자시나리오": "한의사 관점의 상세 환자 기록. 반드시 다음 형식으로 작성:
        
        【환자정보】
        상기 환자는 XX세 XX 환자로 [직업] 종사자이다.
        
        【주소증】
        [발현시점]부터 [주요증상]을 주소로 내원하였다.
        
        【발병 에피소드】
        [발병 전 상황을 구체적으로 기술. 예: '3일 전 영하 10도의 날씨에 버스 정류장에서 40분간 대기한 후 다음날부터 오한과 발열이 시작되었다.' 또는 '과로와 수면 부족이 지속된 후 증상이 발생하였다.' 등 발병 계기를 서술]
        
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
        - 수면: [수면시간, 질, 입면/각성 장애]
        - 한열: [오한/발열 경향, 수족냉증, 온도 선호]
        - 땀: [발한 정도, 부위, 야간 발한]
        - 통증: [부위, 성질, 강도, 빈도]
        - 정신/정서: [스트레스, 불안, 우울, 기억력]
        
        【신체검진 소견】
        - 활력징후: BP, 맥박, 체온, 호흡
        - 전신 상태: 피로감, 체력, 부종, 피부 상태
        - 면색: 창백/홍조/황색/정상 등
        
        【설진 소견】
        - 설질: 색깔, 크기, 형태
        - 설태: 색깔, 두께, 분포
        
        【맥진 소견】
        - 맥위(부침): 부/중/침
        - 맥폭(대세): 세/대/홍  
        - 맥력: 유력/무력
        - 맥상: 활/삽/긴/완 등"
    }}
    
    ## 중요 지침
    1. 모든 출력은 한국어로 작성
    2. 의사 관점으로 작성 (환자 시점 ❌)
    3. 한의학 전문용어 적극 사용 (惡寒, 發熱, 無汗 등)
    4. ⚠️ 변증, 치법, 처방은 절대 생성하지 마세요!
    5. 객관적인 환자 소견만 기술하세요
    """
