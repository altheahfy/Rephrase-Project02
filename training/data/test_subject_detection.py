#!/usr/bin/env python3
"""
主語検出正常動作確認テスト
"""

import sys
sys.path.append('.')

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_subject_detection():
    mapper = DynamicGrammarMapper()
    
    # テストケース
    test_cases = [
        "She quickly runs to school.",
        "He slowly walks.",
        "They carefully study.",
        "I run fast.",
        "The cat sleeps."
    ]
    
    print("=== 主語検出正常動作確認 ===")
    for text in test_cases:
        result = mapper.analyze_sentence(text)
        subject = result.get('main_slots', {}).get('S', 'NOT_FOUND')
        print(f"文: '{text}' → 主語: '{subject}'")

if __name__ == "__main__":
    test_subject_detection()
