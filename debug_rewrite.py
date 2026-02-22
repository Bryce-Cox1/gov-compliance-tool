#!/usr/bin/env python3
"""Debug: See what the LLM is actually generating"""

import os
from dotenv import load_dotenv
from rewrite_engine import RewriteEngine

load_dotenv()

test_text = """The Department of Infrastructure, Transport, Regional Development, Communications and the Arts is responsible for the administration of programs and initiatives that are designed to facilitate the delivery of outcomes that are aligned with the strategic objectives of the Australian Government. Applications for funding under the relevant grant programs must be submitted in accordance with the guidelines that have been published on the department's website, and it is the responsibility of applicants to ensure that all required documentation has been provided prior to the closing date. Failure to comply with the prescribed requirements may result in the application being deemed ineligible for consideration."""

print("🔍 DEBUG: Testing rewrite engine\n")
print("=" * 60)
print("ORIGINAL TEXT:")
print(test_text)
print("\n" + "=" * 60)

engine = RewriteEngine(target_grade=7.0)
result = engine.rewrite_with_validation(test_text)

print("\nREWRITTEN TEXT:")
print(result['rewritten_text'])
print("\n" + "=" * 60)

print("\nSCORES:")
print(f"Reading Grade: {result['new_scores']['grade_level']}")
print(f"Avg Sentence Length: {result['new_scores']['avg_sentence_length']} words")
print(f"Longest Sentence: {result['new_scores']['max_sentence_length']} words")
print(f"Passive Voice: {result['new_scores']['passive_percentage']}%")
print(f"Compliance: {result['new_scores']['compliance']['score']}%")
print(f"Iterations: {result['iterations']}")
print(f"Confidence: {result['confidence']}%")
