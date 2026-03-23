"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Patient Generation & LLM Integration
═══════════════════════════════════════════════════════════════════════════════
"""

import json
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
    
    if not client:
        st.error("API 키 오류. Streamlit Secrets에서 확인하세요.")
        return
    
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
    
    # Build the prompt (auto-dump: all session keys included automatically)
    system_prompt = build_generation_prompt(session)
    
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




