#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AbsoluteOrderManager Phase 1 拡張テスト
他の動詞グループ（be, give, action）への対応確認
"""

import json
from absolute_order_manager import AbsoluteOrderManager

def test_other_verb_groups():
    """他の動詞グループでのAbsoluteOrderManager動作確認"""
    
    # AbsoluteOrderManagerインスタンス
    manager = AbsoluteOrderManager()
    
    # 他動詞グループのテストケース
    test_cases = [
        {
            "group": "be",
            "sentence": "The car is red.",
            "slots": {"S": "The car", "V": "is", "C1": "red"},
            "v_group_key": "be",
            "wh_word": None
        },
        {
            "group": "action",
            "sentence": "I love you.",
            "slots": {"S": "I", "V": "love", "O1": "you"},
            "v_group_key": "action", 
            "wh_word": None
        },
        {
            "group": "give",
            "sentence": "She gave him a book.",
            "slots": {"S": "She", "V": "gave", "O1": "him", "O2": "a book"},
            "v_group_key": "give",
            "wh_word": None
        },
        {
            "group": "action_with_modifier",
            "sentence": "I quickly ran to school yesterday.",
            "slots": {"S": "I", "Aux": "quickly", "V": "ran", "M2": "to school", "M3": "yesterday"},
            "v_group_key": "action",
            "wh_word": None
        }
    ]
    
    print("=== 他動詞グループ対応テスト ===\n")
    
    for case in test_cases:
        print(f"【{case['group']}グループ】{case['sentence']}")
        print(f"スロット: {case['slots']}")
        
        # AbsoluteOrderManager実行
        result = manager.apply_absolute_order(
            case["slots"], 
            case["v_group_key"], 
            case["wh_word"]
        )
        
        # 結果表示
        actual_positions = {}
        for item in result:
            actual_positions[item["slot"]] = item["absolute_position"]
        
        print(f"絶対位置結果: {actual_positions}")
        
        # 順序確認
        sorted_result = sorted(result, key=lambda x: x["absolute_position"])
        word_order = [f"{item['slot']}({item['value']})" for item in sorted_result]
        print(f"語順: {' → '.join(word_order)}")
        
        print("-" * 60)

def analyze_verb_group_coverage():
    """データファイルから全動詞グループのカバレッジを分析"""
    
    with open("final_54_test_data_with_absolute_order_corrected.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 動詞グループ別統計
    v_group_stats = {}
    grammar_category_stats = {}
    
    for case_id, case_data in data["data"].items():
        v_group = case_data.get("V_group_key", "unknown")
        grammar_cat = case_data.get("grammar_category", "unknown")
        
        # V_group統計
        if v_group not in v_group_stats:
            v_group_stats[v_group] = []
        v_group_stats[v_group].append({
            "case_id": case_id,
            "sentence": case_data.get("sentence", ""),
            "slots": case_data.get("expected", {}).get("main_slots", {})
        })
        
        # Grammar category統計
        if grammar_cat not in grammar_category_stats:
            grammar_category_stats[grammar_cat] = 0
        grammar_category_stats[grammar_cat] += 1
    
    print("=== 動詞グループ別データ分析 ===")
    for group, cases in v_group_stats.items():
        print(f"\n【{group}グループ】: {len(cases)}件")
        for case in cases[:3]:  # 最初の3件を表示
            print(f"  Case {case['case_id']}: {case['sentence']}")
            print(f"    スロット: {list(case['slots'].keys())}")
    
    print(f"\n=== 文法カテゴリ別統計 ===")
    for category, count in grammar_category_stats.items():
        print(f"{category}: {count}件")
    
    return v_group_stats, grammar_category_stats

if __name__ == "__main__":
    print("🚀 AbsoluteOrderManager Phase 1 拡張テスト\n")
    
    # 他動詞グループテスト
    test_other_verb_groups()
    
    print("\n" + "="*80)
    
    # データカバレッジ分析
    analyze_verb_group_coverage()
