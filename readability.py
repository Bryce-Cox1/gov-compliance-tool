"""
Simple readability scoring - replaces textstat
Implements Flesch-Kincaid and other formulas directly
"""

import re
import math


class ReadabilityScorer:
    """Calculate readability scores without external dependencies"""
    
    SYLLABLE_PATTERNS = [
        # Subtract syllables
        (r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', -1),
        (r'^mc', 1),
        (r'y(?![aeiou])', 1),
        # Add syllables  
        (r'[aeiouy]{1,2}', 1),
    ]
    
    @staticmethod
    def count_syllables(word):
        """Count syllables in a word"""
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        # Remove non-letters
        word = re.sub(r'[^a-z]', '', word)
        if not word:
            return 1
            
        count = 0
        
        # Count vowel groups
        count = len(re.findall(r'[aeiouy]+', word))
        
        # Subtract silent e
        if word.endswith('e'):
            count -= 1
        
        # Ensure at least 1
        return max(1, count)
    
    @staticmethod
    def split_sentences(text):
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def split_words(text):
        """Split text into words"""
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return [w for w in words if w]
    
    @classmethod
    def flesch_reading_ease(cls, text):
        """
        Flesch Reading Ease score
        206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        """
        sentences = cls.split_sentences(text)
        words = cls.split_words(text)
        
        if not sentences or not words:
            return 0
        
        num_sentences = len(sentences)
        num_words = len(words)
        num_syllables = sum(cls.count_syllables(w) for w in words)
        
        if num_sentences == 0 or num_words == 0:
            return 0
        
        score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
        return round(score, 2)
    
    @classmethod
    def flesch_kincaid_grade(cls, text):
        """
        Flesch-Kincaid Grade Level
        0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        """
        sentences = cls.split_sentences(text)
        words = cls.split_words(text)
        
        if not sentences or not words:
            return 0
        
        num_sentences = len(sentences)
        num_words = len(words)
        num_syllables = sum(cls.count_syllables(w) for w in words)
        
        if num_sentences == 0 or num_words == 0:
            return 0
        
        grade = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
        return round(grade, 2)
    
    @classmethod
    def smog_index(cls, text):
        """
        SMOG Index (Simple Measure of Gobbledygook)
        1.0430 * sqrt(polysyllables * (30 / sentences)) + 3.1291
        """
        sentences = cls.split_sentences(text)
        words = cls.split_words(text)
        
        if not sentences or not words:
            return 0
        
        num_sentences = len(sentences)
        
        # Count polysyllables (3+ syllables)
        polysyllables = sum(1 for w in words if cls.count_syllables(w) >= 3)
        
        if num_sentences < 3:
            # SMOG requires at least 3 sentences, use approximation
            return cls.flesch_kincaid_grade(text)
        
        smog = 1.0430 * math.sqrt(polysyllables * (30 / num_sentences)) + 3.1291
        return round(smog, 2)
