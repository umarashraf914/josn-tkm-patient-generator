"""
═══════════════════════════════════════════════════════════════════════════════
TKM Batch Patient PDF Generator (Standalone CLI)

Generates N virtual patient PDFs using JSON probability distributions
and Gemini LLM, saved in organized folders by disease.

Usage:
    python batch_pdf_generator.py
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import time
from datetime import datetime

from json_patient_sampler import (
    sample_general_patient,
    sample_syndrome_patient,
    apply_correlation_constraints,
    get_syndrome_keys,
)
from prompt_builder import build_generation_prompt
from pdf_generator import generate_patient_pdf_korean
from config import get_api_key
from constants import DISEASE_PATTERNS


# ── Disease choices ──
DISEASES = {
    "1": ("감기",           "Common Cold (J06)"),
    "2": ("알레르기비염",    "Allergic Rhinitis (J30)"),
    "3": ("기능성소화불량",  "Functional Dyspepsia (K30)"),
    "4": ("요통",           "Low Back Pain (M54)"),
}

# Korean disease labels used in prompt builder
DISEASE_LABELS = {
    "감기":           "감기 J06 (Common Cold)",
    "알레르기비염":    "알레르기비염 J30 (Allergic Rhinitis)",
    "기능성소화불량":  "기능성소화불량 K30 (Functional Dyspepsia)",
    "요통":           "요통 M54 (Low Back Pain)",
}


def _init_gemini():
    """Initialize Gemini client."""
    api_key = get_api_key()
    if not api_key or api_key == "PASTE_YOUR_API_KEY_HERE":
        print("\n❌ API 키가 설정되지 않았습니다.")
        print("   .env 파일에 GOOGLE_API_KEY=your_key 를 추가하세요.")
        sys.exit(1)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client
    except ImportError:
        print("\n❌ google-genai 패키지가 설치되지 않았습니다.")
        print("   pip install google-genai")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Gemini 초기화 실패: {e}")
        sys.exit(1)


def _build_session_dict(sampled, disease_key):
    """Convert sampled dict to a session-like dict for prompt_builder."""
    session = dict(sampled)
    session["disease"] = DISEASE_LABELS.get(disease_key, disease_key)

    # Ensure critical keys have defaults
    defaults = {
        "age": 40, "sex": "남", "height": 170, "weight": 70,
        "sbp": 120, "dbp": 80, "temp": 36.5, "pulse_rate": 72, "resp": 18,
        "onset": "3일 전", "course": "", "episode": "",
        "history_conditions": [], "meds_specific": [], "family_hx": [],
        "additional_symptoms": "", "additional_comorbidities": "",
    }
    for k, v in defaults.items():
        if k not in session:
            session[k] = v

    return session


def _generate_one_patient(client, disease_key, patient_num, mode="general",
                          syndrome_key=None):
    """Sample one patient, call LLM, return (summary, scenario, patient_info)."""

    # 1. Sample from JSON probability distributions
    if mode == "syndrome" and syndrome_key:
        sampled = sample_syndrome_patient(disease_key, syndrome_key)
    else:
        sampled = sample_general_patient(disease_key)

    # 2. Apply correlation constraints
    sampled = apply_correlation_constraints(sampled)

    # 3. Build session dict for prompt builder
    session = _build_session_dict(sampled, disease_key)

    # 4. Build LLM prompt
    prompt = build_generation_prompt(session)

    # 5. Call Gemini
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
    except Exception as e:
        print(f"   ⚠ LLM 오류 (환자 #{patient_num}): {e}")
        return None

    summary = data.get("요약", "요약 없음")
    scenario = data.get("환자시나리오", data.get("초진기록", "기록 없음"))

    # Get pattern info
    selected_pattern = "일반"
    if disease_key in DISEASE_PATTERNS:
        patterns = DISEASE_PATTERNS[disease_key]["patterns"]
        if patterns:
            selected_pattern = patterns[0]["name"]

    patient_info = {
        "disease": DISEASE_LABELS.get(disease_key, disease_key),
        "pattern": selected_pattern,
        "age": session.get("age", "N/A"),
        "sex": session.get("sex", "N/A"),
        "height": session.get("height", "N/A"),
        "weight": session.get("weight", "N/A"),
        "sbp": session.get("sbp", "N/A"),
        "dbp": session.get("dbp", "N/A"),
        "pulse_rate": session.get("pulse_rate", "N/A"),
        "temp": session.get("temp", "N/A"),
    }

    return summary, scenario, patient_info


def _choose_disease():
    """Interactive disease selection."""
    print("\n╔══════════════════════════════════════════════╗")
    print("║   한의 가상환자 PDF 일괄 생성기               ║")
    print("╚══════════════════════════════════════════════╝\n")
    print("질환을 선택하세요:\n")
    for num, (kr, en) in DISEASES.items():
        print(f"  [{num}] {kr}  —  {en}")

    while True:
        choice = input("\n번호 입력 (1-4): ").strip()
        if choice in DISEASES:
            return DISEASES[choice][0]
        print("  ❌ 1~4 사이의 번호를 입력하세요.")


def _choose_count():
    """Interactive patient count selection."""
    while True:
        raw = input("\n생성할 환자 수 (1-100): ").strip()
        try:
            n = int(raw)
            if 1 <= n <= 100:
                return n
            print("  ❌ 1~100 사이의 숫자를 입력하세요.")
        except ValueError:
            print("  ❌ 숫자를 입력하세요.")


def _choose_mode(disease_key):
    """Choose general or syndrome mode."""
    syn_keys = get_syndrome_keys(disease_key)
    if not syn_keys:
        return "general", None

    print(f"\n샘플링 모드를 선택하세요:")
    print(f"  [1] 일반 (general) — 전체 확률분포 사용")
    print(f"  [2] 변증별 (syndrome) — 변증유형별 확률분포 사용")

    while True:
        choice = input("\n번호 입력 (1-2): ").strip()
        if choice == "1":
            return "general", None
        elif choice == "2":
            break
        print("  ❌ 1 또는 2를 입력하세요.")

    # Choose specific syndrome
    print(f"\n변증 유형을 선택하세요:")
    for i, sk in enumerate(syn_keys, 1):
        # Try to get a friendly name from DISEASE_PATTERNS
        label = sk
        if disease_key in DISEASE_PATTERNS:
            patterns = DISEASE_PATTERNS[disease_key]["patterns"]
            if i - 1 < len(patterns):
                label = f"{sk} ({patterns[i-1]['name']})"
        print(f"  [{i}] {label}")

    while True:
        raw = input(f"\n번호 입력 (1-{len(syn_keys)}): ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(syn_keys):
                return "syndrome", syn_keys[idx]
        except ValueError:
            pass
        print(f"  ❌ 1~{len(syn_keys)} 사이의 번호를 입력하세요.")


def main():
    """Main CLI entry point."""
    disease_key = _choose_disease()
    n = _choose_count()
    mode, syndrome_key = _choose_mode(disease_key)

    # Prepare output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_label = syndrome_key if syndrome_key else "general"
    out_dir = os.path.join("output", disease_key, f"{mode_label}_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  질환: {disease_key}")
    print(f"  모드: {mode} {'('+syndrome_key+')' if syndrome_key else ''}")
    print(f"  환자수: {n}명")
    print(f"  저장위치: {out_dir}")
    print(f"{'='*55}\n")

    # Initialize Gemini
    print("🔑 Gemini API 초기화 중...")
    client = _init_gemini()
    print("✅ Gemini API 연결 완료\n")

    # Generate patients
    success = 0
    failed = 0

    for i in range(1, n + 1):
        print(f"[{i}/{n}] 환자 생성 중...", end="", flush=True)
        t0 = time.time()

        result = _generate_one_patient(
            client, disease_key, i,
            mode=mode, syndrome_key=syndrome_key,
        )

        if result is None:
            failed += 1
            print(" ❌ 실패")
            continue

        summary, scenario, patient_info = result

        # Generate PDF
        try:
            pdf_bytes = generate_patient_pdf_korean(
                summary=summary,
                scenario=scenario,
                patient_info=patient_info,
            )

            # Save PDF
            filename = f"patient_{i:03d}.pdf"
            filepath = os.path.join(out_dir, filename)
            with open(filepath, "wb") as f:
                f.write(pdf_bytes)

            elapsed = time.time() - t0
            age = patient_info.get("age", "?")
            sex = patient_info.get("sex", "?")
            print(f" ✅ {age}세 {sex} ({elapsed:.1f}s) → {filename}")
            success += 1

        except Exception as e:
            failed += 1
            print(f" ❌ PDF 오류: {e}")

        # Small delay to respect API rate limits
        if i < n:
            time.sleep(0.5)

    # Summary
    print(f"\n{'='*55}")
    print(f"  완료!  성공: {success}명  |  실패: {failed}명")
    print(f"  저장 위치: {out_dir}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
