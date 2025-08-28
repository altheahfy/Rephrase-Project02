#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループのテストケースを正しい期待値で検証
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def test_tell_group_with_correct_expectations():
    """
    tellグループの4つのテストケースを正しい期待値で検証
    """
    print("=== tellグループテスト（正しい期待値版） ===\n")
    
    # テストデータを読み込み
    with open('final_54_test_data_with_absolute_order_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manager = AbsoluteOrderManager()
    
    # 正しい期待値（M1冒頭、M2文尾）
    correct_expectations = {
        "83": {
            "sentence": "What did he tell her at the store?",
            "expected_absolute_order": {"O2": 2, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M2": 8},
            "expected_slots": {
                "O2": "What",
                "Aux": "did", 
                "S": "he",
                "V": "tell",
                "O1": "her",
                "M2": "at the store"  # M3→M2に修正
            }
        },
        "84": {
            "sentence": "Did he tell her a secret there?",
            "expected_absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8},
            "expected_slots": {
                "Aux": "Did",
                "S": "he", 
                "V": "tell",
                "O1": "her",
                "O2": "a secret",
                "M2": "there"  # M3→M2に修正
            }
        },
        "85": {
            "sentence": "Did I tell him a truth in the kitchen?",
            "expected_absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8},
            "expected_slots": {
                "Aux": "Did",
                "S": "I",
                "V": "tell", 
                "O1": "him",
                "O2": "a truth",
                "M2": "in the kitchen"  # M3→M2に修正
            }
        },
        "86": {
            "sentence": "Where did you tell me a story?",
            "expected_absolute_order": {"M2": 1, "Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7},
            "expected_slots": {
                "M2": "Where",
                "Aux": "did",
                "S": "you", 
                "V": "tell",
                "O1": "me",
                "O2": "a story"
            }
        }
    }
    
    # 各テストケースを検証
    for case_id, expected in correct_expectations.items():
        print(f"【Case {case_id}】{expected['sentence']}")
        
        # 現在のデータファイルの内容
        current_case = data['data'][case_id]
        current_slots = current_case['expected']['main_slots']
        
        print(f"現在のスロット: {current_slots}")
        print(f"正しいスロット: {expected['expected_slots']}")
        
        # AbsoluteOrderManagerでテスト
        wh_word = current_case.get('wh_word')
        result = manager.apply_absolute_order(current_slots, "tell", wh_word)
        
        # 期待値と比較
        print(f"期待される絶対順序: {expected['expected_absolute_order']}")
        
        # 結果の絶対位置を抽出
        actual_positions = {item['slot']: item['absolute_position'] for item in result}
        print(f"実際の絶対順序: {actual_positions}")
        
        # 一致チェック
        matches = True
        for slot, expected_pos in expected['expected_absolute_order'].items():
            if slot in actual_positions:
                if actual_positions[slot] != expected_pos:
                    print(f"❌ {slot}: 期待値{expected_pos} ≠ 実際{actual_positions[slot]}")
                    matches = False
                else:
                    print(f"✅ {slot}: {expected_pos}")
            else:
                print(f"❌ {slot}: スロットが見つからない")
                matches = False
        
        if matches:
            print(f"🎉 Case {case_id} 完全一致！")
        else:
            print(f"⚠️ Case {case_id} 不一致あり")
        
        print()

def update_test_data_with_correct_expectations():
    """
    テストデータファイルを正しい期待値で更新
    """
    print("=== テストデータ更新（M1冒頭、M2文尾対応） ===\n")
    
    with open('final_54_test_data_with_absolute_order_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Case 83-86の修正
    corrections = {
        "83": {
            "expected": {
                "main_slots": {
                    "O2": "What",
                    "Aux": "did", 
                    "S": "he",
                    "V": "tell",
                    "O1": "her",
                    "M2": "at the store"  # M3→M2
                },
                "sub_slots": {}
            },
            "description": "O2(what)-2, Aux(did)-3, S(he)-4, V(tell)-5, O1(her)-6, M2(at the store)-8",
            "absolute_order": {"O2": 2, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M2": 8}
        },
        "84": {
            "expected": {
                "main_slots": {
                    "Aux": "Did",
                    "S": "he", 
                    "V": "tell",
                    "O1": "her",
                    "O2": "a secret",
                    "M2": "there"  # M3→M2
                },
                "sub_slots": {}
            },
            "description": "Aux(did)-3, S(he)-4, V(tell)-5, O1(her)-6, O2(a secret)-7, M2(there)-8",
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8}
        },
        "85": {
            "expected": {
                "main_slots": {
                    "Aux": "Did",
                    "S": "I",
                    "V": "tell", 
                    "O1": "him",
                    "O2": "a truth",
                    "M2": "in the kitchen"  # M3→M2
                },
                "sub_slots": {}
            },
            "description": "Aux(did)-3, S(I)-4, V(tell)-5, O1(him)-6, O2(a truth)-7, M2(in the kitchen)-8",
            "absolute_order": {"Aux": 3, "S": 4, "V": 5, "O1": 6, "O2": 7, "M2": 8}
        }
    }
    
    # データ更新
    for case_id, correction in corrections.items():
        data['data'][case_id].update(correction)
        print(f"✅ Case {case_id} 更新完了")
    
    # 保存
    output_filename = 'final_54_test_data_with_absolute_order_corrected.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 更新済みファイル: {output_filename}")
    return output_filename

if __name__ == "__main__":
    # まずテストデータを正しい期待値で更新
    updated_file = update_test_data_with_correct_expectations()
    
    print("\n" + "="*60 + "\n")
    
    # 更新されたデータでテスト実行
    test_tell_group_with_correct_expectations()
