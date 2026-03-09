"""
JSON Variable Name -> Session State Key Mapping
Part 1: Demographics, Vitals, Social History, Current/Family History
"""

# ── Conversion type constants ──
SCALE = "scale"        # option number maps directly to int value
CAT = "categorical"    # option number -> lookup string
RANGE = "range"        # option number -> sample numeric from range
BOOL2 = "bool2"        # 2-option: 1=True, 2=False (or reverse)
LIST_CAT = "list_cat"  # option number -> append string to list
SKIP = "skip"          # computed elsewhere or not mapped

# ══════════════════════════════════════════════════════════════
# MASTER MAPPING TABLE
# Keys   = Korean variable names from JSON files
# Values = (session_key, conversion_type, options_lookup)
#   options_lookup: dict {option_number: value} or None for SCALE
# ══════════════════════════════════════════════════════════════

VAR_MAP = {
    # ─── Demographics (인구학적정보) ───
    "성별": ("sex", CAT, {1: "남", 2: "여"}),
    "나이": ("age", RANGE, {
        1: (5, 19), 2: (20, 39), 3: (40, 54), 4: (55, 69), 5: (70, 85)
    }),
    "직업": ("job", CAT, {
        1: "관리직", 2: "전문직", 3: "사무직", 4: "서비스직",
        5: "판매직", 6: "농림어업직", 7: "기능직", 8: "장치/기계 조작직",
        9: "현장직", 10: "직업군인", 11: "학생/주부/무직/은퇴"
    }),
    "키": ("height", RANGE, {
        1: (145, 152), 2: (153, 160), 3: (161, 172),
        4: (173, 180), 5: (181, 190)
    }),
    "몸무게": ("weight", RANGE, {
        1: (40, 50), 2: (51, 58), 3: (59, 72),
        4: (73, 85), 5: (86, 110)
    }),
    "체질량지수": ("_bmi_cat", SKIP, None),  # computed from height/weight

    # ─── Vital Signs (활력징후) ───
    "혈압": ("sbp", RANGE, {
        1: (70, 89), 2: (90, 119), 3: (120, 139),
        4: (140, 159), 5: (160, 180)
    }),
    "체온": ("temp", RANGE, {
        1: (34.0, 35.9), 2: (36.0, 37.3), 3: (37.4, 37.9),
        4: (38.0, 39.9), 5: (40.0, 41.5)
    }),
    "맥박": ("pulse_rate", RANGE, {
        1: (40, 50), 2: (51, 60), 3: (61, 80),
        4: (81, 100), 5: (101, 130)
    }),
    "호흡": ("resp", RANGE, {
        1: (8, 11), 2: (12, 20), 3: (21, 30)
    }),

    # ─── Current Medical History (현병력) ───
    # These are duplicated in JSON (현병력 vs 가족력 sections)
    # We handle with section-aware disambiguation in the sampler
    "고혈압": ("_hx_hypertension", BOOL2, {1: True, 2: False}),
    "당뇨": ("_hx_diabetes", BOOL2, {1: True, 2: False}),
    "이상지질혈증": ("_hx_dyslipidemia", BOOL2, {1: True, 2: False}),
    "기타": ("_hx_other", SKIP, None),  # handled specially

    # ─── Medication History (약물력) ───
    "혈압약": ("_med_bp", BOOL2, {1: True, 2: False}),
    "당뇨약": ("_med_dm", BOOL2, {1: True, 2: False}),
    "이상지질혈증약": ("_med_lipid", BOOL2, {1: True, 2: False}),
    "수면제": ("_med_sleep", BOOL2, {1: True, 2: False}),
    "항우울제": ("_med_antidep", BOOL2, {1: True, 2: False}),
    "항불안제": ("_med_antianx", BOOL2, {1: True, 2: False}),

    # ─── Family History (가족력) ───
    # "고혈압", "당뇨" are duplicates — handled by section context
    "심장병": ("_fam_heart", BOOL2, {1: True, 2: False}),
    "중풍": ("_fam_stroke", BOOL2, {1: True, 2: False}),

    # ─── Social History: Alcohol (술) ───
    "월간 음주 횟수": ("social_alcohol_freq", CAT, {
        1: "비음주", 2: "월1-2회", 3: "주1-2회",
        4: "주3-4회", 5: "매일"
    }),
    "1회당 음주량": ("social_alcohol_amt", CAT, {
        1: "비음주", 2: "1-2잔", 3: "3-4잔",
        4: "5-6잔", 5: "7잔이상"
    }),

    # ─── Social History: Smoking (담배) ───
    "일간 개피": ("social_smoke_daily", RANGE, {
        1: (0, 0), 2: (1, 5), 3: (6, 10),
        4: (11, 20), 5: (21, 40)
    }),
    "총 흡연기간": ("social_smoke_years", RANGE, {
        1: (0, 0), 2: (1, 5), 3: (6, 15),
        4: (16, 30), 5: (31, 50)
    }),

    # ─── Social History: Exercise (운동) ───
    "주간 횟수": ("social_exercise_freq", RANGE, {
        1: (0, 0), 2: (1, 2), 3: (3, 4), 4: (5, 6), 5: (7, 7)
    }),
    "1회당 평균 운동 시간": ("social_exercise_time", RANGE, {
        1: (0, 0), 2: (10, 20), 3: (30, 45),
        4: (50, 60), 5: (70, 120)
    }),
    "운동 강도": ("social_exercise_int", CAT, {
        1: "없음", 2: "저", 3: "중", 4: "고", 5: "최대"
    }),

    # ─── Women's Health (여성력) ───
    "생리주기": ("mens_cycle", RANGE, {
        1: (14, 17), 2: (18, 20), 3: (21, 35), 4: (36, 39), 5: (40, 60)
    }),
    "생리규칙성": ("mens_regular", CAT, {
        1: "무월경", 2: "규칙", 3: "약간불규칙", 4: "불규칙"
    }),
    "생리기간": ("mens_duration", RANGE, {
        1: (1, 2), 2: (3, 3), 3: (4, 7), 4: (8, 10), 5: (11, 14)
    }),
    "생리 양": ("mens_amt", CAT, {
        1: "매우적음", 2: "적음", 3: "보통", 4: "많음", 5: "매우많음"
    }),
    "생리통강도": ("mens_pain_score", RANGE, {
        1: (0, 0), 2: (1, 3), 3: (4, 5), 4: (6, 7), 5: (8, 10)
    }),
    "생리혈 덩어리여부": ("mens_clot", SCALE, None),
    "생리혈 색": ("mens_color", CAT, {
        1: "연분홍", 2: "선홍", 3: "적색", 4: "암적색", 5: "흑색"
    }),

    # ─── Diet (식사) ───
    "1일 식사횟수": ("diet_freq", RANGE, {
        1: (1, 1), 2: (2, 2), 3: (3, 3), 4: (4, 4), 5: (5, 6)
    }),
    "식사 규칙성": ("diet_regular", CAT, {
        1: "매우규칙적", 2: "규칙적", 3: "보통", 4: "불규칙", 5: "매우불규칙"
    }),
    "1일 평균 식사량": ("diet_amt", CAT, {
        1: "매우적음", 2: "적음", 3: "보통", 4: "많음", 5: "매우많음"
    }),
    "1회 평균식사시간": ("diet_speed", CAT, {
        1: "매우빠름", 2: "빠름", 3: "보통", 4: "느림", 5: "매우느림"
    }),
    "소화정도": ("digestion", CAT, {
        1: "매우좋음", 2: "좋음", 3: "보통", 4: "나쁨", 5: "매우나쁨"
    }),
    "입맛": ("appetite", CAT, {
        1: "없음", 2: "저하", 3: "보통", 4: "좋음", 5: "항진"
    }),

    # ─── Stool (대변) ───
    "대변 횟수": ("stool_freq", CAT, {
        1: "3-4일1회", 2: "2일1회", 3: "1일1-2회", 4: "1일2-3회", 5: "1일3회이상"
    }),
    "대변 색": ("stool_color", CAT, {
        1: "흰색", 2: "황색", 3: "황갈색", 4: "갈색", 5: "흑색", 6: "적색"
    }),
    "대변 굳기(형태)": ("stool_form", CAT, {
        1: "딱딱한덩어리", 2: "소시지형딱딱", 3: "소시지형갈라짐",
        4: "보통", 5: "부드러운덩어리", 6: "흐물흐물", 7: "물변"
    }),
    "배변 후 불편감": ("stool_discomfort", SCALE, None),
    "배변 후 잔변감(강도)": ("stool_residual", SCALE, None),

    # ─── Urine (소변) ───
    "1일 소변 횟수(야간뇨 포함)": ("urine_freq_day", RANGE, {
        1: (0, 2), 2: (3, 4), 3: (5, 7), 4: (8, 10), 5: (11, 15)
    }),
    "야간뇨 횟수": ("urine_freq_night", RANGE, {
        1: (0, 0), 2: (1, 1), 3: (2, 2), 4: (3, 4), 5: (5, 7)
    }),
    "소변 색": ("urine_color", CAT, {
        1: "무색투명", 2: "연한황색", 3: "황색", 4: "진한황색",
        5: "갈색", 6: "적색", 7: "탁한색", 8: "거품"
    }),
    "소변 굵기(소변줄기)": ("urine_stream", CAT, {
        1: "매우약함", 2: "약함", 3: "보통", 4: "강함", 5: "매우강함"
    }),
    "소변 후 불편감": ("urine_discomfort", SCALE, None),
    "배뇨 후 잔뇨감(강도)": ("urine_residual_sev", SCALE, None),
    "유뇨, 요실금 빈도": ("urine_incontinence", SCALE, None),

    # ─── Sleep (수면상태) ───
    "기상시 상쾌도": ("sleep_waking_state", CAT, {
        1: "매우힘듦", 2: "힘듦", 3: "보통", 4: "상쾌", 5: "매우상쾌"
    }),
    "수면 시간": ("sleep_hours", RANGE, {
        1: (2, 4), 2: (5, 6), 3: (7, 9), 4: (10, 10), 5: (11, 13)
    }),
    "수면 깊이": ("sleep_depth", CAT, {
        1: "매우얕음", 2: "얕음", 3: "보통", 4: "깊음", 5: "매우깊음"
    }),
    "불면 빈도": ("insomnia_freq", SCALE, None),
    "꿈의 빈도 및 내용": ("dreams", CAT, {
        1: "거의없음", 2: "가끔평범", 3: "자주꿈", 4: "가끔악몽", 5: "자주악몽"
    }),
    "입면장애": ("insomnia_onset", SCALE, None),
    "수면 중도 각성 횟수": ("insomnia_maintain_count", RANGE, {
        1: (0, 0), 2: (1, 1), 3: (2, 2), 4: (3, 4), 5: (5, 7)
    }),
    "수면 중도 각성 후 재입면 장애": ("insomnia_reentry", SCALE, None),

    # ─── Sweat (땀) ───
    "일상 생활에서 땀 량": ("sweat_amt", CAT, {
        1: "없음", 2: "적음", 3: "보통", 4: "많음", 5: "매우많음"
    }),
    "땀나는 시간대": ("sweat_time", CAT, {
        1: "정상", 2: "주간", 3: "수면중", 4: "식사시"
    }),
    "땀나는 부위": ("sweat_area", CAT, {
        1: "머리얼굴", 2: "손발", 3: "가슴등", 4: "겨드랑이", 5: "전신"
    }),
    "땀 흘린 뒤 느낌": ("sweat_feeling", CAT, {
        1: "매우상쾌", 2: "상쾌", 3: "보통", 4: "지침", 5: "매우지침"
    }),

    # ─── Cold/Heat Tendency (한열경향) ───
    "인체 한열(몸이 차고 더운 정도)": ("cold_heat_body", CAT, {
        1: "매우뜨거움", 2: "약간뜨거움", 3: "보통", 4: "약간참", 5: "매우참"
    }),
    "한열의 편재(상열하한)": ("cold_heat_distribution", SCALE, None),
    "음료 온도 선호도": ("drink_temp", CAT, {
        1: "온수만", 2: "온수선호", 3: "상관없음", 4: "냉수선호", 5: "냉수만"
    }),
    "추위 민감도": ("cold_sensitivity", SCALE, None),
    "더위 민감도": ("heat_sensitivity", SCALE, None),
    "인체에서 비교적 따뜻한 부위": ("warm_body_areas", CAT, {
        1: "없음", 2: "머리", 3: "흉부", 4: "복부전체",
        5: "아랫배", 6: "등허리", 7: "팔손", 8: "다리발"
    }),
    "인체에서 비교적 차가운 부위": ("cold_body_areas", CAT, {
        1: "없음", 2: "머리", 3: "흉부", 4: "복부전체",
        5: "아랫배", 6: "등허리", 7: "팔손", 8: "다리발"
    }),

    # ─── General Condition (전신상태) ───
    "물살/단단": ("body_solidity", CAT, {
        1: "매우무름", 2: "무름", 3: "보통", 4: "단단", 5: "매우단단"
    }),
    "체력강약": ("physical_strength", CAT, {
        1: "매우약함", 2: "약함", 3: "보통", 4: "강함", 5: "매우강함"
    }),
    "피로감": ("fatigue_level", CAT, {
        1: "거의없음", 2: "경미", 3: "중등도", 4: "심함", 5: "매우심함"
    }),
    "부종여부": ("edema", CAT, {
        1: "없음", 2: "경미", 3: "중등도", 4: "심함", 5: "매우심함"
    }),
    "인체 부위의 출혈, 멍듬": ("bruising", CAT, {
        1: "정상", 2: "경미", 3: "중등도", 4: "심함", 5: "매우심함"
    }),
    "평소 컨디션이 안좋을 때 불편한 부위와 증상": ("condition_bad_area", LIST_CAT, {
        1: "없음", 2: "머리불편", 3: "뒷목어깨", 4: "코불편",
        5: "목불편", 6: "가슴불편", 7: "복부불편", 8: "변비",
        9: "설사", 10: "오한몸살", 11: "손발불편"
    }),
    "사지 무력감": ("limb_weakness", SCALE, None),
    "신체통, 근육통 여부": ("body_ache", SCALE, None),
    "신중(身重) 여부": ("body_heaviness", SCALE, None),

    # ─── Skin (피부상태) ───
    "피부트러블": ("skin_trouble", SCALE, None),
    "피부 건조도": ("skin_dry", CAT, {
        1: "정상", 2: "경미", 3: "중등도", 4: "심함", 5: "매우심함"
    }),
    "피부 가려움": ("skin_itch", SCALE, None),

    # ─── Face (얼굴) ───
    "얼굴 색": ("face_color", CAT, {
        1: "창백", 2: "황색", 3: "붉음", 4: "칙칙", 5: "거무스름"
    }),
    "얼굴 광택": ("face_gloss", CAT, {
        1: "없음", 2: "약간", 3: "보통", 4: "충만", 5: "매우충만"
    }),

    # ─── Eyes (눈) ───
    "눈 불편감": ("eye_discomfort", SCALE, None),
    "눈 충혈": ("eye_red", SCALE, None),
    "눈 앞이 캄캄함": ("vision_blackout", SCALE, {
        1: 0, 2: 1, 3: 3, 4: 5
    }),

    # ─── Ears (귀) ───
    "이명(빈도)": ("tinnitus_freq", SCALE, None),
    "이명(강도)": ("tinnitus_sev", SCALE, None),
    "이롱(난청)": ("hearing_sev", SCALE, None),

    # ─── Mouth/Throat (구강, 목) ───
    "입술 색": ("lip_color", CAT, {
        1: "선홍", 2: "창백", 3: "진한빨강", 4: "검붉은색", 5: "보라색"
    }),
    "입술 건조": ("lip_dry", SCALE, None),
    "음수량": ("water_intake", CAT, {
        1: "0.5L미만", 2: "0.5-1L", 3: "1.5-2.5L", 4: "2.5-3.5L", 5: "4L이상"
    }),
    "입마름 정도(구건/구갈)": ("mouth_dry", SCALE, None),
    "인후 건조": ("throat_dry", SCALE, None),
    "구고(입이씀)": ("mouth_bitter", SCALE, None),
    "구취": ("bad_breath", SCALE, None),
    "인후통": ("sore_throat", SCALE, None),
    "기침(빈도)": ("cough_sev", SCALE, None),
    "담(가래) 양": ("phlegm_amt", SCALE, None),
    "담(가래) 색": ("phlegm_color", CAT, {
        1: "투명흰색", 2: "흰색끈적", 3: "노란색", 4: "누런녹색"
    }),
    "딸꾹질": ("hiccup", SCALE, None),

    # ─── Head (두부) ───
    "감기(급성 상기도 감염)와 무관한-두부 불편감(빈도)": ("head_discomfort_freq", SCALE, None),
    "감기(급성 상기도 감염)와 무관한-두부 불편감(강도)": ("head_discomfort_sev", SCALE, None),
    "어지러움(두훈)": ("dizziness_sev", SCALE, None),

    # ─── Neck (뒷목, 경항부) ───
    "뒷목, 경항 불편감(빈도)": ("neck_nape_freq", SCALE, None),
    "뒷목, 경항 불편감(강도)": ("neck_nape_sev", SCALE, None),

    # ─── Chest (흉부) ───
    "호흡소리 크기": ("breath_sound", CAT, {
        1: "매우작음", 2: "작음", 3: "보통", 4: "큼", 5: "매우큼"
    }),
    "흉부 두근거림": ("palpitation", SCALE, None),
    "흉부 답답함(빈도)": ("chest_tight_freq", SCALE, None),
    "흉부 답답함(강도)": ("chest_tight_sev", SCALE, None),
    "흉부 통증(빈도)": ("chest_pain_freq", SCALE, None),
    "흉부통증(강도)": ("chest_pain_sev", SCALE, None),
    "한숨 빈도": ("sighing_freq", SCALE, {1: 0, 2: 2, 3: 3, 4: 5}),

    # ─── Abdomen (복부) ───
    "구역감/구토": ("nausea", SCALE, None),
    "복만/가스 참(강도)": ("bloating", SCALE, None),
    "방귀": ("flatulence", CAT, {
        1: "없음", 2: "1-2회/일", 3: "5-10회/일", 4: "10회이상/일", 5: "매우잦음"
    }),
    "아랫배 불편감(강도)": ("lower_abd_discomfort", SCALE, None),
    "전복부 통증(강도)": ("abd_pain_sev", SCALE, None),
    "복통의 양상": ("abd_pain_type", CAT, {
        1: "없음", 2: "은근한통증", 3: "콕콕찌르는", 4: "쥐어짜는",
        5: "타는듯한", 6: "묵직한", 7: "경련성"
    }),
    "눌렀을 때 복부 압통": ("abd_tenderness", SCALE, None),
    "메스꺼움(강도)": ("nausea_sev", SCALE, None),
    "트림": ("belching", SCALE, None),
    "트림 시 냄새": ("belching_smell", CAT, {
        1: "정상", 2: "시큼한", 3: "썩은달걀", 4: "쓴냄새", 5: "부패냄새"
    }),
    "체함(강도)": ("food_stag_sev", SCALE, None),
    "복직근 긴장감": ("abd_muscle_tension", SCALE, None),
    "복부 덩어리 만져짐": ("abd_mass", SCALE, None),
    "동계": ("abd_pulsation", SCALE, None),
    "장명(장에서 나는 소리)": ("bowel_sound", CAT, {
        1: "없음", 2: "간헐적", 3: "가끔", 4: "지속적", 5: "만성적"
    }),

    # ─── Musculoskeletal (근골격) ───
    "옆구리 불편감(빈도)": ("flank_freq", SCALE, None),
    "옆구리 불편감(강도)": ("flank_sev", SCALE, None),
    "등 불편감(빈도)": ("back_freq", SCALE, None),
    "등 불편감(강도)": ("back_sev", SCALE, None),
    "골반부 불편감(빈도)": ("pelvis_freq", SCALE, None),
    "골반부 불편감(강도)": ("pelvis_sev", SCALE, None),
    "어깨 불편감(빈도)": ("shoulder_freq", SCALE, None),
    "어깨 불편감(강도)": ("shoulder_sev", SCALE, None),
    "팔꿈치불편감(빈도)": ("elbow_freq", SCALE, None),
    "팔꿈치불편감(강도)": ("elbow_sev", SCALE, None),
    "손 또는 발 불편감(빈도)": ("hand_foot_freq", SCALE, None),
    "손 또는 발 불편감(강도)": ("hand_foot_sev", SCALE, None),
    "수족냉증(손발냉감)": ("cold_hands_feet", SCALE, None),
    "다리 불편감": ("leg_discomfort", SCALE, {1: 0, 2: 2, 3: 3, 4: 5}),
    "슬부 불편감(빈도)": ("knee_freq", SCALE, None),
    "슬부 불편감(강도)": ("knee_sev", SCALE, None),

    # ─── Personality (성격) ───
    # Cold uses "성격 완급" while others use "완급"
    "완급(느긋함/급함)": ("personality_speed", SCALE, None),
    "성격 완급(느긋함/급함)": ("personality_speed", SCALE, None),
    "강유(부드러움/감함)": ("personality_soft", SCALE, None),
    "성격 강유(부드러움/감함)": ("personality_soft", SCALE, None),
    "내외(내성적/외향적)": ("personality_io", SCALE, None),
    "성격내외(내성적/외향적)": ("personality_io", SCALE, None),
    "동정(정적/동적)": ("personality_static", SCALE, None),
    "성격 동정(정적/동적)": ("personality_static", SCALE, None),
    "목소리크기(성음크기)": ("voice_vol", CAT, {
        1: "매우작음", 2: "작음", 3: "보통", 4: "큼", 5: "매우큼"
    }),

    # ─── Emotions (감정) ───
    "흥분정도(차분함)": ("excitement", SCALE, None),
    "노(화냄/평온)": ("emot_anger", SCALE, None),
    "우울(우울함)": ("emot_depress", SCALE, None),
    "불안": ("emot_anxiety", SCALE, None),
    "공(두려움/용기)": ("emot_fear", SCALE, None),
    "놀람(잘놀람/평온함)": ("emot_startle", SCALE, None),
    "생각(생각많음/적음)": ("emot_thought", SCALE, None),
    "비탄(슬픔많음/적음)": ("emot_grief", SCALE, None),

    # ─── Mental State (정신상태) ───
    # Cold uses different names than others
    "득신/실신": ("mental_clarity", SCALE, None),
    "정신상태": ("mental_clarity", SCALE, None),
    "기억력저하": ("memory", SCALE, None),
    "기억력": ("memory", SCALE, None),
    "의욕 저하": ("motivation", SCALE, None),
    "의욕": ("motivation", SCALE, None),
    "스트레스 대처력": ("stress_coping", SCALE, None),
    "감정 기복": ("mood_swing", SCALE, None),
}

