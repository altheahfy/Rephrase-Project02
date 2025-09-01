#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 131デバッグスクリプト
"If it rains tomorrow, I will stay home."の処理を詳細追跡
"""

from central_controller import CentralController

def test_case_131():
    print("=== Case 131 Debug Test ===")
    sentence = "If it rains tomorrow, I will stay home."
    print(f"入力文: {sentence}")
    
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print(f"\n=== 処理結果 ===")
    print(f"Success: {result.get('success', False)}")
    print(f"Main slots: {result.get('main_slots', {})}")
    print(f"Sub slots: {result.get('sub_slots', {})}")
    
    # 期待値と比較
    expected_main_slots = {
        "M1": "",
        "S": "I",
        "Aux": "will",
        "V": "stay",
        "M2": "home"
    }
    expected_sub_slots = {
        "sub-s": "If it",
        "sub-v": "rains",
        "sub-m2": "tomorrow",
        "_parent_slot": "M1"
    }
    
    print(f"\n=== 期待値比較 ===")
    actual_main = result.get('main_slots', {})
    actual_sub = result.get('sub_slots', {})
    
    print("Main slots:")
    for key, expected_val in expected_main_slots.items():
        actual_val = actual_main.get(key, "MISSING")
        status = "✅" if actual_val == expected_val else "❌"
        print(f"  {status} {key}: expected='{expected_val}' actual='{actual_val}'")
    
    print("Sub slots:")
    for key, expected_val in expected_sub_slots.items():
        actual_val = actual_sub.get(key, "MISSING")
        status = "✅" if actual_val == expected_val else "❌"
        print(f"  {status} {key}: expected='{expected_val}' actual='{actual_val}'")

if __name__ == "__main__":
    test_case_131()
