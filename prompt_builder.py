"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - LLM Prompt Builder  (Auto-Dump Approach)

All clinical session keys are automatically included in the prompt.
To add a new variable: add it to VAR_MAP → add its session_key to
the appropriate section in GENERAL_SECTIONS or DISEASE_SECTIONS → done.
No hand-coded f-string references required.
═══════════════════════════════════════════════════════════════════════════════
"""

from json_var_mapping import (
    VAR_MAP, VAR_MAP_PULSE_TONGUE,
    VAR_MAP_COLD, VAR_MAP_RHINITIS, VAR_MAP_DYSPEPSIA, VAR_MAP_BACKPAIN,
    SKIP,
)

# ══════════════════════════════════════════════════════════════
# REVERSE MAP: session_key → Korean label
# Built once at import from all VAR_MAPs
# ══════════════════════════════════════════════════════════════

def _build_reverse_map():
    """session_key → first Korean label found across all mapping tables."""
    rev = {}
    for var_map in (VAR_MAP, VAR_MAP_PULSE_TONGUE,
                    VAR_MAP_COLD, VAR_MAP_RHINITIS,
                    VAR_MAP_DYSPEPSIA, VAR_MAP_BACKPAIN):
        for kr_name, entry in var_map.items():
            skey, ctype = entry[0], entry[1]
            if not skey.startswith("_") and ctype != SKIP and skey not in rev:
                rev[skey] = kr_name
    return rev

_REVERSE = _build_reverse_map()

# Keys from session_defaults that are NOT in any VAR_MAP
_EXTRA = {
    "disease":                  "질환명",
    "onset":                    "발현시점",
    "episode":                  "발병 에피소드",
    "dbp":                      "이완기혈압(mmHg)",
    "history_conditions":       "현병력",
    "meds_specific":            "약물력",
    "family_hx":                "가족력",
    "aggravating_factors":      "악화요인",
    "relieving_factors":        "완화요인",
    "compound_pulse":           "복합맥상",
    "cold_heat_pref":           "한열 선호",
    "cold_symptoms_spec":       "감기 기타증상",
    "cold_chief_type":          "감기 주소증 유형",
    "insomnia_maintain":        "중도각성(0-5)",
    "neck_pain_cold":           "경항통(감기)",
    "additional_symptoms":      "추가 증상",
    "additional_comorbidities": "추가 동반질환",
    "exam_stethoscope":         "청진기 호흡음",
    "exam_throat_visual":       "인후부 망진/촉진",
    "exam_tongue_depressor":    "설압자 편도소견",
    "pain_sev":                 "통증강도",
    "pain_nature":              "통증양상",
    "dyspepsia_spec":           "소화불량 증상",
    "snot_type":                "콧물 성상",
}

def _label(key):
    """Korean label for a session key."""
    return _REVERSE.get(key) or _EXTRA.get(key) or key


# ══════════════════════════════════════════════════════════════
# PROMPT SECTIONS
# Single source of truth for what data reaches the LLM.
# Add a session_key here → it appears in the prompt automatically.
# ══════════════════════════════════════════════════════════════

GENERAL_SECTIONS = [
    ("인구학적정보 및 활력징후", [
        "age", "sex", "job", "height", "weight",
        "sbp", "dbp", "temp", "pulse_rate", "resp",
        "onset", "course", "episode",
    ]),
    ("병력", [
        "history_conditions", "meds_specific", "family_hx",
        "aggravating_factors", "relieving_factors",
    ]),
    ("사회력", [
        "social_alcohol_freq", "social_alcohol_amt",
        "social_smoke_daily", "social_smoke_years",
        "social_exercise_freq", "social_exercise_time", "social_exercise_int",
    ]),
    ("여성력", [
        "mens_cycle", "mens_regular", "mens_duration",
        "mens_pain_score", "mens_color", "mens_amt", "mens_clot",
    ]),
    ("식사/소화", [
        "diet_freq", "diet_regular", "diet_amt", "diet_speed",
        "water_intake", "digestion", "appetite",
    ]),
    ("대변", [
        "stool_freq", "stool_color", "stool_form",
        "stool_discomfort", "stool_residual",
    ]),
    ("소변", [
        "urine_color", "urine_freq_day", "urine_freq_night",
        "urine_stream", "urine_discomfort", "urine_residual_sev",
        "urine_incontinence",
    ]),
    ("수면", [
        "sleep_hours", "sleep_depth", "sleep_waking_state",
        "insomnia_onset", "insomnia_maintain", "insomnia_freq",
        "insomnia_maintain_count", "insomnia_reentry", "dreams",
    ]),
    ("땀", [
        "sweat_amt", "sweat_time", "sweat_area", "sweat_feeling",
    ]),
    ("한열", [
        "cold_heat_pref", "cold_heat_body", "cold_heat_distribution",
        "cold_sensitivity", "heat_sensitivity",
        "drink_temp", "cold_hands_feet",
        "warm_body_areas", "cold_body_areas",
    ]),
    ("전신상태", [
        "body_solidity", "physical_strength", "fatigue_level",
        "body_ache", "body_heaviness", "condition_bad_area",
        "edema", "bruising", "limb_weakness", "vision_blackout",
    ]),
    ("피부/면색", [
        "skin_dry", "skin_itch", "skin_trouble",
        "face_color", "face_gloss",
    ]),
    ("눈", [
        "eye_discomfort", "eye_red",
    ]),
    ("귀/어지러움", [
        "tinnitus_sev", "tinnitus_freq", "hearing_sev", "dizziness_sev",
    ]),
    ("구강/인후", [
        "lip_color", "lip_dry", "mouth_dry", "throat_dry",
        "mouth_bitter", "bad_breath", "sore_throat",
        "cough_sev", "phlegm_amt", "phlegm_color", "hiccup",
    ]),
    ("두부/경항부", [
        "head_discomfort_freq", "head_discomfort_sev",
        "neck_nape_freq", "neck_nape_sev",
    ]),
    ("흉부", [
        "breath_sound", "palpitation",
        "chest_tight_freq", "chest_tight_sev",
        "chest_pain_freq", "chest_pain_sev",
        "sighing_freq",
    ]),
    ("복부", [
        "nausea", "nausea_sev", "bloating", "flatulence",
        "belching", "belching_smell", "food_stag_sev",
        "lower_abd_discomfort", "abd_pain_sev", "abd_pain_type",
        "abd_tenderness", "abd_muscle_tension",
        "abd_mass", "abd_pulsation", "bowel_sound",
    ]),
    ("근골격계", [
        "flank_freq", "flank_sev", "back_freq", "back_sev",
        "pelvis_freq", "pelvis_sev",
        "shoulder_freq", "shoulder_sev",
        "elbow_freq", "elbow_sev",
        "hand_foot_freq", "hand_foot_sev",
        "leg_discomfort", "knee_freq", "knee_sev",
    ]),
    ("성격", [
        "personality_speed", "personality_soft",
        "personality_io", "personality_static", "voice_vol",
    ]),
    ("감정/정신", [
        "excitement", "emot_anger", "emot_depress", "emot_anxiety",
        "emot_fear", "emot_startle", "emot_thought", "emot_grief",
        "memory", "motivation", "stress_coping",
        "mental_clarity", "mood_swing",
    ]),
    ("맥진", [
        "compound_pulse",
        "pulse_depth", "pulse_width", "pulse_length",
        "pulse_smooth", "pulse_strength", "pulse_tension",
    ]),
    ("설진", [
        "tongue_color", "tongue_size",
        "tongue_coat_color", "tongue_coat_thick",
        "tongue_marks", "tongue_coat_particle",
    ]),
]

DISEASE_SECTIONS = {
    "감기": [
        ("감기 증상", [
            "fever_sev", "chills_sev", "alternating_chills_fever",
            "snot_sev", "snot_color", "nose_block_sev", "nose_dry",
            "smell_reduction", "sneeze_sev",
            "body_ache_cold", "body_heaviness_cold",
            "headache_cold", "neck_pain_cold",
            "cold_dyspnea", "cold_sweating_check",
            "cold_onset_specific", "cold_chief_type", "cold_symptoms_spec",
            "cold_modifying_factors",
            "past_illness_cold", "past_cold_problem_area",
        ]),
        ("감기 진찰소견", [
            "exam_stethoscope", "exam_throat_visual", "exam_tongue_depressor",
            "exam_lung_sound", "exam_throat", "exam_tonsil",
            "exam_rhinoscope", "exam_rhinoscope_finding",
            "exam_xray", "exam_otoscope", "exam_blood_test",
        ]),
    ],
    "비염": [
        ("알레르기비염 증상", [
            "sneeze_sev", "sneeze_freq", "nose_block_sev",
            "nose_itch_sev", "snot_sev", "snot_color", "snot_type",
            "rhinitis_onset", "rhinitis_past",
            "rhinitis_modifying_factors",
            "exam_rhinoscope_finding",
        ]),
    ],
    "소화불량": [
        ("기능성소화불량 증상", [
            "dyspepsia_onset", "dyspepsia_past",
            "postprandial_fullness", "early_satiety",
            "epigastric_discomfort", "epigastric_burning",
            "dyspepsia_spec", "pain_sev",
            "dyspepsia_modifying_factors", "exam_endoscopy",
        ]),
    ],
    "요통": [
        ("요통 증상", [
            "backpain_onset", "backpain_past",
            "back_discomfort_area", "back_discomfort_freq",
            "back_discomfort_sev",
            "radiation_pain", "pain_duration", "pain_sev",
            "pain_nature", "back_pain_nature",
            "back_modifying_factors",
            "slr_test", "exam_ct", "exam_mri",
        ]),
    ],
}

TAIL_SECTIONS = [
    ("추가 정보", [
        "additional_symptoms", "additional_comorbidities",
    ]),
]


# ══════════════════════════════════════════════════════════════
# DATA BLOCK BUILDER
# ══════════════════════════════════════════════════════════════

def _fmt(val):
    """Format a single session value. Returns None to skip."""
    if val is None:
        return None
    if isinstance(val, list):
        return ", ".join(str(v) for v in val) if val else None
    if isinstance(val, bool):
        return "있음" if val else None
    if val == "" or val == 0:
        return None
    return str(val)


def _render_sections(session, sections):
    """Render (section_name, [keys]) pairs into prompt lines.
    Skips 여성력 section for male patients.
    Skips sections whose values are all empty.
    """
    lines = []
    for name, keys in sections:
        if name == "여성력" and session.get("sex") != "여":
            continue

        body = []
        for k in keys:
            v = _fmt(session.get(k))
            if v:
                body.append(f"  - {_label(k)}: {v}")
        if body:
            lines.append(f"\n### {name}")
            lines.extend(body)
    return lines


def _build_data_block(session):
    """Auto-generate the structured patient data block from session state."""
    lines = []

    # BMI (computed, not a session key)
    h = session.get("height", 0)
    w = session.get("weight", 0)
    if h and w:
        bmi = w / ((h / 100) ** 2)
        lines.append(f"\n※ BMI: {bmi:.1f}")

    # General sections (always included)
    lines.extend(_render_sections(session, GENERAL_SECTIONS))

    # Disease-specific sections (only when disease matches)
    disease = session.get("disease", "")
    for keyword, sections in DISEASE_SECTIONS.items():
        if keyword in disease:
            lines.extend(_render_sections(session, sections))

    # Tail sections
    lines.extend(_render_sections(session, TAIL_SECTIONS))

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# MAIN PROMPT BUILDER
# ══════════════════════════════════════════════════════════════

def build_generation_prompt(session):
    """Build the complete LLM prompt for patient scenario generation.

    The patient-data section is AUTO-GENERATED from session state.
    Only the role instructions and output format are hand-crafted.

    NOTE: This generates PATIENT PRESENTATION DATA ONLY.
    변증 (diagnosis), 치법 (treatment), 처방 (prescription) are NOT generated.
    """
    data_block = _build_data_block(session)

    return f"""당신은 한의 임상 가상환자 시나리오 생성 전문가입니다.

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

