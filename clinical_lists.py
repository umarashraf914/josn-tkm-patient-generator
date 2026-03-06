"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Clinical Symptom & Comorbidity Lists
Based on Clinical Guidelines Pages 24-25
═══════════════════════════════════════════════════════════════════════════════
"""

import random


# ===========================================
# 한의원 다빈도 증상 (Frequent TKM Symptoms - Pages 24-25)
# ===========================================
FREQUENT_TKM_SYMPTOMS = {
    "소화기계": [
        "복통 (腹痛)",
        "식욕부진 (食慾不振)",
        "오심/구토 (惡心/嘔吐)",
    ],
    "호흡기계": [
        "기침 (咳嗽)",
        "가래 (痰)",
        "호흡곤란 (呼吸困難)"
    ],
    "근골격계": [
        "관절통 (關節痛)",
        "근육통 (筋肉痛)",
        "요통 (腰痛)"
    ],
    "신경정신계": [
        "두통 (頭痛)",
        "어지럼증 (眩暈)",
        "불면 (不眠)"
    ],
    "감각기계": [
        "이명 (耳鳴)",
        "안구건조 (眼球乾燥)",
        "시력저하 (視力低下)"
    ],
    "피부계": [
        "피부건조 (皮膚乾燥)",
        "가려움증 (瘙痒症)",
        "두드러기 (蕁麻疹)"
    ],
    "통증계": [
        "경항통 (頸項痛)",
        "견비통 (肩臂痛)",
        "슬통 (膝痛)"
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
# HELPER FUNCTIONS
# ===========================================

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
    exclude_menstrual = False
    if sex == "남":
        exclude_menstrual = True
    if age is not None and age < 12:
        exclude_menstrual = True
    
    all_symptoms = []
    for category, symptoms in FREQUENT_TKM_SYMPTOMS.items():
        if category != exclude_category:
            for symptom in symptoms:
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
