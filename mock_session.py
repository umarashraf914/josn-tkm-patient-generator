"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Mock Session State
Simulates Streamlit session_state for batch processing
═══════════════════════════════════════════════════════════════════════════════
"""

from session_defaults import SESSION_DEFAULTS


class MockSessionState:
    """Mock Streamlit session_state for batch processing."""
    
    def __init__(self):
        # Initialize with default values
        for key, value in SESSION_DEFAULTS.items():
            setattr(self, key, value)
        
        # Add missing attributes that might not be in SESSION_DEFAULTS
        self._ensure_defaults()
    
    def _ensure_defaults(self):
        """Ensure all required attributes exist."""
        # Women's health
        if not hasattr(self, 'mens_regular'):
            self.mens_regular = "규칙적"
        if not hasattr(self, 'mens_cycle'):
            self.mens_cycle = 28
        if not hasattr(self, 'mens_duration'):
            self.mens_duration = 5
        if not hasattr(self, 'mens_pain_score'):
            self.mens_pain_score = 3
        if not hasattr(self, 'mens_color'):
            self.mens_color = "적색"
        
        # Cold symptoms
        if not hasattr(self, 'fever_sev'):
            self.fever_sev = 2
        if not hasattr(self, 'chills_sev'):
            self.chills_sev = 2
        if not hasattr(self, 'snot_sev'):
            self.snot_sev = 2
        if not hasattr(self, 'cough_sev'):
            self.cough_sev = 2
        if not hasattr(self, 'sneeze_sev'):
            self.sneeze_sev = 2
        if not hasattr(self, 'nose_block_sev'):
            self.nose_block_sev = 2
        if not hasattr(self, 'nose_itch_sev'):
            self.nose_itch_sev = 2
        if not hasattr(self, 'pain_sev'):
            self.pain_sev = 3
        
        # Pattern
        if not hasattr(self, 'pattern_idx'):
            self.pattern_idx = 0
        if not hasattr(self, 'pattern_name'):
            self.pattern_name = "N/A"
        
        # Other common fields
        if not hasattr(self, 'cold_symptoms_spec'):
            self.cold_symptoms_spec = []
        if not hasattr(self, 'compound_pulse'):
            self.compound_pulse = "완맥"
    
    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def __getattr__(self, name):
        """Return sensible defaults for missing attributes."""
        # This is called when an attribute doesn't exist
        defaults = {
            'mens_regular': '규칙적',
            'mens_cycle': 28,
            'mens_duration': 5,
            'mens_pain_score': 3,
            'mens_pain': 3,
            'mens_color': '적색',
            'mens_amt': '보통',
            'vision_blackout': False,
            'pattern_idx': 0,
            'pattern_name': 'N/A',
            'compound_pulse': '완맥',
            'episode': '특별한 계기 없이 발생',
            'cold_symptoms_spec': [],
            'additional_symptoms': [],
            'additional_comorbidities': [],
            'aggravating_factors': [],
            'relieving_factors': [],
            'pain_nature': [],
            'dyspepsia_spec': [],
            'cold_chief_type': [],
            'snot_color': '투명',
            'snot_type': '맑음',
            'phlegm_amt': 0,
            'phlegm_color': '없음',
            'cold_onset_specific': 'N/A',
            'sore_throat': False,
            'body_ache_cold': False,
            'body_heaviness_cold': False,
            'headache_cold': False,
            'neck_pain_cold': False,
            'cold_dyspnea': False,
            'cold_sweating_check': False,
            'smell_reduction': 0,
            'alternating_chills_fever': 0,
            'exam_stethoscope': '정상',
            'exam_throat_visual': '정상',
            'exam_tongue_depressor': '정상',
            'exam_rhinoscope_finding': '정상',
            'cold_hands_feet': False,
            'sweat_feeling': '보통',
            # Back pain related
            'morning_stiffness': 0,
            'pain_worse_morning': False,
            'pain_worse_activity': False,
            'pain_worse_rest': False,
            'radiating_pain': False,
            'numbness': 0,
            'weakness_leg': 0,
        }
        if name in defaults:
            return defaults[name]
        # Return 0 for numeric-looking fields, False for bool-looking, empty list for list-looking
        if name.endswith('_sev') or name.endswith('_freq') or name.endswith('_score'):
            return 0
        if name.startswith('is_') or name.endswith('_check'):
            return False
        # Return None for unknown attributes
        return None
    
    def __delattr__(self, name):
        """Handle delattr gracefully - just ignore if attribute doesn't exist."""
        try:
            object.__delattr__(self, name)
        except AttributeError:
            pass  # Ignore if attribute doesn't exist
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __contains__(self, key):
        return hasattr(self, key)
    
    def to_dict(self):
        """Convert to dictionary for hashing/comparison."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class MockStreamlit:
    """Mock Streamlit module for constraint functions."""
    
    def __init__(self):
        self.session_state = MockSessionState()
