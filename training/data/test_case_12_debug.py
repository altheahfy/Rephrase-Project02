#!/usr/bin/env python3
"""
Case 12 whose構文エラー診断テスト
"""

import sys
sys.path.append('.')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_case_12():
    mapper = UnifiedStanzaRephraseMapper()
    
    print("=== Case 12分析 ===")
    sentence = "The man whose car is red lives here."
    print(f"文: {sentence}")
    
    result = mapper.process(sentence)
    
    print(f"実際メイン: {result['slots']}")
    print(f"実際サブ: {result['sub_slots']}")
    
    # 期待値
    expected_main = {"S": "", "V": "lives", "M2": "here"}
    expected_sub = {"sub-s": "The man whose car", "sub-v": "is", "sub-c1": "red"}
    
    print(f"期待メイン: {expected_main}")
    print(f"期待サブ: {expected_sub}")
    
    print(f"問題: 不要なC1='red lives'が追加されている")

if __name__ == "__main__":
    test_case_12()
