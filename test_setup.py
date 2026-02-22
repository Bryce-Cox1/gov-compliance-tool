#!/usr/bin/env python3
"""
Quick setup test script
Run this to verify everything is installed correctly
"""

import sys
import os

def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✓ FastAPI installed")
    except ImportError:
        print("✗ FastAPI missing - run: pip install fastapi")
        return False
    
    try:
        import uvicorn
        print("✓ Uvicorn installed")
    except ImportError:
        print("✗ Uvicorn missing - run: pip install uvicorn")
        return False
    
    try:
        import textstat
        print("✓ textstat installed")
    except ImportError:
        print("✗ textstat missing - run: pip install textstat")
        return False
    
    try:
        import spacy
        print("✓ spaCy installed")
        
        # Test if model is downloaded
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model (en_core_web_sm) downloaded")
        except OSError:
            print("✗ spaCy model missing - run: python -m spacy download en_core_web_sm")
            return False
            
    except ImportError:
        print("✗ spaCy missing - run: pip install spacy")
        return False
    
    try:
        import openai
        print("✓ OpenAI package installed")
    except ImportError:
        print("✗ OpenAI missing - run: pip install openai")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("✗ python-dotenv missing - run: pip install python-dotenv")
        return False
    
    return True


def test_env():
    """Test environment configuration"""
    print("\nTesting environment...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        print("   The tool will work for scoring only (no rewriting)")
        print("   To enable rewriting:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key")
        return False
    
    if api_key.startswith('sk-'):
        print("✓ OPENAI_API_KEY configured")
        return True
    else:
        print("✗ OPENAI_API_KEY doesn't look valid (should start with 'sk-')")
        return False


def test_scoring():
    """Test the scoring engine"""
    print("\nTesting scoring engine...")
    
    try:
        from compliance_scorer import ComplianceScorer
        
        scorer = ComplianceScorer(target_grade=7.0)
        
        # Test with simple text
        test_text = "This is a test. It has short sentences. The reading grade should be low."
        scores = scorer.score_text(test_text)
        
        if scores['grade_level'] > 0:
            print(f"✓ Scoring works (grade: {scores['grade_level']})")
            return True
        else:
            print("✗ Scoring returned zero")
            return False
            
    except Exception as e:
        print(f"✗ Scoring failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Government Compliance Tool - Setup Test")
    print("=" * 60)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Some dependencies are missing")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Test environment
    env_ok = test_env()
    
    # Test scoring
    if not test_scoring():
        print("\n❌ Scoring test failed")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    if env_ok:
        print("✅ ALL TESTS PASSED!")
        print("\nYou're ready to go!")
        print("Run: python app.py")
        print("Then open: http://localhost:8000")
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("\nScoring will work, but rewriting is disabled.")
        print("Add your OpenAI API key to .env to enable rewriting.")
        print("\nYou can still run the app:")
        print("Run: python app.py")
        print("Then open: http://localhost:8000")
    print("=" * 60)


if __name__ == "__main__":
    main()
