"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Batch Generation Script
변증유형별 균등 분배 환자 케이스 생성 (Harmonized Pattern Distribution)
═══════════════════════════════════════════════════════════════════════════════

분배 규칙 (Professor Lee's Specification):
    - 감기: 100개 × 2변증 (풍한형, 풍열형) = 200개
    - 알레르기비염: 40개 × 5변증 = 200개
    - 기능성소화불량: 30개 × 9변증 = 270개
    - 요통: 30개 × 9변증 = 270개
    - 총 940개 케이스

사용법:
    python batch_generator.py                # 전체 생성 (변증별 균등 분배)
    python batch_generator.py --test         # 테스트 (변증당 1개씩)
    python batch_generator.py -d 감기        # 특정 질환만 생성
    python batch_generator.py --random       # 랜덤 분배 (이전 방식)

출력:
    output/
    ├── 감기/
    │   ├── 감기_풍한형_001.pdf ~ 감기_풍한형_100.pdf
    │   ├── 감기_풍열형_001.pdf ~ 감기_풍열형_100.pdf
    │   └── 감기_전체.pdf (통합본)
    ├── 알레르기비염/
    │   ├── 알레르기비염_월비가반_001.pdf ~ ...
    │   └── ...
    ├── 기능성소화불량/
    │   └── ...
    └── 요통/
        └── ...
"""

import os
import sys
import time
import json
import hashlib
import warnings
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

# Suppress font subsetting warnings (harmless - from fonttools library)
warnings.filterwarnings("ignore", message=".*MERG.*subset.*")
warnings.filterwarnings("ignore", category=UserWarning, module="fontTools")
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from google import genai
from fpdf import FPDF

# Import project modules
from randomizer import randomize_inputs, randomize_from_csv_rules
from constraints import apply_all_constraint_rules
from pdf_generator import generate_patient_pdf_korean
from mock_session import MockSessionState, MockStreamlit
from batch_prompt_builder import generate_scenario_with_gemini, GEMINI_MODEL


# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

DISEASES = ["감기", "알레르기비염", "기능성 소화불량", "요통"]
CASES_PER_DISEASE = 200
OUTPUT_DIR = Path("output")
API_DELAY = 1.5  # Seconds between API calls to avoid rate limiting

# Disease name mapping (display name -> CSV key name)
DISEASE_NAME_MAP = {
    "감기": "감기",
    "알레르기비염": "알레르기비염",
    "기능성 소화불량": "기능성소화불량",  # CSV uses no space
    "요통": "요통",
}

# Pattern-based case distribution (Professor Lee's request)
# Each disease has equal cases per pattern type
PATTERN_DISTRIBUTION = {
    "감기": {
        "cases_per_pattern": 100,  # 100 cases × 2 patterns = 200 total
        "patterns": ["풍한형", "풍열형"]
    },
    "알레르기비염": {
        "cases_per_pattern": 40,  # 40 cases × 5 patterns = 200 total
        "patterns": ["월비가반하탕", "사간마황탕", "소청룡탕", "영감강미신하인탕", "마황부자세신탕"]
    },
    "기능성 소화불량": {
        "cases_per_pattern": 30,  # 30 cases × 9 patterns = 270 total
        "patterns": ["한증형", "열증형", "기허형", "양허형", "음허형", "식적형", "담음형", "기체형", "어혈형"]
    },
    "요통": {
        "cases_per_pattern": 30,  # 30 cases × 9 patterns = 270 total
        "patterns": ["한증형", "열증형", "기허형", "양허형", "음허형", "식적형", "담음형", "기체형", "어혈형"]
    }
}

def normalize_disease_name(disease: str) -> str:
    """Normalize disease name to match CSV_PATHS keys."""
    return DISEASE_NAME_MAP.get(disease, disease.replace(" ", ""))


# ═══════════════════════════════════════════════════════════════════════════════
# Patient Generator
# ═══════════════════════════════════════════════════════════════════════════════

def generate_patient_hash(session: MockSessionState) -> str:
    """Generate a hash to check for duplicate patients.
    
    Uses many randomized fields to ensure uniqueness across all generated cases.
    With ~30 fields including continuous values (age, height, weight, vitals),
    the probability of collision is effectively zero.
    """
    # Extended key fields for better uniqueness - includes all major randomized fields
    key_fields = [
        # Demographics
        'age', 'sex', 'disease', 'pattern_idx', 'job',
        # Vitals (continuous values provide high entropy)
        'height', 'weight', 'sbp', 'dbp', 'pulse_rate', 'temp', 'resp',
        # Pulse/tongue diagnosis
        'pulse_depth', 'pulse_width', 'pulse_strength', 'pulse_smooth', 'compound_pulse',
        'tongue_color', 'tongue_size', 'tongue_coat_color', 'tongue_coat_thick',
        # Sleep/lifestyle
        'sleep_hours', 'insomnia_onset', 'insomnia_maintain',
        # Excretion
        'stool_freq', 'urine_freq_day', 'urine_freq_night',
        # Symptoms
        'fever_sev', 'chills_sev', 'cough_sev', 'pain_sev',
        # Other randomized
        'onset', 'course', 'face_color'
    ]
    data = {k: session.get(k) for k in key_fields}
    return hashlib.md5(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()


def generate_unique_patient(disease: str, existing_hashes: set, pattern_idx: int = None, max_attempts: int = 50) -> Optional[MockSessionState]:
    """Generate a unique patient for the given disease and pattern.
    
    Args:
        disease: Disease name
        existing_hashes: Set of existing patient hashes for uniqueness checking
        pattern_idx: Specific pattern index to use (for harmonized generation)
        max_attempts: Maximum attempts to generate unique patient
    """
    
    # Normalize disease name for CSV lookup
    csv_disease_name = normalize_disease_name(disease)
    
    for attempt in range(max_attempts):
        # Create mock streamlit
        st_mock = MockStreamlit()
        session = st_mock.session_state
        
        # Set disease
        session.disease = disease
        
        # Set pattern index if specified (for harmonized distribution)
        if pattern_idx is not None:
            session.pattern_idx = pattern_idx
        
        # Randomize all fields (but keep disease fixed for batch generation)
        randomize_inputs(st_mock, randomize_disease=False)
        
        # Randomize from CSV rules for the disease (use normalized name)
        randomize_from_csv_rules(st_mock, csv_disease_name)
        
        # Force pattern index if specified (override randomization)
        if pattern_idx is not None:
            session.pattern_idx = pattern_idx
        
        # Apply all constraints
        apply_all_constraint_rules(st_mock)
        
        # Check uniqueness
        patient_hash = generate_patient_hash(session)
        if patient_hash not in existing_hashes:
            existing_hashes.add(patient_hash)
            return session
    
    print(f"  ⚠️ Could not generate unique patient after {max_attempts} attempts")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# Gemini API Integration
# ═══════════════════════════════════════════════════════════════════════════════

def setup_gemini():
    """Setup Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # Try to load from .env or secrets
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY"):
                        api_key = line.split("=", 1)[1].strip().strip('"\'')
                        break
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found!")
        print("   Set it as environment variable or create .env file")
        sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    return client


# ═══════════════════════════════════════════════════════════════════════════════
# PDF Generation
# ═══════════════════════════════════════════════════════════════════════════════

def create_patient_pdf(session: MockSessionState, summary: str, scenario: str, output_path: Path) -> bool:
    """Create PDF for a single patient."""
    
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
    
    try:
        pdf_bytes = generate_patient_pdf_korean(summary, scenario, patient_info)
        
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        return True
    except Exception as e:
        print(f"  ❌ PDF creation error: {e}")
        return False


def merge_pdfs(pdf_files: list, output_path: Path):
    """Merge multiple PDFs into one."""
    try:
        from PyPDF2 import PdfMerger
        
        merger = PdfMerger()
        for pdf_file in pdf_files:
            if pdf_file.exists():
                merger.append(str(pdf_file))
        
        merger.write(str(output_path))
        merger.close()
        print(f"  ✅ Merged PDF: {output_path}")
        
    except ImportError:
        print("  ⚠️ PyPDF2 not installed. Skipping merge.")
        print("     Install with: pip install PyPDF2")
    except Exception as e:
        print(f"  ❌ Merge error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main Batch Generation
# ═══════════════════════════════════════════════════════════════════════════════

def batch_generate(diseases: list = None, cases_per_disease: int = None, start_from: int = 1, use_pattern_distribution: bool = True):
    """
    Main batch generation function with harmonized pattern distribution.
    
    Args:
        diseases: List of diseases to generate (default: all 4)
        cases_per_disease: Number of cases per disease (only used if use_pattern_distribution=False)
        start_from: Starting case number (for resuming)
        use_pattern_distribution: If True, use PATTERN_DISTRIBUTION for harmonized generation
    """
    diseases = diseases or DISEASES
    cases_per_disease = cases_per_disease or CASES_PER_DISEASE
    
    # Calculate total cases
    if use_pattern_distribution:
        total_cases = 0
        for d in diseases:
            if d in PATTERN_DISTRIBUTION:
                dist = PATTERN_DISTRIBUTION[d]
                total_cases += dist["cases_per_pattern"] * len(dist["patterns"])
    else:
        total_cases = len(diseases) * cases_per_disease
    
    print("═" * 60)
    print("  TKM Patient Generator - Batch Generation")
    print("═" * 60)
    print(f"  질환: {', '.join(diseases)}")
    
    if use_pattern_distribution:
        print(f"  ⚖️ 변증유형별 균등 분배 모드")
        for d in diseases:
            if d in PATTERN_DISTRIBUTION:
                dist = PATTERN_DISTRIBUTION[d]
                num_patterns = len(dist["patterns"])
                cpp = dist["cases_per_pattern"]
                print(f"     - {d}: {cpp}개 × {num_patterns}변증 = {cpp * num_patterns}개")
    else:
        print(f"  질환당 케이스: {cases_per_disease}")
    
    print(f"  총 케이스: {total_cases}")
    print("═" * 60)
    
    # Setup Gemini
    print("\n🔧 Setting up Gemini API...")
    model = setup_gemini()
    print("  ✅ Gemini API ready")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Track statistics
    total_generated = 0
    total_failed = 0
    start_time = datetime.now()
    
    for disease in diseases:
        print(f"\n{'─' * 60}")
        print(f"📋 Generating: {disease}")
        print(f"{'─' * 60}")
        
        # Create disease folder
        disease_folder = OUTPUT_DIR / disease.replace(" ", "")
        disease_folder.mkdir(exist_ok=True)
        
        # Track unique patients
        existing_hashes = set()
        pdf_files = []
        
        if use_pattern_distribution and disease in PATTERN_DISTRIBUTION:
            # Harmonized generation by pattern
            dist = PATTERN_DISTRIBUTION[disease]
            patterns = dist["patterns"]
            cases_per_pattern = dist["cases_per_pattern"]
            
            # Track PDFs by pattern for per-pattern merging
            pattern_pdf_files = {}
            
            case_num = 0
            for pattern_idx, pattern_name in enumerate(patterns):
                print(f"\n  📌 변증 {pattern_idx + 1}/{len(patterns)}: {pattern_name} ({cases_per_pattern}개)")
                
                # Create pattern subfolder
                pattern_folder = disease_folder / pattern_name
                pattern_folder.mkdir(exist_ok=True)
                pattern_pdf_files[pattern_name] = []
                
                for i in range(cases_per_pattern):
                    case_num += 1
                    print(f"\n    [{case_num}] {pattern_name} #{i+1}...", end=" ")
                    
                    # Generate unique patient with specific pattern
                    session = generate_unique_patient(disease, existing_hashes, pattern_idx=pattern_idx)
                    if not session:
                        total_failed += 1
                        continue
                    
                    print(f"✓ ", end="")
                    
                    # Generate scenario with Gemini
                    print("Gemini...", end=" ")
                    summary, scenario = generate_scenario_with_gemini(model, session)
                    
                    if not scenario:
                        total_failed += 1
                        print("❌")
                        continue
                    
                    print(f"✓ ", end="")
                    
                    # Create PDF in pattern subfolder
                    pdf_filename = f"{disease.replace(' ', '')}_{pattern_name}_{i+1:03d}.pdf"
                    pdf_path = pattern_folder / pdf_filename
                    
                    print("PDF...", end=" ")
                    if create_patient_pdf(session, summary, scenario, pdf_path):
                        pdf_files.append(pdf_path)
                        pattern_pdf_files[pattern_name].append(pdf_path)
                        total_generated += 1
                        print(f"✓ {pdf_filename}")
                    else:
                        total_failed += 1
                        print("❌")
                    
                    # Rate limiting
                    time.sleep(API_DELAY)
        else:
            # Original generation (random patterns)
            for case_num in range(start_from, cases_per_disease + 1):
                print(f"\n  [{case_num}/{cases_per_disease}] Generating patient...", end=" ")
                
                # Generate unique patient
                session = generate_unique_patient(disease, existing_hashes)
                if not session:
                    total_failed += 1
                    continue
                
                print(f"✓ ", end="")
                
                # Generate scenario with Gemini
                print("Calling Gemini...", end=" ")
                summary, scenario = generate_scenario_with_gemini(model, session)
                
                if not scenario:
                    total_failed += 1
                    print("❌")
                    continue
                
                print(f"✓ ", end="")
                
                # Create PDF
                pdf_filename = f"{disease.replace(' ', '')}_{case_num:03d}.pdf"
                pdf_path = disease_folder / pdf_filename
                
                print("Creating PDF...", end=" ")
                if create_patient_pdf(session, summary, scenario, pdf_path):
                    pdf_files.append(pdf_path)
                    total_generated += 1
                    print(f"✓ {pdf_filename}")
                else:
                    total_failed += 1
                    print("❌")
                
                # Rate limiting
                time.sleep(API_DELAY)
        
        # Merge all PDFs for this disease
        if pdf_files:
            print(f"\n  📚 Merging {len(pdf_files)} PDFs...")
            merged_path = disease_folder / f"{disease.replace(' ', '')}_전체.pdf"
            merge_pdfs(pdf_files, merged_path)
    
    # Final statistics
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "═" * 60)
    print("  Generation Complete!")
    print("═" * 60)
    print(f"  ✅ Generated: {total_generated}")
    print(f"  ❌ Failed: {total_failed}")
    print(f"  ⏱️  Duration: {duration}")
    print(f"  📁 Output: {OUTPUT_DIR.absolute()}")
    print("═" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch generate TKM patient cases")
    parser.add_argument("--disease", "-d", type=str, help="Single disease to generate")
    parser.add_argument("--count", "-n", type=int, default=200, help="Cases per disease (default: 200)")
    parser.add_argument("--start", "-s", type=int, default=1, help="Starting case number (for resuming)")
    parser.add_argument("--test", "-t", action="store_true", help="Test mode: generate 1 case per pattern")
    parser.add_argument("--random", "-r", action="store_true", help="Use random pattern distribution (not harmonized)")
    
    args = parser.parse_args()
    
    if args.test:
        # Test mode: 1 case per pattern (harmonized)
        print("🧪 TEST MODE: Generating 1 case per pattern (harmonized)")
        # Temporarily override PATTERN_DISTRIBUTION for test
        for disease in PATTERN_DISTRIBUTION:
            PATTERN_DISTRIBUTION[disease]["cases_per_pattern"] = 1
        batch_generate(use_pattern_distribution=True)
    elif args.disease:
        # Single disease
        if args.disease not in DISEASES:
            print(f"❌ Unknown disease: {args.disease}")
            print(f"   Available: {', '.join(DISEASES)}")
            sys.exit(1)
        batch_generate(
            diseases=[args.disease], 
            cases_per_disease=args.count, 
            start_from=args.start,
            use_pattern_distribution=not args.random
        )
    else:
        # All diseases with harmonized pattern distribution
        batch_generate(
            cases_per_disease=args.count, 
            start_from=args.start,
            use_pattern_distribution=not args.random
        )
