"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Disease-Specific Prompt Sections
Prompt templates for each disease type

NOTE: All disease checks use Korean keywords to match UI dropdown options
═══════════════════════════════════════════════════════════════════════════════
"""


def get_cold_symptoms_section(session, fever_desc, chills_desc, snot_desc, cough_desc):
    """
    Get cold (감기) symptoms section for prompt.
    
    Args:
        session: Streamlit session_state object
        fever_desc: Fever description text
        chills_desc: Chills description text
        snot_desc: Snot/runny nose description text
        cough_desc: Cough description text
    
    Returns:
        Formatted cold symptoms section string, or empty string if not cold
    """
    # Use Korean keyword for disease check
    if "감기" not in session.disease:
        return ""
    
    return f"""
    **감기 증상 (Cold Symptoms):**
    - 발열: {fever_desc} ({session.fever_sev}/5)
    - 오한: {chills_desc} ({session.chills_sev}/5)
    - 콧물: {snot_desc} ({session.snot_sev}/5)
    - 기침: {cough_desc} ({session.cough_sev}/5)
    - 가래양: {getattr(session, 'phlegm_amt', 0)}/5
    - 가래색: {getattr(session, 'phlegm_color', 'N/A')}
    - 기타: {session.cold_symptoms_spec}
    """


def get_rhinitis_symptoms_section(session, sneeze_desc, nose_block_desc, nose_itch_desc, rhinitis_snot_desc):
    """
    Get rhinitis (비염) symptoms section for prompt.
    
    Args:
        session: Streamlit session_state object
        sneeze_desc: Sneezing description text
        nose_block_desc: Nasal blockage description text
        nose_itch_desc: Nose itching description text
        rhinitis_snot_desc: Snot description text
    
    Returns:
        Formatted rhinitis symptoms section string, or empty string if not rhinitis
    """
    # Use Korean keyword for disease check
    if "비염" not in session.disease:
        return ""
    
    return f"""
    **비염 증상 (Rhinitis Symptoms):**
    - 재채기: {sneeze_desc} ({session.sneeze_sev}/5)
    - 코막힘: {nose_block_desc} ({session.nose_block_sev}/5)
    - 코가려움: {nose_itch_desc} ({session.nose_itch_sev}/5)
    - 콧물양: {rhinitis_snot_desc} ({session.snot_sev}/5)
    - 콧물성상: {getattr(session, 'snot_type', 'N/A')}
    """


def get_back_pain_symptoms_section(session):
    """
    Get back pain (요통) symptoms section for prompt.
    
    Args:
        session: Streamlit session_state object
    
    Returns:
        Formatted back pain symptoms section string, or empty string if not back pain
    """
    # Use Korean keyword for disease check
    if "요통" not in session.disease:
        return ""
    
    return f"""
    **요통 증상 (Back Pain Symptoms):**
    - 통증강도: {session.pain_sev}/10 (NRS)
    - 통증양상: {getattr(session, 'pain_nature', [])}
    - 발병요인: {getattr(session, 'back_pain_cause', 'N/A')}
    - 통증시간대: {getattr(session, 'back_pain_timing', 'N/A')}
    - 하지방사: {getattr(session, 'back_radiation', False)}
    """


def get_dyspepsia_symptoms_section(session):
    """
    Get dyspepsia (소화불량) symptoms section for prompt.
    
    Args:
        session: Streamlit session_state object
    
    Returns:
        Formatted dyspepsia symptoms section string, or empty string if not dyspepsia
    """
    # Use Korean keyword for disease check
    if "소화불량" not in session.disease:
        return ""
    
    return f"""
    **소화불량 증상 (Dyspepsia Symptoms):**
    - 복만/복통: {session.pain_sev}/5
    - 식욕: {session.appetite}
    - 소화: {session.digestion}
    - 트림: {getattr(session, 'belching', 0)}/5
    - 속쓰림: {getattr(session, 'acid_reflux', False)}
    - 구역감: {getattr(session, 'nausea', 0)}/5
    - 증상: {getattr(session, 'dyspepsia_spec', [])}
    """


def get_all_disease_symptoms(session, symptom_descriptions):
    """
    Get all disease symptoms sections combined.
    
    Args:
        session: Streamlit session_state object
        symptom_descriptions: Dictionary of symptom descriptions
    
    Returns:
        Combined disease symptoms string
    """
    sections = []
    
    # Use Korean keywords for disease checks
    if "감기" in session.disease:
        sections.append(get_cold_symptoms_section(
            session,
            symptom_descriptions.get('fever', ''),
            symptom_descriptions.get('chills', ''),
            symptom_descriptions.get('snot', ''),
            symptom_descriptions.get('cough', '')
        ))
    
    if "비염" in session.disease:
        sections.append(get_rhinitis_symptoms_section(
            session,
            symptom_descriptions.get('sneeze', ''),
            symptom_descriptions.get('nose_block', ''),
            symptom_descriptions.get('nose_itch', ''),
            symptom_descriptions.get('rhinitis_snot', '')
        ))
    
    if "요통" in session.disease:
        sections.append(get_back_pain_symptoms_section(session))
    
    if "소화불량" in session.disease:
        sections.append(get_dyspepsia_symptoms_section(session))
    
    return "\n".join(filter(None, sections))
