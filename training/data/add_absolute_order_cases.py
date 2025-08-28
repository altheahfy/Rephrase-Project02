#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループの絶対順序テストケースを追加する
"""

import json

def add_absolute_order_test_cases():
    # 既存の整理済みデータを読み込み
    with open('final_54_test_data_reorganized.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # tellグループの絶対順序テストケース
    tell_test_cases = [
        {
            "sentence": "What did he tell her at the store?",
            "description": "M2(what)-1, Aux(did)-3, S(he)-4, V(tell)-5, O1(her)-6, M3(at the store)-8",
            "absolute_order": {"M2": 1, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M3": 8},
            "wh_word": "what",
            "expected": {
                "main_slots": {
                    "M2": "What",
                    "Aux": "did", 
                    "S": "he",
                    "V": "tell",
                    "O1": "her",
                    "M3": "at the store"
                },
                "sub_slots": {}
            }
        },
        {
            "sentence": "Did he tell her a secret there?",
            "description": "Aux(did)-3, S(he)-4, V(tell)-5, O1(her)-6, O2(a secret)-7, M3(there)-8",
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M3": 8},
            "wh_word": None,
            "expected": {
                "main_slots": {
                    "Aux": "Did",
                    "S": "he", 
                    "V": "tell",
                    "O1": "her",
                    "O2": "a secret",
                    "M3": "there"
                },
                "sub_slots": {}
            }
        },
        {
            "sentence": "Did I tell him a truth in the kitchen?",
            "description": "Aux(did)-3, S(I)-4, V(tell)-5, O1(him)-6, O2(a truth)-7, M3(in the kitchen)-8",
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M3": 8},
            "wh_word": None,
            "expected": {
                "main_slots": {
                    "Aux": "Did",
                    "S": "I",
                    "V": "tell", 
                    "O1": "him",
                    "O2": "a truth",
                    "M3": "in the kitchen"
                },
                "sub_slots": {}
            }
        },
        {
            "sentence": "Where did you tell me a story?",
            "description": "M2(where)-1, Aux(did)-3, S(you)-4, V(tell)-5, O1(me)-6, O2(a story)-7",
            "absolute_order": {"M2": 1, "Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7},
            "wh_word": "where",
            "expected": {
                "main_slots": {
                    "M2": "Where",
                    "Aux": "did",
                    "S": "you", 
                    "V": "tell",
                    "O1": "me",
                    "O2": "a story"
                },
                "sub_slots": {}
            }
        }
    ]
    
    # 現在の最大ケースIDを取得
    max_case_id = max(int(case_id) for case_id in data['data'].keys())
    
    print("=== tellグループ絶対順序テストケース追加 ===\n")
    
    # 新しいケースを追加
    new_case_id = max_case_id + 1
    for case in tell_test_cases:
        data['data'][str(new_case_id)] = {
            'V_group_key': 'tell',
            'grammar_category': 'absolute_order_test',
            'sentence': case['sentence'],
            'description': case['description'],
            'absolute_order': case['absolute_order'],
            'wh_word': case['wh_word'],
            'expected': case['expected']
        }
        
        print(f"Case {new_case_id}: {case['sentence']}")
        print(f"  絶対順序: {case['absolute_order']}")
        print(f"  wh-word: {case['wh_word']}")
        print()
        
        new_case_id += 1
    
    # メタ情報更新
    data['meta']['category_counts']['absolute_order_test'] = len(tell_test_cases)
    data['meta']['total_reorganized'] = new_case_id - 1
    data['meta']['tell_group_added'] = True
    
    # 保存
    output_filename = 'final_54_test_data_with_absolute_order.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ tellグループテストケース追加完了！")
    print(f"📁 ファイル: {output_filename}")
    print(f"📊 総ケース数: {new_case_id - 1}")
    print(f"🎯 絶対順序テストケース: {len(tell_test_cases)}件")
    
    # 絶対順序ルール表示
    print("\n=== tellグループ絶対順序ルール ===")
    print("M2=1, O2=2, Aux=3, S=4, V=5, O1=6, O2=7, M3=8")
    print("- M2とO2は位置2で重複するため、疑問詞がある場合はM2が優先")
    print("- wh-word識別子で疑問詞の重複防止")
    print("- 空白箇所も選択肢の母集団に含まれる")

if __name__ == "__main__":
    add_absolute_order_test_cases()
