#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
失敗した3つのケース専用テスト
"""

import sys
from central_controller import CentralController

def test_failed_cases():
    """失敗した3つの関係副詞ケース専用テスト"""
    print("=== 失敗ケース専用テスト ===")
    
    failed_cases = [
        {
            "id": "115",
            "sentence": "The place where we first met holds special memories.",
            "expected_main": {"S": "", "V": "holds", "O1": "special memories"},
            "expected_sub": {"sub-m2": "The place where", "sub-s": "we", "sub-v": "met", "sub-m3": "first", "_parent_slot": "S"}
        },
        {
            "id": "117", 
            "sentence": "The way how they approach problems gets results.",
            "expected_main": {"S": "", "V": "gets", "O1": "results"},
            "expected_sub": {"sub-m2": "The way how", "sub-s": "they", "sub-v": "approach", "sub-o1": "problems", "_parent_slot": "S"}
        },
        {
            "id": "118",
            "sentence": "The reason why technology changed became clear.",
            "expected_main": {"S": "", "V": "became", "C1": "clear"},
            "expected_sub": {"sub-m2": "The reason why", "sub-s": "technology", "sub-v": "changed", "_parent_slot": "S"}
        }
    ]
    
    controller = CentralController()
    
    for case in failed_cases:
        print(f"\n--- Case {case['id']} ---")
        print(f"文: {case['sentence']}")
        
        result = controller.process_sentence(case['sentence'])
        
        print(f"実際の主節: {result.get('main_slots')}")
        print(f"期待の主節: {case['expected_main']}")
        print(f"実際の従節: {result.get('sub_slots')}")
        print(f"期待の従節: {case['expected_sub']}")
        
        main_match = result.get('main_slots') == case['expected_main']
        sub_match = result.get('sub_slots') == case['expected_sub']
        
        print(f"主節一致: {main_match}")
        print(f"従節一致: {sub_match}")
        print(f"総合: {'✅ PASS' if main_match and sub_match else '❌ FAIL'}")

if __name__ == "__main__":
    test_failed_cases()
