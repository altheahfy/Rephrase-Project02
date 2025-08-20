#!/usr/bin/env python3
"""
Case 43 副詞重複エラー診断テスト
"""

import sys
sys.path.append('.')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_case_43():
    mapper = UnifiedStanzaRephraseMapper()
    
    print("=== Case 43分析 ===")
    sentence = "The book that was written very carefully by the author became famous."
    print(f"文: {sentence}")
    
    result = mapper.process(sentence)
    
    print(f"実際メイン: {result['slots']}")
    print(f"実際サブ: {result['sub_slots']}")
    
    # 期待値 (final_54_test_data.jsonから)
    expected_main = {"S": "", "Aux": "was", "V": "written", "M1": "very carefully", "M2": "by the author"}
    expected_sub = {"sub-s": "The book", "sub-v": "became", "sub-c1": "famous"}
    
    print(f"期待メイン: {expected_main}")
    print(f"期待サブ: {expected_sub}")

if __name__ == "__main__":
    test_case_43()
