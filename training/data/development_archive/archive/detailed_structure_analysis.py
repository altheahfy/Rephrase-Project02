#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5文型フルセットDBの縦長フォーマットから複雑例文のスロット構造を分析
"""

import pandas as pd
import numpy as np

def analyze_complex_structure():
    """縦長フォーマットから複雑例文のスロット構造を分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== 5文型フルセットDB構造分析 ===')
    print(f'総レコード数: {len(df)}')
    print(f'カラム: {df.columns.tolist()}')
    print()
    
    # 例文ごとにグループ化
    example_groups = df.groupby('例文ID')
    print(f'例文総数: {len(example_groups)}')
    
    # 例文の文字数を計算
    example_lengths = []
    for example_id, group in example_groups:
        original_text = group['原文'].iloc[0]
        example_lengths.append({
            'example_id': example_id,
            'text': original_text,
            'length': len(original_text),
            'v_group_key': group['V_group_key'].iloc[0]
        })
    
    # 文字数でソート
    example_lengths.sort(key=lambda x: x['length'], reverse=True)
    
    print('\n=== 最も複雑な例文 TOP 5 ===')
    for i, ex in enumerate(example_lengths[:5]):
        print(f'【{i+1}位】 例文ID: {ex["example_id"]} (文字数: {ex["length"]})')
        print(f'V_group_key: {ex["v_group_key"]}')
        print(f'原文: "{ex["text"]}"')
        
        # この例文のスロット構造を詳細表示
        example_data = df[df['例文ID'] == ex['example_id']].copy()
        example_data = example_data.sort_values('Slot_display_order')
        
        print('\n--- スロット構造 ---')
        current_slot = None
        for _, row in example_data.iterrows():
            if pd.notna(row['Slot']):
                slot_info = f"{row['Slot']}[{row['PhraseType']}]: \"{row['SlotPhrase']}\" (order:{row['Slot_display_order']})"
                print(f'  {slot_info}')
                current_slot = row['Slot']
            elif pd.notna(row['SubslotID']) and current_slot:
                print(f'    → {row["SubslotID"]}: "{row["SubslotElement"]}"')
        
        print('=' * 80)
        print()

def analyze_subslot_generation_rules():
    """サブスロット生成ルールを詳細分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== サブスロット生成ルール分析 ===')
    
    # サブスロットがある例を抽出
    subslot_data = df[pd.notna(df['SubslotID'])].copy()
    print(f'サブスロット要素数: {len(subslot_data)}')
    
    # スロット別サブスロット生成パターン
    slot_subslot_patterns = {}
    example_groups = df.groupby('例文ID')
    
    for example_id, group in example_groups:
        # メインスロットとサブスロットを整理
        main_slots = group[pd.notna(group['Slot'])].copy()
        subslots = group[pd.notna(group['SubslotID'])].copy()
        
        if len(subslots) > 0:
            for _, main_row in main_slots.iterrows():
                slot_name = main_row['Slot']
                slot_phrase = main_row['SlotPhrase']
                phrase_type = main_row['PhraseType']
                
                # このスロットの直後に続くサブスロットを探す
                relevant_subslots = []
                next_main_order = float('inf')
                
                # 次のメインスロットの順序を見つける
                later_mains = main_slots[main_slots['Slot_display_order'] > main_row['Slot_display_order']]
                if len(later_mains) > 0:
                    next_main_order = later_mains['Slot_display_order'].min()
                
                # この範囲内のサブスロットを収集
                for _, sub_row in subslots.iterrows():
                    if (sub_row['Slot_display_order'] > main_row['Slot_display_order'] and 
                        sub_row['Slot_display_order'] < next_main_order):
                        relevant_subslots.append({
                            'subslot_id': sub_row['SubslotID'],
                            'element': sub_row['SubslotElement']
                        })
                
                if relevant_subslots:
                    if slot_name not in slot_subslot_patterns:
                        slot_subslot_patterns[slot_name] = []
                    
                    slot_subslot_patterns[slot_name].append({
                        'example_id': example_id,
                        'main_phrase': slot_phrase,
                        'phrase_type': phrase_type,
                        'subslots': relevant_subslots
                    })
    
    # パターン分析結果を表示
    for slot_name, patterns in slot_subslot_patterns.items():
        print(f'\n--- {slot_name}スロットのサブスロット生成パターン ---')
        print(f'サブスロット生成例数: {len(patterns)}')
        
        # タイプ別分類
        type_counts = {}
        subslot_types = set()
        for pattern in patterns:
            p_type = pattern['phrase_type']
            type_counts[p_type] = type_counts.get(p_type, 0) + 1
            for sub in pattern['subslots']:
                subslot_types.add(sub['subslot_id'])
        
        print(f'フレーズタイプ分布: {type_counts}')
        print(f'生成されるサブスロット種類: {sorted(subslot_types)}')
        
        # 代表例
        print('\n【代表例】')
        for i, pattern in enumerate(patterns[:3]):
            print(f'  例{i+1} ({pattern["example_id"]}): "{pattern["main_phrase"]}" [{pattern["phrase_type"]}]')
            for sub in pattern['subslots']:
                print(f'    → {sub["subslot_id"]}: "{sub["element"]}"')
            print()

def analyze_clause_type_patterns():
    """clause型の処理パターンを詳細分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== clause型処理パターン分析 ===')
    
    # clause型のスロットを抽出
    clause_slots = df[(pd.notna(df['Slot'])) & (df['PhraseType'] == 'clause')].copy()
    print(f'clause型スロット総数: {len(clause_slots)}')
    
    # スロット別分布
    slot_counts = clause_slots['Slot'].value_counts()
    print(f'スロット別clause分布: {dict(slot_counts)}')
    
    print('\n--- clause型処理の詳細例 ---')
    for slot_name in slot_counts.index[:4]:  # 上位4つのスロット
        slot_examples = clause_slots[clause_slots['Slot'] == slot_name].head(2)
        
        print(f'\n【{slot_name}スロットのclause例】')
        for _, row in slot_examples.iterrows():
            print(f'例文ID: {row["例文ID"]}')
            print(f'原文: "{df[df["例文ID"] == row["例文ID"]]["原文"].iloc[0]}"')
            print(f'clause内容: "{row["SlotPhrase"]}"')
            
            # このclauseのサブスロット分解を表示
            example_data = df[df['例文ID'] == row['例文ID']].copy()
            example_data = example_data.sort_values('Slot_display_order')
            
            # このスロットの直後のサブスロットを表示
            subslots = example_data[
                (pd.notna(example_data['SubslotID'])) & 
                (example_data['Slot_display_order'] > row['Slot_display_order'])
            ].head(10)  # 最大10個のサブスロット
            
            print('  サブスロット分解:')
            for _, sub_row in subslots.iterrows():
                # 次のメインスロットより前かチェック
                next_main = example_data[
                    (pd.notna(example_data['Slot'])) & 
                    (example_data['Slot_display_order'] > row['Slot_display_order'])
                ]
                if len(next_main) > 0:
                    next_order = next_main['Slot_display_order'].min()
                    if sub_row['Slot_display_order'] >= next_order:
                        break
                
                print(f'    {sub_row["SubslotID"]}: "{sub_row["SubslotElement"]}"')
            print()

if __name__ == "__main__":
    analyze_complex_structure()
    print('\n' + '='*100 + '\n')
    analyze_subslot_generation_rules()
    print('\n' + '='*100 + '\n')
    analyze_clause_type_patterns()
