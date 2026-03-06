"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Patient Generation & LLM Integration
═══════════════════════════════════════════════════════════════════════════════
"""

import json
from data_mappings import get_desc
from constants import DISEASE_PATTERNS
from prompt_builder import build_generation_prompt


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
    
    system_prompt = build_generation_prompt(session, selected_pattern, 
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




