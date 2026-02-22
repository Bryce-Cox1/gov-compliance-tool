#!/usr/bin/env python3
"""Quick test of OpenAI API and rewrite engine"""

import os
from dotenv import load_dotenv
from rewrite_engine import RewriteEngine

# Load environment
load_dotenv()

test_text = """The Department of Infrastructure, Transport, Regional Development, Communications and the Arts is responsible for the administration of programs and initiatives that are designed to facilitate the delivery of outcomes that are aligned with the strategic objectives of the Australian Government."""

print("Testing rewrite engine...")
print("=" * 60)

try:
    engine = RewriteEngine(target_grade=7.0)
    print("✅ Engine initialized")
    
    result = engine.rewrite_with_validation(test_text)
    print("✅ Rewrite successful!")
    print()
    print("Original grade:", result['original_scores']['readability']['grade_level'])
    print("New grade:", result['new_scores']['readability']['grade_level'])
    print()
    print("Rewritten text:")
    print(result['rewritten_text'])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
