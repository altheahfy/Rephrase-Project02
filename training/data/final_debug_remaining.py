#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
残り3ケース詳細デバッグ: Case 12, 28, 52
"""

import json

def analyze_remaining_cases():
    """残り3ケース詳細分析"""
    print("=== 残り3ケース詳細分析 ===")

def analyze_remaining_cases():
    """残り3ケース詳細分析"""
    print("=== 残り3ケース詳細分析 ===")
    
    # ケースデータ読み込み
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # 結果データ読み込み
    with open('batch_results_fixed.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # 対象ケース
    target_cases = [12, 28, 52]
    
    for case_id in target_cases:
        print(f"\n=== Case {case_id} 分析 ===")
        case_data = test_data["data"][str(case_id)]
        result_data = results["results"][str(case_id)]
        
        sentence = case_data["sentence"]
        expected = case_data["expected"]
        actual = result_data["analysis_result"]
        
        print(f"文: {sentence}")
        print(f"期待: {expected}")
        print(f"実際: {actual}")
        
        print(f"\n期待メイン: {expected.get('main_slots', {})}")
        print(f"実際メイン: {actual.get('slots', {})}")
        print(f"期待サブ: {expected.get('sub_slots', {})}")
        print(f"実際サブ: {actual.get('sub_slots', {})}")
        
        # 差分分析
        print("\n差分分析:")
        expected_main = expected.get('main_slots', {})
        actual_main = actual.get('slots', {})
        
        for slot in set(list(expected_main.keys()) + list(actual_main.keys())):
            exp_val = expected_main.get(slot, '(not present)')
            act_val = actual_main.get(slot, '(not present)')
            if exp_val != act_val:
                print(f"  {slot}: 実際='{act_val}' vs 期待='{exp_val}' (❌)")
            else:
                print(f"  {slot}: '{act_val}' (✓)")

if __name__ == "__main__":
    analyze_remaining_cases()
