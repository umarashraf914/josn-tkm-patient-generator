"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Prompts Package
LLM Prompt Templates for Patient Scenario Generation
═══════════════════════════════════════════════════════════════════════════════

This package contains:
- system_prompt: Main system prompt template
- disease_prompts: Disease-specific prompt sections
"""

from .system_prompt import build_system_prompt, get_output_format_instructions
from .disease_prompts import (
    get_cold_symptoms_section,
    get_rhinitis_symptoms_section,
    get_back_pain_symptoms_section,
    get_dyspepsia_symptoms_section
)

__all__ = [
    'build_system_prompt',
    'get_output_format_instructions',
    'get_cold_symptoms_section',
    'get_rhinitis_symptoms_section',
    'get_back_pain_symptoms_section',
    'get_dyspepsia_symptoms_section'
]
