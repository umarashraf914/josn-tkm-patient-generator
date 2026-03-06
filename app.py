"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Main Streamlit Application
한의 임상 가상환자 시나리오 생성기

Updated UI with sidebar controls and main content area with collapsible sections.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
from google import genai
from config import API_KEY, init_session_state
from constants import (
    KCD_CODES, DISEASE_PATTERNS, FREQUENT_TKM_SYMPTOMS, FREQUENT_COMORBIDITIES,
    PAST_COLD_PROBLEM_AREAS, AGGRAVATING_FACTORS, RELIEVING_FACTORS,
    COLD_CHIEF_TYPES, COLD_EXAM_OPTIONS,
    get_pattern_info, get_kcd_info, get_all_symptom_options
)
from constraint_rules import apply_constraint_rules, apply_symptom_correlation_rules
# NOTE: symptom_correlations module is still used in background logic (constraint_rules.py)
from randomizer import randomize_inputs
from patient_generator import generate_patient
from pdf_generator import generate_patient_pdf_korean

# --- API KEY CONFIGURATION ---
if API_KEY == "PASTE_YOUR_API_KEY_HERE" or not API_KEY:
    st.error("⚠️ Please open config.py and paste your API Key!")
else:
    client = genai.Client(api_key=API_KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="한의 임상시나리오 생성기", layout="wide")

# --- INITIALIZE SESSION STATE ---
init_session_state(st)

# --- TRACK PREVIOUS DISEASE/PATTERN FOR AUTO-RANDOMIZATION ---
# Initialize tracking variables if not exists
if '_prev_disease' not in st.session_state:
    st.session_state._prev_disease = st.session_state.get('disease', '')
if '_prev_pattern_idx' not in st.session_state:
    st.session_state._prev_pattern_idx = st.session_state.get('pattern_idx', 0)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ 조작")
    
    # Randomize Button
    if st.button("🎲 랜덤 생성", use_container_width=True, type="primary"):
        randomize_inputs(st)
        st.rerun()
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DIAGNOSIS SECTION IN SIDEBAR
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📋 진단명")
    
    # Disease Selection
    st.markdown("**질환명**")
    disease_opts = [
        "감기/급성상기도감염", 
        "알레르기비염", 
        "요통", 
        "기능성소화불량"
    ]
    st.selectbox("질환", disease_opts, key="disease", label_visibility="collapsed")
    
    # Pattern Selection based on disease
    disease_key = None
    if "감기" in st.session_state.disease:
        disease_key = "감기"
    elif "비염" in st.session_state.disease:
        disease_key = "알레르기비염"
    elif "요통" in st.session_state.disease:
        disease_key = "요통"
    elif "소화불량" in st.session_state.disease:
        disease_key = "기능성소화불량"

    if disease_key and disease_key in DISEASE_PATTERNS:
        patterns = DISEASE_PATTERNS[disease_key]["patterns"]
        # For 알레르기비염, prescription name IS the pattern name, so don't repeat
        if disease_key == "알레르기비염":
            pattern_display = [p['name'] for p in patterns]
        else:
            pattern_display = [f"{p['name']} → {', '.join(p['prescriptions'])}" for p in patterns]
        
        if st.session_state.pattern_idx >= len(pattern_display):
            st.session_state.pattern_idx = 0
        
        st.markdown("**변증/처방**")
        selected_pattern = st.selectbox(
            "변증", 
            pattern_display, 
            index=st.session_state.pattern_idx,
            label_visibility="collapsed"
        )
        st.session_state.pattern_idx = pattern_display.index(selected_pattern)
        
        # Display KCD code info
        kcd_info = get_kcd_info(disease_key)
        if kcd_info:
            st.caption(f"📋 KCD: {kcd_info['main_code']}")
            with st.expander("KCD 상세정보"):
                st.markdown(f"**주코드:** {kcd_info['main_code']}")
                st.markdown("**포함:**")
                for code, desc in kcd_info['sub_codes'].items():
                    st.markdown(f"- {code}: {desc}")
                st.markdown("**제외:**")
                for excl in kcd_info['exclusions']:
                    st.markdown(f"- ❌ {excl}")


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-RANDOMIZE ON DISEASE/PATTERN CHANGE
# ═══════════════════════════════════════════════════════════════════════════════
# Check if disease or pattern changed and auto-randomize
disease_changed = st.session_state.disease != st.session_state._prev_disease
pattern_changed = st.session_state.pattern_idx != st.session_state._prev_pattern_idx

