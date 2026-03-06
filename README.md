# 🏥 TKM Virtual Patient Generator

A Streamlit-based application for generating realistic Traditional Korean Medicine (TKM) clinical scenarios for medical education and training.

## Features

- **4 Disease Categories**: Common Cold (감기), Allergic Rhinitis (비염), Back Pain (요통), Functional Dyspepsia (소화불량)
- **KCD Code Compliant**: Follows official Korean Classification of Diseases (Pages 21-22)
- **Pattern-Based Diagnosis**: 한열허실 (Cold-Heat-Deficiency-Excess) classification (Page 23)
- **KTAS Emergency Exclusion**: Automatically excludes emergency-level vital signs
- **Comprehensive Clinical Variables**: 60+ variables from official TKM clinical documentation
- **CSV-Based Clinical Rules**: Official clinical generation rules for symptom distributions and pattern-specific probabilities

## Pattern Classifications

| Disease | Patterns | Representative Prescriptions |
|---------|----------|------------------------------|
| 감기 (Cold) | 풍한형, 풍열형 | 행소산, 삼소음, 은교산 |
| 비염 (Rhinitis) | 수체형 | 월비가반하탕, 소청룡탕 |
| 요통 (Back Pain) | 한/열/기허/양허/음허/식적/담음/기체/어혈 | 오적산, 팔미지황원 등 |
| 소화불량 (Dyspepsia) | 한/열/기허/양허/음허/식적/담음/기체/어혈 | 이진탕, 소적건비환 등 |

## Project Structure

```
tkm-patient-generator/
├── app.py                    # Main Streamlit application
├── randomizer.py             # Patient data randomization logic
├── generation_rules.py       # CSV-based clinical rule parsing
├── patient_generator.py      # LLM integration for scenario generation
├── data/                     # Clinical rule CSV files
│   ├── gamgi_rules.csv       # 감기 (Common Cold) rules
│   └── allergic_rhinitis_rules.csv  # 알레르기비염 rules
├── prompts/                  # LLM prompt templates
├── constraints/              # Symptom correlation and constraint rules
└── requirements.txt          # Python dependencies
```

## How to Use

1. Click "🎲 Randomize" to generate a new virtual patient
2. Adjust parameters in the sidebar
3. Click "Generate Clinical Scenario" to create AI-generated case

## Installation & Local Development

```bash
# Clone the repository
git clone https://github.com/your-repo/tkm-patient-generator.git
cd tkm-patient-generator

# Create virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## CSV Rule Files

The `data/` folder contains clinical rule CSV files that define:
- **Symptom options**: All possible values for each symptom
- **Patient expressions**: How patients describe each symptom
- **Base probabilities**: Overall distribution of each option
- **Pattern-specific probabilities**: Distribution for each 증형 (pattern)

### File Structure
| File | Disease | Patterns |
|------|---------|----------|
| `gamgi_rules.csv` | 감기 (Common Cold) | 풍한형, 풍열형 |
| `allergic_rhinitis_rules.csv` | 알레르기비염 | 월비가반하탕, 사간마황탕, 소청룡탕, 영강감미신하인탕, 마황부자세신탕 |

### Adding New Disease Rules
1. Create a new CSV file in the `data/` folder following the existing format
2. Add the file path to `CSV_PATHS` in `generation_rules.py`
3. Configure the column indices in `PATTERN_COLUMNS`
4. Update the symptom key mapping in `randomizer.py`

## Deployment (Streamlit Cloud / GitHub)

For deployment to Streamlit Cloud:

1. **Ensure CSV files are committed**: The `data/` folder with CSV files must be in your GitHub repository
2. **No additional configuration needed**: The app loads CSVs from relative paths
3. **Secrets**: Add your OpenAI API key to Streamlit secrets (`.streamlit/secrets.toml` locally, or via Streamlit Cloud dashboard)

```toml
# .streamlit/secrets.toml (not committed to git)
OPENAI_API_KEY = "sk-..."
```

### Troubleshooting Deployment
- If rules don't load, check that CSV files exist in `data/` folder
- Verify file encoding is UTF-8 with BOM (`utf-8-sig`)
- Check Streamlit Cloud logs for any import errors

## Deployment

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## License

For educational and research purposes only.

