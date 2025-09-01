#!/usr/bin/env python3
"""Case 132専用デバッグスクリプト"""

import sys
sys.path.append(".")

from central_controller import CentralController
import json

def test_case_132():
    """Case 132のデバッグテスト"""
    controller = CentralController()
    
    # Case 132: 条件文
    sentence = "If you study hard, you can pass the exam."
    print("=== Case 132 Debug Test ===")
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
            "M2": "",
            "S": "you",
            "Aux": "can",
            "V": "pass",
            "O1": "the exam"
        },
        "sub_slots": {
            "sub-s": "If you",
            "sub-v": "study",
            "sub-m2": "hard",
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
    test_case_132()
