#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_28():
    # Test28データを確認
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test_case = test_data['data']['28']
    sentence = test_case['sentence']
    expected = test_case['expected']
    
    print(f"Test28: {sentence}")
    print(f"期待値: {expected}")
    print()
    
    # システム実行
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)
    
    print(f"システム結果: {result}")
    print()
    
    # 比較
    main_expected = expected['main_slots']
    sub_expected = expected['sub_slots']
    
    main_result = result.get('slots', {})
    sub_result = result.get('sub_slots', {})
    
    print("=== 主節比較 ===")
    print(f"期待値: {main_expected}")
    print(f"システム: {main_result}")
    
    # 期待値に含まれるキーのみを比較
    main_match = True
    for key, expected_value in main_expected.items():
        actual_value = main_result.get(key, '')
        if actual_value != expected_value:
            main_match = False
            print(f"  不一致: {key} 期待='{expected_value}' 実際='{actual_value}'")
    
    print(f"主節一致: {main_match}")
    print()
    
    print("=== 従属節比較 ===")
    print(f"期待値: {sub_expected}")
    print(f"システム: {sub_result}")
    
    # 期待値に含まれるキーのみを比較
    sub_match = True
    for key, expected_value in sub_expected.items():
        actual_value = sub_result.get(key, '')
        if actual_value != expected_value:
            sub_match = False
            print(f"  不一致: {key} 期待='{expected_value}' 実際='{actual_value}'")
    
    print(f"従属節一致: {sub_match}")
    print()
    
    if main_match and sub_match:
        print("結果: PERFECT ✅")
    elif main_match:
        print("結果: PARTIAL ⚠️")
    else:
        print("結果: FAILED ❌")

if __name__ == "__main__":
    test_28()
