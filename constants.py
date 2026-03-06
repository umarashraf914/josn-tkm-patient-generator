"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Constants & Clinical Data
Based on Clinical Guidelines Pages 21-25, 39-40
═══════════════════════════════════════════════════════════════════════════════
"""

# Re-export clinical lists for backward compatibility
from clinical_lists import (
    FREQUENT_TKM_SYMPTOMS,
    FREQUENT_COMORBIDITIES,
    PAST_COLD_PROBLEM_AREAS,
    AGGRAVATING_FACTORS,
    RELIEVING_FACTORS,
    get_random_additional_symptoms,
    get_random_comorbidities,
    get_all_symptom_options,
)

# Re-export cold constants for backward compatibility
from cold_constants import (
    COLD_CHIEF_TYPES,
    COLD_PATIENT_EXPRESSIONS,
    COLD_EXAM_OPTIONS,
)

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
