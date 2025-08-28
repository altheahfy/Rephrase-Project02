#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用グループ人口分析システムテスト
"""

from absolute_order_manager import AbsoluteOrderManager

def test_universal_system():
    """汎用グループ人口分析システムをテスト"""
    
    manager = AbsoluteOrderManager()
    
    # テストケース1: tellグループ（時間副詞あり）
    print("=== テストケース1: tellグループ（時間副詞あり）===")
    
    # グループ母集団: M1 + 基本要素
    group_population = {"M1", "Aux", "S", "V", "O1", "O2", "M2_END"}
    
    test_cases = [
        {
            "sentence": "Did she tell me a story?",
            "slots": {"Aux": "Did", "S": "she", "V": "tell", "O1": "me", "O2": "a story"},
            "expected_order": ["Aux_2", "S_3", "V_4", "O1_5", "O2_6"]
        },
        {
            "sentence": "This morning, did I tell him a truth?",
            "slots": {"M1": "This morning", "Aux": "did", "S": "I", "V": "tell", "O1": "him", "O2": "a truth"},
            "expected_order": ["M1_1", "Aux_2", "S_3", "V_4", "O1_5", "O2_6"]
        },
        {
            "sentence": "Before dinner, did they tell my little brother a funny story?",
            "slots": {"M1": "Before dinner", "Aux": "did", "S": "they", "V": "tell", "O1": "my little brother", "O2": "a funny story"},
            "expected_order": ["M1_1", "Aux_2", "S_3", "V_4", "O1_5", "O2_6"]
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【ケース {i}】{case['sentence']}")
        print(f"スロット: {case['slots']}")
        
        result = manager.apply_absolute_order(
            case["slots"], 
            "tell", 
            None, 
            group_population
        )
        
        # 結果検証
        actual_order = [f"{item['slot']}_{item['absolute_position']}" for item in result]
        print(f"期待順序: {case['expected_order']}")
        print(f"実際順序: {actual_order}")
        
        if actual_order == case['expected_order']:
            print("✅ 正しい絶対位置")
        else:
            print("❌ 絶対位置に問題あり")
        
        print("-" * 50)
    
    # テストケース2: beグループ
    print("\n=== テストケース2: beグループ ===")
    
    be_group_population = {"Aux", "S", "V", "C1"}
    be_case = {
        "sentence": "Is he a teacher?",
        "slots": {"Aux": "Is", "S": "he", "V": "be", "C1": "a teacher"},
        "expected_order": ["Aux_1", "S_2", "V_3", "C1_4"]
    }
    
    print(f"【be例】{be_case['sentence']}")
    print(f"スロット: {be_case['slots']}")
    
    result = manager.apply_absolute_order(
        be_case["slots"], 
        "be", 
        None, 
        be_group_population
    )
    
    actual_order = [f"{item['slot']}_{item['absolute_position']}" for item in result]
    print(f"期待順序: {be_case['expected_order']}")
    print(f"実際順序: {actual_order}")
    
    if actual_order == be_case['expected_order']:
        print("✅ be動詞語順正しい")
    else:
        print("❌ be動詞語順に問題あり")

if __name__ == "__main__":
    test_universal_system()
