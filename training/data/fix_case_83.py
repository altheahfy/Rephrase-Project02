#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 83のWhatをM2からO2に修正する
"""

import json

def fix_case_83():
    # データ読み込み
    with open('final_54_test_data_with_absolute_order.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Case 83を修正
    case_83 = data['data']['83']
    
    print("=== Case 83修正前 ===")
    print(f"sentence: {case_83['sentence']}")
    print(f"description: {case_83['description']}")
    print(f"absolute_order: {case_83['absolute_order']}")
    print(f"expected main_slots: {case_83['expected']['main_slots']}")
    
    # 修正内容
    case_83['description'] = "O2(what)-2, Aux(did)-3, S(he)-4, V(tell)-5, O1(her)-6, M3(at the store)-8"
    case_83['absolute_order'] = {"O2": 2, "Aux": 3, "S": 4, "V": 5, "O1": 6, "M3": 8}
    case_83['expected']['main_slots'] = {
        "O2": "What",
        "Aux": "did", 
        "S": "he",
        "V": "tell",
        "O1": "her",
        "M3": "at the store"
    }
    
    print("\n=== Case 83修正後 ===")
    print(f"sentence: {case_83['sentence']}")
    print(f"description: {case_83['description']}")
    print(f"absolute_order: {case_83['absolute_order']}")
    print(f"expected main_slots: {case_83['expected']['main_slots']}")
    
    # 保存
    output_filename = 'final_54_test_data_with_absolute_order_fixed.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Case 83修正完了！")
    print(f"📁 ファイル: {output_filename}")
    
    # 正しいtellグループ絶対順序ルールを表示
    print("\n=== tellグループ絶対順序ルール（修正版） ===")
    print("M2=1 (場所・時間疑問詞: Where, When等)")
    print("O2=2 (内容疑問詞・直接目的語: What, a secret, a story等)")
    print("Aux=3 (助動詞: did, will等)")
    print("S=4 (主語: he, I, you等)")
    print("V=5 (動詞: tell)")
    print("O1=6 (間接目的語: her, him, me等)")
    print("M3=8 (場所・方法修飾語: at the store, there等)")
    
    print("\n=== 修正された適用例 ===")
    print("'What did he tell her at the store?' → O2(2) + Aux(3) + S(4) + V(5) + O1(6) + M3(8)")
    print("'Where did you tell me a story?' → M2(1) + Aux(3) + S(4) + V(5) + O1(6) + O2(7)")
    print("'Did he tell her a secret there?' → Aux(3) + S(4) + V(5) + O1(6) + O2(7) + M3(8)")

if __name__ == "__main__":
    fix_case_83()