if disease_changed or pattern_changed:
    # Update tracking variables
    st.session_state._prev_disease = st.session_state.disease
    st.session_state._prev_pattern_idx = st.session_state.pattern_idx
    
    # Auto-randomize with the new disease/pattern (but keep disease and pattern fixed)
    randomize_inputs(st, randomize_disease=False)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════════════════════

st.title("📋 한의 임상시나리오 생성기")
st.caption("한의 임상정보 항목 기반 가상환자 생성 시스템")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Demographics & Vitals
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 인구학적정보 및 활력징후", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**인구학적정보**")
        st.number_input("나이 (세)", 10, 100, key="age")  # Min 10 to match CSV rules
        st.selectbox("성별", ["남", "여"], key="sex")
        st.selectbox("직업", ["학생", "사무직", "현장직", "가사"], key="job")
    with c2:
        st.markdown("**신체정보**")
        st.number_input("키 (cm)", 130, 220, key="height")  # Min 130cm for age 10+
        st.number_input("몸무게 (kg)", 30, 150, key="weight")  # Min 30kg for age 10+
        # Calculate and display BMI
        if st.session_state.height > 0:
            bmi = st.session_state.weight / ((st.session_state.height / 100) ** 2)
            st.caption(f"BMI: {bmi:.1f}")
    with c3:
        st.markdown("**활력징후 1**")
        st.number_input("수축기혈압 (mmHg)", 90, 180, key="sbp")
        st.number_input("이완기혈압 (mmHg)", 50, 120, key="dbp")
        st.number_input("맥박 (회/분)", 50, 130, key="pulse_rate")
    with c4:
        st.markdown("**활력징후 2**")
        st.number_input("체온 (°C)", 35.0, 40.5, step=0.1, key="temp")
        st.number_input("호흡 (회/분)", 8, 30, key="resp")
    
    # Onset and Course in a separate row
    o1, o2 = st.columns(2)
    with o1:
        st.selectbox("발현시점", ["1일 전", "2-3일 전", "1주 전", "만성 3개월 이상"], key="onset")
    with o2:
        st.selectbox("경과", ["악화중", "호전중", "비슷/오르내림"], key="course")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Medical History & Lifestyle
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 병력 및 생활습관", expanded=False):
    h1, h2 = st.columns(2)
    with h1:
        st.multiselect("현병력", ["고혈압", "당뇨", "이상지질혈증", "기타"], key="history_conditions")
        st.multiselect("약물력", ["혈압약", "당뇨약", "이상지질혈증약", "수면제", "항우울제", "항불안제"], key="meds_specific")
        st.multiselect("가족력", ["고혈압", "당뇨", "이상지질혈증", "심장병", "중풍", "기타"], key="family_hx")
    with h2:
        st.selectbox("음주", ["비음주", "주간", "매일"], key="social_alcohol_freq")
        st.number_input("흡연 (개피/일)", 0.0, 50.0, key="social_smoke_daily")
        st.selectbox("운동강도", ["저", "중", "고"], key="social_exercise_int")

    if st.session_state.sex == "여":
        st.markdown("**여성력**")
        if st.session_state.mens_duration < 1:
            st.session_state.mens_duration = 5
        if st.session_state.mens_cycle < 1:
            st.session_state.mens_cycle = 28
        w1, w2, w3, w4 = st.columns(4)
        with w1: st.selectbox("생리규칙성", ["규칙", "불규칙", "폐경"], key="mens_regular")
        
        # 폐경인 경우 생리 관련 정보 숨김
        if st.session_state.mens_regular != "폐경":
            with w2: st.number_input("생리기간 (일)", 1, 10, key="mens_duration")
            with w3: st.slider("생리통 (0-10)", 0, 10, key="mens_pain_score")
            with w4: st.selectbox("생리혈 색", ["연함", "적색", "흑자색"], key="mens_color")
        else:
            # 폐경 시 N/A로 표시
            with w2: st.text("생리기간: N/A")
            with w3: st.text("생리통: N/A")
            with w4: st.text("생리혈 색: N/A")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Excretion & Diet
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 배설 및 식사", expanded=False):
    d1, d2, d3 = st.columns(3)
    with d1:
        st.number_input("주간뇨 횟수", 1, 15, key="urine_freq_day")
        st.selectbox("소변 색", ["맑음", "황색", "적색/혈뇨"], key="urine_color")
    with d2:
        st.selectbox("대변 횟수", ["1회/일", "2-3회/일", "변비"], key="stool_freq")
        st.selectbox("대변 색", ["황색", "황갈색", "흑색", "녹색"], key="stool_color")
        st.selectbox("대변 형태", ["보통", "묽음/연변", "굳음/경변"], key="stool_form")
    with d3:
        st.selectbox("식사횟수/일", [1, 2, 3, 4], key="diet_freq")
        st.selectbox("식사규칙성", ["규칙적", "불규칙"], key="diet_regular")
        st.selectbox("음수량", ["0.5L 미만", "0.5-1L", "1-2L", "2L 이상"], key="water_intake")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Sleep, Sweat, Cold/Heat
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 수면, 땀, 한열경향", expanded=False):
    s1, s2, s3 = st.columns(3)
    with s1:
        st.selectbox("기상시 상쾌도", ["개운함", "피곤함", "무거움"], key="sleep_waking_state")
        st.selectbox("수면 깊이", ["깊음", "얕음"], key="sleep_depth")
        st.slider("입면장애 정도", 0, 5, key="insomnia_onset", help="0=없음, 5=심함")
        st.slider("중도각성 정도", 0, 5, key="insomnia_maintain", help="0=없음, 5=심함")
    with s2:
        st.selectbox("땀나는 부위", ["전신", "두부", "야간/도한"], key="sweat_area")
        st.selectbox("땀 후 느낌", ["상쾌", "피곤/냉함", "열감"], key="sweat_feeling")
    with s3:
        st.selectbox("한열경향", ["오한/추위탐", "보통", "열감/더위탐"], key="cold_heat_pref")
        st.selectbox("음료온도 선호", ["냉수", "온수", "열수"], key="drink_temp")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Mental State & Physical Inspection
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 정신상태 및 신체검진", expanded=False):
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("**정신상태**")
        st.selectbox("기억력", ["좋음", "건망", "나쁨"], key="memory")
        st.selectbox("의욕", ["높음", "보통", "낮음", "무기력"], key="motivation")
        st.selectbox("스트레스 대처력", ["좋음", "보통", "나쁨"], key="stress_coping")
    with m2:
        st.markdown("**신체검진**")
        st.selectbox("부종", ["없음", "안면", "하지", "전신"], key="edema")
        st.selectbox("멍듦", ["정상", "잘듦", "절로 생김"], key="bruising")
        c_a, c_b = st.columns(2)
        with c_a: st.checkbox("사지무력감", key="limb_weakness")
        with c_b: st.checkbox("눈앞캄캄함", key="vision_blackout")
        st.markdown("---")
        st.selectbox("피부 건조도", ["정상", "건조", "각질"], key="skin_dry")
        st.checkbox("피부 가려움", key="skin_itch")
        st.slider("이명 강도", 0, 5, key="tinnitus_sev", help="0=없음, 1-2=경미, 3-4=중등도, 5=심함")
        st.slider("난청/이롱 강도", 0, 5, key="hearing_sev", help="0=없음, 1-2=경미, 3-4=중등도, 5=심함")
        st.slider("어지러움/두훈 강도", 0, 5, key="dizziness_sev", help="0=없음, 1-2=경미, 3-4=중등도, 5=심함")
        st.selectbox("면색", ["정상", "창백", "홍조", "황색", "암색"], key="face_color")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Pulse & Tongue Diagnosis
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 맥진 및 설진", expanded=False):
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("**맥진**")
        # 복합맥만 표시 (맥위, 맥폭, 맥력, 맥상은 제거 - Prof. Lee feedback)
        st.text(f"맥상: {st.session_state.get('compound_pulse', '완맥')}")
        st.caption("(맥상은 질환/변증에 따라 자동 설정됩니다)")
    with p2:
        st.markdown("**설진**")
        st.selectbox("설질 색", ["담백", "담홍", "홍설", "강홍/자설"], key="tongue_color")
        st.selectbox("설태 색", ["백태", "황태", "회태"], key="tongue_coat_color")
        st.selectbox("설태 두께", ["박태", "후태", "니태"], key="tongue_coat_thick")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: ROS Pain Grid
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 통증 부위별 문진", expanded=False):
    st.caption("빈도 (0-5) / 강도 (0-10)")
    cols = st.columns(3)
    parts = [("경항부", "pain_neck"), ("요배부", "pain_back"), ("슬부", "pain_knee"), ("견부", "pain_shoulder"), ("주관절", "pain_elbow"), ("수부", "pain_hand")]
    for l, k in parts:
        with cols[0]: st.text(l)
        with cols[1]: st.number_input(f"{l} 빈도", 0, 5, key=f"{k}_f", label_visibility="collapsed")
        with cols[2]: st.number_input(f"{l} 강도", 0, 10, key=f"{k}_i", label_visibility="collapsed")
        st.session_state[k] = [st.session_state[f"{k}_f"], st.session_state[f"{k}_i"]]
    st.checkbox("수족냉증", key="cold_hands_feet")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Chief Complaint Specifics
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 8. 주소증 상세 (변증지표)")
st.caption("감기환자 변증지표")

