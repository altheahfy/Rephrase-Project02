#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルな5文型例文での上位スロットクリア状況確認テスト
"""

from universal_10slot_decomposer import Universal10SlotDecomposer
import json

def test_simple_sentences():
    """シンプルな5文型例文で上位スロットの状況を確認"""
    decomposer = Universal10SlotDecomposer()

    # シンプルな5文型の例文をテスト
    simple_sentences = [
        "I sleep.",  # 第1文型
        "She is happy.",  # 第2文型  
        "He plays tennis.",  # 第3文型
        "I gave her a book.",  # 第4文型
        "They made him captain."  # 第5文型
    ]

    for sentence in simple_sentences:
        print(f"\n=== {sentence} ===")
        result = decomposer.decompose_any_text(sentence)
        
        # まず結果の全体構造を確認
        print(f"結果の構造: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 上位スロットの状況確認 - 実際の結果構造に合わせて修正
        upper_slots = ["M1", "S", "Aux", "V", "O1", "O2", "C1", "C2", "M2", "M3"]
        filled_slots = []
        empty_slots = []
        
        # スロットの実際のキー名をマッピング
        slot_key_map = {
            "M1": "m1", "S": "s", "Aux": "aux", "V": "v",
            "O1": "o1", "O2": "o2", "C1": "c1", "C2": "c2", 
            "M2": "m2", "M3": "m3"
        }
        
        for slot in upper_slots:
            if slot in result:
                # スロットが存在する場合、その内容を確認
                slot_data = result[slot]
                content_key = slot_key_map[slot]
                
                if content_key in slot_data and slot_data[content_key]:
                    filled_slots.append(f"{slot}:{slot_data[content_key]}")
                elif slot_data.get("subslots"):  # サブスロットがある場合
                    filled_slots.append(f"{slot}:サブスロット")
                else:
                    empty_slots.append(slot)
            else:
                empty_slots.append(slot)
        
        print(f"埋まっているスロット: {filled_slots}")
        print(f"空のスロット: {empty_slots}")
        
        # サブスロットがある場合の確認
        has_subslots = any(result.get(slot, {}).get("subslots") for slot in upper_slots if slot in ["M1", "S", "O1", "O2", "C1", "C2", "M2", "M3"])
        print(f"サブスロットあり: {has_subslots}")
        
        if has_subslots:
            print("サブスロット詳細:")
            for slot in ["M1", "S", "O1", "O2", "C1", "C2", "M2", "M3"]:
                if slot in result and result[slot].get("subslots"):
                    print(f"  {slot}のサブスロット: {result[slot]['subslots']}")

if __name__ == "__main__":
    test_simple_sentences()
