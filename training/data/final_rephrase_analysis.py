#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephraseスロット分解ルールの完全分析 - クリーンバージョン
"""

import pandas as pd
import numpy as np

def analyze_rephrase_slot_decomposition():
    """Rephraseスロット分解ルールを完全分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== Rephraseスロット分解ルール完全分析 ===')
    
    # 有効なデータのみ抽出（nanでないもの）
    main_slots = df[(pd.notna(df['Slot'])) & (df['SlotPhrase'] != 'nan')].copy()
    sub_slots = df[pd.notna(df['SubslotID'])].copy()
    
    print(f'有効メインスロット数: {len(main_slots)}')
    print(f'サブスロット要素数: {len(sub_slots)}')
    
    # 例文別にグループ化
    examples = main_slots['例文ID'].unique()
    print(f'例文数: {len(examples)}')
    
    print('\n' + '='*80)
    print('【複雑例文のスロット分解パターン詳細分析】')
    print('='*80)
    
    # 最も複雑な例文3つを詳細分析
    example_complexity = []
    for ex_id in examples:
        ex_data = main_slots[main_slots['例文ID'] == ex_id]
        complexity = len(ex_data)
        original_text = ex_data['原文'].iloc[0]
        example_complexity.append({
            'id': ex_id,
            'text': original_text,
            'complexity': complexity,
            'length': len(original_text)
        })
    
    # 複雑さでソート
    example_complexity.sort(key=lambda x: x['length'], reverse=True)
    
    for i, ex_info in enumerate(example_complexity[:3]):
        ex_id = ex_info['id']
        print(f'\n【例文{i+1}: {ex_id}】')
        print(f'原文: "{ex_info["text"][:100]}..."' if len(ex_info['text']) > 100 else f'原文: "{ex_info["text"]}"')
        print(f'文字数: {ex_info["length"]}, スロット数: {ex_info["complexity"]}')
        
        # この例文のメインスロットを順序通りに表示
        ex_main = main_slots[main_slots['例文ID'] == ex_id].sort_values('Slot_display_order')
        ex_sub = sub_slots[sub_slots['例文ID'] == ex_id]
        
        print('\n--- スロット構造（サブスロット分解付き） ---')
        for _, main_row in ex_main.iterrows():
            slot_name = main_row['Slot']
            slot_phrase = main_row['SlotPhrase']
            phrase_type = main_row['PhraseType']
            order = main_row['Slot_display_order']
            
            print(f'  {slot_name}[{phrase_type}]: "{slot_phrase}" (order:{order})')
            
            # このスロットに対応するサブスロットを表示
            related_subs = ex_sub[ex_sub['Slot_display_order'] == order]
            if len(related_subs) > 0:
                print(f'    → サブスロット分解:')
                for _, sub_row in related_subs.iterrows():
                    print(f'      {sub_row["SubslotID"]}: "{sub_row["SubslotElement"]}"')
        
        print()

