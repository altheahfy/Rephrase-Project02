#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループ固定位置システムテスト
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def test_tell_group_fixed_positions():
    """tellグループの固定位置システムをテスト"""
    
    # AbsoluteOrderManagerインスタンス
    manager = AbsoluteOrderManager()
    
    # tellグループテストケース
    test_cases = [
        {
            "case_id": 83,
            "sentence": "What did he tell her at the store?",
            "slots": {"O2": "What", "Aux": "did", "S": "he", "V": "tell", "O1": "her", "M3": "at the store"},
            "v_group_key": "tell",
            "wh_word": "what",
            "expected": {"O2": 2, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M3": 8}
        },
        {
            "case_id": 84,
            "sentence": "Did he tell her a secret there?",
            "slots": {"Aux": "Did", "S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M3": "there"},
            "v_group_key": "tell",
            "wh_word": None,
            "expected": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M3": 8}
        },
        {
            "case_id": 85,
            "sentence": "Did I tell him a truth in the kitchen?",
            "slots": {"Aux": "Did", "S": "I", "V": "tell", "O1": "him", "O2": "a truth", "M3": "in the kitchen"},
            "v_group_key": "tell",
            "wh_word": None,
            "expected": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M3": 8}
        },
        {
            "case_id": 86,
            "sentence": "Where did you tell me a story?",
            "slots": {"M2": "Where", "Aux": "did", "S": "you", "V": "tell", "O1": "me", "O2": "a story"},
            "v_group_key": "tell",
            "wh_word": "where",
            "expected": {"M2": 1, "Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7}
        }
    ]
    
    print("=== tellグループ固定位置システムテスト ===\n")
    
    all_passed = True
    
    for case in test_cases:
        print(f"【Case {case['case_id']}】{case['sentence']}")
        print(f"スロット: {case['slots']}")
        
        # AbsoluteOrderManager実行
        result = manager.apply_absolute_order(
            case["slots"], 
            case["v_group_key"], 
            case["wh_word"]
        )
        
        # 結果から絶対位置マッピングを生成
        actual_positions = {}
        for item in result:
            actual_positions[item["slot"]] = item["absolute_position"]
        
        print(f"期待される絶対順序: {case['expected']}")
        print(f"実際の絶対順序: {actual_positions}")
        
        # 検証
        case_passed = True
        for slot, expected_position in case["expected"].items():
            if slot in actual_positions:
                actual_position = actual_positions[slot]
                if expected_position == actual_position:
                    print(f"✅ {slot}: {actual_position}")
                else:
                    print(f"❌ {slot}: 期待値{expected_position} ≠ 実際{actual_position}")
                    case_passed = False
            else:
                print(f"❌ {slot}: スロットが見つからない")
                case_passed = False
        
        if case_passed:
            print("✅ テストケース成功")
        else:
            print("❌ テストケース失敗")
            all_passed = False
        
        print("-" * 60)
    
    if all_passed:
        print("\n🎉 全テストケース成功！")
    else:
        print("\n⚠️ 一部テストケースが失敗しました")
    
    return all_passed

if __name__ == "__main__":
    test_tell_group_fixed_positions()
