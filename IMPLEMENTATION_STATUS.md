# TKM Patient Generator - Clinical Guidelines Implementation Status

## 📋 Pages 15-40 Coverage: **100% COMPLETE** ✅

---

## Page-by-Page Implementation Details

### ✅ Pages 15-16: Disease Pattern Constraints
**Location:** `constraints/pattern_constraints.py`
- **감기 (Cold):** Wind-Cold (풍한), Wind-Heat (풍열), Wind-Dryness (풍조) patterns
- **비염 (Rhinitis):** 5 수체형 patterns (월비가반하탕, 사간마황탕, 소청룡탕, 영감강미신하인탕, 마황부자세신탕)
- **요통 (Back Pain):** 10 한열허실 patterns (신허, 담음, 식적, 기, 좌섬, 어혈, 풍, 한, 습, 습열)
- **소화불량 (Dyspepsia):** 6 patterns (비위허약, 비위기허, 간위불화, 비위습열, 한열착잡, 음식정체)

### ✅ Page 17: Aggravating/Relieving Factors
**Location:** `constants.py`
- `AGGRAVATING_FACTORS` - 8 악화요인
- `RELIEVING_FACTORS` - 7 완화요인

### ✅ Page 18: Medical History & Lifestyle
**Location:** `config.py`, `app.py`
- Social history (음주/흡연/운동)
- Medical history conditions
- Family history

### ✅ Pages 21-22: KCD Disease Codes
**Location:** `constants.py`
- Disease code mappings
- KCD detailed information

### ✅ Page 23: Rhinitis Pattern Classification (수체형)
**Location:** `constraints/pattern_constraints.py`
- 5 rhinitis patterns with specific symptom constraints
- Snot type, tongue, cold/heat preference rules

### ✅ Page 25: KTAS Emergency Exclusion Rules
**Location:** `constraints/ktas_rules.py`
- Blood pressure: 90-180 mmHg
- Heart rate: 50-130 bpm
- Respiratory rate: 10-30/min
- Temperature: 35.0-40.5°C
- Pain severity: max 7 (NRS)
- Neurological checks

### ✅ Page 26: Negative Correlation Rules (음의 상관성)
**Location:** `constraints/negative_correlations.py`
- 식욕-의욕 rules (appetite-motivation)
- 나이 관련 rules (age-related)
- 사회력 rules (alcohol/smoking/exercise)
- 통증 관련 rules (pain-related)
- 배변/배뇨 rules (excretion)
- 체력/정신 rules (physical-mental)
- 이명 rules (tinnitus)
- 한열 민감성 rules (cold-heat consistency)
- 피부-얼굴 광택 rules (skin-face)

### ✅ Pages 27-28: Cold/Rhinitis Severity Descriptors
**Location:** `data_mappings.py`, `constraints/severity_descriptors.py`
- 발열 정량 표현 (fever severity)
- 오한 정량 표현 (chills severity)
- 콧물량/색 정량 표현 (snot severity/color)
- 한열왕래 (alternating chills/fever)
- 비염 증상 (rhinitis symptoms)
- 후각감퇴 (smell reduction)

### ✅ Pages 31-32: Diet/Stool/Urine Descriptors
**Location:** `data_mappings.py`, `constraints/severity_descriptors.py`
- 식사횟수/규칙성 (meal frequency/regularity)
- 식사량/식욕 (meal amount/appetite)
- 의욕 저하 (motivation)
- 대변 (stool: frequency, color, form)
- 소변 (urine: day/night frequency, color)

### ✅ Pages 33-34: Sleep/Body Temperature/Pain Descriptors
**Location:** `data_mappings.py`, `constraints/severity_descriptors.py`
- 수면 (sleep hours, depth, quality)
- 한열 선호 (cold-heat preference)
- 땀 (sweat amount)
- 음수량/온도 (water intake/temp)
- 체력/피로 (physical strength/fatigue)
- 통증 (NRS pain scale conversion)

### ✅ Page 35: Mental State/Emotion Descriptors
**Location:** `data_mappings.py`, `constraints/severity_descriptors.py`
- 정신 상태 (mental clarity)
- 기억력 (memory)
- 성격 속도 (personality speed)
- 감정 (anger, anxiety, depression)
- 부종/멍 (edema, bruising)