# ══════════════════════════════════════════════════════════════
# PULSE & TONGUE (맥, 설, 태) — separate dict to keep VAR_MAP smaller
# ══════════════════════════════════════════════════════════════
VAR_MAP_PULSE_TONGUE = {
    "맥 부침 정도(부침)": ("pulse_depth", CAT, {
        1: "부맥", 2: "부맥", 3: "중맥", 4: "침맥", 5: "복맥"
    }),
    "맥 폭 정도(대세)": ("pulse_width", CAT, {
        1: "극세맥", 2: "세맥", 3: "중맥", 4: "대맥", 5: "大맥"
    }),
    "맥 길이 정도(장단)": ("pulse_length", CAT, {
        1: "단", 2: "단", 3: "중", 4: "장", 5: "장"
    }),
    "맥 부드럽고 거친 정도(활삽)": ("pulse_smooth", CAT, {
        1: "삽맥", 2: "삽맥", 3: "완맥", 4: "활맥", 5: "활맥"
    }),
    "세기": ("pulse_strength", CAT, {
        1: "무력", 2: "무력", 3: "중", 4: "유력", 5: "유력"
    }),
    "맥 긴장도(현긴완)": ("pulse_tension", CAT, {
        1: "완", 2: "완", 3: "유", 4: "현", 5: "긴"
    }),
    "혀 색": ("tongue_color", CAT, {
        1: "담백", 2: "담홍", 3: "홍", 4: "강", 5: "청"
    }),
    "혀 크기": ("tongue_size", CAT, {
        1: "매우작음", 2: "작음", 3: "정상", 4: "큼", 5: "매우큼"
    }),
    "혀 흔적-치흔": ("tongue_marks", SCALE, None),
    "설태 색": ("tongue_coat_color", CAT, {1: "황태", 2: "백태"}),
    "설태 두께": ("tongue_coat_thick", CAT, {
        1: "무태", 2: "소태", 3: "박태", 4: "후태"
    }),
    "설태 입자크기": ("tongue_coat_particle", CAT, {
        1: "니태", 2: "니태", 3: "윤", 4: "부태", 5: "부태"
    }),
}