def analyze_subslot_generation_patterns():
    """サブスロット生成パターンの詳細分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('\n' + '='*80)
    print('【サブスロット生成パターン分析】')
    print('='*80)
    
    # 有効なデータのみ抽出
    main_slots = df[(pd.notna(df['Slot'])) & (df['SlotPhrase'] != 'nan')].copy()
    sub_slots = df[pd.notna(df['SubslotID'])].copy()
    
    # スロット別サブスロット生成パターンを分析
    slot_types = main_slots['Slot'].unique()
    
    for slot_type in sorted(slot_types):
        print(f'\n--- {slot_type}スロットの分解パターン ---')
        
        # このスロット種類のメインスロットを取得
        slot_instances = main_slots[main_slots['Slot'] == slot_type]
        
        # サブスロットを持つインスタンスを特定
        instances_with_subs = []
        for _, main_row in slot_instances.iterrows():
            ex_id = main_row['例文ID']
            order = main_row['Slot_display_order']
            
            # 対応するサブスロットを検索
            related_subs = sub_slots[
                (sub_slots['例文ID'] == ex_id) & 
                (sub_slots['Slot_display_order'] == order)
            ]
            
            if len(related_subs) > 0:
                instances_with_subs.append({
                    'main_slot': main_row,
                    'subslots': related_subs
                })
        
        if instances_with_subs:
            print(f'サブスロット生成例数: {len(instances_with_subs)}')
            
            # フレーズタイプ分布
            phrase_types = [inst['main_slot']['PhraseType'] for inst in instances_with_subs]
            type_counts = {}
            for pt in phrase_types:
                type_counts[pt] = type_counts.get(pt, 0) + 1
            print(f'フレーズタイプ分布: {type_counts}')
            
            # 生成されるサブスロット種類
            all_sub_types = set()
            for inst in instances_with_subs:
                for _, sub_row in inst['subslots'].iterrows():
                    all_sub_types.add(sub_row['SubslotID'])
            print(f'生成サブスロット種類: {sorted(all_sub_types)}')
            
            # 代表例を表示
            print('\n【代表例】')
            for i, inst in enumerate(instances_with_subs[:2]):
                main = inst['main_slot']
                print(f'  例{i+1}: "{main["SlotPhrase"]}" [{main["PhraseType"]}]')
                for _, sub_row in inst['subslots'].iterrows():
                    print(f'    → {sub_row["SubslotID"]}: "{sub_row["SubslotElement"]}"')
                print()
        else:
            print('サブスロット生成なし')

def extract_clause_processing_rules():
    """clause型処理ルールの抽出"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('\n' + '='*80)
    print('【clause型処理ルール抽出】')
    print('='*80)
    
    # clause型のメインスロットを抽出
    main_slots = df[(pd.notna(df['Slot'])) & (df['SlotPhrase'] != 'nan')].copy()
    clause_slots = main_slots[main_slots['PhraseType'] == 'clause']
    sub_slots = df[pd.notna(df['SubslotID'])].copy()
    
    print(f'clause型スロット総数: {len(clause_slots)}')
    
    # スロット別clause分布
    slot_counts = clause_slots['Slot'].value_counts()
    print(f'スロット別clause分布: {dict(slot_counts)}')
    
    print('\n--- clause型の詳細分解パターン ---')
    
    clause_patterns = []
    for _, clause_row in clause_slots.iterrows():
        ex_id = clause_row['例文ID']
        order = clause_row['Slot_display_order']
        
        # 対応するサブスロットを検索
        related_subs = sub_slots[
            (sub_slots['例文ID'] == ex_id) & 
            (sub_slots['Slot_display_order'] == order)
        ]
        
        if len(related_subs) > 0:
            clause_patterns.append({
                'slot_type': clause_row['Slot'],
                'clause_phrase': clause_row['SlotPhrase'],
                'example_id': ex_id,
                'subslots': related_subs
            })
    
    # パターン別に整理
    pattern_by_slot = {}
    for pattern in clause_patterns:
        slot_type = pattern['slot_type']
        if slot_type not in pattern_by_slot:
            pattern_by_slot[slot_type] = []
        pattern_by_slot[slot_type].append(pattern)
    
    for slot_type, patterns in pattern_by_slot.items():
        print(f'\n【{slot_type}スロットのclause分解パターン】')
        print(f'パターン数: {len(patterns)}')
        
        # サブスロット種類の統計
        all_sub_types = set()
        for pattern in patterns:
            for _, sub_row in pattern['subslots'].iterrows():
                all_sub_types.add(sub_row['SubslotID'])
        print(f'使用されるサブスロット種類: {sorted(all_sub_types)}')
        
        # 代表例
        print('\n代表例:')
        for i, pattern in enumerate(patterns[:2]):
            print(f'  例{i+1}: "{pattern["clause_phrase"]}"')
            for _, sub_row in pattern['subslots'].iterrows():
                print(f'    → {sub_row["SubslotID"]}: "{sub_row["SubslotElement"]}"')
            print()

if __name__ == "__main__":
    analyze_rephrase_slot_decomposition()
    analyze_subslot_generation_patterns()
    extract_clause_processing_rules()
