#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
グループ内絶対位置固定版のテスト
"""

from absolute_order_manager_group_fixed import AbsoluteOrderManager
import json

def test_group_fixed_position():
    """グループ内絶対位置固定版の検証"""
    
    print("🔍 グループ内絶対位置固定版テスト")
    print("=" * 60)
    
    manager = AbsoluteOrderManager()
    
    # tellグループ母集団
    tell_population = {'Aux', 'M2', 'M2_END', 'O1', 'O2', 'S', 'V'}
    
    print("📋 tellグループ期待される固定位置:")
    print("M1(not in population) → スキップ")
    print("M2 → 位置2")
    print("Aux → 位置3") 
    print("S → 位置4")
    print("V → 位置5")
    print("O1 → 位置6")
    print("O2 → 位置7")
    print("M2_END → 位置8")
    print()
    
    # テストケース1: What疑問文
    print("【Test 1】What did he tell her at the store?")
    slots1 = {'O2': 'What', 'Aux': 'did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'M3': 'at the store'}
    result1 = manager.apply_absolute_order(slots1, "tell", "what", tell_population)
    
    order_display1 = []
    for item in result1:
        order_display1.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display1)}")
    print()
    
    # テストケース2: 通常文（wh-wordなし）
    print("【Test 2】Did he tell her a secret there?")
    slots2 = {'Aux': 'Did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'O2': 'a secret', 'M3': 'there'}
    result2 = manager.apply_absolute_order(slots2, "tell", None, tell_population)
    
    order_display2 = []
    for item in result2:
        order_display2.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display2)}")
    print()
    
    # テストケース3: Where疑問文
    print("【Test 3】Where did you tell me a story?")
    slots3 = {'M2': 'Where', 'Aux': 'did', 'S': 'you', 'V': 'tell', 'O1': 'me', 'O2': 'a story'}
    result3 = manager.apply_absolute_order(slots3, "tell", "where", tell_population)
    
    order_display3 = []
    for item in result3:
        order_display3.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display3)}")
    print()
    
    # 位置一貫性チェック
    print("🔍 位置一貫性チェック:")
    
    # Test1とTest2でAuxの位置が同じか
    aux_pos_1 = next((item['absolute_position'] for item in result1 if item['slot'] == 'Aux'), None)
    aux_pos_2 = next((item['absolute_position'] for item in result2 if item['slot'] == 'Aux'), None)
    
    if aux_pos_1 == aux_pos_2:
        print(f"✅ Aux位置一貫性: Test1({aux_pos_1}) == Test2({aux_pos_2})")
    else:
        print(f"❌ Aux位置不一致: Test1({aux_pos_1}) != Test2({aux_pos_2})")
    
    # Test1とTest3でO2の位置が同じか
    o2_pos_1 = next((item['absolute_position'] for item in result1 if item['slot'] == 'O2'), None)
    o2_pos_3 = next((item['absolute_position'] for item in result3 if item['slot'] == 'O2'), None)
    
    if o2_pos_1 == o2_pos_3:
        print(f"✅ O2位置一貫性: Test1({o2_pos_1}) == Test3({o2_pos_3})")
    else:
        print(f"❌ O2位置不一致: Test1({o2_pos_1}) != Test3({o2_pos_3})")
    
    print()
    print("✅ グループ内絶対位置固定版テスト完了")

if __name__ == "__main__":
    test_group_fixed_position()
