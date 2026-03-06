"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - CSV-based Generation Rules
═══════════════════════════════════════════════════════════════════════════════
This module parses clinical generation rule CSVs and provides probability-based
patient data generation according to official clinical guidelines.

CSV Structure:
- 1.csv: 감기 (Common Cold) - 풍한형/풍열형 patterns
- 2.csv: 알레르기비염 (Allergic Rhinitis) - 5 prescription patterns

The CSV columns contain:
- Category, Subcategory, Item names
- Range numbers (1-N) for options
- Descriptions (qualitative and quantitative)
- Overall probability distribution
- Pattern-specific probability distributions
"""

import csv
import random
import os
from typing import Dict, List, Optional, Tuple, Any


# ============================================================================
# CSV PARSING CONFIGURATION
# ============================================================================

# CSV file paths (relative to this file, stored in data/ folder)
# For local development and deployment (Streamlit Cloud/GitHub), 
# the CSV files should be in the data/ folder within the project
CSV_PATHS = {
    "감기": os.path.join(os.path.dirname(__file__), "data", "gamgi_rules.csv"),
    "알레르기비염": os.path.join(os.path.dirname(__file__), "data", "allergic_rhinitis_rules.csv"),
    "기능성소화불량": os.path.join(os.path.dirname(__file__), "data", "dyspepsia_rules.csv"),
    "요통": os.path.join(os.path.dirname(__file__), "data", "backpain_rules.csv"),
}

# Pattern column indices in each CSV (0-indexed, after the base columns)
# For 감기 (1.csv): columns are [..., 감기환자 생성 규칙 및 비율, 풍한형, 풍열형]
PATTERN_COLUMNS = {
    "감기": {
        "base_prob_col": 9,  # "감기환자 생성 규칙 및 비율"
        "patterns": {
            "풍한형": 10,  # "풍한형 감기환자 생성 비율"
            "풍열형": 11,  # "풍열형 감기환자 생성 비율"
        }
    },
    # For 알레르기비염 (2.csv): columns are [..., 알레르기 비염 환자 생성 규칙 및 비율, 월비가반하탕, 사간마황탕, 소청룡탕, 영강감미신하인탕, 마황부자세신탕]
    "알레르기비염": {
        "base_prob_col": 9,  # "알레르기 비염 환자 생성 규칙 및 비율"
        "patterns": {
            "월비가반하탕": 10,
            "사간마황탕": 11,
            "소청룡탕": 12,
            "영강감미신하인탕": 13,
            "마황부자세신탕": 14,
        }
    },
    # For 기능성소화불량 (3.csv): 한증, 열증, 기허, 양허, 음허, 담음(습), 식적, 어혈, 기체
    "기능성소화불량": {
        "base_prob_col": 9,  # "일반 생성 규칙 및 비율"
        "patterns": {
            "한증형": 10,
            "열증형": 11,
            "기허형": 12,
            "양허형": 13,
            "음허형": 14,
            "담음형": 15,
            "식적형": 16,
            "어혈형": 17,
            "기체형": 18,
        }
    },
    # For 요통 (4.csv): 한증, 열증, 기허, 양허, 음허, 담음(습), 식적, 어혈, 기체
    "요통": {
        "base_prob_col": 9,  # "일반요통환자 생성 규칙 및 비율"
        "patterns": {
            "한증형": 10,
            "열증형": 11,
            "기허형": 12,
            "양허형": 13,
            "음허형": 14,
            "담음형": 15,
            "식적형": 16,
            "어혈형": 17,
            "기체형": 18,
        }
    }
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class SymptomOption:
    """Represents a single option for a symptom with its probabilities."""
    def __init__(self, 
                 option_number: int,
                 qualitative_desc: str,
                 quantitative_desc: str,
                 base_probability: float,
                 pattern_probabilities: Dict[str, float]):
        self.option_number = option_number
        self.qualitative_desc = qualitative_desc
        self.quantitative_desc = quantitative_desc
        self.base_probability = base_probability
        self.pattern_probabilities = pattern_probabilities
    
    def __repr__(self):
        return f"Option({self.option_number}: {self.quantitative_desc[:30]}... base={self.base_probability})"


class SymptomRule:
    """Represents a symptom with all its possible options and probabilities."""
    def __init__(self,
                 category: str,
                 subcategory: str,
                 item_name: str,
                 is_required: bool,
                 importance: int,
                 options: List[SymptomOption]):
        self.category = category
        self.subcategory = subcategory
        self.item_name = item_name
        self.is_required = is_required
        self.importance = importance  # 1=매우중요, 2=중요, 3=약간참고, 4=의미없음
        self.options = options
    
    @property
    def key(self) -> str:
        """Generate a unique key for this symptom."""
        parts = [p for p in [self.category, self.subcategory, self.item_name] if p]
        return "_".join(parts)
    
    def select_option(self, pattern: Optional[str] = None) -> SymptomOption:
        """
        Select an option based on probability weights.
        
        Args:
            pattern: If provided, use pattern-specific probabilities.
                    Otherwise, use base probabilities.
        
        Returns:
            Selected SymptomOption
        """
        if not self.options:
            return None
        
        # Get probabilities
        if pattern and pattern in self.options[0].pattern_probabilities:
            weights = [opt.pattern_probabilities.get(pattern, 0) for opt in self.options]
        else:
            weights = [opt.base_probability for opt in self.options]
        
        # Handle zero-weight edge case
        total = sum(weights)
        if total == 0:
            # Fallback to uniform distribution
            weights = [1.0] * len(self.options)
        
        # Select based on weights
        selected = random.choices(self.options, weights=weights, k=1)[0]
        return selected
    
    def __repr__(self):
        return f"SymptomRule({self.key}, {len(self.options)} options)"


class DiseaseRules:
    """Contains all generation rules for a specific disease."""
    def __init__(self, disease_name: str):
        self.disease_name = disease_name
        self.symptoms: Dict[str, SymptomRule] = {}
        self.patterns: List[str] = []
    
    def add_symptom(self, symptom: SymptomRule):
        """Add a symptom rule."""
        self.symptoms[symptom.key] = symptom
    
    def get_symptom(self, key: str) -> Optional[SymptomRule]:
        """Get a symptom rule by key."""
        return self.symptoms.get(key)
    
    def generate_patient_data(self, pattern: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate patient data for all symptoms based on rules.
        
        Args:
            pattern: Specific pattern to use for probabilities.
        
        Returns:
            Dictionary of symptom_key -> selected option data
        """
        result = {}
        for key, symptom in self.symptoms.items():
            selected = symptom.select_option(pattern)
            if selected:
                result[key] = {
                    "option_number": selected.option_number,
                    "qualitative": selected.qualitative_desc,
                    "quantitative": selected.quantitative_desc,
                    "category": symptom.category,
                    "subcategory": symptom.subcategory,
                    "item": symptom.item_name,
                    "importance": symptom.importance,
                }
        return result


