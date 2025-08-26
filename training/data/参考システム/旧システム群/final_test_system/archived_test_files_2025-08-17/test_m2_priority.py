#!/usr/bin/env python3
"""
M2優先配置ルールのテスト
"""

import os
import sys
import json
import logging

# プロジェクトルートパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_m2_priority():
    # ログレベル設定
    logging.basicConfig(level=logging.DEBUG)
    # テストケース：M2配置が期待される例文
    test_cases = [
        {
            "sentence": "The students study hard for exams.",
            "expected": {"M2": "hard"}
        },
        {
            "sentence": "The student writes essays carefully for better grades.",
            "expected": {"M2": "carefully"}
        },
        {
            "sentence": "The doctor who works carefully saves lives successfully.",
            "expected": {"M2": "successfully"}
        }
    ]
    
    mapper = UnifiedStanzaRephraseMapper()
    print("🎯 M2優先配置ルールテスト")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        print(f"\n📝 テスト{i}: {sentence}")
        
        result = mapper.process(sentence)
        slots = result.get('slots', {})
        
        # M2スロットの確認
        m2_slot = slots.get('M2', 'なし')
        expected_m2 = expected.get('M2', 'なし')
        
        print(f"   システムM2: {m2_slot}")
        print(f"   期待M2: {expected_m2}")
        
        if m2_slot == expected_m2:
            print("   ✅ M2配置正確")
        else:
            print("   ❌ M2配置不正確")
            print(f"   全スロット: {slots}")

if __name__ == "__main__":
    test_m2_priority()