# Disease-specific symptom inputs
if "감기" in st.session_state.disease:
    c1, c2 = st.columns(2)
    with c1:
        st.slider("발열 강도 (1-5)", 1, 5, key="fever_sev", help="1=미열/무열, 5=고열 壯熱")
        st.slider("오한 강도 (1-5)", 1, 5, key="chills_sev", help="1=경미, 5=惡寒重")
    with c2:
        st.slider("콧물 양 (1-5)", 1, 5, key="snot_sev", help="1=경미, 5=콧물 줄줄")
        st.slider("기침 강도 (1-5)", 1, 5, key="cough_sev", help="1=경미, 5=기침 심함")
    
    cold_opts = ["무한 (無汗) - 풍한", "황담 (黃痰) - 풍열", "희박담 (稀薄白痰) - 풍한", "인후건조 (咽乾) - 풍조", "골절동통 (骨節疼痛) - 풍한", "객담소 (咳嗽少痰) - 풍조"]
    st.multiselect("감기 증상", cold_opts, key="cold_symptoms_spec")
    
    with st.expander("📋 감기 가상환자 주증정보 필수항목", expanded=False):
        st.multiselect("감기주소증 유형 (최소 1개 이상)", COLD_CHIEF_TYPES, key="cold_chief_type")
        
        onset_opts = ["1일 전", "2일 전", "3일 전", "4일 전", "5일 전", "1주일 전", "2주일 전", "3주일 전"]
        st.selectbox("발병일", onset_opts, key="cold_onset_specific")
        
        cold_col1, cold_col2, cold_col3 = st.columns(3)
        with cold_col1:
            st.checkbox("인후통", key="sore_throat")
            st.checkbox("몸살", key="body_ache_cold")
            st.checkbox("신중/몸 무거움", key="body_heaviness_cold")
        with cold_col2:
            st.checkbox("두통", key="headache_cold")
            st.checkbox("경항통", key="neck_pain_cold")
            st.checkbox("숨이 가쁨", key="cold_dyspnea")
        with cold_col3:
            st.checkbox("땀 유무", key="cold_sweating_check")
            st.slider("후각감퇴 (0-5)", 0, 5, key="smell_reduction")
        
        st.slider("가래 양 (0-5)", 0, 5, key="phlegm_amt")
        try:
            phlegm_amt_val = int(st.session_state.get("phlegm_amt", 0))
        except (TypeError, ValueError):
            phlegm_amt_val = 0
        if phlegm_amt_val >= 2:
            st.selectbox("가래 색", ["맑음", "백색", "황색", "녹색"], key="phlegm_color")
        
        try:
            snot_sev_val = int(st.session_state.get("snot_sev", 1))
        except (TypeError, ValueError):
            snot_sev_val = 1
        if snot_sev_val >= 2:
            st.selectbox("콧물 색", ["없음", "맑음/투명", "백색", "황색", "녹색"], key="snot_color")
        
        st.slider("한열왕래 (0-5)", 0, 5, key="alternating_chills_fever")
        
        st.markdown("**진찰 및 검사소견**")
        exam_col1, exam_col2 = st.columns(2)
        with exam_col1:
            st.selectbox("청진기 호흡음", COLD_EXAM_OPTIONS["stethoscope"], key="exam_stethoscope")
            st.selectbox("인후부 망진/촉진", COLD_EXAM_OPTIONS["throat_visual"], key="exam_throat_visual")
        with exam_col2:
            st.selectbox("설압자 편도 소견", COLD_EXAM_OPTIONS["tongue_depressor"], key="exam_tongue_depressor")
            st.selectbox("비경 소견", COLD_EXAM_OPTIONS["rhinoscope"], key="exam_rhinoscope_finding")

