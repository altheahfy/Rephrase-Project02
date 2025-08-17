#!/usr/bin/env python3
"""
Test3 - 比較結果で失敗した具体的な例文での診断
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_specific_failures():
    """比較結果で失敗した具体的例文をテスト"""
    print("🔧 具体的失敗例文診断テスト開始...")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    test_cases = [
        {
            'sentence': "I love you.",
            'expected': {'S': 'I', 'V': 'love', 'O1': 'you'},
            'id': 2
        },
        {
            'sentence': "He has finished his homework.",
            'expected': {'S': 'He', 'V': 'finished', 'Aux': 'has', 'O1': 'his homework'},
            'id': 20
        },
        {
            'sentence': "The letter was written by John.",
            'expected': {'S': 'The letter', 'V': 'written', 'Aux': 'was', 'M1': 'by John'},
            'id': 21
        }
    ]
    
    for test_case in test_cases:
        sentence = test_case['sentence']
        expected = test_case['expected']
        test_id = test_case['id']
        
        print(f"\n📖 Test[{test_id}]: '{sentence}'")
        
        result = mapper.process(sentence)
        actual = result.get('slots', {})
        
        print(f"期待値: {expected}")
        print(f"システム: {actual}")
        
        problems = []
        for key, expected_value in expected.items():
            actual_value = actual.get(key, '')
            if actual_value != expected_value:
                problems.append(f"{key}: '{actual_value}' ≠ '{expected_value}'")
        
        if problems:
            print(f"❌ 問題:")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"✅ 正常")

if __name__ == "__main__":
    test_specific_failures()
