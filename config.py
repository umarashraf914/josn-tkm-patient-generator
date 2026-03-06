"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - Configuration & API Key Management
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import streamlit as st

# Re-export SESSION_DEFAULTS for backward compatibility
from session_defaults import SESSION_DEFAULTS

# --- 🔒 API KEY CONFIGURATION ---
# The API key is loaded from (in order of priority):
# 1. Streamlit secrets (for Streamlit Cloud deployment)
# 2. Environment variable GOOGLE_API_KEY (for local development)
# 3. .env file (optional, for local development)

def get_api_key():
    """
    Get the API key from Streamlit secrets or environment variables.
    Works for both local development and Streamlit Cloud deployment.
    """
    # 1. Try Streamlit secrets first (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
            return st.secrets['GOOGLE_API_KEY']
    except Exception:
        pass
    
    # 2. Try environment variable (for local development)
    api_key = os.environ.get('GOOGLE_API_KEY')
    if api_key:
        return api_key
    
    # 3. Try loading from .env file (optional local fallback)
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_API_KEY='):
                        return line.strip().split('=', 1)[1].strip('"\'')
    except Exception:
        pass
    
    # 4. Return placeholder if not found
    return "PASTE_YOUR_API_KEY_HERE"

# Load API key at module import
API_KEY = get_api_key()


def init_session_state(st):
    """Initialize Streamlit session state with defaults."""
    for key, val in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val