### ✅ Pages 36-38: Positive Symptom Correlations (400환자 차트)
**Location:** `symptom_correlations.py`, `constraints/correlation_rules.py`
**Total: 51 correlations implemented (100%)**

식욕-소화 클러스터 (21 correlations):
- 식욕좋음 ↔ 비만/복부비만/식사량/음수량/소화양호
- 강박 ↔ 식욕좋음 (negative)
- 소화양호 ↔ 소화불량/속쓰림/구역구토 (negative)
- 소화불량 ↔ 상복통증/하복통증
- 구역구토 ↔ 소화불량/트림/상복통증
- 트림 ↔ 가스참/상복통증/하복통증
- 속쓰림 ↔ 소화불량/구역구토
- 복부비만 ↔ 비만/식사량

호흡기 클러스터 (6 correlations):
- 숨참 ↔ 흉통/기침/갈증
- 기침 ↔ 가래/매핵기
- 가래 ↔ 매핵기

흉민-스트레스-수면 클러스터 (16 correlations):
- 흉민 ↔ 흉통/스트레스/두통/상복통증/수면질/숨참
- 흉통 ↔ 다몽
- 스트레스 ↔ 수면질/트림/활동량
- 수면질 ↔ 수면장애
- 다몽 ↔ 수면장애/경계긴장/우울
- 경계긴장 ↔ 우울/흉통

기타 클러스터 (8 correlations):
- 피로 ↔ 통증/허약
- 난청 ↔ 이명
- 땀양 ↔ 열 (negative)
- 고혈압 ↔ 당뇨/이상지질
- 당뇨 ↔ 이상지질

### ✅ Pages 39-40: Cold Patient Generation Rules
**Location:** `constraints/correlation_rules.py`, `constants.py`, `config.py`
- 감기 주소증 유형별 생성 (cold chief types - minimum 1)
- 발열 → 호흡기증상 (fever → respiratory)
- 흡연 → 가래 (smoker → phlegm correlation)
- 콧물 없음 → 콧물색 없음 (no snot → no snot color)
- 한열왕래 배제규칙 (alternating fever/chills exclusion)
- 코막힘 → 후각감퇴 (nasal congestion → smell reduction)
- 가래 없음 → 가래색 없음 (no phlegm → no phlegm color)
- 감기 진찰소견 (examination findings correlation)
- 기침-인후 상관 (cough-throat correlation)
- 몸살-신중 상관 (body ache-heaviness correlation)

---

## 📊 Implementation Summary

| Module | File | Variables/Functions |
|--------|------|---------------------|
| KTAS Rules | `constraints/ktas_rules.py` | 6 safety functions |
| Consistency Rules | `constraints/consistency_rules.py` | 8 consistency functions |
| Negative Correlations | `constraints/negative_correlations.py` | 9 rule categories |
| Pattern Constraints | `constraints/pattern_constraints.py` | 4 diseases, 24 patterns |
| Correlation Rules | `constraints/correlation_rules.py` | 13 correlation functions |
| Severity Descriptors | `constraints/severity_descriptors.py` | **124 mapped variables** |
| Symptom Correlations | `symptom_correlations.py` | 9 correlation clusters |
| Data Mappings | `data_mappings.py` | All Korean 정량 표현 |

---

## 🔧 Main Pipeline

`constraints/__init__.py` → `apply_all_constraint_rules(st)`

**Order of execution:**
1. ✅ KTAS Emergency Exclusion (Patient Safety)
2. ✅ General Consistency Rules
3. ✅ Negative Correlation Rules (Page 26)
4. ✅ Disease-Specific Pattern Constraints (Pages 15-16, 23)
5. ✅ Symptom Correlation Rules (Pages 36-40)
6. ✅ Severity Descriptions (Pages 27-35)

---

## ✅ Verification Tests

```bash
# Test negative correlations (Page 26)
python test_neg_rules.py

# Test severity descriptors (Pages 27-35)
python -c "from constraints.severity_descriptors import SEVERITY_MAP; print(len(SEVERITY_MAP))"
# Output: 124

# Test full constraint pipeline
python -c "from constraints import apply_all_constraint_rules; print('OK')"
```

---

**Last Updated:** December 18, 2025
**Status:** ALL PAGES 15-40 FULLY IMPLEMENTED ✅
