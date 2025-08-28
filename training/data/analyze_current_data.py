#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現在のfinal_54_test_data.jsonを分析して、動詞抽出と文法パターン整理を行う
"""

import json
import re
from collections import defaultdict, Counter

def analyze_final_data():
    # データ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== final_54_test_data.json 分析結果 ===\n")
    
    # 基本統計
    print(f"【基本統計】")
    print(f"Total cases: {len(data['data'])}")
    print(f"Meta info: {data['meta']}")
    print()
    
    # 動詞抽出とパターン分析
    verbs = []
    grammar_patterns = []
    sentence_types = {
        'simple': [],      # 単純文
        'relative': [],    # 関係詞
        'passive': [],     # 受動態
        'perfect': [],     # 完了形
        'modal': [],       # 助動詞
        'complex': []      # 複雑構文
    }
    
    for case_id, case_data in data['data'].items():
        sentence = case_data['sentence']
        expected = case_data['expected']
        main_slots = expected['main_slots']
        sub_slots = expected['sub_slots']
        
        # 動詞抽出
        if 'V' in main_slots:
            verb = main_slots['V']
            verbs.append(verb)
        
        # 文型判定
        slot_pattern = list(main_slots.keys())
        grammar_patterns.append(tuple(slot_pattern))
        
        # 文の分類
        if 'who' in sentence or 'which' in sentence or 'that' in sentence.split() or 'whose' in sentence:
            sentence_types['relative'].append((case_id, sentence))
        elif 'was' in sentence and ('written' in sentence or 'crashed' in sentence or 'sent' in sentence):
            sentence_types['passive'].append((case_id, sentence))
        elif 'has' in sentence or 'have' in sentence:
            sentence_types['perfect'].append((case_id, sentence))
        elif any(modal in sentence for modal in ['will', 'would', 'can', 'could', 'should', 'might', 'must']):
            sentence_types['modal'].append((case_id, sentence))
        elif sub_slots:
            sentence_types['complex'].append((case_id, sentence))
        else:
            sentence_types['simple'].append((case_id, sentence))
    
    # 動詞頻度分析
    print("【動詞頻度分析】")
    verb_counter = Counter(verbs)
    for verb, count in verb_counter.most_common():
        print(f"  {verb}: {count}回")
    print()
    
    # 文法パターン分析
    print("【文法パターン分析】")
    pattern_counter = Counter(grammar_patterns)
    for pattern, count in pattern_counter.most_common():
        pattern_str = " + ".join(pattern)
        print(f"  {pattern_str}: {count}回")
    print()
    
    # 文の分類別表示
    for category, sentences in sentence_types.items():
        if sentences:
            print(f"【{category.upper()}文 ({len(sentences)}件)】")
            for case_id, sentence in sentences:
                print(f"  Case {case_id}: {sentence}")
            print()
    
    # V_group_key提案
    print("【V_group_key分類提案】")
    
    # 動詞のグループ化提案
    verb_groups = {
        'be': ['is', 'are', 'was', 'were'],
        'action': ['love', 'runs', 'lies', 'works', 'bought', 'met', 'drives'],
        'communication': ['written', 'sent'],
        'possession': ['has', 'have'],
        'state': ['finished', 'arrived'],
        'modal': [],
        'passive_be': ['was', 'were']  # 受動態用
    }
    
    # 実際の動詞をグループに分類
    grouped_verbs = defaultdict(list)
    for verb in set(verbs):
        if verb in ['is', 'are', 'was', 'were']:
            grouped_verbs['be'].append(verb)
        elif verb in ['has', 'have']:
            grouped_verbs['perfect'].append(verb)
        elif verb in ['love', 'runs', 'lies', 'works', 'drives', 'met']:
            grouped_verbs['action'].append(verb)
        elif verb in ['bought', 'borrowed']:
            grouped_verbs['transaction'].append(verb)
        elif verb in ['written', 'crashed', 'sent']:
            grouped_verbs['passive'].append(verb)
        elif verb in ['finished', 'arrived']:
            grouped_verbs['completion'].append(verb)
        else:
            grouped_verbs['other'].append(verb)
    
    for group, verb_list in grouped_verbs.items():
        print(f"  {group}: {verb_list}")
    print()
    
    # 複雑度分析
    print("【複雑度分析】")
    for case_id, case_data in data['data'].items():
        sentence = case_data['sentence']
        sub_slots = case_data['expected']['sub_slots']
        
        if sub_slots:
            print(f"  Case {case_id}: {sentence}")
            print(f"    Sub-slots: {sub_slots}")
    
if __name__ == "__main__":
    analyze_final_data()