# ============================================================================
# CSV PARSING
# ============================================================================

def parse_percentage(value: str) -> float:
    """Parse a percentage string like '50%' to float 0.5."""
    if not value or value.strip() == "":
        return 0.0
    value = value.strip().replace("%", "").replace(",", ".")
    try:
        return float(value) / 100.0
    except ValueError:
        return 0.0


def is_empty_value(value: str) -> bool:
    """Check if a value represents empty/no value (##name, #NAME?, #VALUE!, etc.)."""
    if not value:
        return True
    value = value.strip().upper()
    return value in ["", "#NAME?", "#VALUE!", "##NAME", "#NAME", "#REF!", "#N/A"]


def parse_csv_file(filepath: str, disease_name: str) -> DiseaseRules:
    """
    Parse a CSV file and extract all generation rules.
    
    Args:
        filepath: Path to the CSV file
        disease_name: Name of the disease (감기 or 알레르기비염)
    
    Returns:
        DiseaseRules object containing all parsed rules
    """
    rules = DiseaseRules(disease_name)
    config = PATTERN_COLUMNS.get(disease_name, {})
    patterns = list(config.get("patterns", {}).keys())
    rules.patterns = patterns
    
    base_prob_col = config.get("base_prob_col", 9)
    pattern_cols = config.get("patterns", {})
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Track current context
    current_category = ""
    current_subcategory = ""
    current_item = ""
    current_options = []
    current_is_required = True
    current_importance = 4
    
    # Skip header rows (first few rows are metadata)
    data_start = 0
    for i, row in enumerate(rows):
        if len(row) > 7 and row[7] and row[7].strip().isdigit():
            # Found a row with option number
            data_start = i
            break
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        # Ensure row has enough columns
        while len(row) < 15:
            row.append("")
        
        # Update context from non-empty category/subcategory cells
        if row[0] and row[0].strip():
            current_category = row[0].strip()
        if row[1] and row[1].strip():
            current_subcategory = row[1].strip()
        if row[2] and row[2].strip():
            current_item = row[2].strip()
        
        # Parse required/importance if present
        if row[3] and row[3].strip():
            current_is_required = "1" in row[3] or "필수" in row[3]
        if row[5] and row[5].strip():
            try:
                current_importance = int(row[5].strip()[0])
            except (ValueError, IndexError):
                current_importance = 4
        
        # Check if this row has an option number (column 7)
        option_num_str = row[7].strip() if len(row) > 7 and row[7] else ""
        
        if option_num_str and option_num_str.isdigit():
            option_num = int(option_num_str)
            
            # Get descriptions
            qualitative_desc = row[6].strip() if len(row) > 6 else ""
            quantitative_desc = row[8].strip() if len(row) > 8 else ""
            
            # Handle empty values in descriptions
            if is_empty_value(qualitative_desc):
                qualitative_desc = ""
            if is_empty_value(quantitative_desc):
                quantitative_desc = qualitative_desc  # Use qualitative as fallback
            
            # Parse base probability
            base_prob = 0.0
            if len(row) > base_prob_col:
                base_prob = parse_percentage(row[base_prob_col])
            
            # Parse pattern-specific probabilities
            pattern_probs = {}
            for pattern_name, col_idx in pattern_cols.items():
                if len(row) > col_idx:
                    pattern_probs[pattern_name] = parse_percentage(row[col_idx])
                else:
                    pattern_probs[pattern_name] = 0.0
            
            # Create option
            option = SymptomOption(
                option_number=option_num,
                qualitative_desc=qualitative_desc,
                quantitative_desc=quantitative_desc,
                base_probability=base_prob,
                pattern_probabilities=pattern_probs
            )
            
            # Check if this is a new symptom or continuation
            symptom_key = "_".join([p for p in [current_category, current_subcategory, current_item] if p])
            
            if symptom_key not in rules.symptoms:
                # Create new symptom rule
                symptom = SymptomRule(
                    category=current_category,
                    subcategory=current_subcategory,
                    item_name=current_item,
                    is_required=current_is_required,
                    importance=current_importance,
                    options=[]
                )
                rules.add_symptom(symptom)
            
            # Add option to symptom
            rules.symptoms[symptom_key].options.append(option)
        
        i += 1
    
    return rules


