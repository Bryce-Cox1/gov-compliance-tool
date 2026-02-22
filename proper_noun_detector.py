"""
Proper Noun Detector
Identify unavoidable proper nouns that inflate reading grades
"""

import re
import spacy
from typing import List, Dict, Set


class ProperNounDetector:
    """Detect proper nouns (Acts, departments, schemes) that can't be simplified"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not loaded. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    # Regex patterns for common government proper nouns
    ACT_PATTERN = r'\b[A-Z][\w\s]+?\s+\([A-Z][\w\s]+?\)\s+[A-Z][\w\s]+?\s+Act\s+\d{4}\b'
    SIMPLE_ACT_PATTERN = r'\b[A-Z][\w\s]+?\s+Act\s+\d{4}\b'
    REGULATION_PATTERN = r'\b[\w\s]+?\s+Regulations?\s+\d{4}\b'
    DEPARTMENT_PATTERN = r'\bDepartment of [\w\s,]+(?:and the [\w\s]+)?'
    
    def detect_all(self, text: str) -> Dict[str, List[str]]:
        """
        Detect all types of proper nouns
        Returns categorized proper nouns
        """
        proper_nouns = {
            'acts': [],
            'regulations': [],
            'departments': [],
            'organizations': [],
            'locations': [],
            'schemes': [],
            'all': []
        }
        
        # Detect Acts (most important)
        proper_nouns['acts'].extend(self._detect_acts(text))
        
        # Detect Regulations
        proper_nouns['regulations'].extend(self._detect_regulations(text))
        
        # Detect Departments
        proper_nouns['departments'].extend(self._detect_departments(text))
        
        # Use spaCy for organizations and locations
        if self.nlp:
            spacy_results = self._detect_with_spacy(text)
            proper_nouns['organizations'].extend(spacy_results['organizations'])
            proper_nouns['locations'].extend(spacy_results['locations'])
        
        # Detect scheme names (multi-word industry terms)
        proper_nouns['schemes'].extend(self._detect_schemes(text))
        
        # Combine all (deduplicate)
        all_nouns = set()
        for category in proper_nouns:
            if category != 'all':
                all_nouns.update(proper_nouns[category])
        
        proper_nouns['all'] = sorted(list(all_nouns), key=len, reverse=True)  # Longest first
        
        return proper_nouns
    
    def _detect_acts(self, text: str) -> List[str]:
        """Detect Act names with year"""
        acts = []
        
        # Complex Acts with parentheses: "Industry (Long Service Leave) Administration Act 1992"
        complex_matches = re.findall(self.ACT_PATTERN, text)
        acts.extend(complex_matches)
        
        # Simple Acts: "Privacy Act 1988" (but not if already part of complex match)
        simple_matches = re.findall(self.SIMPLE_ACT_PATTERN, text)
        for match in simple_matches:
            # Only add if not a substring of an existing match
            if not any(match in act for act in acts):
                acts.append(match)
        
        return acts
    
    def _detect_regulations(self, text: str) -> List[str]:
        """Detect Regulation names"""
        return re.findall(self.REGULATION_PATTERN, text)
    
    def _detect_departments(self, text: str) -> List[str]:
        """Detect Department names (can be very long)"""
        return re.findall(self.DEPARTMENT_PATTERN, text)
    
    def _detect_with_spacy(self, text: str) -> Dict[str, List[str]]:
        """Use spaCy NER for organizations and locations"""
        result = {'organizations': [], 'locations': []}
        
        if not self.nlp:
            return result
        
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                result['organizations'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                result['locations'].append(ent.text)
        
        return result
    
    def _detect_schemes(self, text: str) -> List[str]:
        """
        Detect multi-word scheme/program names
        e.g., "black coal mining industry long service leave scheme"
        """
        schemes = []
        
        # Pattern: industry + service/leave + scheme/program
        scheme_pattern = r'\b(?:\w+\s+){2,8}(?:scheme|program|initiative|fund)\b'
        matches = re.findall(scheme_pattern, text, re.IGNORECASE)
        
        # Filter to only keep long multi-word terms (5+ words)
        schemes = [m.strip() for m in matches if len(m.split()) >= 5]
        
        return schemes
    
    def calculate_proper_noun_density(self, text: str) -> Dict:
        """
        Calculate how much of the text is proper nouns
        """
        proper_nouns = self.detect_all(text)
        
        total_chars = len(text)
        proper_noun_chars = sum(len(noun) for noun in proper_nouns['all'])
        
        total_words = len(text.split())
        proper_noun_words = sum(len(noun.split()) for noun in proper_nouns['all'])
        
        return {
            'total_words': total_words,
            'proper_noun_words': proper_noun_words,
            'proper_noun_percentage': round((proper_noun_words / total_words * 100), 1) if total_words > 0 else 0,
            'proper_noun_count': len(proper_nouns['all']),
            'categories': {k: len(v) for k, v in proper_nouns.items() if k != 'all'}
        }
    
    def strip_proper_nouns(self, text: str) -> str:
        """
        Remove proper nouns from text for content-only scoring
        Replace with placeholder to maintain sentence structure
        """
        proper_nouns = self.detect_all(text)
        
        cleaned_text = text
        
        # Replace proper nouns with generic placeholders (maintain word count)
        for noun in proper_nouns['all']:
            # Create placeholder of similar length
            word_count = len(noun.split())
            placeholder = ' '.join(['term'] * word_count)
            cleaned_text = cleaned_text.replace(noun, placeholder)
        
        return cleaned_text
    
    def get_detection_report(self, text: str) -> str:
        """
        Generate human-readable report of detected proper nouns
        """
        proper_nouns = self.detect_all(text)
        density = self.calculate_proper_noun_density(text)
        
        if not proper_nouns['all']:
            return "No unavoidable proper nouns detected."
        
        report = []
        report.append(f"Found {density['proper_noun_count']} proper noun(s) ({density['proper_noun_percentage']}% of text):\n")
        
        if proper_nouns['acts']:
            report.append("Acts:")
            for act in proper_nouns['acts']:
                report.append(f"  • {act}")
        
        if proper_nouns['regulations']:
            report.append("\nRegulations:")
            for reg in proper_nouns['regulations']:
                report.append(f"  • {reg}")
        
        if proper_nouns['departments']:
            report.append("\nDepartments:")
            for dept in proper_nouns['departments'][:3]:  # Limit to 3
                report.append(f"  • {dept}")
        
        if proper_nouns['schemes']:
            report.append("\nSchemes/Programs:")
            for scheme in proper_nouns['schemes']:
                report.append(f"  • {scheme}")
        
        report.append("\nThese terms cannot be simplified and will affect readability scores.")
        
        return '\n'.join(report)


# Example usage
if __name__ == "__main__":
    detector = ProperNounDetector()
    
    test_text = """
    To qualify for the black coal mining industry long service leave scheme, 
    we look at your job and what you do. You can find more details in the 
    Coal Mining Industry (Long Service Leave) Administration Act 1992.
    """
    
    print("Detected proper nouns:")
    print("=" * 60)
    print(detector.get_detection_report(test_text))
    print("\n" + "=" * 60)
    
    density = detector.calculate_proper_noun_density(test_text)
    print(f"\nDensity: {density['proper_noun_percentage']}% of text")
    print(f"Count: {density['proper_noun_count']}")
