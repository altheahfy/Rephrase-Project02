#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def quick_test19():
    # Test19のみをテスト
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test19 = test_data['data']['19']
    sentence = test19['sentence']
    expected = test19['expected']
    
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)
    
    main_expected = expected['main_slots']
    sub_expected = expected['sub_slots']
    main_result = result.get('slots', {})
    sub_result = result.get('sub_slots', {})
    
    main_match = (main_result == main_expected)
    sub_match = (sub_result == sub_expected)
    
    if main_match and sub_match:
        print("Test19: PERFECT ✅")
    elif main_match:
        print("Test19: PARTIAL ⚠️")
    else:
        print("Test19: FAIL ❌")
        
    print(f"主節一致: {main_match}")
    print(f"従属節一致: {sub_match}")

if __name__ == "__main__":
    quick_test19()
