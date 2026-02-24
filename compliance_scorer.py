"""
Compliance Scorer - Deterministic scoring for government content
Uses mathematical formulas and rule-based NLP (not LLM guessing)
"""

import re
from typing import Dict, List, Tuple
from proper_noun_detector import ProperNounDetector
from readability import ReadabilityScorer


class ComplianceScorer:
    """Score text against Australian Government Style Manual requirements"""
    
    def __init__(self, target_grade: float = 7.0):
        self.target_grade = target_grade
        self.proper_noun_detector = ProperNounDetector()
        
    def score_text(self, text: str) -> Dict:
        """
        Score text against all AGSM requirements
        Returns deterministic scores (not LLM opinions)
        """
        if not text or len(text.strip()) == 0:
            return self._empty_score()
            
        # Readability (mathematical formulas - guaranteed accurate)
        grade_level = ReadabilityScorer.flesch_kincaid_grade(text)
        flesch_score = ReadabilityScorer.flesch_reading_ease(text)
        smog_index = ReadabilityScorer.smog_index(text)
        
        # Sentence analysis (simple counting)
        sentences = self._split_sentences(text)
        words = text.split()
        
        avg_sentence_length = len(words) / max(len(sentences), 1)
        max_sentence_length = max([len(s.split()) for s in sentences]) if sentences else 0
        
        # Passive voice detection (rule-based NLP)
        passive_info = self._detect_passive_voice(text)
        
        # Jargon detection (dictionary-based)
        jargon_count = self._detect_jargon(text)
        
        # Calculate overall compliance
        compliance = self._calculate_compliance(
            grade_level, 
            avg_sentence_length, 
            max_sentence_length,
            passive_info['percentage']
        )
        
        return {
            'grade_level': round(grade_level, 1),
            'flesch_score': round(flesch_score, 1),
            'smog_index': round(smog_index, 1),
            'target_grade': self.target_grade,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'max_sentence_length': max_sentence_length,
            'passive_percentage': round(passive_info['percentage'], 1),
            'passive_sentences': passive_info['sentences'],
            'jargon_count': jargon_count,
            'total_sentences': len(sentences),
            'total_words': len(words),
            'compliance': compliance,
            'issues': self._identify_issues(
                grade_level, 
                avg_sentence_length, 
                max_sentence_length,
                passive_info['percentage']
            )
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple split on common punctuation
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _detect_passive_voice(self, text: str) -> Dict:
        """
        Detect passive voice using regex patterns
        Simple approach (~70-80% accurate, no heavy dependencies)
        """
        sentences = self._split_sentences(text)
        passive_sentences = []
        
        # Common passive voice patterns
        passive_patterns = [
            r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',  # be + past participle
            r'\b(is|are|was|were|be|been|being)\s+\w+en\b',  # be + past participle (irregular)
            r'\bwas\s+\w+ed\s+by\b',  # explicit "was X-ed by"
            r'\bwere\s+\w+ed\s+by\b',  # explicit "were X-ed by"
        ]
        
        for sent in sentences:
            for pattern in passive_patterns:
                if re.search(pattern, sent, re.IGNORECASE):
                    passive_sentences.append(sent)
                    break
        
        total_sentences = len(sentences)
        passive_count = len(passive_sentences)
        passive_pct = (passive_count / max(total_sentences, 1)) * 100
        
        return {
            'sentences': passive_sentences,
            'percentage': passive_pct,
            'count': passive_count
        }
    
    def _detect_jargon(self, text: str) -> int:
        """
        Detect jargon/complex words
        Simple dictionary-based approach for MVP
        """
        # Common government jargon words
        jargon_words = {
            'utilize', 'facilitate', 'implement', 'leverage', 'optimize',
            'subsequent', 'prior', 'commence', 'terminate', 'endeavour',
            'notwithstanding', 'aforementioned', 'heretofore', 'hereby'
        }
        
        words = text.lower().split()
        jargon_count = sum(1 for word in words if word in jargon_words)
        
        return jargon_count
    
    def _calculate_compliance(
        self, 
        grade_level: float, 
        avg_sentence: float, 
        max_sentence: int,
        passive_pct: float
    ) -> Dict:
        """
        Calculate overall compliance score
        Returns which requirements are met/failed
        """
        checks = {
            'grade_level': {
                'passed': abs(grade_level - self.target_grade) <= 1.0,
                'target': f"{self.target_grade} ± 1.0",
                'actual': round(grade_level, 1)
            },
            'avg_sentence_length': {
                'passed': avg_sentence <= 20,
                'target': "≤ 20 words",
                'actual': round(avg_sentence, 1)
            },
            'max_sentence_length': {
                'passed': max_sentence <= 25,
                'target': "≤ 25 words",
                'actual': max_sentence
            },
            'passive_voice': {
                'passed': passive_pct < 10,
                'target': "< 10%",
                'actual': f"{round(passive_pct, 1)}%"
            }
        }
        
        total_checks = len(checks)
        passed_checks = sum(1 for check in checks.values() if check['passed'])
        
        return {
            'checks': checks,
            'score': round((passed_checks / total_checks) * 100, 1),
            'passed': passed_checks,
            'total': total_checks
        }
    
    def _identify_issues(
        self, 
        grade_level: float, 
        avg_sentence: float, 
        max_sentence: int,
        passive_pct: float
    ) -> List[str]:
        """Identify specific issues to fix"""
        issues = []
        
        if grade_level > self.target_grade + 1.0:
            diff = round(grade_level - self.target_grade, 1)
            issues.append(f"Reading grade {diff} levels too high")
        
        if avg_sentence > 20:
            issues.append(f"Sentences too long (avg: {round(avg_sentence, 1)} words)")
        
        if max_sentence > 25:
            issues.append(f"Longest sentence is {max_sentence} words (max: 25)")
        
        if passive_pct >= 10:
            issues.append(f"Too much passive voice ({round(passive_pct, 1)}%)")
        
        if not issues:
            issues.append("No major issues found")
        
        return issues
    
    def _empty_score(self) -> Dict:
        """Return empty score structure"""
        return {
            'grade_level': 0,
            'flesch_score': 0,
            'smog_index': 0,
            'target_grade': self.target_grade,
            'avg_sentence_length': 0,
            'max_sentence_length': 0,
            'passive_percentage': 0,
            'passive_sentences': [],
            'jargon_count': 0,
            'total_sentences': 0,
            'total_words': 0,
            'compliance': {
                'checks': {},
                'score': 0,
                'passed': 0,
                'total': 4
            },
            'issues': ['No text provided']
        }


# Test function
    def score_text_with_context(self, text: str) -> Dict:
        """
        Score text with context awareness of proper nouns
        Provides both full score and content-only score
        """
        # Get standard score
        full_score = self.score_text(text)
        
        # Detect proper nouns
        proper_nouns = self.proper_noun_detector.detect_all(text)
        density = self.proper_noun_detector.calculate_proper_noun_density(text)
        
        # If no proper nouns, return standard score
        if not proper_nouns['all']:
            full_score['proper_nouns'] = {
                'detected': [],
                'count': 0,
                'density_percentage': 0,
                'content_grade': full_score['grade_level'],
                'note': 'No unavoidable proper nouns detected'
            }
            return full_score
        
        # Score content without proper nouns
        content_text = self.proper_noun_detector.strip_proper_nouns(text)
        content_score = self.score_text(content_text)
        
        # Add proper noun context to result
        full_score['proper_nouns'] = {
            'detected': proper_nouns['all'],  # All proper nouns
            'count': len(proper_nouns['all']),
            'density_percentage': density['proper_noun_percentage'],
            'content_grade': content_score['grade_level'],
            'content_compliance': content_score['compliance']['score'],
            'note': self._generate_proper_noun_note(
                full_score['grade_level'],
                content_score['grade_level'],
                len(proper_nouns['all'])
            ),
            'categories': {
                'acts': proper_nouns['acts'],
                'regulations': proper_nouns['regulations'],
                'departments': proper_nouns['departments'],
                'schemes': proper_nouns['schemes'],
                'organizations': proper_nouns['organizations'],
                'locations': proper_nouns['locations']
            }
        }
        
        return full_score
    
    def _generate_proper_noun_note(self, full_grade: float, content_grade: float, noun_count: int) -> str:
        """Generate explanation about proper noun impact"""
        if content_grade <= self.target_grade + 1:
            return f"Content meets Grade {self.target_grade} target. Full grade inflated by {noun_count} unavoidable proper noun(s)."
        else:
            diff = content_grade - self.target_grade
            return f"Content is Grade {content_grade:.1f} (target: {self.target_grade}). Simplify further. Plus {noun_count} unavoidable proper noun(s)."


if __name__ == "__main__":
    # Test with sample government text
    sample_text = """
    The application should be submitted by the applicant to the relevant 
    department. It is important that all fields are completed accurately. 
    Processing times may vary depending on the complexity of the application.
    """
    
    scorer = ComplianceScorer(target_grade=7.0)
    results = scorer.score_text(sample_text)
    
    print("=== SCORING RESULTS ===")
    print(f"Grade Level: {results['grade_level']} (target: {results['target_grade']})")
    print(f"Avg Sentence Length: {results['avg_sentence_length']} words")
    print(f"Passive Voice: {results['passive_percentage']}%")
    print(f"\nCompliance Score: {results['compliance']['score']}%")
    print(f"\nIssues:")
    for issue in results['issues']:
        print(f"  • {issue}")
