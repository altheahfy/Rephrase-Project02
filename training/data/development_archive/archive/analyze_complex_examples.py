#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
複雑例文の詳細なスロット構造とサブスロット分解パターンを分析
"""

import pandas as pd
import numpy as np

def analyze_complex_examples():
    """複雑な例文構造を詳細分析"""
    # データ読み込み
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    # 最も複雑な例文（文字数100以上）を抽出
    complex_examples = df[df['原文'].str.len() > 100].head(5)
    
    print('=== 複雑例文の詳細構造分析 ===')
    print(f'総例文数: {len(df)}')
    print(f'複雑例文数: {len(complex_examples)}')
    print()
    
    slots = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
    sub_slots = ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
    
    for idx, row in complex_examples.iterrows():
        print(f'【例文{idx+1}】')
        print(f'Text: "{row["原文"]}"')
        print(f'V_group_key: {row["V_group_key"]}')
        print(f'文字数: {len(row["原文"])}')
        print()
        
        # メインスロット構造
        print('--- メインスロット構造 ---')
        for slot in slots:
            if pd.notna(row.get(slot)):
                order = row.get(slot + "_order", "N/A")
                slot_type = row.get(slot + "_type", "word")
                print(f'  {slot}[{slot_type}]: "{row[slot]}" (order:{order})')
        print()
        
        # サブスロット構造
        print('--- サブスロット分解構造 ---')
        has_subslots = False
        for slot in slots:
            if pd.notna(row.get(slot)):
                slot_has_subs = False
                for sub in sub_slots:
                    sub_col = slot + '_' + sub
                    if sub_col in row and pd.notna(row[sub_col]):
                        if not slot_has_subs:
                            print(f'  {slot}[] →')
                            slot_has_subs = True
                        print(f'    {sub}: "{row[sub_col]}"')
                        has_subslots = True
        
        if not has_subslots:
            print('  サブスロットなし')
        
        print('=' * 80)
        print()

def analyze_subslot_patterns():
    """サブスロット生成パターンの詳細分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== サブスロット生成パターン詳細分析 ===')
    
    slots = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
    sub_slots = ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
    
    # 各スロットのサブスロット生成パターンを分析
    for main_slot in slots:
        subslot_data = []
        
        for idx, row in df.iterrows():
            if pd.notna(row.get(main_slot)):
                main_content = row[main_slot]
                main_type = row.get(main_slot + "_type", "word")
                
                # このスロットのサブスロットを収集
                slot_subs = {}
                for sub in sub_slots:
                    sub_col = main_slot + '_' + sub
                    if sub_col in row and pd.notna(row[sub_col]):
                        slot_subs[sub] = row[sub_col]
                
                if slot_subs:  # サブスロットがある場合
                    subslot_data.append({
                        'main_content': main_content,
                        'main_type': main_type,
                        'subslots': slot_subs
                    })
        
        if subslot_data:
            print(f'\n--- {main_slot}スロットのサブスロット生成パターン ---')
            print(f'サブスロット生成例数: {len(subslot_data)}')
            
            # タイプ別分類
            type_counts = {}
            for item in subslot_data:
                t = item['main_type']
                type_counts[t] = type_counts.get(t, 0) + 1
            print(f'タイプ分布: {type_counts}')
            
            # サブスロット種類の分析
            all_sub_types = set()
            for item in subslot_data:
                all_sub_types.update(item['subslots'].keys())
            print(f'生成されるサブスロット種類: {sorted(all_sub_types)}')
            
            # 代表例を表示
            print('\n【代表例】')
            for i, item in enumerate(subslot_data[:3]):
                print(f'  例{i+1}: "{item["main_content"]}" ({item["main_type"]})')
                for sub_type, sub_content in item['subslots'].items():
                    print(f'    → {sub_type}: "{sub_content}"')
                print()

def analyze_clause_processing():
    """clause型処理の詳細分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== clause型処理パターン分析 ===')
    
    slots = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
    
    clause_examples = []
    for main_slot in slots:
        type_col = main_slot + "_type"
        for idx, row in df.iterrows():
            if pd.notna(row.get(main_slot)) and row.get(type_col) == "clause":
                clause_examples.append({
                    'slot': main_slot,
                    'content': row[main_slot],
                    'order': row.get(main_slot + "_order", "N/A"),
                    'row_idx': idx
                })
    
    print(f'clause型スロット総数: {len(clause_examples)}')
    
    # スロット別clause分布
    slot_counts = {}
    for item in clause_examples:
        slot = item['slot']
        slot_counts[slot] = slot_counts.get(slot, 0) + 1
    print(f'スロット別clause分布: {slot_counts}')
    
    print('\n【clause処理の代表例】')
    for slot in ['S', 'M1', 'M2', 'M3']:  # 主要なclause型スロット
        slot_examples = [item for item in clause_examples if item['slot'] == slot]
        if slot_examples:
            print(f'\n--- {slot}スロットのclause例 ---')
            for i, item in enumerate(slot_examples[:2]):
                print(f'  例{i+1}: "{item["content"]}" (order:{item["order"]})')
                
                # 対応するサブスロットを表示
                row = df.iloc[item['row_idx']]
                sub_slots = ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
                for sub in sub_slots:
                    sub_col = slot + '_' + sub
                    if sub_col in row and pd.notna(row[sub_col]):
                        print(f'    → {sub}: "{row[sub_col]}"')
                print()

if __name__ == "__main__":
    analyze_complex_examples()
    print()
    analyze_subslot_patterns()
    print()
    analyze_clause_processing()
