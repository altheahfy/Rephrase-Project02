#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包括的検証スクリプト - あらゆる観点から解析結果を検証
"""

import pandas as pd
import json
from collections import defaultdict, Counter
import re
import os

def main():
    print("=" * 60)
    print("🔍 包括的検証開始 - あらゆる観点からチェック")
    print("=" * 60)
    
    # Excelファイルを探す
    excel_files = [f for f in os.listdir('.') if f.startswith('例文入力元_分解結果_v2_') and f.endswith('.xlsx')]
    if not excel_files:
        print("❌ Excelファイルが見つかりません")
        return
    
    excel_file = sorted(excel_files)[-1]  # 最新のファイル
    print(f"📊 検証対象ファイル: {excel_file}")
    
    try:
        df = pd.read_excel(excel_file)
        print(f"✅ Excel読み込み成功: {len(df)} 行")
    except Exception as e:
        print(f"❌ Excel読み込みエラー: {e}")
        return
    
    # 1. データ構造の基本検証
    print("\n" + "=" * 50)
    print("1️⃣ データ構造の基本検証")
    print("=" * 50)
    
    print(f"📊 総行数: {len(df)}")
    print(f"📊 列数: {len(df.columns)}")
    print(f"📊 列名: {list(df.columns)}")
    
    # 空欄・欠損値チェック
    null_counts = df.isnull().sum()
    print(f"\n🔍 欠損値チェック:")
    for col in df.columns:
        if null_counts[col] > 0:
            print(f"  ❌ {col}: {null_counts[col]} 件の欠損値")
        else:
            print(f"  ✅ {col}: 欠損値なし")
    
    # 実際の列名にマッピング
    column_mapping = {
        'example': '原文',
        'slot': 'Slot', 
        'order': 'Slot_display_order',
        'label': 'PhraseType',
        'value': 'SlotPhrase'
    }
    
    # 2. Order値の詳細分析
    print("\n" + "=" * 50)
    print("2️⃣ Order値の詳細分析")
    print("=" * 50)
    
    if 'Slot_display_order' in df.columns:
        order_distribution = df['Slot_display_order'].value_counts().sort_index()
        print("📊 Order値の分布:")
        for order_val, count in order_distribution.items():
            print(f"  order={order_val}: {count} 件")
        
        # 異常なorder値をチェック
        abnormal_orders = df[df['Slot_display_order'] > 10]
        if len(abnormal_orders) > 0:
            print(f"\n❌ 異常なorder値 (>10): {len(abnormal_orders)} 件")
            print(abnormal_orders[['原文', 'Slot', 'Slot_display_order', 'PhraseType']].head())
        else:
            print("✅ 異常なorder値はありません")
    
    # 3. スロット分析
    print("\n" + "=" * 50)
    print("3️⃣ スロット分析")
    print("=" * 50)
    
    if 'Slot' in df.columns:
        slot_distribution = df['Slot'].value_counts()
        print("📊 スロット分布:")
        for slot, count in slot_distribution.items():
            print(f"  {slot}: {count} 件")
        
        # 各スロットのorder値範囲をチェック
        print("\n🔍 スロット別order値範囲:")
        for slot in sorted(df['Slot'].unique()):
            slot_orders = df[df['Slot'] == slot]['Slot_display_order'].unique()
            print(f"  {slot}: {sorted(slot_orders)}")
    
    # 4. Label分析（phrase/word）
    print("\n" + "=" * 50)
    print("4️⃣ Label分析（phrase/word）")
    print("=" * 50)
    
    if 'PhraseType' in df.columns:
        label_distribution = df['PhraseType'].value_counts()
        print("📊 Label分布:")
        for label, count in label_distribution.items():
            print(f"  {label}: {count} 件")
        
        # スロット別のlabel分布
        print("\n🔍 スロット別label分布:")
        for slot in sorted(df['Slot'].unique()):
            slot_labels = df[df['Slot'] == slot]['PhraseType'].value_counts()
            print(f"  {slot}: {dict(slot_labels)}")
    
    # 5. 例文レベルの分析
    print("\n" + "=" * 50)
    print("5️⃣ 例文レベルの分析")
    print("=" * 50)
    
    # 原文が欠損していない行のみで分析
    df_with_example = df.dropna(subset=['原文'])
    if len(df_with_example) > 0:
        unique_examples = df_with_example['原文'].nunique()
        print(f"📊 ユニークな例文数: {unique_examples}")
        
        # 例文あたりの要素数分布
        elements_per_example = df_with_example.groupby('原文').size()
        print(f"📊 例文あたりの要素数:")
        print(f"  平均: {elements_per_example.mean():.1f}")
        print(f"  最小: {elements_per_example.min()}")
        print(f"  最大: {elements_per_example.max()}")
        
        # 最も複雑な例文を表示
        most_complex = elements_per_example.idxmax()
        print(f"\n🔍 最も複雑な例文 ({elements_per_example.max()} 要素):")
        print(f"  {most_complex}")
        complex_elements = df_with_example[df_with_example['原文'] == most_complex][['Slot', 'Slot_display_order', 'SlotPhrase', 'PhraseType']]
        print(complex_elements.to_string(index=False))
    
    # 6. Value内容の分析
    print("\n" + "=" * 50)
    print("6️⃣ Value内容の分析")
    print("=" * 50)
    
    if 'SlotPhrase' in df.columns:
        # 空のvalue値をチェック
        empty_values = df[df['SlotPhrase'].isna() | (df['SlotPhrase'] == '')]
        if len(empty_values) > 0:
            print(f"❌ 空のSlotPhrase: {len(empty_values)} 件")
            print(empty_values[['原文', 'Slot', 'SlotPhrase']].head())
        else:
            print("✅ 空のSlotPhrase値はありません")
        
        # 各スロットの典型的なvalue例
        print(f"\n🔍 スロット別SlotPhrase例:")
        for slot in sorted(df['Slot'].unique()):
            slot_values = df[df['Slot'] == slot]['SlotPhrase'].value_counts().head(3)
            print(f"  {slot}: {list(slot_values.index)}")
    
    # 7. 一貫性チェック
    print("\n" + "=" * 50)
    print("7️⃣ 一貫性チェック")
    print("=" * 50)
    
    # 同じ例文内でのorder値重複チェック
    print("🔍 例文内order値重複チェック:")
    order_conflicts = []
    df_with_example = df.dropna(subset=['原文'])
    for example in df_with_example['原文'].unique():
        example_data = df_with_example[df_with_example['原文'] == example]
        order_counts = example_data['Slot_display_order'].value_counts()
        duplicated_orders = order_counts[order_counts > 1]
        if len(duplicated_orders) > 0:
            order_conflicts.append((example, duplicated_orders.index.tolist()))
    
    if order_conflicts:
        print(f"❌ Order値重複: {len(order_conflicts)} 例文")
        for example, dup_orders in order_conflicts[:5]:  # 最初の5件表示
            print(f"  {example}: order {dup_orders}")
    else:
        print("✅ Order値重複なし")
    
    # 8. 特定パターンの検証
    print("\n" + "=" * 50)
    print("8️⃣ 特定パターンの検証")
    print("=" * 50)
    
    # where文の検証
    where_examples = df[df['SlotPhrase'].str.contains('where', case=False, na=False)]
    if len(where_examples) > 0:
        print(f"🔍 Where文の検証: {len(where_examples)} 件")
        for _, row in where_examples.iterrows():
            print(f"  例文: {row['原文']}")
            print(f"  スロット: {row['Slot']}, Order: {row['Slot_display_order']}, Value: {row['SlotPhrase']}")
    
    # 時間表現の検証
    time_patterns = ['years?', 'months?', 'days?', 'hours?', 'minutes?', 'tomorrow', 'yesterday', 'tonight', 'soon', 'later']
    time_regex = '|'.join(time_patterns)
    time_examples = df[df['SlotPhrase'].str.contains(time_regex, case=False, na=False)]
    if len(time_examples) > 0:
        print(f"\n🔍 時間表現の検証: {len(time_examples)} 件")
        time_slot_dist = time_examples['Slot'].value_counts()
        print(f"  スロット分布: {dict(time_slot_dist)}")
        
        # M3以外に時間表現がある場合は警告
        non_m3_time = time_examples[time_examples['Slot'] != 'M3']
        if len(non_m3_time) > 0:
            print(f"  ⚠️  M3以外の時間表現: {len(non_m3_time)} 件")
    
    print("\n" + "=" * 60)
    print("🎉 包括的検証完了")
    print("=" * 60)

if __name__ == "__main__":
    main()
