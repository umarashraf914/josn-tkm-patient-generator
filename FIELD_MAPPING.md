# TKM Patient Generator - Field Mapping & Data Flow

## 🎯 Overview: What Happens When You Press "Randomize"

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    RANDOMIZATION DATA FLOW                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STEP 1: HARDCODED RANDOM (randomizer.py lines 720-950)                    │
│  ────────────────────────────────────────────────────────                  │
│  • Sets ALL fields with simple random.choice() / random.randint()          │
│  • NOT based on CSV probabilities                                          │
│  • Example: age = random.randint(20, 80)                                   │
│                                                                             │
│           ↓                                                                 │
│                                                                             │
│  STEP 2: CSV PROBABILITY OVERRIDE (for 감기/알레르기비염 only)              │
│  ────────────────────────────────────────────────────────────               │
│  • Calls _apply_csv_cold_randomization() or _apply_csv_rhinitis_...()      │
│  • OVERWRITES some Step 1 values with CSV-based probabilities              │
│  • Uses data/gamgi_rules.csv or data/allergic_rhinitis_rules.csv           │
│                                                                             │
│           ↓                                                                 │
│                                                                             │
│  STEP 3: CONSTRAINT RULES (constraints/ folder)                            │
│  ────────────────────────────────────────────────                          │
│  • May MODIFY values to ensure clinical consistency                        │
│  • 6 sub-modules applied in order                                          │
│                                                                             │
│           ↓                                                                 │
│                                                                             │
│  STEP 4: CORRELATION RULES                                                 │
│  ────────────────────────────────────────────                              │
│  • Applies symptom correlations (fever↔chills, etc.)                       │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Field Source Mapping

### Legend:
- 🟢 **CSV** = Value comes from CSV probability rules (GOOD - uses your data!)
- 🟡 **HARDCODED** = Value from random.choice/randint (NOT using CSV)
- 🔵 **CONSTRAINT** = Value may be modified by constraint rules
- ⚪ **UNUSED** = In CSV but not mapped to app

---

### 1. 인구학적정보 (Demographics)

| App Variable | CSV Key | Source | UI Status | Notes |
|-------------|---------|--------|-----------|-------|
| `age` | `인구학적 정보_..._나이` | 🟢 CSV | ✅ Shown | Age range mapped |
| `sex` | `인구학적 정보_..._성별` | 🟢 CSV | ✅ Shown | Male/Female |
| `job` | `인구학적 정보_..._직업` | 🟢 CSV | ✅ Shown | 11 job categories |
| `height` | `인구학적 정보_..._키` | 🟢 CSV | ✅ Shown | Height range mapped |
| `weight` | `인구학적 정보_..._몸무게` | 🟢 CSV | ✅ Shown | Weight range mapped |

---

### 2. 활력징후 (Vital Signs)

| App Variable | CSV Key | Source | UI Status | Notes |
|-------------|---------|--------|-----------|-------|
| `temp` | `활력징후_..._체온` | 🟢 CSV → 🔵 CONSTRAINT | ✅ Shown | May be adjusted by fever consistency rule |
| `pulse_rate` | `활력징후_..._맥박` | 🟢 CSV | ✅ Shown | |
| `resp` | `활력징후_..._호흡` | 🟢 CSV | ✅ Shown | |
| `sbp` | `활력징후_..._혈압` | 🟢 CSV | ✅ Shown | Systolic BP |
| `dbp` | (derived) | 🟡 HARDCODED | ✅ Shown | Diastolic not in CSV separately |

---

### 3. 현병력/약물력/가족력 (History)

| App Variable | CSV Key | Source | Notes |
|-------------|---------|--------|-------|
| `history_conditions` | `현병력_활력징후_고혈압/당뇨/이상지질혈증` | 🟢 CSV | ✅ 15%/30%/45% |
| `meds_specific` | `약물력_활력징후_*` | 🟢 CSV | Linked to conditions |
| `family_hx` | `가족력_..._고혈압/당뇨/심장병/중풍` | 🟢 CSV | |

---

### 4. 사회력 (Social History)

| App Variable | CSV Key | Source | Notes |
|-------------|---------|--------|-------|
| `social_alcohol_freq` | `사회력_술_월간 음주 횟수` | 🟢 CSV | |
| `social_alcohol_amt` | `사회력_술_1회당 음주량` | 🟢 CSV | |
| `social_smoke_daily` | `사회력_담배_일간 개피` | 🟢 CSV | |
| `social_exercise_int` | `사회력_운동_운동 강도` | 🟢 CSV | |
| `social_exercise_time` | `사회력_운동_1회당 평균 운동 시간` | 🟢 CSV | |

