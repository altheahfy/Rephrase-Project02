#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_28_detailed():
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test_case = test_data['data']['28']
    sentence = test_case['sentence']
    expected = test_case['expected']
    
    print(f"Test28: {sentence}")
    print(f"期待値: {expected}")
    print()
    
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)
    
    main_result = result.get('slots', {})
    sub_result = result.get('sub_slots', {})
    
    main_expected = expected['main_slots']
    sub_expected = expected['sub_slots']
    
    print("=== 主節比較 ===")
    print(f"期待値: {main_expected}")
    print(f"システム: {main_result}")
    main_match = (main_result == main_expected)
    print(f"主節一致: {main_match}")
    print()
    
    print("=== 従属節比較 ===")
    print(f"期待値: {sub_expected}")
    print(f"システム: {sub_result}")
    sub_match = (sub_result == sub_expected)
    print(f"従属節一致: {sub_match}")
    
    if not main_match:
        print("\n主節の不一致詳細:")
        for key in set(list(main_expected.keys()) + list(main_result.keys())):
            exp_val = main_expected.get(key, "MISSING")
            sys_val = main_result.get(key, "MISSING")
            match_status = "✅" if exp_val == sys_val else "❌"
            print(f"  {key}: 期待値='{exp_val}' システム='{sys_val}' {match_status}")
    
    if not sub_match:
        print("\n従属節の不一致詳細:")
        for key in set(list(sub_expected.keys()) + list(sub_result.keys())):
            exp_val = sub_expected.get(key, "MISSING")
            sys_val = sub_result.get(key, "MISSING")
            match_status = "✅" if exp_val == sys_val else "❌"
            print(f"  {key}: 期待値='{exp_val}' システム='{sys_val}' {match_status}")

if __name__ == "__main__":
    test_28_detailed()
