#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
正当なテスト：unified_stanza_rephrase_mapper.py直接テスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_sentence_52():
    """Test 52の正当なテスト"""
    
    print("=== 初期化中... ===")
    mapper = UnifiedStanzaRephraseMapper()
    
    sentence = "The documents being reviewed thoroughly will be approved soon."
    print(f"=== 処理開始: {sentence} ===")
    
    result = mapper.process(sentence)
    
    print("\n=== Test 52 正当なテスト結果 ===")
    print(f"文: {sentence}")
    print(f"slots: {result['slots']}")
    print(f"sub_slots: {result['sub_slots']}")
    
    # 期待値との比較
    expected_sub_aux = "The documents being"
    actual_sub_aux = result['sub_slots'].get('sub-aux', '')
    
    print(f"\n=== 結果検証 ===")
    print(f"期待値 sub-aux: '{expected_sub_aux}'")
    print(f"実際値 sub-aux: '{actual_sub_aux}'")
    
    if actual_sub_aux == expected_sub_aux:
        print("✅ Test 52: PASS")
        return True
    else:
        print("❌ Test 52: FAIL")
        return False

if __name__ == "__main__":
    test_sentence_52()