# ══════════════════════════════════════════════════════════════
# DISEASE-SPECIFIC VARIABLES
# ══════════════════════════════════════════════════════════════
VAR_MAP_COLD = {
    "감기증상 발현시점": ("cold_onset_specific", CAT, {
        1: "1주이내", 2: "1주-1개월", 3: "1-3개월",
        4: "3-6개월", 5: "6개월-1년", 6: "1년이상"
    }),
    "경과": ("course", CAT, {1: "악화중"}),
    "경과1": ("course", CAT, {1: "악화중"}),
    "과거 감기 경험": ("past_illness_cold", BOOL2, {1: True, 2: False}),
    "과거 감기증상 시 문제가 되는 부위": ("past_cold_problem_area", LIST_CAT, {
        1: "없음", 2: "코", 3: "목", 4: "머리",
        5: "몸살", 6: "기침가래", 7: "소화기"
    }),
    "평소 감기걸렸을 때 문제되는 부위": ("past_cold_problem_area", LIST_CAT, {
        1: "없음", 2: "코", 3: "목", 4: "머리",
        5: "몸살", 6: "기침가래", 7: "소화기"
    }),
    "발열": ("fever_sev", SCALE, None),
    "오한": ("chills_sev", SCALE, None),
    "한열왕래": ("alternating_chills_fever", SCALE, None),
    "콧물 감기": ("snot_sev", SCALE, None),
    "코막힘": ("nose_block_sev", SCALE, None),
    "후각 감퇴": ("smell_reduction", SCALE, None),
    "코 건조함": ("nose_dry", SCALE, {1: 0, 2: 1, 3: 3, 4: 5}),
    "재채기": ("sneeze_sev", SCALE, None),
    "기침": ("cough_sev", SCALE, None),
    "몸살, 신체통, 근육통": ("body_ache_cold", SCALE, None),
    "신중(身重)": ("body_heaviness_cold", SCALE, None),
    "두부, 뒷목 불편감(강도)": ("headache_cold", SCALE, None),
    "감기 시 땀 유무": ("cold_sweating_check", SCALE, None),
    "숨이 가쁨": ("cold_dyspnea", SCALE, {1: 0, 2: 2, 3: 3, 4: 5}),
    "감기 완화요인/악화요인": ("cold_modifying_factors", LIST_CAT, {
        1: "없음", 2: "온열완화", 3: "냉기악화",
        4: "피로악화", 5: "스트레스악화", 6: "음식영향"
    }),
    # Cold examinations
    "호흡음(폐음) 진찰": ("exam_lung_sound", CAT, {
        1: "정상", 2: "약간이상", 3: "이상", 4: "심각"
    }),
    "인후부 진찰": ("exam_throat", CAT, {
        1: "정상", 2: "약간충혈", 3: "충혈", 4: "심한충혈"
    }),
    "편도진찰": ("exam_tonsil", CAT, {
        1: "정상", 2: "약간비대", 3: "비대", 4: "심한비대"
    }),
    "X-ray 검사": ("exam_xray", BOOL2, {1: True, 2: False}),
    "이경 검사": ("exam_otoscope", BOOL2, {1: True, 2: False}),
    "비경 검사": ("exam_rhinoscope", BOOL2, {1: True, 2: False}),
    "혈액검사": ("exam_blood_test", BOOL2, {1: True, 2: False}),
}

