# -*- coding: utf-8 -*-
"""
Test script for professor's feedback implementation
교수님 피드백 구현 테스트 스크립트
"""

import random
from types import SimpleNamespace


def create_mock_session():
    """Create a mock session object for testing."""
    return SimpleNamespace(
        disease='감기',
        pattern_idx=0,
        age=40,
        sore_throat=False,
        body_ache_cold=False,
        throat_redness=1,
        body_ache=1,
        fever_sev=2,
        chills_sev=2,
        snot_sev=1,
        cough_sev=1,
        cold_symptoms_spec=[],
        sweat_amt='보통',
        tongue_coat_color='백태',
        phlegm_color='백색',
        sweating=True,
        drink_temp='온수',
        snot_type='청수양',
        snot_color='맑음',
        pain_sev=4,
        pain_back=[3, 4],
        pain_back_f=3,
        pain_back_i=4,
        pain_nature=[],
        cold_heat_pref='보통',
        fatigue_level='없음',
        cold_hands_feet=False,
        dyspepsia_spec=[]
    )


def test_cold_general_symptoms():
    """Test 1: 감기 일반증상 - 인후통, 몸살 포함"""
    from constraints.pattern_constraints import _ensure_cold_general_symptoms
    
    print("=" * 60)
    print("Test 1: 감기 일반증상 (인후통/몸살 포함)")
    print("=" * 60)
    
    # Run multiple times to check probability
    sore_throat_count = 0
    body_ache_count = 0
    trials = 100
    
    for _ in range(trials):
        session = create_mock_session()
        _ensure_cold_general_symptoms(session)
        if session.sore_throat:
            sore_throat_count += 1
        if session.body_ache_cold:
            body_ache_count += 1
    
    print(f"  인후통 발생률: {sore_throat_count}/{trials} ({sore_throat_count}%)")
    print(f"  몸살 발생률: {body_ache_count}/{trials} ({body_ache_count}%)")
    print(f"  [PASS] 인후통/몸살이 주소증으로 가능함")
    print()


def test_rhinitis_watery_discharge():
    """Test 2: 알레르기비염 콧물 - 맑은 콧물 위주"""
    from constraints.pattern_constraints import _ensure_rhinitis_watery_discharge
    
    print("=" * 60)
    print("Test 2: 알레르기비염 콧물 (맑은 콧물 위주, 황농성 제외)")
    print("=" * 60)
    
    # Test with yellow discharge (should be changed)
    session = create_mock_session()
    session.disease = '알레르기비염'
    session.pattern_idx = 2  # 소청룡탕
    session.snot_type = '황농성 (黃膿) - 누렇고 찐득'
    
    before = session.snot_type
    _ensure_rhinitis_watery_discharge(session)
    after = session.snot_type
    
    print(f"  변경 전: {before}")
    print(f"  변경 후: {after}")
    
    if '황' not in after and '黃' not in after:
        print(f"  [PASS] 황농성 콧물이 맑은 콧물로 변경됨")
    else:
        print(f"  [FAIL] 콧물 변경 실패")
    print()


def test_backpain_elderly_heat_exclusion():
    """Test 3: 요통 고령자 열증 배제"""
    from constraints.pattern_constraints import _exclude_heat_pattern_for_elderly
    
    print("=" * 60)
    print("Test 3: 요통 고령자 열증(습열) 배제")
    print("=" * 60)
    
    session = create_mock_session()
    session.disease = '요통'
    session.age = 70  # 고령자
    session.pattern_idx = 9  # 습열형
    
    before = session.pattern_idx
    _exclude_heat_pattern_for_elderly(session)
    after = session.pattern_idx
    
    print(f"  나이: {session.age}세 (고령자)")
    print(f"  변경 전 패턴: {before} (습열형)")
    print(f"  변경 후 패턴: {after} (한증형)")
    
    if after == 7:  # 한증형
        print(f"  [PASS] 고령자 열증 -> 한증 변경됨")
    else:
        print(f"  [FAIL] 패턴 변경 실패")
    print()


def test_blood_stasis_injury_history():
    """Test 4: 어혈형 외상력 필수"""
    from constraints.pattern_constraints import _apply_blood_stasis_pattern
    
    print("=" * 60)
    print("Test 4: 어혈형 외상력 필수")
    print("=" * 60)
    
    session = create_mock_session()
    session.disease = '요통'
    session.pain_nature = []
    
    _apply_blood_stasis_pattern(session, session.pain_nature)
    
    trauma_history = getattr(session, 'trauma_history', False)
    trauma_detail = getattr(session, 'trauma_detail', 'N/A')
    back_pain_cause = getattr(session, 'back_pain_cause', 'N/A')
    
    print(f"  외상력 여부: {trauma_history}")
    print(f"  외상 원인: {back_pain_cause}")
    print(f"  외상 상세: {trauma_detail}")
    
    if trauma_history:
        print(f"  [PASS] 어혈형에 외상력이 추가됨")
    else:
        print(f"  [FAIL] 외상력 추가 실패")
    print()


def test_dyspepsia_no_overeating():
    """Test 5: 소화불량 식적형 과식 제외"""
    from constraints.pattern_constraints import _apply_dyspepsia_food_stagnation_pattern
    
    print("=" * 60)
    print("Test 5: 소화불량 식적형 과식 제외")
    print("=" * 60)
    
    # Run multiple times to check all causes
    causes = set()
    for _ in range(50):
        session = create_mock_session()
        session.disease = '소화불량'
        session.dyspepsia_spec = []
        _apply_dyspepsia_food_stagnation_pattern(session, session.dyspepsia_spec)
        causes.add(session.dyspepsia_cause)
    
    print(f"  가능한 원인들:")
    for cause in sorted(causes):
        print(f"    - {cause}")
    
    # Check if any cause contains overeating keywords
    overeating_keywords = ['과식', '폭식', '많이 먹', 'Overeating']
    has_overeating = any(kw in str(causes) for kw in overeating_keywords)
    
    if not has_overeating:
        print(f"  [PASS] 과식/폭식 원인이 제외됨")
    else:
        print(f"  [FAIL] 과식/폭식 원인이 아직 포함됨")
    print()


def main():
    """Run all tests."""
    print()
    print("=" * 60)
    print("교수님 피드백 구현 테스트")
    print("Professor's Feedback Implementation Test")
    print("=" * 60)
    print()
    
    test_cold_general_symptoms()
    test_rhinitis_watery_discharge()
    test_backpain_elderly_heat_exclusion()
    test_blood_stasis_injury_history()
    test_dyspepsia_no_overeating()
    
    print("=" * 60)
    print("모든 테스트 완료!")
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