⚠️ 중요: 아래 환자 정보에서 제공되지 않은 항목은 시나리오에서 생략하거나
"특이소견 없음"으로 간략히 처리하세요.
양성 소견(증상이 있는 항목)을 중심으로 자세히 서술하세요.

## 환자 정보
{data_block}

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
    [발병 전 상황을 구체적으로 기술. 예: '3일 전 영하 10도의 날씨에
    버스 정류장에서 40분간 대기한 후 다음날부터 오한과 발열이
    시작되었다.' 또는 '과로와 수면 부족이 지속된 후 증상이
    발생하였다.' 등 발병 계기를 서술]

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
    - 성격: [완급/강유/내외향/동정, 목소리]
    - 감정: [분노/우울/불안/공포/놀람/사려/비탄]

    【신체검진 소견】
    - 활력징후: BP, 맥박, 체온, 호흡
    - 전신 상태: 피로감, 체력, 부종, 피부 상태
    - 면색: 창백/홍조/황색/정상 등
    - 구강: 입술색/건조, 구강건조, 구고(입쓴맛)

    【설진 소견】
    - 설질: 색깔, 크기, 형태, 치흔
    - 설태: 색깔, 두께, 입자크기

    【맥진 소견】
    - 맥위(부침): 부/중/침
    - 맥폭(대세): 세/중/대
    - 맥장(장단): 단/중/장
    - 맥활삽: 삽/완/활
    - 맥력: 무력/중/유력
    - 맥긴장(현긴완): 완/유/현/긴
    - 복합맥상: 종합 맥 판정"
}}

## 중요 지침
1. 모든 출력은 한국어로 작성
2. 의사 관점으로 작성 (환자 시점 ❌)
3. 한의학 전문용어 적극 사용 (惡寒, 發熱, 無汗 등)
4. ⚠️ 변증, 치법, 처방은 절대 생성하지 마세요!
5. 객관적인 환자 소견만 기술하세요
6. 제공된 맥진 6요소(부침/대세/장단/활삽/맥력/현긴완)를 반드시 설진과 함께 기술하세요
7. 제공된 성격/감정/정신 데이터를 계통적 문진에 반드시 포함하세요
"""
