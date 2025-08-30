#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの詳細な配置表示
"""

import json

def display_basic_adverbs_detailed():
    """基本副詞グループの詳細な配置を表示"""
    
    # データファイル読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # basic_adverbsグループを抽出
    basic_adverbs_data = []
    for key, item in data['data'].items():
        if item.get('grammar_category') == 'basic_adverbs':
            sentence = item['sentence']
            words = sentence.replace('?', '').replace('.', '').split()
            basic_adverbs_data.append({
                'sentence': sentence,
                'words': words
            })
    
    print("=" * 80)
    print("基本副詞グループの詳細分析")
    print("=" * 80)
    
    # 最初の10例文を詳細表示
    for i, data_item in enumerate(basic_adverbs_data[:10], 1):
        print(f"\n例文{i}: {data_item['sentence']}")
        print(f"単語: {data_item['words']}")
        
        # 各単語の位置と役割を分析
        words = data_item['words']
        print("位置と役割:")
        
        for pos, word in enumerate(words):
            role = ""
            
            # 文法的役割の判定
            if word in ['The', 'the']:
                role = "Det (冠詞)"
            elif word in ['is', 'was', 'were']:
                role = "Aux (助動詞)"
            elif word in ['being']:
                role = "Aux2 (進行形助動詞)"
            elif word.lower() in ['study', 'baked', 'eaten', 'opened', 'repaired', 'written', 'solved', 'constructed', 'explains']:
                role = "V (動詞)"
            elif word.lower() in ['hard', 'carefully', 'quickly', 'clearly', 'gently', 'very', 'daily']:
                if pos == 0:
                    role = "M1_beginning (副詞・文頭)"
                elif pos == len(words) - 1:
                    role = "M1_end (副詞・文末)"
                else:
                    role = "M1_middle (副詞・文中)"
            elif word.lower() in ['yesterday', 'today', 'last', 'week']:
                role = "M2_time (時間副詞)"
            elif word in ['by']:
                role = "Prep (前置詞)"
            elif word.lower() in ['cake', 'door', 'students', 'car', 'window', 'message', 'problem', 'building', 'teacher']:
                role = "S (主語)"
            elif word.lower() in ['mother', 'children', 'key', 'exams', 'breeze', 'manager', 'team', 'workers', 'students']:
                role = "O (目的語)"
            else:
                role = "Other"
            
            print(f"  位置{pos:2d}: {word:12} → {role}")
        
        print("-" * 60)
    
    print(f"\n=== 抽出された要素の位置別統計 ===")
    
    # 各役割の位置統計
    role_positions = {
        'Det': [],
        'Aux': [],
        'Aux2': [],
        'V': [],
        'M1_middle': [],
        'M1_end': [],
        'M2_time': [],
        'Prep': []
    }
    
    for data_item in basic_adverbs_data[:10]:
        words = data_item['words']
        for pos, word in enumerate(words):
            if word in ['The', 'the']:
                role_positions['Det'].append(pos)
            elif word in ['is', 'was', 'were']:
                role_positions['Aux'].append(pos)
            elif word in ['being']:
                role_positions['Aux2'].append(pos)
            elif word.lower() in ['study', 'baked', 'eaten', 'opened', 'repaired', 'written', 'solved', 'constructed', 'explains']:
                role_positions['V'].append(pos)
            elif word.lower() in ['hard', 'carefully', 'quickly', 'clearly', 'gently', 'very', 'daily']:
                if pos == len(words) - 1:
                    role_positions['M1_end'].append(pos)
                else:
                    role_positions['M1_middle'].append(pos)
            elif word.lower() in ['yesterday', 'today', 'last', 'week']:
                role_positions['M2_time'].append(pos)
            elif word in ['by']:
                role_positions['Prep'].append(pos)
    
    for role, positions in role_positions.items():
        if positions:
            avg_pos = sum(positions) / len(positions)
            print(f"{role:15} → 位置: {positions} (平均: {avg_pos:.1f})")
    
    # 固定order
    sorted_roles = sorted(role_positions.keys(), 
                         key=lambda x: sum(role_positions[x]) / len(role_positions[x]) if role_positions[x] else 999)
    
    print(f"\n=== 基本副詞グループ固定order ===")
    for i, role in enumerate(sorted_roles, 1):
        positions = role_positions[role]
        if positions:
            avg_pos = sum(positions) / len(positions)
            print(f"列{i}: {role} (平均位置: {avg_pos:.1f})")
        else:
            print(f"列{i}: {role} (出現なし)")

if __name__ == "__main__":
    display_basic_adverbs_detailed()
