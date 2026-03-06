# data_mappings.py

# ==========================================
# 1. RESPIRATORY & RHINITIS (From Prompt 1)
# Updated with exact Korean descriptions from Pages 27-30
# ==========================================
PART_1 = {
    # ---------------------------------------------------------
    # COMMON COLD VARIABLES (Source: Pages 27, 57-60)
    # Weights: [Cold_WC (Wind-Cold 풍한), Cold_WH (Wind-Heat 풍열), Cold_WD (Wind-Dryness 풍조)]
    # Descriptions updated from Page 27 table
    # ---------------------------------------------------------
    "fever_sev": {
        # Page 27: 발열 정량 표현
        1: {"desc": "없음, 35도 이하. 발열 증상이 전혀 없음 (저체온)", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.00, "Cold_WD": 0.30}},
        2: {"desc": "발열 증상이 전혀 없음 (정상체온)", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.00, "Cold_WD": 0.50}},
        3: {"desc": "뚜렷한 열감이 느껴지며, 이로 인해 피로감이나 불편감이 동반됨 (약 37.4°C ~ 37.9°C)", "weights": {"Cold_WC": 0.08, "Cold_WH": 0.25, "Cold_WD": 0.15}},
        4: {"desc": "몸이 뜨겁다고 느끼고, 이로 인한 전신 근육통이나 두통이 동반됨. 활동이 힘들어 눕고 싶다는 생각이 듦 (약 38°C ~ 39.9°C)", "weights": {"Cold_WC": 0.08, "Cold_WH": 0.50, "Cold_WD": 0.05}},
        5: {"desc": "몸이 불덩이처럼 뜨겁고, 어지러움이나 혼미함을 동반할 수 있으며, 일상생활이 불가능한 상태 (약 40°C 이상)", "weights": {"Cold_WC": 0.08, "Cold_WH": 0.30, "Cold_WD": 0.00}}
    },
    "chills_sev": {
        # Page 27: 오한 정량 표현
        1: {"desc": "오한 증상이 전혀 없음", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.40, "Cold_WD": 0.40}},
        2: {"desc": "경미하게 춥다고 느껴져, 옷을 껴입거나 이불을 덮으려고 함. 가벼운 몸살 기운이 동반될 수 있음", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40, "Cold_WD": 0.40}},
        3: {"desc": "뚜렷하게 춥다고 느껴져, 옷을 껴입거나 이불을 덮어야 함. 몸살 기운이 동반될 수 있음", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.15, "Cold_WD": 0.15}},
        4: {"desc": "심함, 열이 나는데도 불구하고, 몸이 떨릴 정도로 춥다고 느껴짐", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.00, "Cold_WD": 0.05}},
        5: {"desc": "매우 심함, 따뜻한 환경에서도 극심한 추위를 느낌. 이가 부딪히기도 하며, 일상적인 활동이 불가능한 상태", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.00, "Cold_WD": 0.00}}
    },
    "snot_sev": {
        # Page 27-28: 콧물량 정량 표현
        1: {"desc": "없음", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.00, "Cold_WD": 0.00}},
        2: {"desc": "경미, 콧물이 약간 흐르지만, 휴지가 거의 필요 없거나 가끔 한두 번 닦아내는 정도", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.15, "Cold_WD": 0.10}},
        3: {"desc": "중등도, 콧물이 계속 흘러", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20, "Cold_WD": 0.15}},
        4: {"desc": "휴지를 자주 사용하게 되며, 코를 푸는 횟수가 늘어남. 심함, 콧물이 멈추지 않고 계속 흘러내려 휴지를 달고 살아야 하며, 코를 풀어도 금방 다시 참", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.05, "Cold_WD": 0.05}},
        5: {"desc": "매우 심함, 콧물이 수도꼭지처럼 쏟아져 휴지로 감당하기 어려울 정도. 코 주변 피부가 헐거나 집중이 불가능함", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.03, "Cold_WD": 0.00}}
    },
    "snot_color": {
        # Page 27-28: 콧물색 정량 표현
        1: {"desc": "투명 콧물이 나옴", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.15, "Cold_WD": 0.10}},
        2: {"desc": "콧물이 점차 끈적해지기 시작하며, 흰색의 콧물이 나옴", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.20, "Cold_WD": 0.10}},
        3: {"desc": "콧물이 누렇고 끈적하게 변함", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.65, "Cold_WD": 0.15}}
    },
    "cough_sev": {
        1: {"desc": "기침 안함", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.10, "Cold_WD": 0.00}},
        2: {"desc": "가끔 기침 (간헐적)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10, "Cold_WD": 0.05}},
        3: {"desc": "자주 기침함 (빈번함)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10, "Cold_WD": 0.05}},
        4: {"desc": "하루종일 기침 (지속적)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10, "Cold_WD": 0.05}},
        5: {"desc": "발작적인 기침 (만성적/발작적)", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.60, "Cold_WD": 0.10}}
    },
    "phlegm_amt": {
        1: {"desc": "가래 없음", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.05, "Cold_WD": 0.00}},
        2: {"desc": "마른 가래 (잘 안나옴)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20, "Cold_WD": 0.05}},
        3: {"desc": "소량 (뱉으면 조금 나옴)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.25, "Cold_WD": 0.10}},
        4: {"desc": "다량 (자주 뱉어냄)", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10, "Cold_WD": 0.05}},
        5: {"desc": "매우 많음 (계속 생김)", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.10, "Cold_WD": 0.00}}
    },
    "phlegm_color": {
        1: {"desc": "맑은 가래", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.00, "Cold_WD": 0.00}},
        2: {"desc": "끈적한 흰 가래", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.10, "Cold_WD": 0.05}},
        3: {"desc": "누런 가래", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.15, "Cold_WD": 0.05}},
        4: {"desc": "찐득한 누런/녹색 가래", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.75, "Cold_WD": 0.10}}
    },
    
    # Page 27: 한열왕래 (Alternating Chills and Fever)
    "alternating_chills_fever": {
        1: {"desc": "없음, 오한과 발열이 번갈아 나타나는 증상은 없음", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50, "Cold_WD": 0.50}},
        2: {"desc": "뚜렷한 오한(추위)이 느껴져 옷을 껴입고 싶다가, 잠시 후에는 뚜렷한 발열(더위)이 느껴져 답답해지는 증상이 번갈아 나타남", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30, "Cold_WD": 0.30}},
        3: {"desc": "몸이 으슬으슬 춥다가, 잠시 후에는 덥다고 느끼지는 등, 체온의 조절이 불안정한 불편감이 있음", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15, "Cold_WD": 0.15}},
        5: {"desc": "몸이 떨릴 정도의 오한이 명확하게 나타난 후, 땀이 날 정도의 뚜렷한 발열이 이어지는 증상이 반복됨. 일상 활동에 지장을 줌", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05, "Cold_WD": 0.05}}
    },

    # ---------------------------------------------------------
    # RHINITIS VARIABLES (Source: Pages 27-28, 93-95)
    # Updated with Page 28 descriptions
    # ---------------------------------------------------------
    "rhinitis_sneeze": {
        1: {"desc": "재채기 안함", "weights": {"R_Fluid": 0.00}},
        2: {"desc": "어쩌다 한두 번 (간헐적)", "weights": {"R_Fluid": 0.20}},
        3: {"desc": "재채기를 자주 함 (빈번함)", "weights": {"R_Fluid": 0.35}},
        4: {"desc": "재채기를 매일 함 (지속적)", "weights": {"R_Fluid": 0.30}},
        5: {"desc": "재채기 발작 수준 (만성적)", "weights": {"R_Fluid": 0.15}}
    },
    "rhinitis_block": {
        # Page 28: 코막힘 정량 표현
        1: {"desc": "없음, 코막힘이 전혀 없음. 코로 숨쉬기가 매우 편안함", "weights": {"R_Fluid": 0.00}},
        2: {"desc": "코막힘이 약간 있으나 코로 숨쉬기 편함", "weights": {"R_Fluid": 0.15}},
        3: {"desc": "코막힘이 있고 숨쉬기 약간 불편함", "weights": {"R_Fluid": 0.35}},
        4: {"desc": "코막힘이 분명하게 느껴지고 숨쉬기 불편함", "weights": {"R_Fluid": 0.35}},
        5: {"desc": "양쪽 코가 심하게 막혀 코로 숨쉬기가 매우 힘듦", "weights": {"R_Fluid": 0.15}}
    },
    "rhinitis_itch": {
        1: {"desc": "코 가려움 없음", "weights": {"R_Fluid": 0.00}},
        2: {"desc": "약간 가려움 (무시 가능)", "weights": {"R_Fluid": 0.15}},
        3: {"desc": "자주 비빔 (신경 쓰임)", "weights": {"R_Fluid": 0.35}},
        4: {"desc": "심하게 가려움 (일상 방해)", "weights": {"R_Fluid": 0.35}},
        5: {"desc": "매우 심함 (상처/염증)", "weights": {"R_Fluid": 0.15}}
    },
    "rhinitis_snot_sev": {
        1: {"desc": "콧물이 없음", "weights": {"R_Fluid": 0.00}},
        2: {"desc": "콧물 조금 흐름 (경미)", "weights": {"R_Fluid": 0.15}},
        3: {"desc": "콧물이 줄줄 (중등도)", "weights": {"R_Fluid": 0.35}},
        4: {"desc": "쉼 없이 흐름 (심함)", "weights": {"R_Fluid": 0.35}},
        5: {"desc": "감당 불가 (매우 심함)", "weights": {"R_Fluid": 0.15}}
    },
    "rhinitis_snot_type": {
        1: {"desc": "맑고 투명한 콧물 (청수양 淸水樣)", "weights": {"R_Fluid": 0.60}},
        2: {"desc": "약간 끈적하고 흰 콧물 (백점액 白粘)", "weights": {"R_Fluid": 0.30}},
        3: {"desc": "누렇고 진한 콧물 (황농성 黃膿)", "weights": {"R_Fluid": 0.10}}
    },
    
    # Page 28: 후각감퇴 (Smell Reduction)
    "smell_reduction": {
        1: {"desc": "후각에 문제 없음", "weights": {"R_Fluid": 0.30}},
        2: {"desc": "후각이 감퇴되었지만, 냄새를 대부분 맡을 수 있음", "weights": {"R_Fluid": 0.30}},
        3: {"desc": "후각이 감퇴되었지만, 냄새를 맡기도 하고 못맡기도 함. 강열한 냄새는 맡을 수 있음", "weights": {"R_Fluid": 0.20}},
        4: {"desc": "후각이 감퇴됨. 냄새를 전혀 맡지 못함", "weights": {"R_Fluid": 0.15}},
        5: {"desc": "후각이 감퇴됨. 냄새를 전혀 맡지 못함 (완전 후각 상실)", "weights": {"R_Fluid": 0.05}}
    }
}

