#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wh-word位置1修正版での実データ検証結果をファイル出力
"""

import json
from absolute_order_manager_fixed import AbsoluteOrderManager
from datetime import datetime

def test_real_data_groups_to_file_fixed():
    """wh-word修正版でtellグループと基本副詞グループを検証し、結果をファイル出力"""
    
    # 出力ファイルを準備
    output_file = "absolute_order_verification_results_wh_fixed.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        # ヘッダー情報
        f.write("=" * 80 + "\n")
        f.write("AbsoluteOrderManager 実データ検証結果（wh-word位置1修正版）\n")
        f.write(f"実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # データ読み込み
        with open("final_54_test_data_with_absolute_order_fixed.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
        
        manager = AbsoluteOrderManager()
        
        # tellグループの分析
        f.write("🔍 tellグループ分析（wh-word位置1修正版）\n")
        f.write("=" * 60 + "\n")
        
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
                mapped_elements = set()
                for slot_name in slots.keys():
                    if slot_name == "M3":
                        mapped_elements.add("M2_END")
                    else:
                        mapped_elements.add(slot_name)
                tell_all_elements.update(mapped_elements)
            
            f.write(f"tellグループ母集団: {sorted(list(tell_all_elements))}\n\n")
            
            # 各tellケースの絶対位置計算
            for case in tell_cases:
                f.write(f"【Case {case['case_id']}】{case['sentence']}\n")
                f.write(f"スロット: {case['slots']}\n")
                
                # wh-word検出
                wh_word = None
                for slot_value in case["slots"].values():
                    if slot_value.lower() in ["what", "where", "when", "why", "how", "who", "whom"]:
                        wh_word = slot_value.lower()
                        break
                
                f.write(f"検出wh-word: {wh_word}\n")
                
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
                
                f.write(f"📍 絶対位置: {' → '.join(order_display)}\n")
                f.write("-" * 50 + "\n")
        
        # 基本副詞グループの分析
        f.write("\n" + "🔍 基本副詞グループ分析（wh-word位置1修正版）\n")
        f.write("=" * 60 + "\n")
        
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
                f.write(f"\n🎯 {v_group}グループ（基本副詞）\n")
                
                # 母集団分析
                group_all_elements = set()
                for case in cases:
                    slots = case["slots"]
                    mapped_elements = set()
                    for slot_name in slots.keys():
                        if slot_name == "M3":
                            mapped_elements.add("M2_END")
                        else:
                            mapped_elements.add(slot_name)
                    group_all_elements.update(mapped_elements)
                
                f.write(f"母集団: {sorted(list(group_all_elements))}\n")
                
                # 各ケースの絶対位置計算
                for case in cases:
                    f.write(f"\n【Case {case['case_id']}】{case['sentence']}\n")
                    f.write(f"スロット: {case['slots']}\n")
                    
                    # wh-word検出
                    wh_word = None
                    for slot_value in case["slots"].values():
                        if slot_value.lower() in ["what", "where", "when", "why", "how", "who", "whom"]:
                            wh_word = slot_value.lower()
                            break
                    
                    f.write(f"検出wh-word: {wh_word}\n")
                    
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
                    
                    f.write(f"📍 絶対位置: {' → '.join(order_display)}\n")
                
                f.write("-" * 40 + "\n")
        
        f.write("\n🎉 wh-word位置1修正版実データ検証完了\n")
        f.write("=" * 80 + "\n")
    
    print(f"✅ 検証結果を {output_file} に出力しました")
    return output_file

if __name__ == "__main__":
    output_file = test_real_data_groups_to_file_fixed()
    print(f"📁 ファイル場所: {output_file}")
