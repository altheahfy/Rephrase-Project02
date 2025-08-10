#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Order=99問題の詳細分析
"""

import pandas as pd
import os

def main():
    print("🔍 Order=99問題の詳細分析")
    print("=" * 50)
    
    # Excelファイルを探す
    excel_files = [f for f in os.listdir('.') if f.startswith('例文入力元_分解結果_v2_') and f.endswith('.xlsx')]
    if not excel_files:
        print("❌ Excelファイルが見つかりません")
        return
    
    excel_file = sorted(excel_files)[-1]
    print(f"📊 対象ファイル: {excel_file}")
    
    df = pd.read_excel(excel_file)
    
    # Order=99の詳細分析
    order_99_data = df[df['Slot_display_order'] == 99]
    print(f"\n❌ Order=99 の詳細 ({len(order_99_data)} 件):")
    
    print("\n📊 V_group_key別の分布:")
    vgroup_dist = order_99_data['V_group_key'].value_counts()
    for vgroup, count in vgroup_dist.items():
        print(f"  {vgroup}: {count} 件")
    
    print("\n📊 スロット別の分布:")
    slot_dist = order_99_data['Slot'].value_counts()
    for slot, count in slot_dist.items():
        print(f"  {slot}: {count} 件")
    
    print(f"\n🔍 Order=99 の具体例:")
    sample_99 = order_99_data[['V_group_key', 'Slot', 'SlotPhrase', 'Slot_display_order']].head(10)
    print(sample_99.to_string(index=False))
    
    # 正常なorder値との比較
    print(f"\n✅ 正常なorder値の分布:")
    normal_orders = df[df['Slot_display_order'] != 99]
    normal_dist = normal_orders['Slot_display_order'].value_counts().sort_index()
    for order_val, count in normal_dist.items():
        print(f"  order={order_val}: {count} 件")

if __name__ == "__main__":
    main()
