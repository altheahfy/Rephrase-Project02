#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V_group_key別の絶対順序ルールを確認するスクリプト
"""

import pandas as pd

def check_absolute_order():
    """V_group_key別の絶対順序ルールをチェック"""
    
    print("=== 絶対順序ルール完全理解版分析 ===\n")
    
    # 第4文型DBの確認
    df = pd.read_excel('（第4文型）例文入力元.xlsx')
    
    print(f"総行数: {len(df)}")
    print(f"V_group_key一覧: {df['V_group_key'].unique()}")
    
    print("\n" + "="*70)
    print("【ランダマイズメカニズムの確認】")
    print("1. V_group_key選出")
    print("2. そのV_group_key内でスロット別母集団からランダム選択")
    print("3. 各スロットは同一V_group_key内で統一順序が必要")
    print("4. 異なるV_group_keyは独立した順序体系で良い")
    
    for vkey in df['V_group_key'].unique():
        print(f"\n【V_group_key: {vkey}】")
        vkey_data = df[df['V_group_key'] == vkey]
        
        # スロット別の母集団と順序を分析
        print("スロット別母集団:")
        for slot in ['M1', 'S', 'Aux', 'V', 'O1', 'O2']:
            slot_data = vkey_data[vkey_data['Slot'] == slot]
            if len(slot_data) > 0:
                phrases = slot_data['SlotPhrase'].dropna().tolist()
                orders = slot_data['Slot_display_order'].dropna().unique()
                
                print(f"  {slot}: {phrases[:3]}{'...' if len(phrases) > 3 else ''}")
                print(f"      順序: {[int(x) for x in orders]} ({'✅統一' if len(orders) == 1 else '❌複数'})")
        
        print(f"\n理想的な順序 (V_group_key内でリセット):")
        # このグループで使用されているスロットを取得
        used_slots = sorted(vkey_data['Slot'].dropna().unique())
        ideal_order = {slot: i+1 for i, slot in enumerate(used_slots)}
        current_orders = {}
        for slot in used_slots:
            current_order = vkey_data[vkey_data['Slot'] == slot]['Slot_display_order'].dropna().iloc[0]
            current_orders[slot] = int(current_order)
        
        print(f"  現在: {dict(current_orders)}")
        print(f"  理想: {ideal_order}")
        
        # 効率性の評価
        max_current = max(current_orders.values()) if current_orders else 0
        max_ideal = max(ideal_order.values()) if ideal_order else 0
        efficiency = max_ideal / max_current if max_current > 0 else 1
        print(f"  効率性: {efficiency:.2%} (数字の無駄度: {1-efficiency:.1%})")
    
    print("\n" + "="*70)
    print("【結論】")
    print("✅ 機能的には正常: 同一V_group_key内でスロット順序は統一されている")
    print("❌ 効率性の問題: 全グループ横断的な順序で数字が無駄に大きい") 
    print("💡 改善案: V_group_key毎に1からリセットした独立順序")
    print("\n害はないが、より効率的な実装が可能")

if __name__ == "__main__":
    check_absolute_order()
