#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実データでのAbsoluteOrderManager検証テスト
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def test_real_data_groups():
    """実データのtellグループと基本副詞グループで検証"""
    
    # データ読み込み
    with open("final_54_test_data_with_absolute_order_fixed.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    manager = AbsoluteOrderManager()
    
    # tellグループの抽出と分析
    print("=" * 60)
    print("🔍 tellグループ分析")
    print("=" * 60)
    
    tell_cases = []
    for case_id, case_data in data["data"].items():
        if case_data.get("V_group_key") == "tell":
            tell_cases.append({
                "case_id": case_id,
                "sentence": case_data.get("sentence", ""),
                "slots": case_data.get("expected", {}).get("main_slots", {}),
                "v_group_key": case_data.get("V_group_key"),
                "grammar_category": case_data.get("grammar_category")
            })
    
    if tell_cases:
        # tellグループ母集団分析
        tell_all_elements = set()
        for case in tell_cases:
            slots = case["slots"]
            # M3 → M2_ENDマッピングを適用
            mapped_elements = set()
            for slot_name in slots.keys():
                if slot_name == "M3":
                    mapped_elements.add("M2_END")
                else:
                    mapped_elements.add(slot_name)
            tell_all_elements.update(mapped_elements)
        
        print(f"tellグループ母集団: {sorted(list(tell_all_elements))}")
        print()
        
        # 各tellケースの絶対位置計算
        for case in tell_cases:
            print(f"【Case {case['case_id']}】{case['sentence']}")
            print(f"スロット: {case['slots']}")
            
            # wh-word検出
            wh_word = None
            for slot_value in case["slots"].values():
                if slot_value.lower() in ["what", "where", "when", "why", "how", "who", "whom"]:
                    wh_word = slot_value.lower()
                    break
            
            # 絶対位置計算
            result = manager.apply_absolute_order(
                case["slots"], 
                "tell", 
                wh_word, 
                tell_all_elements
            )
            
            # 結果表示
            order_display = []
            for item in result:
                order_display.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
            
            print(f"📍 絶対位置: {' → '.join(order_display)}")
            print("-" * 50)
    
    # 基本副詞グループの抽出と分析
    print("\n" + "=" * 60)
    print("🔍 基本副詞グループ分析")
    print("=" * 60)
    
    adverb_cases = []
    for case_id, case_data in data["data"].items():
        if case_data.get("grammar_category") == "basic_adverbs":
            adverb_cases.append({
                "case_id": case_id,
                "sentence": case_data.get("sentence", ""),
                "slots": case_data.get("expected", {}).get("main_slots", {}),
                "v_group_key": case_data.get("V_group_key"),
                "grammar_category": case_data.get("grammar_category")
            })
    
    if adverb_cases:
        # V_group_key別にグループ化
        adverb_groups = {}
        for case in adverb_cases:
            v_group = case["v_group_key"]
            if v_group not in adverb_groups:
                adverb_groups[v_group] = []
            adverb_groups[v_group].append(case)
        
        # 各V_group_key別に処理
        for v_group, cases in adverb_groups.items():
            print(f"\n🎯 {v_group}グループ（基本副詞）")
            
            # 母集団分析
            group_all_elements = set()
            for case in cases:
                slots = case["slots"]
                # M3 → M2_ENDマッピングを適用
                mapped_elements = set()
                for slot_name in slots.keys():
                    if slot_name == "M3":
                        mapped_elements.add("M2_END")
                    else:
                        mapped_elements.add(slot_name)
                group_all_elements.update(mapped_elements)
            
            print(f"母集団: {sorted(list(group_all_elements))}")
            
            # 各ケースの絶対位置計算
            for case in cases:
                print(f"\n【Case {case['case_id']}】{case['sentence']}")
                print(f"スロット: {case['slots']}")
                
                # wh-word検出
                wh_word = None
                for slot_value in case["slots"].values():
                    if slot_value.lower() in ["what", "where", "when", "why", "how", "who", "whom"]:
                        wh_word = slot_value.lower()
                        break
                
                # 絶対位置計算
                result = manager.apply_absolute_order(
                    case["slots"], 
                    v_group, 
                    wh_word, 
                    group_all_elements
                )
                
                # 結果表示
                order_display = []
                for item in result:
                    order_display.append(f"{item['slot']}({item['value']})_{item['absolute_position']}")
                
                print(f"📍 絶対位置: {' → '.join(order_display)}")
            
            print("-" * 40)
    
    print("\n🎉 実データ検証完了")

if __name__ == "__main__":
    test_real_data_groups()