# ==========================================
# 2. INTERNAL & EXCRETION (From Prompt 2)
# Updated with exact Korean descriptions from Pages 31-32
# ==========================================
PART_2 = {
    # ---------------------------------------------------------
    # Page 31: 1일 식사횟수 (Daily Meal Frequency)
    # ---------------------------------------------------------
    "diet_freq": {
        1: {"desc": "하루 식사 횟수가 1회입니다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        2: {"desc": "하루 식사 횟수가 2회입니다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "하루 식사 횟수가 3회입니다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "하루 식사 횟수가 4회입니다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        5: {"desc": "하루 식사 횟수가 5회 이상이며, 소식(小食)으로 조금씩 자주 먹는 편입니다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}} 
    },
    # ---------------------------------------------------------
    # Page 31: 식사규칙성 (Meal Regularity)
    # ---------------------------------------------------------
    "diet_regular": {
        1: {"desc": "매우 규칙적, 거의 정해진 시간에 규칙적으로 식사함.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        2: {"desc": "규칙적, 거의 정해진 시간에 규칙적으로 식사함.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        3: {"desc": "왔다갔다 함. 식사 시간이 규칙적이다가 불규칙적이다가 함.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "불규칙, 주로 아침을 거르고 점심, 저녁에 과식하는 경향.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        5: {"desc": "매우 불규칙, 식사 시간이 매일 다르고 폭식과 결식을 반복함.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    "diet_amt": {
        1: {"desc": "매우 적음 (<1공기)", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        2: {"desc": "적은 편 (1-2공기)", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        3: {"desc": "보통 (3공기)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "많음 (4-5공기/과식)", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        5: {"desc": "매우 많음 (>5공기/폭식)", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}
    },
    "digestion": {
        1: {"desc": "매우 좋음 (속이 편안함)", "weights": {"Cold_WC": 0.26, "Cold_WH": 0.26}},
        2: {"desc": "좋은 편", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        3: {"desc": "속이 자주 더부룩함", "weights": {"Cold_WC": 0.26, "Cold_WH": 0.26}},
        4: {"desc": "거의 매일 속이 불편함", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        5: {"desc": "만성적인 소화불량", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.00}}
    },
    # ---------------------------------------------------------
    # Page 31: 입맛/식욕 (Appetite) - 정량 표현 from guideline
    # ---------------------------------------------------------
    "appetite": {
        1: {"desc": "식욕 없음, 음식에 대한 생각이나 욕구 자체가 전혀 없는 상태.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        2: {"desc": "입맛 저하, 배는 고픈 것을 느끼지만 특정 음식이 당기거나 '먹고 싶다'는 적극적인 욕구가 없는 상태.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        3: {"desc": "보통, 식사 시간이 되면 자연스럽게 배고픔을 느끼고, 음식을 맛있게 섭취함.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "식욕 좋음, 항상 입맛이 좋은 편.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "식욕 항진, 식욕이 과도하게 왕성하여 스스로 조절하는 데 어려움을 겪으며, 포만감을 느껴도 계속 먹고 싶은 충동이 있음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # ---------------------------------------------------------
    # Page 31: 의욕 저하 (Motivation/Enthusiasm) - 정량 표현 from guideline
    # ---------------------------------------------------------
    "motivation_level": {
        1: {"desc": "매우 높은 편, 일상적인 활동이나 업무를 긍정적이고 능동적으로 수행하며, 의욕이 넘침.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        2: {"desc": "높은 편, 일상적인 활동이나 업무를 긍정적이고 능동적으로 수행하며, 대체로 의욕이 있는 편.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        3: {"desc": "보통, 해야 할 일은 수행하지만, 그 이상의 적극적인 의욕이나 열정은 부족한 일반적인 상태.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "저하, 매사에 의욕이 없고, 간단한 일상 활동조차 귀찮고 힘들게 느끼며, 소극적이거나 회피하는 경향이 생김.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        5: {"desc": "매우 저하, 의욕이 완전히 상실되어, 식사, 수면 등 기본적인 활동을 포함한 모든 일에 흥미나 관심이 없는 무기력한 상태.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },

    # ---------------------------------------------------------
    # STOOL - Pages 31
    # ---------------------------------------------------------
    "stool_freq": {
        1: {"desc": "매우 적음 (주 2회 이하)", "weights": {"Cold_WC": 0.04, "Cold_WH": 0.16}},
        2: {"desc": "다소 적음 (주 3-4회)", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.30}},
        3: {"desc": "정상 (1일 1-2회)", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "잦은 편 (1일 2-3회)", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.10}},
        5: {"desc": "매우 잦음 (1일 3-4회 이상)", "weights": {"Cold_WC": 0.16, "Cold_WH": 0.04}}
    },
    "stool_color": {
        1: {"desc": "황금색/밝은 노란색", "weights": {"Cold_WC": 0.06, "Cold_WH": 0.06}},
        2: {"desc": "황토색/진한 노란색", "weights": {"Cold_WC": 0.06, "Cold_WH": 0.06}},
        3: {"desc": "황갈색/된장색", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "진한 갈색/고동색", "weights": {"Cold_WC": 0.46, "Cold_WH": 0.46}},
        5: {"desc": "녹갈색/짙은 풀색", "weights": {"Cold_WC": 0.04, "Cold_WH": 0.04}}
    },
    "stool_form": {
        1: {"desc": "단단한 염소 똥 모양", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.10}},
        2: {"desc": "딱딱/울퉁불퉁한 소시지", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.20}},
        3: {"desc": "표면이 갈라진 소시지", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "부드러운 떡가래 모양", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        5: {"desc": "물렁물렁한 수제비 모양", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.00}}
    },
    # ---------------------------------------------------------
    # Page 31: 배변 후 불편감 (Stool Discomfort After) - 정량 표현 from guideline
    # ---------------------------------------------------------
    "stool_discomfort": {
        1: {"desc": "배변 후 느낌이 매우 상쾌하다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        2: {"desc": "배변 후 느낌이 상쾌하다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        3: {"desc": "보통, 배변 후 느낌이 불쾌하지도 상쾌하지도 않다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "배변 후 느낌이 불쾌하고 어딘가 모르게 시원치 않다.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "배변 후 느낌이 매우 불쾌하고 시원치 않다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    # ---------------------------------------------------------
    # Page 31: 배변 후 잔변감(강도) (Stool Residual Feeling Severity) - 정량 표현 from guideline
    # ---------------------------------------------------------
    "stool_residual": {
        1: {"desc": "없음, 배변 후 불편감이 전혀 없는 상태.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "경미한 불편감, 약간 덜 본 것 같은 찜찜한 느낌이 들지만, 금방 잊어버리는 수준.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "중등도 불편감, 변이 남아있는 느낌이 분명하게 느껴져, 화장실에 더 앉아있거나 일상 중에도 신경이 쓰임.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "심한 불쾌감, 다시 화장실에 가고 싶다는 생각이 들 정도로 불쾌감이 심하며, 복부 팽만감이나 불편함을 동반함.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심한 불쾌감, 화장실을 다녀와도 전혀 변을 보지 않은 것처럼 느껴질 정도로 극심한 불쾌감을 느끼며, 아무것도 할 수 없는 상태.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },

    # ---------------------------------------------------------
    # URINE - Pages 31-32
    # ---------------------------------------------------------
    # Page 31-32: 1일 소변 횟수 - 야간뇨 횟수 (Daily Urine Frequency)
    "urine_freq_day": {
        1: {"desc": "1일 소변 횟수가 0회에서 2회 사이이다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        2: {"desc": "1일 소변 횟수가 3회에서 4회 사이이다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        3: {"desc": "1일 소변 횟수가 5회에서 7회 사이이다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "1일 소변 횟수가 8회에서 10회 사이이다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "1일 소변 횟수가 11회 이상이다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 31-32: 야간뇨 횟수 (Nocturia Frequency)
    "urine_freq_night": {
        1: {"desc": "정상, 야간뇨 횟수가 0회이다.", "weights": {"Cold_WC": 0.70, "Cold_WH": 0.50}},
        2: {"desc": "경미, 야간뇨 횟수가 1회이다.", "weights": {"Cold_WC": 0.26, "Cold_WH": 0.26}},
        3: {"desc": "중등도, 야간뇨 횟수가 2회이다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.06}},
        4: {"desc": "심함, 야간뇨 횟수가 3회에서 4회 사이이다.", "weights": {"Cold_WC": 0.06, "Cold_WH": 0.00}},
        5: {"desc": "매우 심함, 야간뇨 횟수가 5회 이상이다.", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.00}}
    },
    "urine_color": {
        1: {"desc": "무색/물처럼 맑음", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.00}},
        2: {"desc": "매우 옅은 노란색", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.00}},
        3: {"desc": "옅은 노란색/볏짚색", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "맑은 노란색", "weights": {"Cold_WC": 0.36, "Cold_WH": 0.36}},
        5: {"desc": "다소 진한 노란색", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 32: 소변 후 불편감 (Urine Discomfort After)
    "urine_discomfort": {
        1: {"desc": "소변 후 느낌이 매우 상쾌하다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        2: {"desc": "소변 후 느낌이 상쾌하다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.50}},
        3: {"desc": "보통, 소변 후 느낌이 불쾌하지도 상쾌하지도 않다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "소변 후 느낌이 불쾌하다.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.10}},
        5: {"desc": "소변 후 느낌이 매우 불쾌하다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.00}}
    },
    # Page 32: 배뇨 후 잔뇨감(강도) (Urine Residual Feeling Severity) - 정량 표현 from guideline
    "urine_residual": {
        1: {"desc": "없음, 잔뇨감이 전혀 없는 상태.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "경미한 잔뇨감, 소변이 약간 덜 나온 것 같은 찜찜한 느낌이 들지만, 금방 잊어버리는 수준.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "중등도 잔뇨감, 소변이 남아있는 느낌이 분명하게 느껴져, 화장실에 더 머무르거나 일상 중에도 신경이 쓰임.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "심한 잔뇨감, 소변을 본 직후에도 다시 화장실에 가고 싶다는 생각이 들 정도로 잔뇨감이 심하며, 아랫배의 불편함을 동반함.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심한 잔뇨감, 소변을 전혀 보지 않은 것처럼 느껴질 정도로 극심한 불쾌감을 느끼며, 아무것도 할 수 없는 상태.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    # Legacy urine_comfort for backwards compatibility
    "urine_comfort": {
        1: {"desc": "소변 보고 속이 아주 시원함", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        2: {"desc": "소변 보고 시원하고 개운함", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.50}},
        3: {"desc": "소변 보고 불편함 없이 무난함", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "소변 보고 뭔가 불편함", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10}},
        5: {"desc": "소변 보고 전혀 개운치 않음", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10}}
    }
}

# ==========================================
# 3. BODY, SLEEP & TEMP (From Prompt 3)
# Updated with exact Korean descriptions from Pages 33-35
# ==========================================
PART_3 = {
    # ---------------------------------------------------------
    # SLEEP - Pages 33
    # ---------------------------------------------------------
    # Page 33: 총 수면 시간 (Total Sleep Hours)
    "sleep_hours": {
        1: {"desc": "하루에 4시간 이하로 수면합니다.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.03}},
        2: {"desc": "하루에 5시간에서 6시간 정도 수면합니다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.20}},
        3: {"desc": "하루에 7시간에서 9시간 정도 수면합니다.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.25}},
        4: {"desc": "하루에 10시간에서 11시간 정도 수면합니다.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.02}},
        5: {"desc": "하루에 12시간 이상으로 수면합니다.", "weights": {"Cold_WC": 0.02, "Cold_WH": 0.01}}
    },
    # Page 33: 수면 숙면도 (Sleep Depth)
    "sleep_depth": {
        1: {"desc": "숙면도가 좋은 편, 깊이 잠들어 중간에 깨는 일이 거의 없음.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.15}},
        2: {"desc": "숙면도가 보통, 대체로 잠을 잘 자지만 가끔 중간에 깰 때가 있음.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.30}},
        3: {"desc": "숙면도가 나쁜 편, 잠을 설치거나 중간에 자주 깸.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.15}},
        4: {"desc": "숙면도가 매우 나쁨, 잠을 깊이 자지 못하고 중간에 여러 번 깸. 수면의 질이 좋지 않음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.05}},
        5: {"desc": "수면 장애, 잠을 거의 자지 못하거나 자더라도 선잠만 자고 자주 깨어남.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.03}}
    },
    # Page 33: 잠에 드는 데 걸리는 시간 (입면잠복기, Sleep Latency)
    "sleep_latency": {
        1: {"desc": "정상, 잠에 드는 데 걸리는 시간이 10분 이내입니다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "경미, 잠에 드는 데 걸리는 시간이 10분에서 20분 사이입니다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "중등도, 잠에 드는 데 걸리는 시간이 20분에서 30분 사이입니다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "심함, 잠에 드는 데 걸리는 시간이 30분에서 1시간 사이입니다.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심함, 잠에 드는 데 걸리는 시간이 1시간 이상입니다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    # Page 33: 기상 후 컨디션 (Sleep Quality / Morning Condition)
    "sleep_quality": {
        1: {"desc": "기상 후 컨디션이 매우 좋은 편입니다. 개운하고 활력이 넘침.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        2: {"desc": "기상 후 컨디션이 좋은 편입니다. 대체로 개운하게 일어남.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "기상 후 컨디션이 보통입니다. 개운하지도 않고 피곤하지도 않은 무난한 상태.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "기상 후 컨디션이 나쁜 편입니다. 일어나기 힘들거나 개운하지 않음.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "기상 후 컨디션이 매우 나쁜 편입니다. 충분히 자도 피곤하고 무겁게 느껴짐.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },

    # ---------------------------------------------------------
    # BODY TEMPERATURE & SWEAT - Pages 33-34
    # ---------------------------------------------------------
    # Page 33: 평소 체열감 (Daily Body Temperature Sensation)
    "cold_heat_pref": {
        1: {"desc": "평소 체열감이 매우 열이 많은 편이다. 항상 덥고 더위를 많이 탄다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        2: {"desc": "평소 체열감이 열이 많은 편이다. 대체로 더운 편이고 더위를 탄다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        3: {"desc": "평소 체열감이 보통이다. 덥지도 춥지도 않은 중립적인 상태.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "평소 체열감이 냉한 편이다. 대체로 추운 편이고 추위를 탄다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "평소 체열감이 매우 냉한 편이다. 항상 춥고 추위를 많이 탄다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 33-34: 땀 분비량 (Sweat Amount)
    "sweat_amt": {
        1: {"desc": "땀 분비량이 거의 없는 편이다. 더운 환경이나 운동을 해도 땀이 잘 안 난다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.02}},
        2: {"desc": "땀 분비량이 적은 편이다. 적당히 운동을 하거나 더운 곳에서만 약간 땀이 난다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.15}},
        3: {"desc": "땀 분비량이 적당한 편이다. 활동량이나 환경에 따라 자연스럽게 땀이 난다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.20}},
        4: {"desc": "땀 분비량이 많은 편이다. 쉽게 땀이 나고 땀을 많이 흘리는 편이다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10}},
        5: {"desc": "땀 분비량이 매우 많은 편이다. 조금만 움직여도 땀이 많이 나거나, 가만히 있어도 땀이 난다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.05}}
    },
    # Page 34: 음수량 (Water Intake Amount)
    "drink_amt": {
        1: {"desc": "1일 음수량이 250mL(종이컵 1컵) 이하이다.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        2: {"desc": "1일 음수량이 250mL에서 500mL(종이컵 1~2컵) 정도이다.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        3: {"desc": "1일 음수량이 500mL에서 1L(종이컵 2~4컵) 정도이다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "1일 음수량이 1L에서 2L(종이컵 4~8컵) 정도이다.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        5: {"desc": "1일 음수량이 2L(종이컵 8컵) 이상이다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}
    },
    # Page 34: 선호 음료 온도 (Drink Temperature Preference)
    "drink_temp": {
        1: {"desc": "선호 음료 온도가 뜨거운 것, 뜨거운 음료만 마시고 차가운 것은 잘 안 마신다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.05}},
        2: {"desc": "선호 음료 온도가 따뜻한 것, 따뜻한 음료를 선호하지만 가끔 차가운 것도 마신다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.10}},
        3: {"desc": "선호 음료 온도가 상관없음, 음료 온도에 크게 신경 쓰지 않고 다 잘 마신다.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.25}},
        4: {"desc": "선호 음료 온도가 시원한 것, 시원하거나 차가운 음료를 선호한다.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.15}},
        5: {"desc": "선호 음료 온도가 차가운 것, 얼음이 들어간 차가운 음료만 마신다.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.30}}
    },

    # ---------------------------------------------------------
    # PHYSICAL STRENGTH & FATIGUE - Pages 32-33
    # Updated with exact guideline descriptions
    # ---------------------------------------------------------
    # Page 32: 체력강약 (Physical Strength) - 정량 표현 from guideline
    "physical_strength": {
        1: {"desc": "매우 약함, 항상 무기력하고 조금만 움직여도 숨이 참. 얼굴이 창백하고 어지럼증을 자주 느낌.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        2: {"desc": "약한 편, 평소 기운이 없고 쉽게 피로해짐. 식욕이 없거나 식후에 잘 졸리고, 목소리에 힘이 없음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        3: {"desc": "보통, 일상생활에 필요한 체력을 가지고 있으며, 피로하면 휴식 후 잘 회복됨.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "강한 편, 활력이 넘치고, 웬만해서는 잘 지치지 않음. 잔병치레가 거의 없고 회복이 빠름.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        5: {"desc": "매우 강함, 체격이 건실하고 에너지가 넘쳐 주체하기 어려울 정도. 목소리가 매우 크고 우렁참.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 32: 피로감 (Fatigue Level) - 정량 표현 from guideline
    "fatigue": {
        1: {"desc": "거의 없음, 피로를 거의 느끼지 않으며, 아침에 일어날 때 몸이 개운하고 활력이 넘치는 최상의 컨디션 상태.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        2: {"desc": "경미, 일상생활에 큰 지장은 없으나 가벼운 피로가 있음.", "weights": {"Cold_WC": 0.35, "Cold_WH": 0.35}},
        3: {"desc": "중등도, 아침에 일어날 때부터 개운하지 않고, 하루 종일 전반적인 피로감이 지속됨. 일상생활은 가능하지만 의욕이나 집중력이 다소 저하됨.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "심함, 피로감이 심하여 뚜렷한 집중력 저하를 느끼며, 업무나 학업 등 일상적인 활동을 수행하는 것이 힘겹게 느껴짐.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심함, 극심한 피로와 무기력감으로 인해 일상생활을 영위하는 것 자체가 어려움. 잠을 자거나 푹 쉬어도 피로가 전혀 회복되지 않는 느낌.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    # Page 33: 신체통, 근육통 여부 (Body Pain / Muscle Pain) - 정량 표현 from guideline
    "body_muscle_pain": {
        1: {"desc": "없음, 몸살 기운이나 전신 통증을 전혀 느끼지 않음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "경미, 일시적으로 몸이 뻐근하거나 약간 무거운 느낌이 들지만, 휴식 후 완전히 회복됨. 일상생활 지장 없음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "중등도, 특별한 활동 없이도 몸이 찌뿌둥하거나 무겁고(예: 짧은 숨이 가라앉는 느낌), 여기저기 가벼운 통증이 느껴짐. 활동에 약간의 불편감을 줌.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "심함, 전신 근육통이나 몸살 기운이 뚜렷하며, 몸이 매우 무겁게 느껴져 활동하기가 힘듦. 집중력 저하 등을 동반하여 일상생활에 제약을 받음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심함, 극심한 전신 통증이나 몸살 기운, 혹은 몸을 가누기 힘들 정도의 무거움으로 인해, 기본적인 일상 활동조차 어려운 상태.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },
    # Page 33: 신중(身重) 여부 (Body Heaviness) - 정량 표현 from guideline
    "body_heaviness": {
        1: {"desc": "없음, 몸이 상쾌함", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "경미, 많이 걷거나 피곤할 때 잠깐 몸이 무거우며, 휴식 후 완전히 회복됨.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "중등도, 피곤한 날 몸이 무거우며, 일상 중 불편감을 느낌.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "심함, 몸이 무겁고 불편함을 뚜렷하게 느낌.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "매우 심함, 몸이 매우 무겁고 삶의 질에 큰 지장을 줌.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },

    # ---------------------------------------------------------
    # PAIN - Page 34
    # ---------------------------------------------------------
    # Page 34: 평소 통증 유무 (Daily Pain Presence)
    "pain_presence": {
        1: {"desc": "평소 통증이 없음, 일상에서 통증을 느끼지 않음.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50}},
        2: {"desc": "평소 통증이 있음, 특정 부위나 상황에서 통증을 느낌.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50}}
    },
    # Page 34: 통증 부위 (Pain Location) - Multiple choice
    "pain_location": {
        1: {"desc": "머리 (두통)", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        2: {"desc": "목", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        3: {"desc": "어깨", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        4: {"desc": "허리", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "무릎", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        6: {"desc": "팔/손목", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        7: {"desc": "다리/발목", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 34: 통증 강도 (Pain Severity) - NRS 기준
    "pain_severity": {
        1: {"desc": "통증 강도 0: 통증이 전혀 없음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "통증 강도 1-3: 경미한 통증, 약간 불편한 정도.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "통증 강도 4-6: 중등도 통증, 일상생활에 지장이 있는 정도.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        4: {"desc": "통증 강도 7-9: 심한 통증, 집중이 어렵고 활동에 큰 제한이 있음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        5: {"desc": "통증 강도 10: 극심한 통증, 참을 수 없는 최악의 통증.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },

    # ---------------------------------------------------------
    # SKIN & FACE - Pages 33-34
    # ---------------------------------------------------------
    # Page 33: 피부 건조도 (Skin Dryness) - 정량 표현 from guideline
    "skin_dry": {
        1: {"desc": "정상, 피부에 당김이나 건조함이 전혀 없고 매끄럽고 편안한 상태.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        2: {"desc": "경미, 겉으로는 괜찮아 보이나, 세안 후나 특정 환경에서 피부 속이 당기는 느낌(속당김)이 듦.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        3: {"desc": "중등도, 피부 표면이 당기는 것이 뚜렷하게 느껴지며, 입가나 뺨 주변에 미세한 각질이 하얗게 일어나기 시작함.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        4: {"desc": "심함, 피부가 건조하여 각질이 눈에 띄게 일어나고 피부가 거칠어짐.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "매우 심함, 피부가 매우 건조하여, 하얀 각질을 넘어 피부 표면이 갈라짐(균열)", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 34: 얼굴 광택 (Face Gloss) - 정량 표현 from guideline
    "face_gloss": {
        1: {"desc": "윤기없음, 얼굴에 생기나 광택이 보이며 매마른 느낌을 줌.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        2: {"desc": "윤기가 약간 있음, 피부가 전반적으로 칙칙하고 생기가 부족하지만, 아주 약간의 광택은 남아있는 상태.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        3: {"desc": "윤기가 보통, 피부에 자연스럽고 건강한 광택이 도는 상태. 푸석하지도, 번들거리지도 않는 평균적인 상태.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}},
        4: {"desc": "윤기가 좋은함, 피부가 건강하여 빛나며, 맑은 생기가 넘쳐 보임. 촉촉하고 광택이 도는 상태.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        5: {"desc": "윤기가 충만함, 얼굴에서 빛이 나는 것처럼 광택이 매우 풍부하여, 누가 봐도 아주 건강하고 활력이 넘쳐 보이는 상태.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}
    },
    # Page 35: 안색 (Face Color)
    "face_color": {
        1: {"desc": "안색이 흰색/창백함, 얼굴이 창백하거나 핏기가 없음.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.15}},
        2: {"desc": "안색이 황색/누런 편, 얼굴이 누렇거나 칙칙한 느낌.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.25}},
        3: {"desc": "안색이 붉은 편, 얼굴이 붉거나 홍조가 있음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.05}},
        4: {"desc": "안색이 검붉은 편, 얼굴 피부톤이 칙칙하고 어두움.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.02}},
        5: {"desc": "안색이 검은/거무스름한 편, 얼굴이 어둡고 생기가 없음.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.02}}
    },

    # ---------------------------------------------------------
    # SENSORY - Pages 34
    # ---------------------------------------------------------
    # Page 34: 이명(빈도) (Tinnitus Frequency) - 정량 표현 from guideline
    "tinnitus_freq": {
        1: {"desc": "없음, 이명을 전혀 느끼지 않음.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50}},
        2: {"desc": "일시적, 매우 피곤하거나, 아주 조용한 곳에 있을 때만 잠깐 나타나며, 금방 사라짐.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        3: {"desc": "간헐적, 주기적으로(주 1~3회) 이명이 느껴지지만, 일상생활에 큰 지장은 없음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        4: {"desc": "지속적, 거의 매일 이명을 느끼며, 이로 인해 소리나 증상에 신경이 쓰이고 제약을 받음.", "weights": {"Cold_WC": 0.07, "Cold_WH": 0.07}},
        5: {"desc": "만성적, 깨어있는 시간 내내 이명이 지속되어, 소리, 수면 등 삶의 질 전반에 큰 영향을 줌.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.03}}
    },
    # Page 34: 이명(강도) (Tinnitus Severity) - 정량 표현 from guideline
    "tinnitus_sev": {
        1: {"desc": "없음, 불편감이 전혀 없는 상태.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50}},
        2: {"desc": "경미한 불편감, 이명 소리가 매우 작아서, 아주 조용한 환경에서 집중할 때만 의식되는 수준.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}},
        3: {"desc": "중등도 불편감, 일상적인 소음 속에서도 이명이 의식되며, 이로 인해 집중력이 다소 저하되고 약간의 신경이 쓰임.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        4: {"desc": "심한 불쾌감, 이명 소리가 커서 다른 소리를 듣는 데 방해가 되거나, 수면을 방해하고, 뚜렷한 스트레스를 유발함.", "weights": {"Cold_WC": 0.07, "Cold_WH": 0.07}},
        5: {"desc": "매우 심한 불쾌감, 참을 수 없을 정도로 이명 소리가 크거나 거슬려, 다른 생각이나 활동이 불가능하고, 극심한 고통이나 불안감을 유발함.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.03}}
    },
    # Legacy tinnitus for backwards compatibility
    "tinnitus": {
        1: {"desc": "이명이 없음, 귀에서 소리가 들리는 증상이 없음.", "weights": {"Cold_WC": 0.80, "Cold_WH": 0.40}},
        2: {"desc": "이명이 가끔 있음, 간헐적으로 귀에서 소리가 들리지만 일상에 지장이 없음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}},
        3: {"desc": "이명이 자주 있음, 귀에서 소리가 자주 들려 신경이 쓰임.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}},
        4: {"desc": "이명이 거의 항상 있음, 지속적으로 귀에서 소리가 들려 일상에 불편함.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.03}},
        5: {"desc": "이명이 심각한 수준, 항상 소리가 들려 수면이나 집중에 큰 지장이 있음.", "weights": {"Cold_WC": 0.02, "Cold_WH": 0.02}}
    },
    # Page 35: 눈 불편감 (Eye Discomfort)
    "eye_discomfort": {
        1: {"desc": "눈이 편안함, 눈에 불편감이 전혀 없음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        2: {"desc": "눈이 가끔 불편함, 간헐적으로 눈이 건조하거나 뻑뻑함.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}},
        3: {"desc": "눈이 자주 불편함, 자주 눈이 건조하거나 피로함을 느낌.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}},
        4: {"desc": "눈이 항상 불편함, 눈 건조감이나 피로가 지속적임.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        5: {"desc": "눈 불편감이 심각함, 안구건조증 등으로 일상에 지장이 있음.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}
    },

    # ---------------------------------------------------------
    # EDEMA & BRUISING (Legacy/Additional)
    # ---------------------------------------------------------
    "edema": {
        1: {"desc": "부종이 전혀 없음, 손발이나 얼굴이 붓지 않음.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.30}},
        2: {"desc": "부종이 가끔 있음, 일시적으로 손발이나 얼굴이 붓는 경우가 있음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.15}},
        3: {"desc": "부종이 자주 있음, 자주 손발이나 얼굴이 붓는 편.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.05}},
        4: {"desc": "부종이 지속됨, 부기가 잘 빠지지 않고 지속됨.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.00}},
        5: {"desc": "부종이 심각함, 항상 부어있고 일상에 불편함.", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.00}}
    },
    "bruising": {
        1: {"desc": "멍이 잘 안 드는 편, 부딪혀도 멍이 잘 들지 않음.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.30}},
        2: {"desc": "멍이 보통, 세게 부딪히면 멍이 드는 정도.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.10}},
        3: {"desc": "멍이 쉽게 드는 편, 조금만 부딪혀도 멍이 듦.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.05}},
        4: {"desc": "멍이 매우 쉽게 듦, 살짝 스쳐도 멍이 듦.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.00}},
        5: {"desc": "원인 없이 멍이 듦, 부딪힌 기억이 없어도 멍이 생김.", "weights": {"Cold_WC": 0.00, "Cold_WH": 0.00}}
    }
}

# ==========================================
# 4. MENTAL & DIAGNOSTICS (From Prompt 4)
# Updated with exact Korean descriptions from Page 35
# ==========================================
PART_4 = {
    # ---------------------------------------------------------
    # MENTAL STATE & EMOTION - Page 35
    # ---------------------------------------------------------
    # Page 35: 득신/실신 - 정신 상태 (Mental Clarity)
    "mental_state": {
        1: {"desc": "매우 맑음, 정신이 매우 맑고 집중력이 높은 최상의 상태. 대체로 맑음, 정신이 대체로 맑고 깨끗한 편이나, 피곤하거나 스트레스를 받으면 가끔 멍해지거나 깜빡 잊어버릴 때가 있음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        2: {"desc": "맑고 깨끗한 편, 정신이 대체로 맑고 깨끗한 편이나, 피곤하거나 스트레스를 받으면 가끔 멍해지거나 깜빡 잊어버릴 때가 있음.", "weights": {"Cold_WC": 0.35, "Cold_WH": 0.35}}, 
        3: {"desc": "경미한 혼미, 정신이 안개 낀 것처럼 가끔 흐려지고, 생각이 잘 정리되지 않으며, 사소한 일을 자주 깜빡함.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "중등도 혼미, 정신이 자주 흐릿하고 멍한 상태가 지속됨. 이로 인해 집중력에 뚜렷한 저하를 느끼며, 업무나 학업 등 일상생활에 지장을 받음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        5: {"desc": "심한 혼미, 정신이 매우 흐릿하고 혼미하여, 사고나 판단이 어려움. 의식이 몽롱하여 일상생활을 영위하는 것 자체가 어려움.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}} 
    },
    # Page 35: 기억력 저하 (Memory Decline)
    "memory": {
        1: {"desc": "매우 좋음, 기억력에 전혀 문제가 없음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        2: {"desc": "좋음, 기억력에 문제가 없음.", "weights": {"Cold_WC": 0.35, "Cold_WH": 0.35}}, 
        3: {"desc": "약간 나쁨, 깜빡하는 횟수가 뚜렷하게 늘었다고 스스로 인지하며(예: 약속, 사람 이름), 이로 인해 메모나 알람에 의존하게 됨.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "나쁨, 중요한 약속이나 최근 대화 내용을 잊어버리는 등, 기억력 저하로 인해 업무나 일상적인 활동에 뚜렷한 지장을 받음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        5: {"desc": "매우 나쁨, 방금 일어난 일이나 익숙한 정보(예: 가족 이름)도 기억하기 어려움.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}} 
    },
    # Page 35: 의욕 (Motivation) - 이미 PART_2에 motivation_level로 정의됨
    "motivation": {
        1: {"desc": "의욕이 매우 높음, 일상적인 활동이나 업무를 긍정적이고 능동적으로 수행하며, 의욕이 넘침.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}, 
        2: {"desc": "의욕이 높은 편, 일상적인 활동이나 업무를 긍정적이고 능동적으로 수행하며, 대체로 의욕이 있는 편.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        3: {"desc": "의욕이 보통, 해야 할 일은 수행하지만, 그 이상의 적극적인 의욕이나 열정은 부족한 일반적인 상태.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "의욕이 저하됨, 매사에 의욕이 없고, 간단한 일상 활동조차 귀찮고 힘들게 느끼며, 소극적이거나 회피하는 경향이 생김.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        5: {"desc": "의욕이 매우 저하됨, 의욕이 완전히 상실되어, 식사, 수면 등 기본적인 활동을 포함한 모든 일에 흥미나 관심이 없는 무기력한 상태.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}} 
    },
    # Page 35: 성격/성미 (Personality Speed)
    "personality_speed": {
        1: {"desc": "성격이 매우 느긋함, 여유롭고 급하지 않은 편.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}}, 
        2: {"desc": "성격이 느긋한 편, 대체로 여유 있고 급하지 않음.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}, 
        3: {"desc": "성격이 보통, 상황에 따라 적당히 급하기도 하고 느긋하기도 함.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}}, 
        4: {"desc": "성격이 급한 편, 성미가 급하고 빨리빨리 하는 스타일.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}, 
        5: {"desc": "성격이 매우 급함, 매우 성급하고 조급해하는 편.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}} 
    },
    # Page 35: 분노/화 (Anger)
    "emot_anger": {
        1: {"desc": "화를 거의 안 냄, 화나는 일이 있어도 평온하게 넘김.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        2: {"desc": "화를 잘 참는 편, 화가 나도 대체로 잘 참고 표현을 자제함.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}}, 
        3: {"desc": "화내는 정도가 보통, 보통 수준으로 화를 내거나 표현함.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "화를 잘 내는 편, 쉽게 짜증나거나 화를 내는 편.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}, 
        5: {"desc": "화를 자주 냄, 자주 화를 내거나 분노 조절이 어려움.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}} 
    },
    # Page 35: 불안 (Anxiety)
    "emot_anxiety": {
        1: {"desc": "불안감이 거의 없음, 평소 불안을 느끼지 않고 마음이 평온함.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        2: {"desc": "불안감이 적은 편, 가끔 긴장되거나 불안할 때가 있지만 대체로 평온함.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}}, 
        3: {"desc": "불안감이 보통, 보통 수준의 걱정이나 불안감이 있음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "불안감이 많은 편, 자주 걱정하거나 불안해함.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}, 
        5: {"desc": "불안감이 매우 심함, 항상 불안하거나 걱정이 많아 일상에 지장이 있음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}} 
    },
    # Page 35: 우울 (Depression)
    "emot_depress": {
        1: {"desc": "우울감이 거의 없음, 평소 밝고 긍정적이며 우울하지 않음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        2: {"desc": "우울감이 적은 편, 가끔 기분이 처지지만 대체로 괜찮음.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}}, 
        3: {"desc": "우울감이 보통, 보통 수준의 기분 저하가 있음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        4: {"desc": "우울감이 많은 편, 자주 우울하거나 기분이 가라앉음.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.20}}, 
        5: {"desc": "우울감이 매우 심함, 항상 우울하고 무기력하며 일상에 지장이 있음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.10}} 
    },

    # ---------------------------------------------------------
    # PULSE DIAGNOSIS (Source: Page 62 & 90-91)
    # ---------------------------------------------------------
    "pulse_rate": {
        1: {"desc": "맥박이 매우 느림 (지맥), 분당 60회 미만.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.00}}, 
        2: {"desc": "맥박이 느린 편 (완맥), 분당 60~70회.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.05}}, 
        3: {"desc": "맥박이 보통 (평맥), 분당 70~80회.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.40}}, 
        4: {"desc": "맥박이 빠른 편 (삭맥), 분당 80~90회.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.35}}, 
        5: {"desc": "맥박이 매우 빠름 (질맥), 분당 90회 이상.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.20}} 
    },
    "pulse_depth": {
        1: {"desc": "맥이 표면에서 느껴짐 (부맥), 가볍게 눌러도 맥이 잡힘.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.30}}, 
        2: {"desc": "맥이 약간 표면에서 느껴짐, 가볍게 눌렀을 때 맥이 잡히는 편.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.30}}, 
        3: {"desc": "맥이 중간 깊이에서 느껴짐 (중맥), 보통 세기로 눌러야 맥이 잡힘.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.25}},
        4: {"desc": "맥이 깊은 곳에서 느껴짐 (침맥), 세게 눌러야 맥이 잡힘.", "weights": {"Cold_WC": 0.08, "Cold_WH": 0.12}}, 
        5: {"desc": "맥이 매우 깊은 곳에서 느껴짐 (복맥), 매우 세게 눌러야 맥이 잡힘.", "weights": {"Cold_WC": 0.02, "Cold_WH": 0.03}} 
    },
    "pulse_strength": {
        1: {"desc": "맥이 매우 약함 (미맥), 맥을 찾기 어려울 정도로 미약함.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}}, 
        2: {"desc": "맥이 약한 편 (약맥), 맥이 약하게 느껴짐.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}}, 
        3: {"desc": "맥이 보통 (완맥), 일반적인 세기의 맥.", "weights": {"Cold_WC": 0.50, "Cold_WH": 0.50}}, 
        4: {"desc": "맥이 강한 편 (실맥), 맥이 힘 있게 느껴짐.", "weights": {"Cold_WC": 0.25, "Cold_WH": 0.25}}, 
        5: {"desc": "맥이 매우 강함 (대맥), 맥이 매우 힘 있고 세게 느껴짐.", "weights": {"Cold_WC": 0.05, "Cold_WH": 0.05}} 
    },

    # ---------------------------------------------------------
    # TONGUE DIAGNOSIS (Source: Pages 91-92)
    # ---------------------------------------------------------
    "tongue_color": {
        1: {"desc": "설색이 담백함 (담백설), 혀가 창백하고 혈색이 없음.", "weights": {"Cold_WC": 0.30, "Cold_WH": 0.05}}, 
        2: {"desc": "설색이 담홍색 (담홍설), 혀가 옅은 분홍빛으로 정상적인 색.", "weights": {"Cold_WC": 0.40, "Cold_WH": 0.30}}, 
        3: {"desc": "설색이 홍색 (홍설), 혀가 붉은 색.", "weights": {"Cold_WC": 0.20, "Cold_WH": 0.40}}, 
        4: {"desc": "설색이 강홍색 (강설), 혀가 짙은 붉은 색.", "weights": {"Cold_WC": 0.07, "Cold_WH": 0.20}}, 
        5: {"desc": "설색이 자색/청자색 (청자설), 혀가 자주색이나 푸른빛이 돔.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.05}} 
    },
    "tongue_coat": {
        1: {"desc": "설태가 황색 (황태), 혀에 누런 태가 끼어 있음.", "weights": {"Cold_WC": 0.10, "Cold_WH": 0.50}}, 
        2: {"desc": "설태가 백색 (백태), 혀에 흰 태가 끼어 있음.", "weights": {"Cold_WC": 0.70, "Cold_WH": 0.30}}, 
        3: {"desc": "설태가 없음 (무태), 혀에 태가 거의 없음.", "weights": {"Cold_WC": 0.15, "Cold_WH": 0.15}},
        4: {"desc": "설태가 두꺼움 (후태), 태가 두껍게 끼어 있음.", "weights": {"Cold_WC": 0.03, "Cold_WH": 0.03}},
        5: {"desc": "설태가 끈적함 (니태), 태가 끈적하고 더러운 느낌.", "weights": {"Cold_WC": 0.02, "Cold_WH": 0.02}}
    }
}

# ==========================================
# MERGE ALL DATA
# ==========================================
CLINICAL_DATA = {}
CLINICAL_DATA.update(PART_1)
CLINICAL_DATA.update(PART_2)
CLINICAL_DATA.update(PART_3)
CLINICAL_DATA.update(PART_4)

# NOTE: PART_5 is added after being defined below

# Helper function to get text
def get_desc(variable, level):
    try:
        return CLINICAL_DATA[variable][level]['desc']
    except:
        return ""

# Helper function to get weights
def get_weights(variable, level):
    try:
        return CLINICAL_DATA[variable][level]['weights']
    except:
        return {}

# ==========================================
# 5. BACK PAIN & DYSPEPSIA PATTERNS (Page 23)
# 한열허실 based pattern classification
# ==========================================
PART_5 = {
    # ---------------------------------------------------------
    # BACK PAIN (요통) SYMPTOM WEIGHTS - Page 23
    # Pattern Keys: BP_Cold, BP_Heat, BP_QiDef, BP_YangDef, BP_YinDef, 
    #               BP_FoodStag, BP_Phlegm, BP_QiStag, BP_BloodStasis
    # ---------------------------------------------------------
    "back_pain_sev": {
        1: {"desc": "통증 없음", "weights": {
            "BP_Cold": 0.00, "BP_Heat": 0.00, "BP_QiDef": 0.00, "BP_YangDef": 0.00, "BP_YinDef": 0.00,
            "BP_FoodStag": 0.00, "BP_Phlegm": 0.00, "BP_QiStag": 0.00, "BP_BloodStasis": 0.00}},
        2: {"desc": "약간 (경미)", "weights": {
            "BP_Cold": 0.15, "BP_Heat": 0.15, "BP_QiDef": 0.30, "BP_YangDef": 0.25, "BP_YinDef": 0.25,
            "BP_FoodStag": 0.20, "BP_Phlegm": 0.20, "BP_QiStag": 0.20, "BP_BloodStasis": 0.10}},
        3: {"desc": "중등도", "weights": {
            "BP_Cold": 0.35, "BP_Heat": 0.35, "BP_QiDef": 0.40, "BP_YangDef": 0.40, "BP_YinDef": 0.40,
            "BP_FoodStag": 0.40, "BP_Phlegm": 0.40, "BP_QiStag": 0.40, "BP_BloodStasis": 0.30}},
        4: {"desc": "심함", "weights": {
            "BP_Cold": 0.35, "BP_Heat": 0.35, "BP_QiDef": 0.25, "BP_YangDef": 0.25, "BP_YinDef": 0.25,
            "BP_FoodStag": 0.30, "BP_Phlegm": 0.30, "BP_QiStag": 0.30, "BP_BloodStasis": 0.40}},
        5: {"desc": "매우 심함", "weights": {
            "BP_Cold": 0.15, "BP_Heat": 0.15, "BP_QiDef": 0.05, "BP_YangDef": 0.10, "BP_YinDef": 0.10,
            "BP_FoodStag": 0.10, "BP_Phlegm": 0.10, "BP_QiStag": 0.10, "BP_BloodStasis": 0.20}}
    },
    "back_pain_cold_agg": {  # 한통 - worse with cold
        1: {"desc": "냉기에 무관", "weights": {
            "BP_Cold": 0.00, "BP_Heat": 0.60, "BP_QiDef": 0.30, "BP_YangDef": 0.10, "BP_YinDef": 0.40,
            "BP_FoodStag": 0.40, "BP_Phlegm": 0.30, "BP_QiStag": 0.40, "BP_BloodStasis": 0.30}},
        2: {"desc": "약간 민감", "weights": {
            "BP_Cold": 0.20, "BP_Heat": 0.30, "BP_QiDef": 0.40, "BP_YangDef": 0.30, "BP_YinDef": 0.35,
            "BP_FoodStag": 0.35, "BP_Phlegm": 0.40, "BP_QiStag": 0.35, "BP_BloodStasis": 0.35}},
        3: {"desc": "찬 것에 악화", "weights": {
            "BP_Cold": 0.50, "BP_Heat": 0.10, "BP_QiDef": 0.20, "BP_YangDef": 0.40, "BP_YinDef": 0.20,
            "BP_FoodStag": 0.20, "BP_Phlegm": 0.25, "BP_QiStag": 0.20, "BP_BloodStasis": 0.25}},
        4: {"desc": "냉기시 심함", "weights": {
            "BP_Cold": 0.25, "BP_Heat": 0.00, "BP_QiDef": 0.08, "BP_YangDef": 0.15, "BP_YinDef": 0.05,
            "BP_FoodStag": 0.05, "BP_Phlegm": 0.05, "BP_QiStag": 0.05, "BP_BloodStasis": 0.08}},
        5: {"desc": "극심한 한통", "weights": {
            "BP_Cold": 0.05, "BP_Heat": 0.00, "BP_QiDef": 0.02, "BP_YangDef": 0.05, "BP_YinDef": 0.00,
            "BP_FoodStag": 0.00, "BP_Phlegm": 0.00, "BP_QiStag": 0.00, "BP_BloodStasis": 0.02}}
    },
    "back_pain_warmth_relief": {  # 득온즉감 - better with warmth
        1: {"desc": "온기에 무관", "weights": {
            "BP_Cold": 0.00, "BP_Heat": 0.50, "BP_QiDef": 0.30, "BP_YangDef": 0.10, "BP_YinDef": 0.50,
            "BP_FoodStag": 0.40, "BP_Phlegm": 0.30, "BP_QiStag": 0.40, "BP_BloodStasis": 0.30}},
        2: {"desc": "약간 호전", "weights": {
            "BP_Cold": 0.20, "BP_Heat": 0.30, "BP_QiDef": 0.35, "BP_YangDef": 0.30, "BP_YinDef": 0.30,
            "BP_FoodStag": 0.35, "BP_Phlegm": 0.35, "BP_QiStag": 0.35, "BP_BloodStasis": 0.35}},
        3: {"desc": "따뜻하면 호전", "weights": {
            "BP_Cold": 0.50, "BP_Heat": 0.15, "BP_QiDef": 0.25, "BP_YangDef": 0.40, "BP_YinDef": 0.15,
            "BP_FoodStag": 0.20, "BP_Phlegm": 0.25, "BP_QiStag": 0.20, "BP_BloodStasis": 0.25}},
        4: {"desc": "온찜질 필수", "weights": {
            "BP_Cold": 0.25, "BP_Heat": 0.05, "BP_QiDef": 0.08, "BP_YangDef": 0.15, "BP_YinDef": 0.05,
            "BP_FoodStag": 0.05, "BP_Phlegm": 0.08, "BP_QiStag": 0.05, "BP_BloodStasis": 0.08}},
        5: {"desc": "극도 온열선호", "weights": {
            "BP_Cold": 0.05, "BP_Heat": 0.00, "BP_QiDef": 0.02, "BP_YangDef": 0.05, "BP_YinDef": 0.00,
            "BP_FoodStag": 0.00, "BP_Phlegm": 0.02, "BP_QiStag": 0.00, "BP_BloodStasis": 0.02}}
    },
    "back_pain_stabbing": {  # 자통 - stabbing pain (Blood Stasis marker)
        1: {"desc": "찌르는 통증 없음", "weights": {
            "BP_Cold": 0.40, "BP_Heat": 0.40, "BP_QiDef": 0.50, "BP_YangDef": 0.45, "BP_YinDef": 0.45,
            "BP_FoodStag": 0.45, "BP_Phlegm": 0.40, "BP_QiStag": 0.30, "BP_BloodStasis": 0.05}},
        2: {"desc": "가끔 찌름", "weights": {
            "BP_Cold": 0.35, "BP_Heat": 0.35, "BP_QiDef": 0.30, "BP_YangDef": 0.30, "BP_YinDef": 0.30,
            "BP_FoodStag": 0.30, "BP_Phlegm": 0.35, "BP_QiStag": 0.35, "BP_BloodStasis": 0.20}},
        3: {"desc": "자주 찌르는 통증", "weights": {
            "BP_Cold": 0.20, "BP_Heat": 0.20, "BP_QiDef": 0.15, "BP_YangDef": 0.20, "BP_YinDef": 0.20,
            "BP_FoodStag": 0.20, "BP_Phlegm": 0.20, "BP_QiStag": 0.25, "BP_BloodStasis": 0.40}},
        4: {"desc": "심한 자통", "weights": {
            "BP_Cold": 0.05, "BP_Heat": 0.05, "BP_QiDef": 0.05, "BP_YangDef": 0.05, "BP_YinDef": 0.05,
           
            "BP_FoodStag": 0.05, "BP_Phlegm": 0.05, "BP_QiStag": 0.08, "BP_BloodStasis": 0.25}},
        5: {"desc": "칼로 찌르는 듯", "weights": {
            "BP_Cold": 0.00, "BP_Heat": 0.00, "BP_QiDef": 0.00, "BP_YangDef": 0.00, "BP_YinDef": 0.00,
            "BP_FoodStag": 0.00, "BP_Phlegm": 0.00, "BP_QiStag": 0.02, "BP_BloodStasis": 0.10}}
    },
    "back_pain_moving": {  # 유주통 - moving pain (Phlegm marker)
        1: {"desc": "고정 통증", "weights": {
            "BP_Cold": 0.35, "BP_Heat": 0.35, "BP_QiDef": 0.40, "BP_YangDef": 0.40, "BP_YinDef": 0.40,
            "BP_FoodStag": 0.40, "BP_Phlegm": 0.05, "BP_QiStag": 0.20, "BP_BloodStasis": 0.45}},
        2: {"desc": "가끔 이동", "weights": {
            "BP_Cold": 0.35, "BP_Heat": 0.35, "BP_QiDef": 0.35, "BP_YangDef": 0.35, "BP_YinDef": 0.35,
            "BP_FoodStag": 0.35, "BP_Phlegm": 0.25, "BP_QiStag": 0.30, "BP_BloodStasis": 0.30}},
        3: {"desc": "통증 부위 변화", "weights": {
            "BP_Cold": 0.20, "BP_Heat": 0.20, "BP_QiDef": 0.20, "BP_YangDef": 0.20, "BP_YinDef": 0.20,
            "BP_FoodStag": 0.20, "BP_Phlegm": 0.40, "BP_QiStag": 0.35, "BP_BloodStasis": 0.20}},
        4: {"desc": "자주 이동", "weights": {
            "BP_Cold": 0.08, "BP_Heat": 0.08, "BP_QiDef": 0.05, "BP_YangDef": 0.05, "BP_YinDef": 0.05,
            "BP_FoodStag": 0.05, "BP_Phlegm": 0.25, "BP_QiStag": 0.12, "BP_BloodStasis": 0.05}},
        5: {"desc": "항상 이동 (유주통)", "weights": {
            "BP_Cold": 0.02, "BP_Heat": 0.02, "BP_QiDef": 0.00, "BP_YangDef": 0.00, "BP_YinDef": 0.00,
            "BP_FoodStag": 0.00, "BP_Phlegm": 0.05, "BP_QiStag": 0.03, "BP_BloodStasis": 0.00}}
    },

    # ---------------------------------------------------------
    # DYSPEPSIA (소화불량) SYMPTOM WEIGHTS - Page 23
    # Pattern Keys: DY_Cold, DY_Heat, DY_QiDef, DY_YangDef, DY_YinDef,
    #               DY_FoodStag, DY_Phlegm, DY_QiStag, DY_BloodStasis
    # ---------------------------------------------------------
    "dyspepsia_bloating": {
        1: {"desc": "복부팽만 없음", "weights": {
            "DY_Cold": 0.20, "DY_Heat": 0.20, "DY_QiDef": 0.15, "DY_YangDef": 0.15, "DY_YinDef": 0.25,
            "DY_FoodStag": 0.05, "DY_Phlegm": 0.10, "DY_QiStag": 0.10, "DY_BloodStasis": 0.25}},
        2: {"desc": "약간 더부룩함", "weights": {
            "DY_Cold": 0.25, "DY_Heat": 0.25, "DY_QiDef": 0.30, "DY_YangDef": 0.25, "DY_YinDef": 0.30,
            "DY_FoodStag": 0.20, "DY_Phlegm": 0.25, "DY_QiStag": 0.25, "DY_BloodStasis": 0.30}},
        3: {"desc": "식후 불편", "weights": {
            "DY_Cold": 0.30, "DY_Heat": 0.30, "DY_QiDef": 0.35, "DY_YangDef": 0.35, "DY_YinDef": 0.30,
            "DY_FoodStag": 0.35, "DY_Phlegm": 0.35, "DY_QiStag": 0.35, "DY_BloodStasis": 0.30}},
        4: {"desc": "심한 복만", "weights": {
            "DY_Cold": 0.20, "DY_Heat": 0.20, "DY_QiDef": 0.15, "DY_YangDef": 0.20, "DY_YinDef": 0.12,
            "DY_FoodStag": 0.30, "DY_Phlegm": 0.25, "DY_QiStag": 0.25, "DY_BloodStasis": 0.12}},
        5: {"desc": "극심한 팽만", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.05, "DY_QiDef": 0.05, "DY_YangDef": 0.05, "DY_YinDef": 0.03,
            "DY_FoodStag": 0.10, "DY_Phlegm": 0.05, "DY_QiStag": 0.05, "DY_BloodStasis": 0.03}}
    },
    "dyspepsia_cold_food_agg": {  # 찬 음식에 악화
        1: {"desc": "찬 음식 무관", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.50, "DY_QiDef": 0.30, "DY_YangDef": 0.10, "DY_YinDef": 0.40,
            "DY_FoodStag": 0.35, "DY_Phlegm": 0.30, "DY_QiStag": 0.35, "DY_BloodStasis": 0.35}},
        2: {"desc": "약간 민감", "weights": {
            "DY_Cold": 0.20, "DY_Heat": 0.30, "DY_QiDef": 0.35, "DY_YangDef": 0.25, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.35, "DY_Phlegm": 0.35, "DY_QiStag": 0.35, "DY_BloodStasis": 0.35}},
        3: {"desc": "찬것 먹으면 악화", "weights": {
            "DY_Cold": 0.45, "DY_Heat": 0.15, "DY_QiDef": 0.25, "DY_YangDef": 0.40, "DY_YinDef": 0.20,
            "DY_FoodStag": 0.25, "DY_Phlegm": 0.30, "DY_QiStag": 0.25, "DY_BloodStasis": 0.25}},
        4: {"desc": "찬음식 기피", "weights": {
            "DY_Cold": 0.25, "DY_Heat": 0.05, "DY_QiDef": 0.08, "DY_YangDef": 0.20, "DY_YinDef": 0.05,
            "DY_FoodStag": 0.05, "DY_Phlegm": 0.05, "DY_QiStag": 0.05, "DY_BloodStasis": 0.05}},
        5: {"desc": "절대 찬것 안됨", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.00, "DY_QiDef": 0.02, "DY_YangDef": 0.05, "DY_YinDef": 0.00,
            "DY_FoodStag": 0.00, "DY_Phlegm": 0.00, "DY_QiStag": 0.00, "DY_BloodStasis": 0.00}}
    },
    "dyspepsia_acid_reflux": {  # 신물 - acid reflux
       
        1: {"desc": "신물 없음", "weights": {
            "DY_Cold": 0.50, "DY_Heat": 0.30, "DY_QiDef": 0.45, "DY_YangDef": 0.50, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.20, "DY_Phlegm": 0.40, "DY_QiStag": 0.30, "DY_BloodStasis": 0.45}},
        2: {"desc": "가끔 신물", "weights": {
            "DY_Cold": 0.30, "DY_Heat": 0.35, "DY_QiDef": 0.35, "DY_YangDef": 0.30, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.35, "DY_Phlegm": 0.35, "DY_QiStag": 0.35, "DY_BloodStasis": 0.35}},
        3: {"desc": "식후 신물", "weights": {
            "DY_Cold": 0.15, "DY_Heat": 0.25, "DY_QiDef": 0.15, "DY_YangDef": 0.15, "DY_YinDef": 0.20,
            "DY_FoodStag": 0.30, "DY_Phlegm": 0.20, "DY_QiStag": 0.25, "DY_BloodStasis": 0.15}},
        4: {"desc": "자주 신물", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.08, "DY_QiDef": 0.05, "DY_YangDef": 0.05, "DY_YinDef": 0.08,
            "DY_FoodStag": 0.12, "DY_Phlegm": 0.05, "DY_QiStag": 0.08, "DY_BloodStasis": 0.05}},
        5: {"desc": "항상 신물", "weights": {
            "DY_Cold": 0.00, "DY_Heat": 0.02, "DY_QiDef": 0.00, "DY_YangDef": 0.00, "DY_YinDef": 0.02,
            "DY_FoodStag": 0.03, "DY_Phlegm": 0.00, "DY_QiStag": 0.02, "DY_BloodStasis": 0.00}}
    },
    "dyspepsia_foul_belch": {  # 부패취 - foul belching (Food Stagnation marker)
        1: {"desc": "트림 냄새 없음", "weights": {
            "DY_Cold": 0.50, "DY_Heat": 0.40, "DY_QiDef": 0.50, "DY_YangDef": 0.50, "DY_YinDef": 0.45,
            "DY_FoodStag": 0.05, "DY_Phlegm": 0.40, "DY_QiStag": 0.40, "DY_BloodStasis": 0.50}},
        2: {"desc": "가끔 냄새", "weights": {
            "DY_Cold": 0.30, "DY_Heat": 0.35, "DY_QiDef": 0.30, "DY_YangDef": 0.30, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.25, "DY_Phlegm": 0.35, "DY_QiStag": 0.35, "DY_BloodStasis": 0.30}},
        3: {"desc": "트림시 냄새", "weights": {
            "DY_Cold": 0.15, "DY_Heat": 0.20, "DY_QiDef": 0.15, "DY_YangDef": 0.15, "DY_YinDef": 0.15,
            "DY_FoodStag": 0.40, "DY_Phlegm": 0.20, "DY_QiStag": 0.20, "DY_BloodStasis": 0.15}},
        4: {"desc": "부패취 심함", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.05, "DY_QiDef": 0.05, "DY_YangDef": 0.05, "DY_YinDef": 0.05,
            "DY_FoodStag": 0.25, "DY_Phlegm": 0.05, "DY_QiStag": 0.05, "DY_BloodStasis": 0.05}},
        5: {"desc": "극심한 부패취", "weights": {
            "DY_Cold": 0.00, "DY_Heat": 0.00, "DY_QiDef": 0.00, "DY_YangDef": 0.00, "DY_YinDef": 0.00,
            "DY_FoodStag": 0.05, "DY_Phlegm": 0.00, "DY_QiStag": 0.00, "DY_BloodStasis": 0.00}}
    },
    "dyspepsia_cold_limbs": {  # 수족냉증 - cold limbs (Yang Deficiency marker)
        1: {"desc": "손발 따뜻함", "weights": {
            "DY_Cold": 0.10, "DY_Heat": 0.50, "DY_QiDef": 0.30, "DY_YangDef": 0.05, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.40, "DY_Phlegm": 0.30, "DY_QiStag": 0.35, "DY_BloodStasis": 0.30}},
        2: {"desc": "약간 시림", "weights": {
            "DY_Cold": 0.25, "DY_Heat": 0.30, "DY_QiDef": 0.35, "DY_YangDef": 0.20, "DY_YinDef": 0.35,
            "DY_FoodStag": 0.35, "DY_Phlegm": 0.35, "DY_QiStag": 0.35, "DY_BloodStasis": 0.35}},
        3: {"desc": "손발 차가움", "weights": {
            "DY_Cold": 0.40, "DY_Heat": 0.15, "DY_QiDef": 0.25, "DY_YangDef": 0.40, "DY_YinDef": 0.25,
            "DY_FoodStag": 0.20, "DY_Phlegm": 0.30, "DY_QiStag": 0.25, "DY_BloodStasis": 0.30}},
        4: {"desc": "수족냉증 심함", "weights": {
            "DY_Cold": 0.20, "DY_Heat": 0.05, "DY_QiDef": 0.08, "DY_YangDef": 0.30, "DY_YinDef": 0.05,
            "DY_FoodStag": 0.05, "DY_Phlegm": 0.05, "DY_QiStag": 0.05, "DY_BloodStasis": 0.05}},
        5: {"desc": "극심 수족냉", "weights": {
            "DY_Cold": 0.05, "DY_Heat": 0.00, "DY_QiDef": 0.02, "DY_YangDef": 0.05, "DY_YinDef": 0.00,
            "DY_FoodStag": 0.00, "DY_Phlegm": 0.00, "DY_QiStag": 0.00, "DY_BloodStasis": 0.00}}
    },

    # ---------------------------------------------------------
    # ALLERGIC RHINITIS - FLUID RETENTION (수체형) - Page 23
    # Single unified pattern for rhinitis as per official doc
    # ---------------------------------------------------------
    "rhinitis_fluid_severity": {
        1: {"desc": "증상 없음", "weights": {"R_Fluid": 0.00}},
        2: {"desc": "경미 (Mild)", "weights": {"R_Fluid": 0.25}},
        3: {"desc": "중등도 (Moderate)", "weights": {"R_Fluid": 0.40}},
        4: {"desc": "심함 (Severe)", "weights": {"R_Fluid": 0.25}},
        5: {"desc": "매우 심함 (Very Severe)", "weights": {"R_Fluid": 0.10}}
    }
}

# ==========================================
# FINAL MERGE - ALL DATA (Including PART_5)
# ==========================================
CLINICAL_DATA.update(PART_5)  # Add PART_5 to CLINICAL_DATA

# Helper function to get all descriptions for a variable
def get_all_descs(variable):
    descs = []
    try:
        for level in CLINICAL_DATA[variable]:
            descs.append(CLINICAL_DATA[variable][level]['desc'])
    except:
        return []
    return descs

# Helper function to get all weights for a variable
def get_all_weights(variable):
    weights = []
    try:
        for level in CLINICAL_DATA[variable]:
            weights.append(CLINICAL_DATA[variable][level]['weights'])
    except:
        return []
    return weights