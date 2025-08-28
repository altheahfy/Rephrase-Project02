#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
final_54_test_data.jsonの例文を文法カテゴリ別に並び替える
"""

import json
from collections import OrderedDict

def reorganize_test_data():
    # データ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 文法カテゴリ別に分類
    categories = {
        'basic_5_patterns': [],      # 基本5文型
        'basic_adverbs': [],         # 基本副詞
        'relative_clauses': [],      # 関係節
        'passive_voice': [],         # 受動態
        'perfect_tense': [],         # 完了形
        'modal_verbs': [],           # 助動詞
        'complex_constructions': []  # 複雑構文
    }
    
    print("=== 文法カテゴリ別分類結果 ===\n")
    
    for case_id, case_data in data['data'].items():
        sentence = case_data['sentence']
        expected = case_data['expected']
        main_slots = expected['main_slots']
        sub_slots = expected['sub_slots']
        
        case_info = {
            'case_id': case_id,
            'sentence': sentence,
            'expected': expected
        }
        
        # カテゴリ分類ロジック
        if sub_slots and any(key in ['sub-s', 'sub-v', 'sub-o1'] for key in sub_slots.keys()):
            # 関係詞節
            if 'who' in sentence or 'which' in sentence or 'that' in sentence.split() or 'whose' in sentence:
                categories['relative_clauses'].append(case_info)
            # where/when/why/how系
            elif 'where' in sentence or 'when' in sentence or 'why' in sentence or 'how' in sentence:
                categories['complex_constructions'].append(case_info)
            # その他の複雑構文
            else:
                categories['complex_constructions'].append(case_info)
        
        elif 'has' in sentence or 'have' in sentence:
            # 完了形
            categories['perfect_tense'].append(case_info)
        
        elif 'was' in sentence and ('written' in sentence or 'sent' in sentence or 'built' in sentence):
            # 受動態（明確な受動態）
            categories['passive_voice'].append(case_info)
        
        elif any(modal in sentence for modal in ['will', 'would', 'can', 'could', 'should', 'might', 'must']):
            # 助動詞
            categories['modal_verbs'].append(case_info)
        
        elif len(main_slots) >= 3 and any(slot in main_slots for slot in ['M1', 'M2', 'M3']):
            # 基本副詞（修飾語を含む基本文型）
            categories['basic_adverbs'].append(case_info)
        
        else:
            # 基本5文型
            categories['basic_5_patterns'].append(case_info)
    
    # 各カテゴリの内容を表示
    for category, cases in categories.items():
        print(f"【{category.upper()} ({len(cases)}件)】")
        for case in cases:
            print(f"  Case {case['case_id']}: {case['sentence']}")
        print()
    
    # 新しい順序でデータを再構築
    reorganized_data = OrderedDict()
    reorganized_data['meta'] = data['meta'].copy()
    reorganized_data['data'] = OrderedDict()
    
    new_case_id = 1
    category_order = [
        'basic_5_patterns',
        'basic_adverbs', 
        'relative_clauses',
        'passive_voice',
        'perfect_tense',
        'modal_verbs',
        'complex_constructions'
    ]
    
    # V_group_key分類マッピング
    verb_to_group = {
        # be動詞群
        'is': 'be', 'are': 'be', 'was': 'be', 'were': 'be',
        
        # 行動動詞群
        'love': 'action', 'runs': 'action', 'run': 'action', 'works': 'action',
        'lives': 'action', 'drives': 'action', 'met': 'action', 'fly': 'action',
        'play': 'action', 'plays': 'action', 'jogs': 'action', 'sat': 'action',
        'eat': 'action', 'reads': 'action', 'sings': 'action',
        
        # 変化動詞群
        'became': 'become', 'become': 'become',
        
        # 学習動詞群
        'study': 'study', 'studies': 'study',
        
        # コミュニケーション動詞群
        'told': 'communication', 'call': 'communication', 'speaks': 'communication',
        'explains': 'communication', 'writes': 'communication',
        
        # 取引動詞群
        'gave': 'transaction', 'bought': 'transaction', 'found': 'transaction',
        'made': 'transaction',
        
        # 知覚動詞群
        'looks': 'perception', 'tastes': 'perception', 'read': 'perception',
        
        # 完了動詞群
        'finished': 'completion', 'completed': 'completion', 'arrived': 'completion',
        'solved': 'completion',
        
        # 受動態動詞群
        'written': 'passive', 'sent': 'passive', 'built': 'passive',
        'repaired': 'passive', 'opened': 'passive', 'baked': 'passive',
        'eaten': 'passive', 'crashed': 'passive',
        
        # 完了形助動詞
        'has': 'perfect', 'have': 'perfect',
        
        # その他
        'needs': 'other', 'saves': 'other', 'passes': 'other',
        'acts': 'other', 'waiting': 'other', 'supervised': 'other',
        'approved': 'other', 'improved': 'other', 'published': 'other',
        'constructed': 'other', 'unexpected': 'other', 'succeeds': 'other',
        'respected': 'other'
    }
    
    # カテゴリ順に並び替え
    for category in category_order:
        for case in categories[category]:
            # V_group_keyを追加
            main_verb = case['expected']['main_slots'].get('V', '')
            v_group_key = verb_to_group.get(main_verb, 'other')
            
            reorganized_data['data'][str(new_case_id)] = {
                'V_group_key': v_group_key,
                'grammar_category': category,
                'sentence': case['sentence'],
                'expected': case['expected']
            }
            new_case_id += 1
    
    # 新しいファイルに保存
    output_filename = 'final_54_test_data_reorganized.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(reorganized_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 並び替え完了！新しいファイル: {output_filename}")
    print(f"📊 総ケース数: {new_case_id - 1}")
    
    # 統計情報更新
    reorganized_data['meta'].update({
        'reorganized': True,
        'category_counts': {cat: len(cases) for cat, cases in categories.items()},
        'total_reorganized': new_case_id - 1
    })
    
    # 最終版保存
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(reorganized_data, f, ensure_ascii=False, indent=2)
    
    return reorganized_data

if __name__ == "__main__":
    reorganize_test_data()
