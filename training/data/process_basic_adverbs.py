#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループに同じ方法を適用
"""

import json

def process_basic_adverbs_group():
    """基本副詞グループに同じ処理を適用"""
    
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
    
    print(f"=== 基本副詞グループ ({len(basic_adverbs_data)}例文) ===")
    for i, data_item in enumerate(basic_adverbs_data[:10], 1):  # 最初の10例文を表示
        print(f"例文{i}: {data_item['sentence']}")
    
    if len(basic_adverbs_data) > 10:
        print(f"... 他{len(basic_adverbs_data) - 10}例文")
    
    # tellグループと同じ方法で処理
    print(f"\n=== 単語分割結果（最初の5例文）===")
    for i, data_item in enumerate(basic_adverbs_data[:5], 1):
        print(f"例文{i}: {data_item['words']}")
    
    # tellグループと同じ方法を適用
    from tell_group_correct_enumeration import enumerate_tell_group_correct
    from tell_group_order_arrangement import arrange_tell_group_elements
    
    print(f"\n=== 基本副詞グループに同じ処理を適用 ===")
    
    # ①要素列挙（文法的役割ベース）
    print("①要素列挙段階:")
    # 基本副詞グループの文法的役割を分析
    all_grammar_roles = set()
    
    # サンプル文から文法的役割を推定
    sample_analysis = []
    for i, data_item in enumerate(basic_adverbs_data[:10]):  # 最初の10例文で分析
        words = data_item['words']
        sentence = data_item['sentence']
        
        # 文法的役割の簡易推定
        roles = {}
        
        # 副詞を特定
        adverbs = ['hard', 'carefully', 'quickly', 'clearly', 'gently', 'very', 'daily', 'last']
        time_adverbs = ['yesterday', 'today', 'last', 'daily', 'week']
        
        for pos, word in enumerate(words):
            if word.lower() in adverbs:
                if pos == 0:
                    roles[f"M1_beginning"] = word
                elif pos == len(words) - 1:
                    roles[f"M1_end"] = word
                else:
                    roles[f"M1_middle"] = word
            elif word.lower() in time_adverbs or word.lower() in ['week']:
                roles["M2_time"] = word
            elif word in ['The', 'the']:
                roles["Det"] = word  
            elif word in ['is', 'was', 'were']:
                roles["Aux"] = word
            elif word in ['being']:
                roles["Aux2"] = word
            elif word.lower() in ['study', 'baked', 'eaten', 'opened', 'repaired', 'written', 'solved', 'constructed', 'explains']:
                roles["V"] = word
            elif word in ['by']:
                roles["Prep"] = word
        
        sample_analysis.append({
            'sentence': sentence,
            'words': words,
            'roles': roles
        })
        
        all_grammar_roles.update(roles.keys())
    
    print(f"推定された文法的役割: {sorted(all_grammar_roles)}")
    
    # ②語順配置
    print(f"\n②語順配置段階:")
    
    # 各役割の平均位置を計算
    role_positions = {}
    for role in all_grammar_roles:
        positions = []
        for analysis in sample_analysis:
            if role in analysis['roles']:
                word = analysis['roles'][role]
                pos = analysis['words'].index(word) if word in analysis['words'] else -1
                if pos >= 0:
                    positions.append(pos)
        
        if positions:
            avg_pos = sum(positions) / len(positions)
            role_positions[role] = avg_pos
            print(f"{role:15} → 平均位置: {avg_pos:.1f}")
    
    # 平均位置でソート
    sorted_roles = sorted(all_grammar_roles, key=lambda x: role_positions.get(x, 999))
    
    print(f"\n=== 基本副詞グループ固定order ===")
    for i, role in enumerate(sorted_roles, 1):
        avg_pos = role_positions.get(role, 999)
        if avg_pos != 999:
            print(f"{role}_{i} (平均位置: {avg_pos:.1f})")
        else:
            print(f"{role}_{i} (出現なし)")
    
    return basic_adverbs_data, sorted_roles

if __name__ == "__main__":
    result = process_basic_adverbs_group()