elif "비염" in st.session_state.disease:
    st.caption("알레르기비염 변증지표 (수체형)")
    r1, r2 = st.columns(2)
    with r1:
        st.slider("재채기 (嚏噴 1-5)", 1, 5, key="sneeze_sev")
        st.slider("코막힘 (鼻塞 1-5)", 1, 5, key="nose_block_sev")
    with r2:
        st.slider("코가려움 (鼻癢 1-5)", 1, 5, key="nose_itch_sev")
        st.slider("콧물 양 (鼻涕 1-5)", 1, 5, key="snot_sev")
    st.selectbox("콧물 성상", ["청수양 (淸水樣) - 맑은 콧물", "백점액 (白粘) - 희고 끈적", "황농성 (黃膿) - 누렇고 찐득"], key="snot_type")

elif "소화불량" in st.session_state.disease:
    st.caption("기능성소화불량 변증지표 (한열허실 팔강변증)")
    st.slider("복만/복통 강도 (1-5)", 1, 5, key="pain_sev")
    dys_opts = ["신물 (吞酸) - 간위불화/식적", "트림 (噯氣) - 기체/식적", "구역/구토 (惡心嘔吐) - 습열", "구고 (口苦) - 열증/습열", "부패취 (噯氣腐臭) - 식적", "수족냉증 (四肢厥冷) - 한증/허증", "식후복만 (食後腹脹) - 비위허약", "사지권태 (四肢倦怠) - 기허"]
    st.multiselect("소화불량 증상", dys_opts, key="dyspepsia_spec")

