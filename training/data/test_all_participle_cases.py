#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # 4つの分詞構文ケースをテスト
    test_cases = [
        {
            "id": 49,
            "sentence": "The team working overtime completed the project successfully yesterday.",
            "expected": {
                "main_slots": {"S": "", "V": "completed", "O1": "the project", "M2": "successfully", "M3": "yesterday"},
                "sub_slots": {"sub-v": "the team working", "sub-m2": "overtime"}
            }
        },
        {
            "id": 50,
            "sentence": "The woman standing quietly near the door was waiting patiently.",
            "expected": {
                "main_slots": {"S": "", "Aux": "was", "V": "waiting", "M3": "patiently"},
                "sub_slots": {"sub-v": "the woman standing", "sub-m2": "quietly", "sub-m3": "near the door"}
            }
        },
        {
            "id": 51,
            "sentence": "The children playing happily in the garden were supervised carefully.",
            "expected": {
                "main_slots": {"S": "", "Aux": "were", "V": "supervised", "M3": "carefully"},
                "sub_slots": {"sub-v": "the children playing", "sub-m2": "happily", "sub-m3": "in the garden"}
            }
        },
        {
            "id": 52,
            "sentence": "The documents being reviewed thoroughly will be approved soon.",
            "expected": {
                "main_slots": {"S": "", "Aux": "will be", "V": "approved", "M2": "soon"},
                "sub_slots": {"sub-aux": "the documents being", "sub-v": "reviewed", "sub-m2": "thoroughly"}
            }
        }
    ]
    
    success_count = 0
    
    for case in test_cases:
        print(f"\n=== Case {case['id']}: {case['sentence']} ===")
        
        result = mapper.process(case['sentence'])
        actual_main = result.get('slots', {})
        actual_sub = result.get('sub_slots', {})
        expected_main = case['expected']['main_slots']
        expected_sub = case['expected']['sub_slots']
        
        # 比較
        main_match = all(actual_main.get(k) == v for k, v in expected_main.items())
        sub_match = all(actual_sub.get(k) == v for k, v in expected_sub.items())
        
        if main_match and sub_match:
            print("✅ COMPLETE MATCH")
            success_count += 1
        else:
            print("❌ MISMATCH")
            print(f"Expected main: {expected_main}")
            print(f"Actual main:   {actual_main}")
            print(f"Expected sub:  {expected_sub}")
            print(f"Actual sub:    {actual_sub}")
        
        detected_patterns = result.get('grammar_info', {}).get('detected_patterns', [])
        print(f"Detected patterns: {detected_patterns}")
    
    print(f"\n📊 分詞構文テスト結果: {success_count}/4 ケース成功 ({success_count/4*100:.1f}%)")

if __name__ == "__main__":
    main()
