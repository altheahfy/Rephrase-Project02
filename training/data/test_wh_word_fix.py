#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wh-word位置1修正版のテスト
"""

from absolute_order_manager_fixed import AbsoluteOrderManager
import json

def test_wh_word_position_fix():
    """wh-word位置1修正の検証"""
    
    print("🔍 wh-word位置1修正版テスト")
    print("=" * 60)
    
    manager = AbsoluteOrderManager()
    
    # tellグループ母集団
    tell_population = {'Aux', 'M2', 'M2_END', 'O1', 'O2', 'S', 'V'}
    
    # テストケース1: What（O2に配置、位置1に移動すべき）
    print("【Test 1】What did he tell her at the store?")
    slots1 = {'O2': 'What', 'Aux': 'did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'M3': 'at the store'}
    result1 = manager.apply_absolute_order(slots1, "tell", "what", tell_population)
    
    order_display1 = []
    for item in result1:
        order_display1.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display1)}")
    print()
    
    # テストケース2: Where（M2に配置、位置1に移動すべき）
    print("【Test 2】Where did you tell me a story?")
    slots2 = {'M2': 'Where', 'Aux': 'did', 'S': 'you', 'V': 'tell', 'O1': 'me', 'O2': 'a story'}
    result2 = manager.apply_absolute_order(slots2, "tell", "where", tell_population)
    
    order_display2 = []
    for item in result2:
        order_display2.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display2)}")
    print()
    
    # テストケース3: 通常文（wh-wordなし）
    print("【Test 3】Did he tell her a secret there?")
    slots3 = {'Aux': 'Did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'O2': 'a secret', 'M3': 'there'}
    result3 = manager.apply_absolute_order(slots3, "tell", None, tell_population)
    
    order_display3 = []
    for item in result3:
        order_display3.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
    print(f"📍 結果: {' → '.join(order_display3)}")
    print()
    
    print("✅ wh-word位置1修正版テスト完了")

if __name__ == "__main__":
    test_wh_word_position_fix()
