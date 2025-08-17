#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test32のみを検証
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_only_32():
    """Test32のみを実行"""
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Test32のみ実行
    test_case = test_data['data']['32']
    sentence = test_case['sentence']
    expected = test_case['expected']
    
    print(f"Test32: {sentence}")
    print(f"期待値: {expected}")
    
    # システム実行
    result = mapper.process(sentence)
    system_main = result.get('slots', {})
    system_sub = result.get('sub_slots', {})
    
    expected_main = expected.get('main_slots', {})
    expected_sub = expected.get('sub_slots', {})
    
    print(f"システム: {system_main}")
    print(f"期待値主節: {expected_main}")
    
    # 比較
    main_match = system_main == expected_main
    sub_match = system_sub == expected_sub
    
    print(f"主節一致: {main_match}")
    print(f"従属節一致: {sub_match}")
    
    if main_match and sub_match:
        print("結果: PERFECT ✅")
    elif main_match or sub_match:
        print("結果: PARTIAL ⚠️")
    else:
        print("結果: FAIL ❌")

if __name__ == "__main__":
    test_only_32()