VAR_MAP_RHINITIS = {
    "알러지비염 발현시점": ("rhinitis_onset", CAT, {
        1: "1주이내", 2: "1주-1개월", 3: "1-3개월",
        4: "3-6개월", 5: "6개월-1년", 6: "1년이상"
    }),
    "과거 알러지비염 경험": ("rhinitis_past", BOOL2, {1: True, 2: False}),
    "콧물 량": ("snot_sev", SCALE, None),
    "콧물 색": ("snot_color", CAT, {
        1: "맑은색", 2: "흰색", 3: "노란색"
    }),
    "재채기(정도)": ("sneeze_sev", SCALE, None),
    "재채기(빈도)": ("sneeze_freq", SCALE, None),
    "코 가려움": ("nose_itch_sev", SCALE, None),
    "알러지비염 완화요인/악화요인": ("rhinitis_modifying_factors", LIST_CAT, {
        1: "없음", 2: "환절기악화", 3: "먼지악화", 4: "냉기악화",
        5: "온열완화", 6: "실내완화", 7: "약물완화"
    }),
    "비경검사(점막이 부어있으면 안됨)": ("exam_rhinoscope_finding", CAT, {
        1: "정상", 2: "이상"
    }),
}

VAR_MAP_DYSPEPSIA = {
    "소화불량 시작시점": ("dyspepsia_onset", CAT, {
        1: "1주이내", 2: "1주-1개월", 3: "1-3개월",
        4: "3-6개월", 5: "6개월-1년", 6: "1년이상"
    }),
    "경과2. 과거유사경험": ("dyspepsia_past", BOOL2, {1: True, 2: False}),
    "식후포만감": ("postprandial_fullness", SCALE, None),
    "조기포만감": ("early_satiety", SCALE, None),
    "상복부 불편감(강도), 상복부 통증": ("epigastric_discomfort", SCALE, None),
    "상복부 속쓰림(강도)": ("epigastric_burning", SCALE, None),
    "소화불량 완화요인/악화요인": ("dyspepsia_modifying_factors", LIST_CAT, {
        1: "없음", 2: "식후악화", 3: "공복악화",
        4: "스트레스악화", 5: "온열완화"
    }),
    "위내시경 검사": ("exam_endoscopy", BOOL2, {1: True, 2: False}),
}

