#!/usr/bin/env python3
"""Case 133専用デバッグスクリプト"""

import sys
sys.path.append(".")

from central_controller import CentralController
import json

def test_case_133():
    """Case 133のデバッグテスト"""
    controller = CentralController()
    
    # Case 133: 仮定法過去
    sentence = "If I were rich, I would travel around the world."
    print("=== Case 133 Debug Test ===")
    print(f"入力文: {sentence}")
    
    # 処理実行
    result = controller.process_sentence(sentence)
    
    print("=== 処理結果 ===")
    print(f"Success: {result.get('success', False)}")
    print(f"Main slots: {result.get('main_slots', {})}")
    print(f"Sub slots: {result.get('sub_slots', {})}")
    
    # 期待値と比較
    expected = {
        "main_slots": {
            "S": "I",
            "Aux": "would",
            "V": "travel",
            "M2": "",
            "M3": "around the world"
        },
        "sub_slots": {
            "sub-s": "If I",
            "sub-v": "were",
            "sub-c1": "rich",
            "_parent_slot": "M2"
        }
    }
    
    print("=== 期待値比較 ===")
    if result.get('success', False):
        main_slots = result.get('main_slots', {})
        sub_slots = result.get('sub_slots', {})
        
        print("Main slots:")
        for key, expected_value in expected['main_slots'].items():
            actual_value = main_slots.get(key, "MISSING")
            status = "✅" if actual_value == expected_value else "❌"
            print(f"  {status} {key}: expected='{expected_value}' actual='{actual_value}'")
        
        print("Sub slots:")
        for key, expected_value in expected['sub_slots'].items():
            actual_value = sub_slots.get(key, "MISSING")
            status = "✅" if actual_value == expected_value else "❌"
            print(f"  {status} {key}: expected='{expected_value}' actual='{actual_value}'")
    else:
        print("❌ 処理が失敗しました")

if __name__ == "__main__":
    test_case_133()
