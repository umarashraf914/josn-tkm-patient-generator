"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Session State Defaults
Based on Pages 17-19: Complete TKM Clinical Information Items (한의 임상정보 항목)
═══════════════════════════════════════════════════════════════════════════════
"""

SESSION_DEFAULTS = {
    # ===========================================
    # 인구학적정보 (Demographics) - Page 17
    # ===========================================
    "age": 45, "sex": "남", "job": "현장직",
    "height": 175, "weight": 70,  # 키, 몸무게 -> BMI calculated
    
    # ===========================================
    # 활력징후 (Vital Signs) - Page 18
    # ===========================================
    "sbp": 120, "dbp": 80, "temp": 36.5, "pulse_rate": 72, "resp": 18,
    "consciousness": "A",  # AVPU 의식상태: A(Alert), V(Voice), P(Pain), U(Unresponsive)
    "spo2": 98,  # 산소포화도 (%)

    # ===========================================
    # O/S 경과 (Onset/History) - Page 17
    # ===========================================
    "onset": "1주 전",  # 증상 발현시점
    "course": "악화중",  # 경과
    "episode": "",  # 발병 에피소드 (발병 계기)
    "past_illness": [],  # 과거 질병 경험
    "past_cold_problem_area": [],  # 과거 감기증상 시 문제가 되는 부위
    "aggravating_factors": [],  # 악화요인
    "relieving_factors": [],  # 완화요인

    # ===========================================
    # 현병력 (Current Medical History) - Page 18
    # ===========================================
    "history_conditions": [],  # 고혈압, 당뇨, 이상지질혈증, 기타
    
    # ===========================================
    # 약물력 (Medication History) - Page 18
    # ===========================================
    "meds_specific": [],  # 혈압약, 당뇨약, 이상지질혈증약, 수면제, 항우울제, 항불안제
    
    # ===========================================
    # 가족력 (Family History) - Page 18
    # ===========================================
    "family_hx": [],  # 고혈압, 당뇨, 심장병, 중풍, 기타

    # ===========================================
    # 사회력 (Social History) - Page 18
    # ===========================================
    # 술 (Alcohol)
    "social_alcohol_freq": "비음주",  # 월간 음주 횟수
    "social_alcohol_amt": 0.0,  # 1회당 음주량
    # 담배 (Smoking)
    "social_smoke_daily": 0.0,  # 일간 개피
    "social_smoke_years": 0,  # 총 흡연기간 (years)
    # 운동 (Exercise)
    "social_exercise_freq": 0,  # 주간 횟수
    "social_exercise_time": 0,  # 1회당 평균 운동 시간
    "social_exercise_int": "중",  # 운동 강도

    # ===========================================
    # 여성력 (Women's Health) - Page 18 (가임기 여성 14-50세만)
    # ===========================================
    "mens_cycle": 28,  # 생리주기
    "mens_regular": "규칙",  # 생리규칙성
    "mens_duration": 5,  # 생리기간
    "mens_amt": "보통",  # 생리 양
    "mens_pain_score": 0,  # 생리통강도 (0-10)
    "mens_clot": False,  # 생리혈 덩어리여부
    "mens_color": "적색",  # 생리혈 색

    # ===========================================
    # 식사 (Diet) - Page 18
    # ===========================================
    "diet_freq": 3,  # 1일 식사횟수
    "diet_regular": "규칙적",  # 식사 규칙성
    "diet_amt": "보통",  # 1일 평균 식사량
    "diet_speed": "보통",  # 1회 평균식사시간
    "digestion": "보통",  # 소화여부/소화정도
    "appetite": "보통",  # 입맛

    # ===========================================
    # 대변 (Stool) - Page 18-19
    # ===========================================
    "stool_freq": "1회/일",  # 대변 횟수
    "stool_color": "황갈색",  # 대변 색
    "stool_form": "보통",  # 대변 굵기(형태)
    "stool_discomfort": False,  # 배변 후 불편감
    "stool_residual": 0,  # 배변 후 잔변감(강도) 0-5

    # ===========================================
    # 소변 (Urine) - Page 19
    # ===========================================
    "urine_freq_day": 5,  # 1일 소변 횟수
    "urine_freq_night": 0,  # 야간뇨 횟수
    "urine_color": "황색",  # 소변 색
    "urine_stream": "정상",  # 소변 굵기(소변줄기)
    "urine_discomfort": False,  # 소변 후 불편감
    "urine_residual": False,  # 배뇨 후 잔뇨감
    "urine_residual_sev": 0,  # 잔뇨감 강도 0-5
    "urine_incontinence": False,  # 유뇨/요실금

    # ===========================================
    # 수면상태 (Sleep) - Page 19
    # ===========================================
    "sleep_waking_state": "개운함",  # 기상시 상쾌도
    "sleep_hours": 7,  # 수면 시간
    "sleep_depth": "깊음",  # 수면 깊이
    "insomnia_freq": 0,  # 불면 빈도 (0-5)
    "dreams": "거의 없음",  # 꿈의 빈도 및 내용
    "insomnia_onset": 0,  # 입면장애 정도 (0-5, 0=없음)
    "insomnia_maintain": 0,  # 중도각성 정도 (0-5, 0=없음)
    "insomnia_maintain_count": 0,  # 수면 중도 각성 횟수
    "insomnia_reentry": 0,  # 재입면장애 정도 (0-5, 0=없음)

    # ===========================================
    # 땀 (Sweat) - Page 19
    # ===========================================
    "sweat_amt": "보통",  # 일상 생활에서 땀 량
    "sweat_time": "주간",  # 땀나는 시간대
    "sweat_area": "전신",  # 땀나는 부위
    "sweat_feeling": "상쾌",  # 땀 흘린 뒤 느낌

    # ===========================================
    # 한열경향 (Cold/Heat Tendency) - Page 19
    # ===========================================
    "cold_heat_body": "보통",  # 인체 한열(몸이 차고 더운 정도)
    "cold_heat_distribution": "균등",  # 한열의 편재(상열하한)
    "drink_temp": "온수",  # 음료 온도 선호도
    "cold_sensitivity": 3,  # 주위 민감도 (1-5)
    "heat_sensitivity": 3,  # 더위 민감도 (1-5)
    "cold_heat_pref": "보통",  # Legacy compatibility

    # ===========================================
    # 전신상태 (General Condition) - Page 19
    # ===========================================
    "body_solidity": "단단",  # 물살/단단
    "physical_strength": "보통",  # 체력강약
    "fatigue_level": "약함",  # 피로감
    "edema": "없음",  # 부종여부
    "bruising": "정상",  # 인체 부위의 출혈/멍듦
    "condition_bad_area": [],  # 평소 컨디션이 안좋을 때 불편한 부위
    "limb_weakness": False,  # 사지 무력감

    # ===========================================
    # 피부상태 (Skin Condition) - Page 19
    # ===========================================
    "skin_trouble": False,  # 피부트러블
    "skin_dry": "정상",  # 피부 건조도
    "skin_itch": False,  # 피부 가려움

    # ===========================================
    # 얼굴 (Face) - Page 17
    # ===========================================
    "face_color": "정상",  # 얼굴 색
    "face_gloss": "정상",  # 얼굴 광택

    # ===========================================
    # 눈 (Eyes) - Page 17
    # ===========================================
    "eye_discomfort": False,  # 눈 불편감
    "eye_red": False,  # 눈 충혈
    "vision_blackout": False,  # 눈 앞이 캄캄함

    # ===========================================
    # 귀 (Ears) - Page 17
    # ===========================================
    "tinnitus_freq": 0,  # 이명(빈도) 0-5
    "tinnitus_sev": 0,  # 이명(강도) 0-5
    "hearing_sev": 0,  # 이롱(난청) 0-5

    # ===========================================
    # 구강/목 (Mouth/Throat) - Page 17-18
    # ===========================================
    "lip_color": "정상",  # 입술 색
    "lip_dry": False,  # 입술 건조
    "water_intake": "1-2L",  # 음수량
    "mouth_dry": 0,  # 입마름 정도(구건/구갈) 0-5
    "throat_dry": False,  # 인후 건조
    "mouth_bitter": False,  # 구고(입이 씀)
    "bad_breath": False,  # 구취
    "hiccup": False,  # 딸꾹질

    # ===========================================
    # 어지러움 (Dizziness) - Page 18
    # ===========================================
    "dizziness_sev": 0,  # 어지러움(두훈) 0-5

    # ===========================================
    # 뒷목/경항부 (Neck/Nape) - Page 18
    # ===========================================
    "neck_nape_freq": 0,  # 뒷목, 경항 불편감(빈도) 0-5
    "neck_nape_sev": 0,  # 뒷목, 경항 불편감(강도) 0-5

    # ===========================================
    # 흉부 (Chest) - Page 18
    # ===========================================
    "breath_sound": "정상",  # 호흡소리 크기
    "palpitation": 0,  # 흉부 두근거림 0-5
    "chest_tight_freq": 0,  # 흉부 답답함(빈도) 0-5
    "chest_tight_sev": 0,  # 흉부 답답함(강도) 0-5
    "chest_pain_freq": 0,  # 흉부 통증(빈도) 0-5
    "chest_pain_sev": 0,  # 흉부 통증(강도) 0-5
    "sighing_freq": 0,  # 한숨 빈도 0-5
    "nausea": 0,  # 구역감/구토 0-5
    "bloating": 0,  # 복만/가스 참(강도) 0-5
    "flatulence": "보통",  # 방귀

    # ===========================================
    # 기능성 소화불량 (Functional Dyspepsia) - Page 18
    # ===========================================
    "lower_abd_discomfort": 0,  # 아랫배 불편감(강도) 0-5
    "abd_pain_sev": 0,  # 전복부 통증(강도) 0-5
    "abd_pain_type": "없음",  # 복통의 양상
    "abd_tenderness": False,  # 눌렀을 때 복부 압통
    "nausea_sev": 0,  # 메스꺼움(강도) 0-5
    "belching": 0,  # 트림 0-5
    "belching_smell": "없음",  # 트림 시 냄새
    "food_stag_sev": 0,  # 체한(강도) 0-5
    "abd_muscle_tension": False,  # 복직근 긴장감
    "abd_mass": False,  # 복부 덩어리 만져짐
    "abd_pulsation": False,  # 동계
    "bowel_sound": "정상",  # 장명(장에서 나는 소리)

    # ===========================================
    # 옆구리/등/골반 (Flank/Back/Pelvis) - Page 18
    # ===========================================
    "flank_freq": 0, "flank_sev": 0,  # 옆구리 불편감
    "back_freq": 0, "back_sev": 0,  # 등 불편감
    "pelvis_freq": 0, "pelvis_sev": 0,  # 골반부 불편감

    # ===========================================
    # 어깨/팔꿈치/손,발 (Shoulder/Elbow/Hands,Feet) - Page 18
    # ===========================================
    "shoulder_freq": 0, "shoulder_sev": 0,  # 어깨 불편감
    "elbow_freq": 0, "elbow_sev": 0,  # 팔꿈치 불편감
    "hand_foot_freq": 0, "hand_foot_sev": 0,  # 손 또는 발 불편감
    "cold_hands_feet": False,  # 수족냉증(손발냉감)

    # ===========================================
    # 고관절/무릎 (Hip/Knee) - Page 18
    # ===========================================
    "leg_discomfort": 0,  # 다리 불편감 0-5
    "knee_freq": 0, "knee_sev": 0,  # 슬부 불편감

    # ===========================================
    # 정신상태 (Mental State) - Page 19
    # ===========================================
    "mental_clarity": "맑음",  # 정신상태
    "memory": "좋음",  # 기억력
    "motivation": "보통",  # 의욕
    "stress_coping": "보통",  # 스트레스 대처력
    "mood_swing": "안정",  # 감정 기복

    # ===========================================
    # 성격/성양 (Personality) - Page 19
    # ===========================================
    "personality_speed": 3,  # 성격 완급(느긋함/급함) 1-5
    "personality_soft": 3,  # 성격 강유(부드러움/강함) 1-5
    "personality_io": 3,  # 성격내외(내성적/외향적) 1-5
    "personality_static": 3,  # 성격 동정(정적/동적) 1-5

    # ===========================================
    # 감정상태 (Emotional State) - Page 19
    # ===========================================
    "voice_vol": "보통",  # 목소리크기(성음크기)
    "excitement": 3,  # 흥분정도(차분함) 1-5
    "emot_anger": 1,  # 노(화냄/평온) 1-5
    "emot_depress": 1,  # 우울(우울함) 1-5
    "emot_anxiety": 1,  # 불안 1-5
    "emot_fear": 1,  # 공(두려움/용기) 1-5
    "emot_startle": 1,  # 놀람(잘놀람/평온함) 1-5
    "emot_thought": 1,  # 생각(생각많음/적음) 1-5
    "emot_grief": 1,  # 비탄(슬픔많음/적음) 1-5

    # ===========================================
    # 맥 (Pulse Diagnosis) - Page 19
    # ===========================================
    "compound_pulse": "완맥",  # 복합맥 (질환별 규칙 적용)
    "pulse_depth": "중맥",  # 맥 부침 정도(부침)
    "pulse_width": "대맥",  # 맥 폭 정도(대세)
    "pulse_length": "장",  # 맥 길이 정도(장단)
    "pulse_smooth": "완맥",  # 맥 부드럽고 거친 정도(활삽)
    "pulse_strength": "유력",  # 세기
    "pulse_tension": "유",  # 맥 긴장도(현긴완)

    # ===========================================
    # 설 (Tongue) - Page 19
    # ===========================================
    "tongue_color": "담홍",  # 혀 색
    "tongue_size": "정상",  # 혀 크기
    "tongue_marks": False,  # 혀 흔적/치흔

    # ===========================================
    # 태 (Tongue Coat) - Page 19
    # ===========================================
    "tongue_coat_color": "백태",  # 설태 색
    "tongue_coat_thick": "박태",  # 설태 두께
    "tongue_coat_particle": "윤",  # 설태 입자크기

    # ===========================================
    # PAIN GRID (통증 부위별 빈도/강도)
    # ===========================================
    "pain_neck": [0,0], "pain_shoulder": [0,0], "pain_back": [0,0], "pain_knee": [0,0],
    "pain_hand": [0,0], "pain_elbow": [0,0], "pain_flank": [0,0], "pain_pelvis": [0,0], "pain_hip": [0,0],
    # Pain grid _f (frequency) and _i (intensity) individual keys for Streamlit widgets
    "pain_neck_f": 0, "pain_neck_i": 0,
    "pain_shoulder_f": 0, "pain_shoulder_i": 0,
    "pain_back_f": 0, "pain_back_i": 0,
    "pain_knee_f": 0, "pain_knee_i": 0,
    "pain_hand_f": 0, "pain_hand_i": 0,
    "pain_elbow_f": 0, "pain_elbow_i": 0,
    "pain_flank_f": 0, "pain_flank_i": 0,
    "pain_pelvis_f": 0, "pain_pelvis_i": 0,
    "pain_hip_f": 0, "pain_hip_i": 0,

    # ===========================================
    # 한의사 진찰 및 검사소견 (TKM Examinations) - Page 17
    # ===========================================
    "exam_lung_sound": None,  # 호흡음(폐음) 진찰
    "exam_throat": None,  # 인후부 진찰
    "exam_tonsil": None,  # 편도진찰
    "exams": [],  # X-ray, 이경, 비경, 혈액검사, CT, MRI, 내시경
    "exam_xray": None,  # X-ray
    "exam_otoscope": None,  # 이경
    "exam_rhinoscope": None,  # 비경
    "exam_blood_test": None,  # 혈액검사
    "exam_ct": None,  # CT
    "exam_mri": None,  # MRI
    "exam_endoscopy": None,  # 내시경

    # ===========================================
    # DIAGNOSIS & SPECIFICS (진단 및 특이사항)
    # ===========================================
    "disease": "감기/급성상기도감염",
    "pattern_idx": 0,
    
    # Cold Specifics (감기 특이사항) - Page 15, 39-40
    "fever_sev": 1, "chills_sev": 1, "snot_sev": 1, "cough_sev": 1,
    "phlegm_amt": 0,  # 가래 양
    "phlegm_color": "없음",  # 가래 색
    "sweating": False,  # 무한/유한
    "cold_symptoms_spec": [],
    
    # Page 39-40: 감기 가상환자 주증정보 필수항목
    "cold_chief_type": [],  # 감기주소증 유형 (최소 1개 이상)
    "cold_onset_specific": "",  # O/S 구체적 날로 제시 (예 1일 전, 1주일 전 등)
    "cold_background_story": "",  # 경과: 감기 걸리게 된 배경, 당시 상황 (AI 자체 생성)
    "cold_sweating_check": False,  # 감기시 땀 유무 (검증 항목)
    "cold_dyspnea": False,  # 숨이 가쁨 (동반증상)
    "snot_color": "없음",  # 콧물 색 (콧물 있을 때만)
    "smell_reduction": 0,  # 후각감퇴 (코막힘 있을 때만) 0-5
    "alternating_chills_fever": 0,  # 한열왕래 0-5 (Page 40: 배제규칙 적용)
    "body_ache_cold": False,  # 몸살 (신체통, 근육통, 관절통)
    "body_heaviness_cold": False,  # 신중 (몸이 무거움)
    "headache_cold": False,  # 두통
    "neck_pain_cold": False,  # 경항통
    "sore_throat": False,  # 인후통
    
    # Page 40: 진찰 및 검사소견 (감기)
    "exam_stethoscope": "정상",  # 청진기를 이용한 호흡음 진찰소견
    "exam_throat_visual": "정상",  # 한의사의 망진/촉진을 통한 인후부 진찰소견
    "exam_tongue_depressor": "정상",  # 설압자를 이용한 편도 진찰소견
    "exam_rhinoscope_finding": "정상",  # 비경을 이용한 진찰소견
    
    # Rhinitis Specifics (비염 특이사항)
    "sneeze_sev": 1, "nose_block_sev": 1, "nose_itch_sev": 1, 
    "snot_type": "청수양 (淸水樣) - 맑은 콧물",
    
    # Back Pain Specifics (요통 특이사항) - Page 15-16
    "pain_sev": 1,
    "pain_nature": [],
    "back_pain_cause": "None",  # 발병 요인
    "back_pain_timing": "Constant",  # 통증 시간대
    "back_radiation": False,  # 다리로 방사
    
    # Dyspepsia Specifics (소화불량 특이사항) - Page 16
    "dyspepsia_spec": [],
    "acid_reflux": False,  # 신물
    "bitter_taste": False,  # 구고
    "foul_belch": False,  # 부패취
    "epigastric_pain": 0,  # 명치 통증 0-5
    "cold_limbs_dyspepsia": False,  # 수족냉증
    
    # ===========================================
    # 추가증상 및 동반질환 (Pages 24-25)
    # Additional symptoms for realistic patient generation
    # ===========================================
    "additional_symptoms": [],  # 한의원 다빈도 증상 중 무작위 1-2개 추가
    "additional_comorbidities": [],  # 다빈도 동반질환 중 무작위 0-2개 추가
    
    # ===========================================
    # PDF Export (시나리오 내보내기)
    # ===========================================
    "scenario_generated": False,  # 시나리오 생성 여부
    "generated_summary": "",  # 생성된 요약
    "generated_scenario": "",  # 생성된 시나리오
    "generated_patient_info": {},  # 환자 기본 정보
}
