#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
グループ人口分析テスト - tellグループ全体の要素分析
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def analyze_tell_group_population():
    """tellグループの人口分析を実行"""
    
    # tellグループ全データを読み込み
    with open("final_54_test_data_with_absolute_order_corrected.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # tellグループデータを抽出
    tell_group_cases = []
    for case_id, case_data in data["data"].items():
        if case_data.get("V_group_key") == "tell":
            tell_group_cases.append({
                "case_id": case_id,
                "sentence": case_data.get("sentence", ""),
                "slots": case_data.get("expected", {}).get("main_slots", {}),
                "v_group_key": case_data.get("V_group_key"),
                "grammar_category": case_data.get("grammar_category")
            })
    
    print(f"=== tellグループ人口分析 ===")
    print(f"tellグループ総数: {len(tell_group_cases)}件")
    print()
    
    # グループ内の全要素を収集
    all_elements = set()
    cases_with_elements = []
    
    for case in tell_group_cases:
        case_id = case.get("case_id", "unknown")
        sentence = case.get("sentence", "")
        slots = case.get("slots", {})
        
        # 現在の文の要素を収集
        case_elements = set(slots.keys())
        all_elements.update(case_elements)
        
        cases_with_elements.append({
            "case_id": case_id,
            "sentence": sentence,
            "elements": case_elements,
            "slots": slots
        })
        
        print(f"Case {case_id}: {list(case_elements)}")
    
    print()
    print(f"tellグループ全体に存在する要素: {sorted(list(all_elements))}")
    print()
    
    # グループ人口分析に基づく絶対位置計算のテスト
    manager = AbsoluteOrderManager()
    
    print("=== グループ人口分析による絶対位置計算テスト ===")
    
    # M3をM2_ENDにマッピングした要素セットを作成
    mapped_all_elements = set()
    for element in all_elements:
        if element == "M3":
            mapped_all_elements.add("M2_END")
        else:
            mapped_all_elements.add(element)
    
    print(f"マッピング後グループ要素: {sorted(list(mapped_all_elements))}")
    print()
    
    # 各ケースをグループ人口分析で処理
    for case_data in cases_with_elements:
        case_id = case_data["case_id"]
        sentence = case_data["sentence"]
        slots = case_data["slots"]
        
        print(f"【Case {case_id}】{sentence}")
        
        # wh-word検出
        wh_word = None
        for slot_value in slots.values():
            if slot_value.lower() in ["what", "where", "when", "why", "how", "who", "whom"]:
                wh_word = slot_value.lower()
                break
        
        # グループ人口分析を使用した絶対位置計算
        result = manager.apply_absolute_order(
            slots, 
            "tell", 
            wh_word, 
            group_population=mapped_all_elements
        )
        
        # 結果表示
        actual_positions = {}
        for item in result:
            actual_positions[item["slot"]] = item["absolute_position"]
        
        print(f"グループ人口分析結果: {actual_positions}")
        print("-" * 50)
    
    return all_elements, cases_with_elements

if __name__ == "__main__":
    analyze_tell_group_population()
