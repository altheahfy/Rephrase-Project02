#!/usr/bin/env python3
"""
副詞ハンドラーのデバッグテスト
"""

from adverb_handler import AdverbHandler

def test_adverb_handler():
    handler = AdverbHandler()
    
    test_sentence = "The students study hard for exams."
    print(f"テスト文: {test_sentence}")
    
    result = handler.process(test_sentence)
    
    print(f"\n結果:")
    print(f"Success: {result['success']}")
    print(f"Separated text: '{result['separated_text']}'")
    print(f"Modifiers: {result['modifiers']}")
    print(f"Verb positions: {result.get('verb_positions', {})}")
    print(f"Modifier slots: {result.get('modifier_slots', {})}")

if __name__ == "__main__":
    test_adverb_handler()
