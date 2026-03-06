"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Constants & Clinical Data
Based on Clinical Guidelines Pages 21-25, 39-40
═══════════════════════════════════════════════════════════════════════════════
"""

import random

# ===========================================
# KCD CODE MAPPINGS (Pages 21-22)
# 대표질병과 KCD 코드 매핑
# ===========================================
KCD_CODES = {
    "감기": {
        "main_code": "J06",
        "sub_codes": {
            "J06.0": "급성 후두인두염 (Acute laryngopharyngitis)",
            "J06.8": "여러부위의 기타 급성 상기도감염 (Other acute upper respiratory infections of multiple sites)",
            "J06.9": "상세불명의 급성 상기도감염 (Acute upper respiratory infection unspecified)"
        },
        "exclusions": [
            "J22 - 급성호흡기감염 NOS (Acute respiratory infection NOS)",
            "J09, J10.1 - 인플루엔자바이러스 확인됨 (Influenza virus identified)",
            "J11.1 - 인플루엔자바이러스 미확인 (Influenza virus not identified)",
            "J98.7 - 호흡기감염 NOS (Respiratory infection NOS)"
        ]
    },
    "알레르기비염": {
        "main_code": "J30",
        "sub_codes": {
            "J30.0": "혈관운동성비염 (Vasomotor rhinitis)",
            "J30.1": "화분에 의한 알레르기비염 (Allergic rhinitis due to pollen, Hay fever, Pollinosis)",
            "J30.2": "기타 계절성 알레르기비염 (Other seasonal allergic rhinitis)",
            "J30.3": "기타 알레르기비염 (Other allergic rhinitis)",
            "J30.4": "다년성 알레르기비염/상세불명 (Perennial allergic rhinitis, unspecified)"
        },
        "exclusions": [
            "J45.0- 천식을 동반한 알레르기비염 (Allergic rhinitis with asthma)"
        ]
    },
    "요통": {
        "main_code": "M54",
        "sub_codes": {
            "M54.5": "등통증 (Dorsalgia)",
            "M54.50": "척추의 여러 부위 (Low back pain, multiple sites in spine)",
            "M54.55": "흉요추부 (Low back pain, thoracolumbar region)",
            "M54.56": "요추부 (Low back pain, lumbar region)",
            "M54.57": "요천부 (Low back pain, lumbosacral region)",
            "M54.58": "천추 및 천미추부 (Low back pain, sacral and sacrococcygeal region)",
            "M54.59": "상세불명의 부위 (Low back pain, site unspecified)"
        },
        "exclusions": [
            "M51.2 - 추간판 전위로 인한 요통 (Lumbago due to intervertebral disc displacement)",
            "M54.4 - 좌골신경통을 동반한 요통 (Lumbago with sciatica)"
        ]
    },
    "기능성소화불량": {
        "main_code": "K30",
        "sub_codes": {
            "K30": "기능성소화불량 (Functional dyspepsia)"
        },
        "exclusions": [
            "R10.19 - 상세불명 (NOS)",
            "F45.3 - 신경성/심인성 (Nervous, Neurotic, Psychogenic)",
            "R12 - 속쓰림 (Heartburn)"
        ]
    }
}

# ===========================================
# PATTERN CLASSIFICATION (Page 23)
# 질병별 변증유형 분류
# ===========================================
DISEASE_PATTERNS = {
    "감기": {
        "kcd_code": "J06",
        "patterns": [
            {"id": "Cold_WC", "name": "풍한형 (風寒型)", "prescriptions": ["행소산", "삼소음", "소청룡탕"]},
            {"id": "Cold_WH", "name": "풍열형 (風熱型)", "prescriptions": ["은교산", "상국음", "연교패독산"]}
        ],
        "note": "상기도 감염의 경우 통상 급성임을 감안하여 풍한형과 풍열형 변증을 선정 (Page 23)"
    },
    "알레르기비염": {
        "kcd_code": "J30",
        "patterns": [
            # Prof. Lee feedback: Use prescription names as pattern group names for 알레르기비염
            # (Since there's only 1 pattern group, use prescriptions directly as groups)
            {"id": "R_WBG", "name": "월비가반하탕", "prescriptions": ["월비가반하탕"]},
            {"id": "R_SGM", "name": "사간마황탕", "prescriptions": ["사간마황탕"]},
            {"id": "R_SCY", "name": "소청룡탕", "prescriptions": ["소청룡탕"]},
            {"id": "R_YGG", "name": "영감강미신하인탕", "prescriptions": ["영감강미신하인탕"]},
            {"id": "R_MHB", "name": "마황부자세신탕", "prescriptions": ["마황부자세신탕"]}
        ],
        "note": "알레르기 비염 - 처방명을 변증그룹명으로 사용 (Prof. Lee feedback)"
    },
    "요통": {
        "kcd_code": "M54",
        "patterns": [
            # Page 23: 질병별 변증유형 분류 - 요통 (Original prescriptions - correct)
            {"id": "BP_Cold", "name": "한증형 (寒證型)", "prescriptions": ["오적산"]},
            {"id": "BP_Heat", "name": "열증형 (熱證型)", "prescriptions": ["이묘창백산", "칠묘창백산"]},
            {"id": "BP_QiDef", "name": "기허형 (氣虛型)", "prescriptions": ["두충환", "사군자탕"]},
            {"id": "BP_YangDef", "name": "양허형 (陽虛型)", "prescriptions": ["팔미지황원"]},
            {"id": "BP_YinDef", "name": "음허형 (陰虛型)", "prescriptions": ["육미지황원"]},
            {"id": "BP_FoodStag", "name": "식적형 (食積型)", "prescriptions": ["소적건비환"]},
            {"id": "BP_Phlegm", "name": "담음형 (痰飮型)", "prescriptions": ["이진탕", "궁하탕"]},
            {"id": "BP_QiStag", "name": "기체형 (氣滯型)", "prescriptions": ["칠기탕", "소간해울탕"]},
            {"id": "BP_BloodStasis", "name": "어혈형 (瘀血型)", "prescriptions": ["서근산", "독활탕"]}
        ],
        "note": "요통 - 질병별 변증유형 분류 (Page 23)"
    },
    "기능성소화불량": {
        "kcd_code": "K30",
        "patterns": [
            # Page 23: 질병별 변증유형 분류 - 기능성소화불량 (Professor Lee's corrected prescriptions)
            {"id": "DY_Cold", "name": "한증형 (寒證型)", "prescriptions": ["이중탕", "안중산"]},
            {"id": "DY_Heat", "name": "열증형 (熱證型)", "prescriptions": ["황련해독탕", "반하사심탕"]},
            {"id": "DY_QiDef", "name": "기허형 (氣虛型)", "prescriptions": ["사군자탕", "육군자탕"]},
            {"id": "DY_YangDef", "name": "양허형 (陽虛型)", "prescriptions": ["사역탕"]},
            {"id": "DY_YinDef", "name": "음허형 (陰虛型)", "prescriptions": ["익위탕", "마자인환"]},
            {"id": "DY_FoodStag", "name": "식적형 (食積型)", "prescriptions": ["내소화중탕", "지실소비환"]},
            {"id": "DY_Phlegm", "name": "담음형 (痰飮型)", "prescriptions": ["이진탕", "궁하탕", "평위산"]},
            {"id": "DY_QiStag", "name": "기체형 (氣滯型)", "prescriptions": ["소요산", "시호소간탕"]},
            {"id": "DY_BloodStasis", "name": "어혈형 (瘀血型)", "prescriptions": ["단삼음", "혈부축어탕"]}
        ],
        "note": "기능성소화불량 - 질병별 변증유형 분류 (Professor Lee's corrected prescriptions)"
    }
}

# ===========================================
# 한의원 다빈도 증상 및 병증 (Pages 24-25)
# Frequent TKM Symptoms & Conditions for Realistic Patient Generation
# 가상환자 현실성 향상을 위해 1-2개 무작위 추가
# ===========================================
FREQUENT_TKM_SYMPTOMS = {
    "통증계": [
        "두통 (頭痛)",
        "경항통 (頸項痛)",
        "견통 (肩痛)",
        "요통 (腰痛)",
        "슬통 (膝痛)",
        "족저통 (足底痛)",
        "관절통 (關節痛)"
    ],
    "소화기계": [
        "소화불량 (消化不良)",
        "식욕부진 (食欲不振)",
        "오심 (惡心)",
        "복통 (腹痛)",
        "변비 (便秘)",
        "설사 (泄瀉)"
    ],
    "호흡기계": [
        "기침 (咳嗽)",
        "천식 (喘息)",
        "인후통 (咽喉痛)",
        "비염 (鼻炎)"
    ],
    "신경정신계": [
        "불면 (不眠)",
        "두훈 (頭暈/어지러움)",
        "피로 (疲勞)",
        "건망 (健忘)",
        "심계 (心悸/두근거림)",
        "불안 (不安)",
        "우울 (憂鬱)"
    ],
    "피부계": [
        "피부가려움 (皮膚瘙癢)",
        "피부건조 (皮膚乾燥)",
        "두드러기 (蕁麻疹)"
    ],
    "비뇨생식기계": [
        "빈뇨 (頻尿)",
        "야간뇨 (夜間尿)",
        "월경통 (月經痛)",
        "월경불순 (月經不順)"
    ],
    "전신증상": [
        "수족냉증 (手足冷症)",
        "자한 (自汗/주간 식은땀)",
        "도한 (盜汗/야간 식은땀)",
        "부종 (浮腫)",
        "권태 (倦怠)"
    ]
}

# 다빈도 동반질환/기왕력 (Frequent Comorbidities - Pages 24-25)
FREQUENT_COMORBIDITIES = [
    "고혈압 (高血壓)",
    "당뇨 (糖尿)",
    "이상지질혈증 (異常脂質血症)",
    "갑상선질환 (甲狀腺疾患)",
    "위염/역류성식도염 (胃炎/逆流性食道炎)",
    "골다공증 (骨多孔症)",
    "관절염 (關節炎)",
    "전립선비대 (前立腺肥大)",
    "빈혈 (貧血)"
]

# 과거 감기증상 시 문제 부위 (Page 17)
PAST_COLD_PROBLEM_AREAS = [
    "목/인후부 (咽喉部)",
    "코 (鼻部)",
    "기관지/폐 (氣管支/肺部)",
    "귀 (耳部)",
    "두통 (頭痛)",
    "근육통 (筋肉痛)"
]

# 악화요인 (Aggravating Factors) - Page 17
AGGRAVATING_FACTORS = [
    "과로 (過勞)",
    "수면부족 (睡眠不足)",
    "스트레스 (Stress)",
    "찬바람/냉기 (冷氣)",
    "습한환경 (濕環境)",
    "기름진음식 (油膩食)",
    "음주 (飮酒)",
    "흡연 (吸煙)",
    "장시간앉기 (久坐)",
    "무거운짐 (重物)"
]

# 완화요인 (Relieving Factors) - Page 17
RELIEVING_FACTORS = [
    "휴식 (休息)",
    "수면 (睡眠)",
    "따뜻하게함 (溫暖)",
    "스트레칭 (Stretching)",
    "온찜질 (溫熱敷)",
    "안정 (安靜)",
    "식이조절 (食餌調節)"
]

# ===========================================
# PAGE 39: 감기주소증 유형 (Cold Chief Complaint Types)
# 최소 1개 이상 생성 필수
# [교수님 피드백] 목감기(인후통), 몸살(신체통) 포함 필수
# ===========================================
COLD_CHIEF_TYPES = [
    "발열증상 위주",
    "오한증상 위주",
    "콧물 위주",
    "코막힘 위주",
    "인후통 위주 (목감기)",  # [교수님 피드백] 목감기 명시
    "재채기 위주",
    "기침증상 위주",
    "가래 위주",
    "몸살 위주 (신체통/근육통/관절통)",  # [교수님 피드백] 몸살 명시
    "신중 위주 (몸이 무거움)",
    "두통/경항통 위주"
]

# Page 39: 감기 가상환자 표현 (Natural Language Symptoms)
COLD_PATIENT_EXPRESSIONS = {
    "주소": [
        "콧물이 계속 나요",
        "코가 꽉 막혔어요",
        "목이 아파요",
        "목이 따끔거려요",
        "목이 부었어요",
        "침 삼킬 때 아파요",
        "재채기가 자꾸 나와요",
        "기침을 해요",
        "가래가 끊어요",
        "가래가 껴요",
        "열이 나요",
        "몸에 열감이 있어요",
        "몸이 으슬으슬 추워요",
        "머리가 아파요",
        "머리가 띵해요",
        "온몸이 수셔요",
        "몸살 기운이 있어요",
        "기운이 하나도 없어요",
        "목소리가 쉬었어요"
    ],
    "검증": [
        "어지러워요",
        "눈 앞이 흐릿해져요",
        "머리에 뭘 씌운 것 같아요",
        "냄새를 못말아요",
        "정신이 흐릿해요",
        "약 기운 때문인지 자꾸 졸려서 일하기 힘들어요 (양약 부작용 호소)"
    ]
}

# Page 40: 감기 진찰소견 옵션
COLD_EXAM_OPTIONS = {
    "stethoscope": ["정상", "수포음", "천명음", "감소"],
    "throat_visual": ["정상", "발적", "부종", "삼출물"],
    "tongue_depressor": ["정상", "편도비대", "삼출물", "염증"],
    "rhinoscope": ["정상", "충혈", "분비물", "폴립"]
}


# ===========================================
# HELPER FUNCTIONS
# ===========================================

def get_pattern_info(disease_key, pattern_idx):
    """Get pattern details including name and prescriptions."""
    if disease_key in DISEASE_PATTERNS:
        patterns = DISEASE_PATTERNS[disease_key]["patterns"]
        if 0 <= pattern_idx < len(patterns):
            return patterns[pattern_idx]
    return None


def get_kcd_info(disease_key):
    """Get KCD code information for a disease."""
    return KCD_CODES.get(disease_key, None)


def get_random_additional_symptoms(exclude_category=None, count=None, sex=None, age=None):
    """
    Get 1-2 random additional symptoms from the frequent TKM symptoms list.
    Used to add realistic comorbidity/symptoms to generated patients (Pages 24-25).
    
    Args:
        exclude_category: Category to exclude (e.g., "통증계" for back pain patients)
        count: Number of symptoms to add (default: random 1-2)
        sex: Patient's sex ("남" or "여") - used to exclude menstrual symptoms for males
        age: Patient's age - used to exclude menstrual symptoms for young children
    
    Returns:
        List of additional symptom strings
    """
    if count is None:
        count = random.randint(1, 2)
    
    # Menstrual symptoms to exclude for male patients and young children (< 12)
    female_only_symptoms = [
        "월경통 (月經痛)",
        "월경불순 (月經不順)"
    ]
    
    # Determine if menstrual symptoms should be excluded
    # - Male patients: always exclude
    # - Young children (under 12): exclude regardless of sex
    exclude_menstrual = False
    if sex == "남":
        exclude_menstrual = True
    if age is not None and age < 12:
        exclude_menstrual = True
    
    all_symptoms = []
    for category, symptoms in FREQUENT_TKM_SYMPTOMS.items():
        if category != exclude_category:
            for symptom in symptoms:
                # Exclude menstrual symptoms if applicable
                if exclude_menstrual and symptom in female_only_symptoms:
                    continue
                all_symptoms.append(symptom)
    
    if len(all_symptoms) < count:
        count = len(all_symptoms)
    
    return random.sample(all_symptoms, count)


def get_random_comorbidities(count=None):
    """
    Get random comorbidities from the frequent comorbidity list.
    
    Args:
        count: Number of comorbidities (default: random 0-2)
    
    Returns:
        List of comorbidity strings
    """
    if count is None:
        count = random.randint(0, 2)
    
    if count == 0:
        return []
    
    return random.sample(FREQUENT_COMORBIDITIES, min(count, len(FREQUENT_COMORBIDITIES)))


def get_all_symptom_options():
    """Get all symptoms flattened into a single list."""
    all_symptoms = []
    for category, symptoms in FREQUENT_TKM_SYMPTOMS.items():
        all_symptoms.extend(symptoms)
    return all_symptoms