---

### 5. 감기 주증상 (Cold Chief Symptoms) - 감기 ONLY

| App Variable | CSV Key | Source | Notes |
|-------------|---------|--------|-------|
| `fever_sev` | `감기환자_감기주소증 유형_발열` | 🟢 CSV | |
| `chills_sev` | `감기환자_감기주소증 유형_오한` | 🟢 CSV | |
| `snot_sev` | `감기환자_감기주소증 유형_콧물 감기` | 🟢 CSV | |
| `snot_color` | `감기환자_감기주소증 유형_콧물 색` | 🟢 CSV | |
| `nasal_congestion` | `감기환자_감기주소증 유형_코막힘` | 🟢 CSV | |
| `sore_throat` | `감기환자_감기주소증 유형_인후통` | 🟢 CSV | |
| `sneeze_sev` | `감기환자_감기주소증 유형_재채기` | 🟢 CSV | |
| `cough_sev` | `감기환자_감기주소증 유형_기침` | 🟢 CSV | |
| `phlegm_amt` | `감기환자_감기주소증 유형_담(가래) 양` | 🟢 CSV | |
| `phlegm_color` | `감기환자_감기주소증 유형_담(가래) 색` | 🟢 CSV | |
| `body_ache` | `감기환자_감기주소증 유형_몸살, 신체통, 근육통` | 🟢 CSV | |
| `headache` | `감기환자_감기주소증 유형_두부, 뒷목 불편감(강도)` | 🟢 CSV | |
| `sweat_during_cold` | `감기환자_감기주소증 유형_감기 시 땀 유무` | 🟢 CSV | |

---

### 6. 식사/대변/소변/수면 (Diet/Stool/Urine/Sleep)

| App Variable | CSV Key | Source | Notes |
|-------------|---------|--------|-------|
| `diet_speed` | `환자 현재 상태-식변면한한열_식사시간_1회 평균식사시간` | 🟢 CSV | |
| `appetite` | `환자 현재 상태-식변면한한열_소화여부_입맛` | 🟢 CSV | |
| `diet_freq` | `환자 현재 상태-식변면한한열_식사 량_1일 식사횟수` | 🟢 CSV | |
| `stool_freq` | `환자 현재 상태-식변면한한열_대변_대변 횟수` | 🟢 CSV | |
| `stool_form` | `환자 현재 상태-식변면한한열_대변_대변 굳기(형태)` | 🟢 CSV → 🔵 | May be adjusted |
| `urine_freq_day` | `환자 현재 상태-식변면한한열_소변_소변 횟수` | 🟢 CSV | |
| `urine_freq_night` | `환자 현재 상태-식변면한한열_소변_야간뇨 횟수` | 🟢 CSV | |
| `sleep_hours` | `환자 현재 상태-식변면한한열_수면_수면시간` | 🟢 CSV | |
| `sleep_depth` | `환자 현재 상태-식변면한한열_수면_수면깊이` | 🟢 CSV → 🔵 | May be adjusted |

---

### 7. Fields NOT Covered by CSV (Still Hardcoded)

These fields are set by `random.choice()` in Layer 1 and NOT overwritten by CSV:

| App Variable | Current Source | Notes |
|-------------|----------------|-------|
| `course` | 🟡 HARDCODED | "Worsening/Improving/Fluctuating" |
| `past_cold_problem_area` | 🟡 HARDCODED | Random sample from list |
| `aggravating_factors` | 🟡 HARDCODED | Random sample from list |
| `relieving_factors` | 🟡 HARDCODED | Random sample from list |
| `additional_symptoms` | 🟡 HARDCODED | Random sample |
| `additional_comorbidities` | 🟡 HARDCODED | Random sample |

---

## 📋 Constraint Rules (Layer 3)

These rules may MODIFY values after randomization:

### 1. KTAS Rules (`ktas_rules.py`)
- Emergency exclusion for patient safety
- Ensures vitals are within safe ranges

### 2. Consistency Rules (`consistency_rules.py`)
- **Fever↔Temperature**: High fever must have high temp
- **Women's Health**: Only for females 14-50
- **BMI↔Body**: Low BMI can't be "solid"
- **Sleep**: Short sleep = tired waking

