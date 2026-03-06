"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Batch Generation Script
200 환자 케이스 × 4 질환 = 800 PDF 생성
═══════════════════════════════════════════════════════════════════════════════

사용법:
    python batch_generate.py

출력:
    output/
    ├── 감기/
    │   ├── patient_001.pdf
    │   ├── patient_002.pdf
    │   ├── ...
    │   └── 감기_전체.pdf (합본)
    ├── 알레르기비염/
    │   ├── patient_001.pdf
    │   ├── ...
    │   └── 알레르기비염_전체.pdf
    ├── 요통/
    │   └── ...
    └── 기능성소화불량/
        └── ...
"""

import os
import sys
import time
import json
import hashlib
import random
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google import genai
from fpdf import FPDF

# Global GenAI client
genai_client = None

# Import from existing modules
from config import DEFAULT_VALUES
from randomizer import randomize_all_fields
from patient_generator import generate_patient_prompt
from constraints import apply_all_constraint_rules
from pdf_generator import generate_patient_pdf_korean

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

# Gemini API Key - set your key here or use environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Number of patients per disease
PATIENTS_PER_DISEASE = 200

# Diseases to generate
DISEASES = ["감기", "알레르기비염", "요통", "기능성 소화불량"]

# Output directory
OUTPUT_DIR = Path("output")

# Rate limiting (requests per minute for Gemini API)
REQUESTS_PER_MINUTE = 15  # Gemini free tier limit
DELAY_BETWEEN_REQUESTS = 60 / REQUESTS_PER_MINUTE + 0.5  # Add buffer


# ═══════════════════════════════════════════════════════════════════════════════
# Mock Session State (simulates Streamlit session_state)
# ═══════════════════════════════════════════════════════════════════════════════

class MockSessionState:
    """Mock Streamlit session_state for batch processing."""
    
    def __init__(self):
        # Initialize with default values
        for key, value in DEFAULT_VALUES.items():
            setattr(self, key, value)
    
    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def __contains__(self, key):
        return hasattr(self, key)
    
    def to_dict(self):
        """Convert to dictionary for hashing/comparison."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class MockStreamlit:
    """Mock Streamlit module for constraint application."""
    
    def __init__(self):
        self.session_state = MockSessionState()


# ═══════════════════════════════════════════════════════════════════════════════
# Patient Generation
# ═══════════════════════════════════════════════════════════════════════════════

def generate_unique_hash(session) -> str:
    """Generate a hash to check for duplicate patients."""
    # Key fields that define uniqueness
    key_fields = [
        'age', 'sex', 'disease', 'pattern_name',
        'height', 'weight', 'job',
        'fever_sev', 'chills_sev', 'cough_sev', 'snot_sev',
        'compound_pulse', 'tongue_color',
        'cold_onset', 'sbp', 'dbp'
    ]
    
    data = {k: session.get(k, '') for k in key_fields}
    data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(data_str.encode()).hexdigest()


def generate_patient_data(disease: str, existing_hashes: set) -> tuple:
    """
    Generate a unique patient's randomized data.
    
    Returns:
        (MockStreamlit, hash) or (None, None) if duplicate
    """
    max_attempts = 10
    
    for _ in range(max_attempts):
        # Create mock streamlit
        st = MockStreamlit()
        st.session_state.disease = disease
        
        # Randomize all fields
        randomize_all_fields(st.session_state)
        
        # Apply all constraint rules
        apply_all_constraint_rules(st)
        
        # Check uniqueness
        patient_hash = generate_unique_hash(st.session_state)
        
        if patient_hash not in existing_hashes:
            return st, patient_hash
    
    return None, None


def call_gemini_api(prompt: str) -> str:
    """Call Gemini API to generate patient scenario."""
    try:
        response = genai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"  ⚠️ Gemini API 오류: {e}")
        return None


def extract_summary_and_scenario(response_text: str) -> tuple:
    """Extract summary and scenario from Gemini response."""
    if not response_text:
        return "요약 생성 실패", "시나리오 생성 실패"
    
    lines = response_text.strip().split('\n')
    
    # Find summary section
    summary = ""
    scenario = ""
    in_summary = False
    in_scenario = False
    
    for line in lines:
        if '요약' in line or 'Summary' in line:
            in_summary = True
            in_scenario = False
            continue
        elif '환자정보' in line or '【환자정보】' in line or '[환자정보]' in line:
            in_summary = False
            in_scenario = True
        
        if in_summary and line.strip():
            summary += line + "\n"
        elif in_scenario:
            scenario += line + "\n"
    
    # If parsing failed, use whole response as scenario
    if not scenario:
        scenario = response_text
    if not summary:
        # Generate simple summary from first few lines
        summary = '\n'.join(lines[:3])
    
    return summary.strip(), scenario.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# PDF Generation
# ═══════════════════════════════════════════════════════════════════════════════

