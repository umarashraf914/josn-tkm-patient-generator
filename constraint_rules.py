"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Constraint Rules Bridge Module
═══════════════════════════════════════════════════════════════════════════════

This module serves as a bridge to the modular constraints package.
For new code, import directly from the constraints package:
    from constraints import apply_all_constraint_rules

This file maintains backward compatibility with existing code.
"""

# Import from the new modular constraints package
from constraints import (
    apply_all_constraint_rules,
    apply_ktas_rules,
    apply_consistency_rules,
    apply_negative_correlation_rules,
    apply_cold_constraints,
    apply_rhinitis_constraints,
    apply_back_pain_constraints,
    apply_dyspepsia_constraints,
    apply_symptom_correlation_rules
)


def apply_constraint_rules(st):
    """
    Apply all constraint rules. This is the main entry point.
    
    DEPRECATED: Use `from constraints import apply_all_constraint_rules` instead.
    
    Args:
        st: Streamlit module (uses st.session_state)
    """
    apply_all_constraint_rules(st)


# Re-export for backward compatibility
__all__ = [
    'apply_constraint_rules',
    'apply_symptom_correlation_rules',
    'apply_negative_correlation_rules',
    'apply_ktas_rules',
    'apply_consistency_rules',
    'apply_cold_constraints',
    'apply_rhinitis_constraints', 
    'apply_back_pain_constraints',
    'apply_dyspepsia_constraints'
]
