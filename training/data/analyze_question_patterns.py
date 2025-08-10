#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分離疑問詞パターン分析
====================
5文型フルセットDBから分離疑問詞（文頭に飛ぶサブスロット）のパターンを検出・分析
"""

import pandas as pd
import re

def analyze_question_patterns():
    """疑問詞パターンの分析"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== 分離疑問詞パターン分析 ===')
    
    # 疑問詞で始まる例文を検索
    question_starters = ['What', 'How', 'When', 'Where', 'Why', 'Which', 'Who']
    question_pattern = '^(' + '|'.join(question_starters) + ')'
    
    question_examples = df[df['原文'].str.contains(question_pattern, case=False, na=False)]
    print(f'疑問文で始まる例数: {len(question_examples)}')
    
    if len(question_examples) > 0:
        print('\n【疑問文の例】')
        for _, row in question_examples.iterrows():
            print(f'例文ID: {row["例文ID"]}')
            print(f'原文: "{row["原文"]}"')
            print()
    
    # 疑問詞を含む全ての文を検索（文中に含まれる場合も）
    question_words_pattern = 'what|how|when|where|why|which|who'
    question_containing = df[df['原文'].str.contains(question_words_pattern, case=False, na=False)]
    print(f'疑問詞を含む全例文数: {len(question_containing)}')
    
    if len(question_containing) > 0:
        print('\n【疑問詞を含む文の例】')
        unique_examples = question_containing.drop_duplicates('例文ID')
        for _, row in unique_examples.head(5).iterrows():
            ex_id = row['例文ID']
            original_text = row['原文']
            print(f'例文ID: {ex_id}')
            print(f'原文: "{original_text}"')
            
            # この例文の詳細なスロット構造を表示
            ex_data = df[df['例文ID'] == ex_id].copy()
            main_slots = ex_data[(pd.notna(ex_data['Slot'])) & (ex_data['SlotPhrase'] != 'nan')]
            sub_slots = ex_data[pd.notna(ex_data['SubslotID'])]
            
            if len(main_slots) > 0:
                print('スロット構造:')
                for _, slot_row in main_slots.sort_values('Slot_display_order').iterrows():
                    slot_name = slot_row['Slot']
                    slot_phrase = slot_row['SlotPhrase'] 
                    phrase_type = slot_row['PhraseType']
                    order = slot_row['Slot_display_order']
                    print(f'  {slot_name}[{phrase_type}]: "{slot_phrase}" (order:{order})')
                    
                    # 対応するサブスロット
                    related_subs = sub_slots[sub_slots['Slot_display_order'] == order]
                    for _, sub_row in related_subs.iterrows():
                        print(f'    → {sub_row["SubslotID"]}: "{sub_row["SubslotElement"]}"')
            print('-' * 60)
            print()

def analyze_word_order_patterns():
    """語順パターンの詳細分析（分離疑問詞の検出）"""
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print('=== 特殊語順パターン分析 ===')
    
    # 例文別にグループ化
    examples = df.groupby('例文ID')
    
    special_order_cases = []
    
    for ex_id, group in examples:
        original_text = group['原文'].iloc[0]
        
        # メインスロットの順序を分析
        main_slots = group[(pd.notna(group['Slot'])) & (group['SlotPhrase'] != 'nan')]
        
        if len(main_slots) > 1:
            orders = main_slots['Slot_display_order'].tolist()
            
            # 順序に特殊性があるかチェック
            # 1. order 0 があるか（通常は1から始まる）
            # 2. 大きく飛んだ順序があるか
            # 3. 疑問詞が含まれているか
            
            has_zero_order = 0 in orders
            has_question_word = bool(re.search(r'\b(what|how|when|where|why|which|who)\b', 
                                             original_text, re.IGNORECASE))
            max_order = max(orders) if orders else 0
            min_order = min(orders) if orders else 0
            order_gap = max_order - min_order > len(orders)  # 順序に大きなギャップがある
            
            if has_zero_order or has_question_word or order_gap:
                special_order_cases.append({
                    'example_id': ex_id,
                    'text': original_text,
                    'has_zero_order': has_zero_order,
                    'has_question_word': has_question_word,
                    'order_gap': order_gap,
                    'orders': sorted(orders),
                    'slots_data': main_slots
                })
    
    print(f'特殊語順パターン検出: {len(special_order_cases)}例')
    
    if special_order_cases:
        print('\n【特殊語順の詳細分析】')
        for case in special_order_cases:
            print(f'例文ID: {case["example_id"]}')
            print(f'原文: "{case["text"]}"')
            print(f'特殊性: zero_order={case["has_zero_order"]}, question_word={case["has_question_word"]}, order_gap={case["order_gap"]}')
            print(f'順序リスト: {case["orders"]}')
            
            print('詳細スロット:')
            for _, slot_row in case['slots_data'].sort_values('Slot_display_order').iterrows():
                print(f'  order:{slot_row["Slot_display_order"]} {slot_row["Slot"]}: "{slot_row["SlotPhrase"]}"')
            
            print('=' * 60)
            print()

if __name__ == "__main__":
    analyze_question_patterns()
    print()
    analyze_word_order_patterns()