# ============================================================================
# GLOBAL RULES CACHE
# ============================================================================

_RULES_CACHE: Dict[str, DiseaseRules] = {}


def load_rules(disease_name: str, csv_path: Optional[str] = None) -> DiseaseRules:
    """
    Load generation rules for a disease from CSV.
    
    Args:
        disease_name: Name of the disease (감기 or 알레르기비염)
        csv_path: Optional custom CSV path
    
    Returns:
        DiseaseRules object
    """
    if disease_name in _RULES_CACHE:
        return _RULES_CACHE[disease_name]
    
    if csv_path is None:
        csv_path = CSV_PATHS.get(disease_name)
        if csv_path is None:
            raise ValueError(f"No CSV path configured for disease: {disease_name}")
    
    # Resolve relative path
    if not os.path.isabs(csv_path):
        csv_path = os.path.abspath(csv_path)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    rules = parse_csv_file(csv_path, disease_name)
    _RULES_CACHE[disease_name] = rules
    return rules


def get_available_diseases() -> List[str]:
    """Get list of diseases with configured CSV paths."""
    return list(CSV_PATHS.keys())


def get_patterns_for_disease(disease_name: str) -> List[str]:
    """Get list of patterns for a disease."""
    config = PATTERN_COLUMNS.get(disease_name, {})
    return list(config.get("patterns", {}).keys())


