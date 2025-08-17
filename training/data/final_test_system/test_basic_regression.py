#!/usr/bin/env python3
"""
基本的なテストケースで退行確認
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_basic_regression():
    """基本的なケースが壊れていないか確認"""
    
    test_cases = [
        {
            "sentence": "The car is red.",
            "expected": {"S": "The car", "V": "is", "C1": "red"}
        },
        {
            "sentence": "I love you.", 
            "expected": {"S": "I", "V": "love", "O1": "you"}
        },
        {
            "sentence": "He has finished his homework.",
            "expected": {"S": "He", "Aux": "has", "V": "finished", "O1": "his homework"}
        }
    ]
    
    mapper = UnifiedStanzaRephraseMapper()
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('auxiliary_complex')
    
    print("🔍 基本的なテストケース実行...")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        sentence = test["sentence"]
        expected = test["expected"]
        
        print(f"\n📝 テスト{i}: {sentence}")
        
        result = mapper.process(sentence)
        actual = result.get('slots', {})
        
        # 空文字を除去
        actual_clean = {k: v for k, v in actual.items() if v}
        
        # 比較
        is_match = actual_clean == expected
        status = "✅ 成功" if is_match else "❌ 失敗"
        
        print(f"  {status}")
        if not is_match:
            print(f"    期待値: {expected}")
            print(f"    実際値: {actual_clean}")

if __name__ == "__main__":
    test_basic_regression()
