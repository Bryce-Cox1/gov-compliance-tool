"""
Rewrite Engine - LLM-based rewriting with validation loop
Uses scoring engine to validate output (not LLM self-scoring)
"""

import os
from typing import Dict, Tuple
from openai import OpenAI
from compliance_scorer import ComplianceScorer
from agsm_rules import AGSMRules
from proper_noun_detector import ProperNounDetector


class RewriteEngine:
    """Rewrite text to meet AGSM requirements with validation"""
    
    def __init__(self, api_key: str = None, target_grade: float = 7.0):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.scorer = ComplianceScorer(target_grade=target_grade)
        self.agsm_checker = AGSMRules()
        self.proper_noun_detector = ProperNounDetector()
        self.target_grade = target_grade
        self.max_iterations = 3
    
    def rewrite_with_validation(self, text: str) -> Dict:
        """
        Rewrite text and validate it meets requirements
        Returns: original_scores, rewritten_text, new_scores, confidence, iterations
        """
        # Score original text (with proper noun context)
        original_scores = self.scorer.score_text_with_context(text)
        
        # If already meets requirements, return as-is
        if original_scores['compliance']['score'] >= 90:
            return {
                'original_text': text,
                'original_scores': original_scores,
                'rewritten_text': text,
                'new_scores': original_scores,
                'confidence': 95,
                'iterations': 0,
                'message': 'Text already meets requirements'
            }
        
        # Rewrite with validation loop
        current_text = text
        best_text = text
        best_scores = original_scores
        best_compliance = original_scores['compliance']['score']
        
        for iteration in range(self.max_iterations):
            # Score current version (with context awareness)
            current_scores = self.scorer.score_text_with_context(current_text)
            
            # Check if we've met all requirements
            if current_scores['compliance']['score'] >= 90:
                return {
                    'original_text': text,
                    'original_scores': original_scores,
                    'rewritten_text': current_text,
                    'new_scores': current_scores,
                    'confidence': self._calculate_confidence(current_scores),
                    'iterations': iteration + 1,
                    'message': 'Successfully met all requirements'
                }
            
            # Track best version
            if current_scores['compliance']['score'] > best_compliance:
                best_text = current_text
                best_scores = current_scores
                best_compliance = current_scores['compliance']['score']
            
            # Build prompt with SPECIFIC feedback
            prompt = self._build_prompt(current_text, current_scores)
            
            # Get LLM rewrite
            current_text = self._llm_rewrite(prompt)
        
        # After max iterations, return best attempt
        final_scores = self.scorer.score_text_with_context(best_text)
        confidence = self._calculate_confidence(final_scores)
        
        return {
            'original_text': text,
            'original_scores': original_scores,
            'rewritten_text': best_text,
            'new_scores': final_scores,
            'confidence': confidence,
            'iterations': self.max_iterations,
            'message': f'Improved to {final_scores["compliance"]["score"]}% compliance'
        }
    
    def _build_prompt(self, text: str, scores: Dict) -> str:
        """Build prompt with specific issues to fix"""
        
        # Check for AGSM violations first
        violations = self.agsm_checker.find_violations(text)
        agsm_instructions = self.agsm_checker.generate_fix_instructions(violations)
        
        # Detect proper nouns that shouldn't be simplified
        proper_nouns = self.proper_noun_detector.detect_all(text)
        
        # Identify specific problems
        problems = []
        fixes = []
        
        compliance = scores['compliance']['checks']
        
        if not compliance['grade_level']['passed']:
            actual = compliance['grade_level']['actual']
            target = self.target_grade
            problems.append(f"Reading grade is {actual} (target: {target})")
            fixes.append("CRITICAL: Replace complex/formal words with everyday language")
            fixes.append("Examples: 'facilitate' → 'help', 'utilize' → 'use', 'commence' → 'start'")
            fixes.append("Break complex ideas into multiple simple sentences")
        
        if not compliance['avg_sentence_length']['passed']:
            actual = compliance['avg_sentence_length']['actual']
            problems.append(f"Average sentence length is {actual} words (target: ≤20)")
            fixes.append("Break long sentences into shorter ones")
        
        if not compliance['max_sentence_length']['passed']:
            actual = compliance['max_sentence_length']['actual']
            problems.append(f"Longest sentence is {actual} words (max: 25)")
            fixes.append("Split the longest sentences")
        
        if not compliance['passive_voice']['passed']:
            actual = compliance['passive_voice']['actual']
            problems.append(f"Passive voice: {actual} (target: <10%)")
            fixes.append("Convert passive voice to active voice")
            
            # Show which sentences are passive
            if scores['passive_sentences']:
                problems.append(f"Passive sentences found: {len(scores['passive_sentences'])}")
        
        # Build prompt
        agsm_section = ""
        if agsm_instructions:
            agsm_section = f"\nAGSM STYLE VIOLATIONS (FIX THESE FIRST):\n{agsm_instructions}\n"
        
        proper_noun_section = ""
        if proper_nouns['all']:
            proper_noun_section = "\nDO NOT SIMPLIFY THESE PROPER NOUNS (they're official terms):\n"
            for noun in proper_nouns['all'][:10]:  # First 10
                proper_noun_section += f"  • {noun}\n"
            proper_noun_section += "Keep these exact terms. Simplify everything else.\n"
        
        prompt = f"""You are a government content editor specializing in the Australian Government Style Manual.
{agsm_section}{proper_noun_section}
CURRENT PROBLEMS:
{chr(10).join(f"• {p}" for p in problems)}

REQUIRED FIXES:
{chr(10).join(f"• {f}" for f in fixes)}

TARGET REQUIREMENTS:
• Reading grade: {self.target_grade} (Flesch-Kincaid) - THIS IS CRITICAL
• Average sentence length: 15-20 words
• Maximum sentence length: 25 words
• Passive voice: Less than 10% of sentences
• Plain language: Avoid jargon, use simple everyday words

IMPORTANT RULES:
1. Maintain the original meaning and all key information
2. Keep a professional but approachable tone
3. Use active voice: "You should submit" not "The form should be submitted"
4. Break up long sentences into multiple short sentences
5. AGGRESSIVELY replace formal/complex words with everyday alternatives:
   - "facilitate" → "help" or "make easier"
   - "utilize" → "use"
   - "commence" → "start" or "begin"
   - "prior to" → "before"
   - "in accordance with" → "following" or "as shown in"
   - "submit" → "send" or "give us"
   - "ensure" → "make sure"
   - "requirements" → "what you need" or "rules"
6. Address the Australian public directly (use "you" and "your")
7. If reading grade is still too high, simplify even more aggressively

Original text:
{text}

Rewrite the text to fix ALL the problems listed above while maintaining accuracy and meaning."""

        return prompt
    
    def _llm_rewrite(self, prompt: str) -> str:
        """Call LLM to rewrite text"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cheaper, faster, good enough for this
                messages=[
                    {"role": "system", "content": "You are an expert government content editor specializing in plain language. Your PRIMARY goal is to reduce reading grade level to Grade 7 by using simple, everyday words that anyone can understand. Replace ALL formal/bureaucratic language with conversational alternatives."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=2000
            )
            
            rewritten = response.choices[0].message.content.strip()
            return rewritten
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return prompt.split("Original text:")[-1].strip()  # Return original on error
    
    def _calculate_confidence(self, scores: Dict) -> int:
        """
        Calculate confidence score based on validated metrics
        Higher confidence for things we can measure deterministically
        """
        confidence = 100
        compliance = scores['compliance']['checks']
        
        # Reading grade (guaranteed - it's math)
        if not compliance['grade_level']['passed']:
            confidence -= 25
        
        # Sentence length (guaranteed - word count)
        if not compliance['avg_sentence_length']['passed']:
            confidence -= 15
        
        if not compliance['max_sentence_length']['passed']:
            confidence -= 10
        
        # Passive voice (high confidence - rule-based NLP)
        if not compliance['passive_voice']['passed']:
            confidence -= 20
        
        # Bonus points for high compliance
        if scores['compliance']['score'] >= 95:
            confidence = min(100, confidence + 5)
        
        return max(60, confidence)  # Never go below 60% (we always improve something)


# Test function
if __name__ == "__main__":
    # Test with sample text
    sample = """
    The application should be submitted by the applicant to the relevant department. 
    It is important that all fields are completed accurately. Processing times may 
    vary depending on the complexity of the application and the volume of applications 
    being processed at any given time.
    """
    
    print("Testing rewrite engine...")
    print("Note: Requires OPENAI_API_KEY environment variable")
    
    try:
        engine = RewriteEngine(target_grade=7.0)
        result = engine.rewrite_with_validation(sample)
        
        print("\n=== ORIGINAL ===")
        print(f"Grade: {result['original_scores']['grade_level']}")
        print(f"Compliance: {result['original_scores']['compliance']['score']}%")
        
        print("\n=== REWRITTEN ===")
        print(result['rewritten_text'])
        print(f"\nGrade: {result['new_scores']['grade_level']}")
        print(f"Compliance: {result['new_scores']['compliance']['score']}%")
        print(f"Confidence: {result['confidence']}%")
        print(f"Iterations: {result['iterations']}")
        
    except ValueError as e:
        print(f"Error: {e}")
