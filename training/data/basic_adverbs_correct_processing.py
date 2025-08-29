#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループをtellグループと同じ方法で正しく処理
"""

import json

def process_basic_adverbs_correctly():
    """基本副詞グループをtellグループと同じ方法で処理"""
    
    # データファイル読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # basic_adverbsグループを抽出
    basic_adverbs_sentences = []
    for key, item in data['data'].items():
        if item.get('grammar_category') == 'basic_adverbs':
            sentence = item['sentence']
            words = sentence.replace('?', '').replace('.', '').split()
            basic_adverbs_sentences.append({
                'sentence': sentence,
                'words': words
            })
    
    print("=== 基本副詞グループ例文（最初の10文）===")
    for i, sentence_data in enumerate(basic_adverbs_sentences[:10], 1):
        print(f"例文{i}: {sentence_data['sentence']}")
    
    # tellグループと同じ①要素列挙→②語順配置の方法を適用
    
    # ①文法的役割による要素列挙
    print(f"\n=== ①要素列挙段階（文法的役割ベース）===")
    
    # 各例文の文法的役割を分析（手動で正確に）
    grammar_analysis = [
        # 例文1: The cake is being baked by my mother.
        {
            "sentence": "The cake is being baked by my mother.",
            "roles": {
                "S": "The cake",
                "Aux": "is being", 
                "V": "baked",
                "Prep": "by",
                "O": "my mother"
            }
        },
        # 例文2: The cake was eaten by the children.
        {
            "sentence": "The cake was eaten by the children.",
            "roles": {
                "S": "The cake",
                "Aux": "was",
                "V": "eaten", 
                "Prep": "by",
                "O": "the children"
            }
        },
        # 例文3: The door was opened by the key.
        {
            "sentence": "The door was opened by the key.",
            "roles": {
                "S": "The door",
                "Aux": "was",
                "V": "opened",
                "Prep": "by", 
                "O": "the key"
            }
        },
        # 例文4: The students study hard for exams.
        {
            "sentence": "The students study hard for exams.",
            "roles": {
                "S": "The students",
                "V": "study",
                "M1": "hard",
                "Prep": "for",
                "O": "exams"
            }
        },
        # 例文5: The car was repaired last week.
        {
            "sentence": "The car was repaired last week.",
            "roles": {
                "S": "The car", 
                "Aux": "was",
                "V": "repaired",
                "M2": "last week"
            }
        },
        # 例文6: The window was gently opened by the morning breeze.
        {
            "sentence": "The window was gently opened by the morning breeze.",
            "roles": {
                "S": "The window",
                "Aux": "was",
                "M1": "gently",
                "V": "opened",
                "Prep": "by",
                "O": "the morning breeze"
            }
        },
        # 例文7: The message is being carefully written by the manager.
        {
            "sentence": "The message is being carefully written by the manager.",
            "roles": {
                "S": "The message",
                "Aux": "is being",
                "M1": "carefully", 
                "V": "written",
                "Prep": "by",
                "O": "the manager"
            }
        },
        # 例文8: The problem was quickly solved by the expert team.
        {
            "sentence": "The problem was quickly solved by the expert team.",
            "roles": {
                "S": "The problem",
                "Aux": "was",
                "M1": "quickly",
                "V": "solved",
                "Prep": "by", 
                "O": "the expert team"
            }
        },
        # 例文9: The building is being constructed very carefully by skilled workers.
        {
            "sentence": "The building is being constructed very carefully by skilled workers.",
            "roles": {
                "S": "The building",
                "Aux": "is being",
                "V": "constructed",
                "M1": "very carefully",
                "Prep": "by",
                "O": "skilled workers"
            }
        },
        # 例文10: The teacher explains grammar clearly to confused students daily.
        {
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "roles": {
                "S": "The teacher",
                "V": "explains", 
                "O1": "grammar",
                "M1": "clearly",
                "Prep": "to",
                "O2": "confused students",
                "M2": "daily"
            }
        }
    ]
    
    # 全ての文法的役割を収集
    all_grammar_roles = set()
    for analysis in grammar_analysis:
        all_grammar_roles.update(analysis["roles"].keys())
    
    sorted_roles = sorted(list(all_grammar_roles))
    
    print(f"抽出された文法的役割（要素）: {len(sorted_roles)}個")
    for i, role in enumerate(sorted_roles, 1):
        print(f"{i}. {role}")
    
    # ②語順による配置
    print(f"\n=== ②語順配置段階 ===")
    
    # 各文法的役割の位置を計算
    role_positions = {}
    
    for role in sorted_roles:
        positions = []
        for analysis in grammar_analysis:
            if role in analysis["roles"]:
                # その役割の単語/句が文中のどの位置にあるかを計算
                role_content = analysis["roles"][role]
                sentence_words = analysis["sentence"].replace('?', '').replace('.', '').split()
                
                # 役割の開始位置を特定
                if role_content in analysis["sentence"]:
                    # 簡易的に最初の単語の位置を使用
                    first_word = role_content.split()[0]
                    if first_word in sentence_words:
                        pos = sentence_words.index(first_word)
                        positions.append(pos)
        
        if positions:
            avg_pos = sum(positions) / len(positions)
            role_positions[role] = avg_pos
            print(f"{role:8} → 位置: {positions} (平均: {avg_pos:.1f})")
    
    # 平均位置でソート
    sorted_roles_by_position = sorted(sorted_roles, key=lambda x: role_positions.get(x, 999))
    
    print(f"\n=== 基本副詞グループ固定order ===")
    for i, role in enumerate(sorted_roles_by_position, 1):
        avg_pos = role_positions.get(role, 999)
        if avg_pos != 999:
            print(f"{role}_{i} (平均位置: {avg_pos:.1f})")
        else:
            print(f"{role}_{i} (出現なし)")
    
    return sorted_roles_by_position, grammar_analysis

if __name__ == "__main__":
    result = process_basic_adverbs_correctly()