VAR_MAP_BACKPAIN = {
    "요통 발현시점": ("backpain_onset", CAT, {
        1: "1주이내", 2: "1주-1개월", 3: "1-3개월",
        4: "3-6개월", 5: "6개월-1년", 6: "1년이상"
    }),
    "과거 요통": ("backpain_past", BOOL2, {1: True, 2: False}),
    "허리 불편부위": ("back_discomfort_area", CAT, {
        1: "모름", 2: "아래", 3: "위", 4: "정중간", 5: "좌우편측", 6: "전반"
    }),
    "허리 불편(빈도)": ("back_discomfort_freq", SCALE, None),
    "허리 불편(강도)": ("back_discomfort_sev", SCALE, None),
    "방산통": ("radiation_pain", CAT, {
        1: "없음", 2: "옆으로약간", 3: "엉덩이까지", 4: "다리까지"
    }),
    "통증지속시간": ("pain_duration", SCALE, None),
    "허리 통증의 양상": ("back_pain_nature", LIST_CAT, {
        1: "당기는", 2: "찌르는", 3: "무거운", 4: "쑤시는",
        5: "차고시린", 6: "돌아다니는", 7: "고정된", 8: "굽히기어려운"
    }),
    "허리통증 악화요인/완화요인": ("back_modifying_factors", LIST_CAT, {
        1: "없음", 2: "앉으면악화", 3: "서면악화", 4: "움직이면악화",
        5: "쉬면완화", 6: "온열완화", 7: "냉기악화",
        8: "아침악화", 9: "저녁악화"
    }),
    "하지직거상검사": ("slr_test", BOOL2, {1: True, 2: False}),
    "CT 검사": ("exam_ct", BOOL2, {1: True, 2: False}),
    "MRI 검사": ("exam_mri", BOOL2, {1: True, 2: False}),
}