# ============================================================================
# WEIGHTED SELECTION INTERFACE (Compatible with existing randomizer.py)
# ============================================================================

def get_weighted_value(
    disease_name: str,
    symptom_key: str,
    pattern: Optional[str] = None
) -> Tuple[int, str, str]:
    """
    Get a weighted random value for a symptom.
    
    Args:
        disease_name: Name of the disease
        symptom_key: Key identifying the symptom
        pattern: Optional pattern for pattern-specific probabilities
    
    Returns:
        Tuple of (option_number, qualitative_desc, quantitative_desc)
    """
    try:
        rules = load_rules(disease_name)
        symptom = rules.get_symptom(symptom_key)
        if symptom:
            option = symptom.select_option(pattern)
            if option:
                return (option.option_number, option.qualitative_desc, option.quantitative_desc)
    except Exception as e:
        print(f"Warning: Could not load rules for {disease_name}/{symptom_key}: {e}")
    
    # Fallback
    return (1, "", "")


def generate_patient_from_rules(
    disease_name: str,
    pattern: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate complete patient data using CSV-based rules.
    
    Args:
        disease_name: Name of the disease
        pattern: Specific pattern to use for probabilities
    
    Returns:
        Dictionary with all generated symptom values
    """
    try:
        rules = load_rules(disease_name)
        return rules.generate_patient_data(pattern)
    except Exception as e:
        print(f"Warning: Could not generate patient data for {disease_name}: {e}")
        return {}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def list_all_symptoms(disease_name: str) -> List[str]:
    """List all available symptom keys for a disease."""
    try:
        rules = load_rules(disease_name)
        return list(rules.symptoms.keys())
    except Exception:
        return []


def get_symptom_options(disease_name: str, symptom_key: str) -> List[Dict]:
    """Get all options for a symptom with their probabilities."""
    try:
        rules = load_rules(disease_name)
        symptom = rules.get_symptom(symptom_key)
        if symptom:
            return [
                {
                    "number": opt.option_number,
                    "qualitative": opt.qualitative_desc,
                    "quantitative": opt.quantitative_desc,
                    "base_prob": opt.base_probability,
                    "pattern_probs": opt.pattern_probabilities
                }
                for opt in symptom.options
            ]
    except Exception:
        pass
    return []


def print_rules_summary(disease_name: str):
    """Print a summary of all rules for debugging."""
    try:
        rules = load_rules(disease_name)
        print(f"\n{'='*60}")
        print(f"Disease: {disease_name}")
        print(f"Patterns: {rules.patterns}")
        print(f"Total symptoms: {len(rules.symptoms)}")
        print(f"{'='*60}")
        
        for key, symptom in list(rules.symptoms.items())[:10]:  # First 10
            print(f"\n{key}:")
            print(f"  Required: {symptom.is_required}, Importance: {symptom.importance}")
            print(f"  Options: {len(symptom.options)}")
            for opt in symptom.options[:3]:  # First 3 options
                print(f"    {opt.option_number}: {opt.quantitative_desc[:50]}...")
                print(f"       Base: {opt.base_probability:.1%}, Patterns: {opt.pattern_probabilities}")
    except Exception as e:
        print(f"Error loading rules: {e}")


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Test loading and parsing
    import sys
    
    # Update paths for testing
    CSV_PATHS["감기"] = r"c:\Users\KIOM_User\Desktop\1.csv"
    CSV_PATHS["알레르기비염"] = r"c:\Users\KIOM_User\Desktop\2.csv"
    
    for disease in ["감기", "알레르기비염"]:
        print(f"\n\nTesting {disease}...")
        try:
            print_rules_summary(disease)
            
            # Test generation
            print(f"\n--- Test patient generation for {disease} ---")
            patterns = get_patterns_for_disease(disease)
            if patterns:
                pattern = patterns[0]
                print(f"Using pattern: {pattern}")
                data = generate_patient_from_rules(disease, pattern)
                print(f"Generated {len(data)} symptom values")
                for key, value in list(data.items())[:5]:
                    print(f"  {key}: option {value['option_number']} - {value['quantitative'][:40]}...")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