### 3. Negative Correlation Rules (`negative_correlations.py`)
- Prevents illogical combinations
- Example: Can't have both "no sweating" and "excessive sweating"

### 4. Pattern Constraints (`pattern_constraints.py`)
- Disease-specific constraints
- 풍한형 vs 풍열형 differences

### 5. Correlation Rules (`correlation_rules.py`)
- Positive symptom correlations
- Example: High fever often means chills

### 6. Severity Descriptors (`severity_descriptors.py`)
- Adds Korean text descriptions for numeric values

---

## ✅ Verification: CSV Probabilities ARE Working

Test result (1000 patients):
```
고혈압 (Hypertension): 30.9% (Expected: 30%) ✅
당뇨 (Diabetes): 15.8% (Expected: 15%) ✅  
이상지질혈증 (Dyslipidemia): 44.6% (Expected: 45%) ✅
```

The CSV probability rules ARE being applied correctly!

---

## 🔧 Recommended Actions

1. **Remove hardcoded values for CSV-covered fields** in `randomizer.py`
2. **Add logging** to track which layer set each value
3. **Simplify the flow** by making CSV the single source of truth

---

## 📝 LLM Prompt Field Mapping (patient_generator.py)

All fields shown in the UI are passed to the LLM prompt for scenario generation:

### Section 1: 인구학적정보 및 활력징후
- `age`, `sex`, `job` ✅
- `height`, `weight`, BMI (calculated) ✅
- `onset`, `course` ✅
- `sbp`, `dbp`, `pulse_rate`, `temp`, `resp` ✅

### Section 2: 병력 및 생활습관
- `history_conditions`, `meds_specific`, `family_hx` ✅
- `aggravating_factors`, `relieving_factors` ✅
- `social_alcohol_freq`, `social_smoke_daily`, `social_exercise_int` ✅
- Women's health: `mens_cycle`, `mens_regular`, `mens_duration`, `mens_pain_score`, `mens_color` ✅

### Section 3: 배설 및 식사
- `diet_freq`, `diet_regular`, `water_intake` ✅
- `stool_freq`, `stool_color`, `stool_form` ✅
- `urine_color`, `urine_freq_day`, `urine_freq_night` ✅

### Section 4: 수면, 땀, 한열
- `sleep_hours`, `sleep_depth`, `sleep_waking_state` ✅
- `insomnia_onset`, `insomnia_maintain` ✅
- `sweat_amt`, `sweat_area` ✅
- `cold_heat_pref`, `drink_temp` ✅

### Section 5: 정신상태 및 신체검진
- `memory`, `motivation`, `stress_coping` ✅
- `edema`, `bruising`, `limb_weakness` ✅
- `skin_dry`, `skin_itch` ✅
- `tinnitus_sev`, `hearing_sev`, `dizziness_sev` ✅
- `face_color` ✅

### Section 6: 맥진 및 설진 소견
- `pulse_depth`, `pulse_width`, `pulse_strength`, `pulse_smooth` ✅
- `tongue_color`, `tongue_size` ✅
- `tongue_coat_color`, `tongue_coat_thick` ✅

### Section 7: 주소증 (Disease-specific)
**감기:**
- `fever_sev`, `chills_sev`, `snot_sev`, `cough_sev` ✅
- `snot_color`, `phlegm_amt`, `phlegm_color` ✅
- `cold_symptoms_spec`, `cold_chief_type`, `cold_onset_specific` ✅
- `sore_throat`, `body_ache_cold`, `body_heaviness_cold` ✅
- `headache_cold`, `neck_pain_cold`, `cold_dyspnea` ✅
- `cold_sweating_check`, `smell_reduction`, `alternating_chills_fever` ✅
- Exam findings: `exam_stethoscope`, `exam_throat_visual`, `exam_tongue_depressor`, `exam_rhinoscope_finding` ✅

**비염:**
- `sneeze_sev`, `nose_block_sev`, `nose_itch_sev`, `snot_sev` ✅
- `snot_type` ✅

**요통:**
- `pain_sev`, `pain_nature` ✅

**소화불량:**
- `pain_sev`, `dyspepsia_spec` ✅

### Section 8: 추가 증상 및 동반질환
- `additional_symptoms`, `additional_comorbidities` ✅

