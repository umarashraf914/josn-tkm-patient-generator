"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Constraints Package
Based on Clinical Guidelines Pages 15-16, 25, 26, 27-35, 36-40
═══════════════════════════════════════════════════════════════════════════════

This package contains modular constraint rules:
- ktas_rules: Emergency exclusion rules (Page 25)
- consistency_rules: General clinical consistency rules
- negative_correlations: Negative correlation rules (Page 26) - prevent illogical combinations
- pattern_constraints: Disease-specific pattern constraints (Pages 15-16)
- correlation_rules: Symptom correlation rules (Pages 36-40)
- severity_descriptors: Severity level descriptions (Pages 27-35) - Korean 정량 표현
- pulse_rules: 맥진 규칙 - 질환별 허용 맥 및 복합맥 조합 규칙
"""

from .ktas_rules import apply_ktas_rules
from .consistency_rules import apply_consistency_rules
from .negative_correlations import apply_negative_correlation_rules
from .pattern_constraints import (
    apply_cold_constraints,
    apply_rhinitis_constraints,
    apply_back_pain_constraints,
    apply_dyspepsia_constraints
)
from .correlation_rules import apply_symptom_correlation_rules
from .severity_descriptors import (
    apply_severity_descriptions,
    get_severity_description,
    get_all_severity_descriptions
)
from .pulse_rules import (
    apply_pulse_rules,
    get_allowed_pulses,
    get_pulse_description,
    DISEASE_PULSE_MAP
)

__all__ = [
    'apply_ktas_rules',
    'apply_consistency_rules',
    'apply_negative_correlation_rules',
    'apply_cold_constraints',
    'apply_rhinitis_constraints',
    'apply_back_pain_constraints',
    'apply_dyspepsia_constraints',
    'apply_symptom_correlation_rules',
    'apply_severity_descriptions',
    'get_severity_description',
    'get_all_severity_descriptions',
    'apply_pulse_rules',
    'get_allowed_pulses',
    'get_pulse_description',
    'DISEASE_PULSE_MAP',
    'apply_all_constraint_rules'
]


def apply_all_constraint_rules(st):
    """
    Apply all constraint rules in the correct order.
    This is the main entry point for constraint application.
    
    Order:
    1. KTAS safety rules (critical - must be first)
    2. General Consistency Rules
    3. Negative Correlation Rules (Page 26 - prevent illogical combinations)
    4. Pulse Rules (맥진 규칙 - 질환별 허용 맥)
    5. Pattern-specific constraints (disease-specific)
    6. Symptom Correlation Rules (positive correlations)
    7. Severity Descriptions (Pages 27-35 - add Korean text descriptions)
    """
    session = st.session_state
    
    # 1. KTAS Emergency Exclusion (Critical - Patient Safety)
    apply_ktas_rules(session)
    
    # 2. General Consistency Rules
    apply_consistency_rules(session)
    
    # 3. Negative Correlation Rules (Page 26)
    # Prevent illogical combinations BEFORE pattern constraints
    apply_negative_correlation_rules(session)
    
    # 4. Pulse Rules (맥진 규칙)
    # Apply disease-specific pulse selection BEFORE pattern constraints
    apply_pulse_rules(session)
    
    # 5. Disease-Specific Pattern Constraints
    apply_cold_constraints(session)
    apply_rhinitis_constraints(session)
    apply_back_pain_constraints(session)
    apply_dyspepsia_constraints(session)
    
    # 6. Symptom Correlation Rules (positive correlations)
    apply_symptom_correlation_rules(session)
    
    # 7. Severity Descriptions (Pages 27-35)
    # Add Korean text descriptions for all numeric severity levels
    apply_severity_descriptions(session)
