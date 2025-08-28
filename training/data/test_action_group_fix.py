#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正後のactionグループテスト
"""

from absolute_order_manager import AbsoluteOrderManager

def test_action_group_fix():
    """修正後のactionグループをテスト"""
    
    manager = AbsoluteOrderManager()
    
    print("=== 修正後actionグループテスト ===\n")
    
    # テストケース1: She sings beautifully
    test_cases = [
        {
            "sentence": "She sings beautifully.",
            "slots": {"S": "She", "V": "sings", "M2": "beautifully"},
            "v_group_key": "action",
            "group_population": {"S", "V", "M2"},
            "expected_order": "S(She)_1 → V(sings)_2 → M2(beautifully)_3"
        },
        {
            "sentence": "We always eat breakfast together.",
            "slots": {"S": "We", "V": "eat", "O1": "breakfast", "M1": "always", "M2": "together"},
            "v_group_key": "action", 
            "group_population": {"M1", "S", "V", "O1", "M2"},
            "expected_order": "M1(always)_1 → S(We)_2 → V(eat)_3 → O1(breakfast)_4 → M2(together)_5"
        },
        {
            "sentence": "The cat quietly sat on the mat.",
            "slots": {"S": "The cat", "V": "sat", "M1": "quietly", "M2": "on the mat"},
            "v_group_key": "action",
            "group_population": {"M1", "S", "V", "M2"},
            "expected_order": "M1(quietly)_1 → S(The cat)_2 → V(sat)_3 → M2(on the mat)_4"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"【ケース {i}】{case['sentence']}")
        print(f"スロット: {case['slots']}")
        print(f"期待語順: {case['expected_order']}")
        
        result = manager.apply_absolute_order(
            case["slots"],
            case["v_group_key"],
            None,
            case["group_population"]
        )
        
        # 結果表示
        actual_order = " → ".join([f"{item['slot']}({item['value']})_{item['absolute_position']}" for item in result])
        print(f"実際語順: {actual_order}")
        
        if actual_order == case['expected_order']:
            print("✅ 正しい語順")
        else:
            print("❌ 語順に問題あり")
        
        print("-" * 60)

if __name__ == "__main__":
    test_action_group_fix()
