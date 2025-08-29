#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用システムテスト（group_populationを使用）
"""

from absolute_order_manager_group_fixed import AbsoluteOrderManager

def test_universal_system():
    """
    汎用システムのテスト（母集団から要素リストを動的生成）
    """
    print("🎯 汎用システムテスト（母集団ベース）")
    print("=" * 60)
    
    # tellグループの母集団データ（例）
    tell_group_population = [
        {
            "slots": {"O2": "What", "Aux": "did", "S": "he", "V": "tell", "O1": "her", "M2": "at the store"},
            "group_info": {"V_group_key": "tell"}
        },
        {
            "slots": {"Aux": "Did", "S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M2": "there"},
            "group_info": {"V_group_key": "tell"}
        },
        {
            "slots": {"M2": "Where", "Aux": "did", "S": "you", "V": "tell", "O1": "me", "O2": "a story"},
            "group_info": {"V_group_key": "tell"}
        },
        {
            "slots": {"Aux": "Did", "S": "I", "V": "tell", "O1": "him", "O2": "a truth", "M2": "in the kitchen"},
            "group_info": {"V_group_key": "tell"}
        }
    ]
    
    manager = AbsoluteOrderManager()
    
    # テストケース1: What疑問詞
    print("\n📋 Test Case 1: What did he tell her at the store?")
    test_slots = {"O2": "What", "Aux": "did", "S": "he", "V": "tell", "O1": "her", "M2": "at the store"}
    result = manager.apply_absolute_order(test_slots, "tell", group_population=tell_group_population)
    
    actual_order = {}
    for item in result:
        actual_order[item["slot"]] = item["absolute_position"]
    
    print(f"🎯 Result: {actual_order}")
    
    # テストケース2: 標準文
    print("\n📋 Test Case 2: Did he tell her a secret there?")
    test_slots = {"Aux": "Did", "S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M2": "there"}
    result = manager.apply_absolute_order(test_slots, "tell", group_population=tell_group_population)
    
    actual_order = {}
    for item in result:
        actual_order[item["slot"]] = item["absolute_position"]
    
    print(f"🎯 Result: {actual_order}")

if __name__ == "__main__":
    test_universal_system()