elif "요통" in st.session_state.disease:
    st.caption("요통 변증지표 (한열허실 팔강변증)")
    st.slider("통증 강도 (NRS 1-10)", 1, 10, key="pain_sev", help="1=경미, 10=극심")
    pain_opts = ["유주통 (遊走痛) - 풍/담음", "자통 (刺痛) - 어혈", "한통 (寒痛) - 한", "득온즉감 (得溫則減) - 한", "야간통 (夜甚) - 어혈", "중통 (重痛) - 습", "구립즉심 (久立則甚) - 기", "신허요통 (腎虛腰痛) - 신허"]
    st.multiselect("통증 양상", pain_opts, key="pain_nature")

# ═══════════════════════════════════════════════════════════════════════════════
# Additional Symptoms & Correlations (Collapsed by default)
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("➤ 추가 증상 및 동반질환", expanded=False):
    st.caption("한의원 다빈도 증상 중 무작위 1-2개가 현실성을 위해 추가됩니다.")
    col_add1, col_add2 = st.columns(2)
    with col_add1:
        st.multiselect("추가 증상", get_all_symptom_options(), key="additional_symptoms")
    with col_add2:
        st.multiselect("추가 동반질환", FREQUENT_COMORBIDITIES, key="additional_comorbidities")

# NOTE: Symptom correlation logic is still applied in the background during randomization
# (see constraint_rules.py and symptom_correlations.py) but UI section removed for cleaner interface

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE BUTTON (at the end of main content)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
if st.button("✨ 가상환자 시나리오 생성", type="primary", use_container_width=True):
    generate_patient(st, client)

# ═══════════════════════════════════════════════════════════════════════════════
# PDF DOWNLOAD BUTTON (shows after scenario is generated)
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.get('scenario_generated', False):
    st.markdown("---")
    st.markdown("### 📥 시나리오 내보내기")
    
    # Generate PDF
    try:
        pdf_bytes = generate_patient_pdf_korean(
            summary=st.session_state.get('generated_summary', ''),
            scenario=st.session_state.get('generated_scenario', ''),
            patient_info=st.session_state.get('generated_patient_info', {})
        )
        
        # Ensure we have bytes type for Streamlit
        if isinstance(pdf_bytes, bytearray):
            pdf_bytes = bytes(pdf_bytes)
        
        # Create download button
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"patient_case_{timestamp}.pdf"
        
        st.download_button(
            label="📄 PDF 다운로드",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"PDF 생성 오류: Invalid binary data format: {type(pdf_bytes)}" if 'pdf_bytes' in dir() else f"PDF 생성 오류: {e}")