# ══════════════════════════════════════════════════════════════
# DISEASE FILE PATHS & CONFIGS
# ══════════════════════════════════════════════════════════════
DISEASE_FILES = {
    "감기": {
        "general": "data/diseases/vertical_general_probs/common_cold_general_probs.json",
        "syndrome": "data/diseases/horizontal_syndrome_probs/common_cold_syndrome_probs.json",
        "code": "J06",
        "label": "감기/급성상기도감염",
    },
    "알레르기비염": {
        "general": "data/diseases/vertical_general_probs/allergic_rhinitis_general_probs.json",
        "syndrome": "data/diseases/horizontal_syndrome_probs/allergic_rhinitis_syndrome_probs.json",
        "code": "J30",
        "label": "알레르기비염",
    },
    "기능성소화불량": {
        "general": "data/diseases/vertical_general_probs/functional_dyspepsia_general_probs.json",
        "syndrome": "data/diseases/horizontal_syndrome_probs/functional_dyspepsia_syndrome_probs.json",
        "code": "K30",
        "label": "기능성소화불량",
    },
    "요통": {
        "general": "data/diseases/vertical_general_probs/lower_back_pain_general_probs.json",
        "syndrome": "data/diseases/horizontal_syndrome_probs/lower_back_pain_syndrome_probs.json",
        "code": "M54",
        "label": "요통",
    },
}

DISEASE_SPECIFIC_MAPS = {
    "감기": VAR_MAP_COLD,
    "알레르기비염": VAR_MAP_RHINITIS,
    "기능성소화불량": VAR_MAP_DYSPEPSIA,
    "요통": VAR_MAP_BACKPAIN,
}

CONSTRAINTS_FILE = "data/rules/all_correlation_scales.json"

# Cold file has 체온 split across 3 entries (opts 1, 2, 3-5)
# The sampler merges them before sampling
COLD_TEMP_MERGE = True

# Duplicate variable names that appear in BOTH 현병력 and 가족력
SECTION_DUPES = {"고혈압", "당뇨", "이상지질혈증", "기타"}


def get_full_var_map(disease_key):
    """Return merged mapping dict for a given disease."""
    merged = {}
    merged.update(VAR_MAP)
    merged.update(VAR_MAP_PULSE_TONGUE)
    specific = DISEASE_SPECIFIC_MAPS.get(disease_key, {})
    merged.update(specific)
    return merged
