#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループの実際のテストデータでAbsoluteOrderManagerを検証
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def test_with_real_tell_data():
    """
    実際のtellグループテストデータでAbsoluteOrderManagerを検証
    """
    print("=== tellグループ実データテスト ===\n")
    
    # AbsoluteOrderManagerを初期化
    manager = AbsoluteOrderManager()
    
    # 修正済みテストデータを読み込み
    with open('final_54_test_data_with_absolute_order_fixed.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # tellグループのケースを抽出
    tell_cases = []
    for case_id, case_data in test_data['data'].items():
        if case_data.get('V_group_key') == 'tell':
            tell_cases.append({
                'case_id': case_id,
                'sentence': case_data['sentence'],
                'expected_slots': case_data['expected']['main_slots'],
                'expected_absolute_order': case_data.get('absolute_order', {}),
                'wh_word': case_data.get('wh_word'),
                'description': case_data.get('description', '')
            })
    
    print(f"tellグループケース数: {len(tell_cases)}")
    print()
    
    # 各ケースでAbsoluteOrderManagerをテスト
    for i, case in enumerate(tell_cases, 1):
        print(f"【ケース{i}】Case {case['case_id']}: {case['sentence']}")
        print(f"期待される順序: {case['description']}")
        print(f"wh-word: {case['wh_word']}")
        
        # AbsoluteOrderManagerで順序計算
        result = manager.apply_absolute_order(
            case['expected_slots'], 
            'tell', 
            case['wh_word']
        )
        
        # 結果比較
        print(f"計算結果:")
        for slot_info in result:
            slot_name = slot_info['slot']
            slot_value = slot_info['value']
            position = slot_info['absolute_position']
            print(f"  {slot_name}({slot_value}) → position {position}")
        
        # 期待値との比較（もしあれば）
        if case['expected_absolute_order']:
            print(f"期待値: {case['expected_absolute_order']}")
            
            # 一致チェック
            calculated_order = {item['slot']: item['absolute_position'] for item in result}
            matches = True
            for slot, expected_pos in case['expected_absolute_order'].items():
                if slot in calculated_order:
                    if calculated_order[slot] != expected_pos:
                        print(f"  ❌ {slot}: 期待値{expected_pos} != 計算値{calculated_order[slot]}")
                        matches = False
                    else:
                        print(f"  ✅ {slot}: 期待値{expected_pos} = 計算値{calculated_order[slot]}")
                else:
                    print(f"  ❌ {slot}: 計算結果に存在しない")
                    matches = False
            
            if matches:
                print("  🎉 完全一致！")
            else:
                print("  ⚠️ 不一致あり")
        else:
            print("  期待値なし（参考計算）")
        
        print("-" * 50)
        print()
    
    # 動的順序パターンの分析
    print("=== 動的順序パターン分析 ===")
    
    # M1の有無によるパターン分類
    m1_present = []
    m1_absent = []
    
    for case in tell_cases:
        if 'M1' in case['expected_slots']:
            m1_present.append(case)
        else:
            m1_absent.append(case)
    
    print(f"M1あり: {len(m1_present)}件")
    print(f"M1なし: {len(m1_absent)}件")
    
    if m1_present:
        print("\n【M1ありパターン】")
        for case in m1_present:
            print(f"  Case {case['case_id']}: {case['sentence']}")
    
    if m1_absent:
        print("\n【M1なしパターン】")
        for case in m1_absent:
            print(f"  Case {case['case_id']}: {case['sentence']}")
    
    # wh-word分析
    print("\n=== wh-word分析 ===")
    wh_words = {}
    for case in tell_cases:
        wh = case['wh_word']
        if wh:
            if wh not in wh_words:
                wh_words[wh] = []
            wh_words[wh].append(case)
    
    for wh, cases in wh_words.items():
        print(f"{wh}: {len(cases)}件")
        for case in cases:
            print(f"  Case {case['case_id']}: {case['sentence']}")


if __name__ == "__main__":
    test_with_real_tell_data()