def create_patient_pdf(session, summary: str, scenario: str, output_path: Path) -> bool:
    """Create a single patient PDF."""
    try:
        patient_info = {
            'disease': session.disease,
            'pattern': session.get('pattern_name', 'N/A'),
            'age': session.age,
            'sex': session.sex,
            'height': session.height,
            'weight': session.weight,
            'sbp': session.sbp,
            'dbp': session.dbp,
            'pulse_rate': session.pulse_rate,
            'temp': session.temp,
        }
        
        pdf_bytes = generate_patient_pdf_korean(summary, scenario, patient_info)
        
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        return True
    except Exception as e:
        print(f"  ⚠️ PDF 생성 오류: {e}")
        return False


def merge_pdfs(pdf_paths: list, output_path: Path):
    """Merge multiple PDFs into one combined PDF."""
    from PyPDF2 import PdfMerger
    
    merger = PdfMerger()
    
    for pdf_path in pdf_paths:
        if pdf_path.exists():
            merger.append(str(pdf_path))
    
    merger.write(str(output_path))
    merger.close()


# ═══════════════════════════════════════════════════════════════════════════════
# Main Batch Generation
# ═══════════════════════════════════════════════════════════════════════════════

def setup_output_directories():
    """Create output directory structure."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    for disease in DISEASES:
        disease_dir = OUTPUT_DIR / disease.replace(" ", "")
        disease_dir.mkdir(exist_ok=True)
    
    print(f"📁 출력 디렉토리 생성 완료: {OUTPUT_DIR}")


def generate_for_disease(disease: str, api_key: str):
    """Generate all patients for a single disease."""
    print(f"\n{'='*60}")
    print(f"🏥 {disease} 환자 생성 시작 ({PATIENTS_PER_DISEASE}명)")
    print(f"{'='*60}")
    
    disease_dir = OUTPUT_DIR / disease.replace(" ", "")
    existing_hashes = set()
    generated_pdfs = []
    
    # Configure Gemini
    global genai_client
    genai_client = genai.Client(api_key=api_key)
    
    for i in range(1, PATIENTS_PER_DISEASE + 1):
        print(f"\n[{i}/{PATIENTS_PER_DISEASE}] 환자 생성 중...")
        
        # 1. Generate unique patient data
        st, patient_hash = generate_patient_data(disease, existing_hashes)
        
        if st is None:
            print(f"  ⚠️ 고유한 환자 생성 실패, 건너뜀")
            continue
        
        existing_hashes.add(patient_hash)
        session = st.session_state
        
        print(f"  ✓ 환자 데이터: {session.age}세 {session.sex}, {session.get('pattern_name', 'N/A')}")
        
        # 2. Generate prompt
        prompt = generate_patient_prompt(session)
        
        # 3. Call Gemini API
        print(f"  → Gemini API 호출 중...")
        response = call_gemini_api(prompt)
        
        if response:
            # 4. Extract summary and scenario
            summary, scenario = extract_summary_and_scenario(response)
            
            # 5. Create PDF
            pdf_path = disease_dir / f"patient_{i:03d}.pdf"
            
            if create_patient_pdf(session, summary, scenario, pdf_path):
                generated_pdfs.append(pdf_path)
                print(f"  ✓ PDF 저장: {pdf_path.name}")
            
        # Rate limiting
        if i < PATIENTS_PER_DISEASE:
            print(f"  ⏳ API 대기 ({DELAY_BETWEEN_REQUESTS:.1f}초)...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Create combined PDF
    if generated_pdfs:
        print(f"\n📚 {disease} 합본 PDF 생성 중...")
        combined_path = disease_dir / f"{disease.replace(' ', '')}_전체.pdf"
        
        try:
            merge_pdfs(generated_pdfs, combined_path)
            print(f"  ✓ 합본 PDF 저장: {combined_path}")
        except ImportError:
            print("  ⚠️ PyPDF2 필요: pip install PyPDF2")
        except Exception as e:
            print(f"  ⚠️ 합본 실패: {e}")
    
    return len(generated_pdfs)


def main():
    """Main entry point for batch generation."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║          TKM Patient Generator - Batch Generation (800 환자)                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check API key
    api_key = GEMINI_API_KEY
    if not api_key:
        api_key = input("Gemini API Key를 입력하세요: ").strip()
        if not api_key:
            print("❌ API Key가 필요합니다.")
            return
    
    # Setup directories
    setup_output_directories()
    
    # Estimate time
    total_patients = PATIENTS_PER_DISEASE * len(DISEASES)
    estimated_minutes = (total_patients * DELAY_BETWEEN_REQUESTS) / 60
    print(f"\n⏱️ 예상 소요 시간: 약 {estimated_minutes:.0f}분 ({total_patients}명)")
    print(f"   (API 속도 제한: {REQUESTS_PER_MINUTE}회/분)")
    
    confirm = input("\n계속하시겠습니까? (y/n): ").strip().lower()
    if confirm != 'y':
        print("취소되었습니다.")
        return
    
    # Generate for each disease
    start_time = datetime.now()
    total_generated = 0
    
    for disease in DISEASES:
        count = generate_for_disease(disease, api_key)
        total_generated += count
    
    # Summary
    elapsed = datetime.now() - start_time
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              생성 완료!                                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  총 생성: {total_generated:4d} / {total_patients} 환자                                           ║
║  소요 시간: {str(elapsed).split('.')[0]}                                              ║
║  출력 위치: {str(OUTPUT_DIR):<50} ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
