#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5文型フルセットDBからRephraseスロット分解ルールを詳細分析
"""

import pandas as pd
import json

def analyze_rephrase_rules():
    """5文型フルセットDBからRephraseルールを詳細分析"""
    
    print("=== Rephraseスロット分解ルール詳細分析 ===\n")
    
    # 5文型フルセットDBの読み込み
    df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
    
    print(f"総行数: {len(df)}")
    print(f"V_group_key一覧: {df['V_group_key'].unique()}")
    print(f"スロット種類: {sorted(df['Slot'].unique())}")
    
    # サブスロット構造の詳細分析
    print("\n" + "="*70)
    print("【サブスロット構造の詳細分析】")
    
    subslot_data = df[pd.notna(df['SubslotID'])]
    print(f"サブスロット要素数: {len(subslot_data)}")
    print(f"サブスロットID種類: {sorted(subslot_data['SubslotID'].unique())}")
    
    # 関係詞節処理の分析
    print("\n--- 関係詞節処理パターン ---")
    
    # 最も複雑な例文（ex007）の詳細分析
    complex_example = df[df['例文ID'] == 'ex007']
    if len(complex_example) > 0:
        original_text = complex_example['原文'].dropna().iloc[0]
        print(f"複雑例文: \"{original_text[:100]}...\"")
        
        print("\nスロット構造:")
        for _, row in complex_example.iterrows():
            if pd.notna(row['Slot']):
                slot = row['Slot']
                phrase = row['SlotPhrase'] if pd.notna(row['SlotPhrase']) else ''
                phrase_type = row['PhraseType'] if pd.notna(row['PhraseType']) else ''
                subslot_id = row['SubslotID'] if pd.notna(row['SubslotID']) else ''
                subslot_element = row['SubslotElement'] if pd.notna(row['SubslotElement']) else ''
                order = row['Slot_display_order'] if pd.notna(row['Slot_display_order']) else ''
                
                if subslot_id:
                    print(f"  {slot}[{phrase_type}] → {subslot_id}: \"{subslot_element}\" (order:{order})")
                else:
                    print(f"  {slot}[{phrase_type}]: \"{phrase}\" (order:{order})")
    
    # 各スロットの分解パターン分析
    print("\n" + "="*70)
    print("【各スロットの分解パターン分析】")
    
    for slot in ['S', 'C2', 'M1', 'M2']:
        print(f"\n--- {slot}スロットの分解パターン ---")
        slot_data = df[df['Slot'] == slot]
        
        # phrase/clause/wordの分類
        phrase_types = slot_data['PhraseType'].value_counts()
        print(f"分類: {dict(phrase_types)}")
        
        # サブスロット使用例
        subslot_examples = slot_data[pd.notna(slot_data['SubslotID'])]
        if len(subslot_examples) > 0:
            print("サブスロット例:")
            subslot_ids = subslot_examples['SubslotID'].unique()[:5]
            for sub_id in subslot_ids:
                examples = subslot_examples[subslot_examples['SubslotID'] == sub_id]['SubslotElement'].tolist()[:2]
                print(f"  {sub_id}: {examples}")
        
        # 具体例の表示
        examples = slot_data['SlotPhrase'].dropna().unique()[:3]
        if len(examples) > 0:
            print(f"具体例: {list(examples)}")
    
    print("\n" + "="*70)
    print("【現在のルール辞書との比較】")
    
    # 現在のルール辞書を読み込み
    try:
        with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
            current_rules = json.load(f)
        
        print(f"現在のルール辞書: v{current_rules['version']}")
        print(f"ルール数: {len(current_rules['rules'])}")
        
        # ルールのカテゴリ分析
        rule_categories = {}
        for rule in current_rules['rules']:
            rule_id = rule['id']
            if 'time' in rule_id or 'manner' in rule_id or 'place' in rule_id:
                category = 'M系ルール'
            elif 'subject' in rule_id or 'pronoun' in rule_id:
                category = 'S系ルール'
            elif 'aux' in rule_id:
                category = 'Aux系ルール'
            elif 'phrasal' in rule_id or 'particle' in rule_id:
                category = '句動詞ルール'
            else:
                category = 'その他'
            
            rule_categories[category] = rule_categories.get(category, 0) + 1
        
        print(f"ルールカテゴリ分布: {rule_categories}")
        
        print("\n不足している可能性のあるルール:")
        
        # 5文型DBから見つかるがルール辞書にないパターン
        db_patterns = set()
        
        # サブスロット生成ルール
        subslot_patterns = df[pd.notna(df['SubslotID'])]['SubslotID'].unique()
        print(f"- サブスロット生成ルール: {len(subslot_patterns)}種類")
        print(f"  例: {list(subslot_patterns[:5])}")
        
        # clause型の処理ルール
        clause_data = df[df['PhraseType'] == 'clause']
        if len(clause_data) > 0:
            print(f"- clause型処理ルール: {len(clause_data)}件")
            clause_examples = clause_data['SlotPhrase'].dropna().unique()[:3]
            print(f"  例: {list(clause_examples)}")
        
    except FileNotFoundError:
        print("rephrase_rules_v1.0.json が見つかりません")
    
    print("\n" + "="*70)
    print("【実装が必要な新ルール】")
    print("1. 関係詞節サブスロット自動生成")
    print("2. clause型の複文処理")
    print("3. 複雑な修飾句の階層分解")
    print("4. 補語句（C2）の詳細分解")
    print("5. 時間・場所・様態の正確な分類")

if __name__ == "__main__":
    analyze_rephrase_rules()
