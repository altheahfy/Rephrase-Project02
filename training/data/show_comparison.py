#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# データ読み込み
with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

with open('batch_results_fixed.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 問題の3ケースを表示
cases = [12, 28, 52]

for case_id in cases:
    print('=' * 80)
    sentence = test_data["data"][str(case_id)]["sentence"]
    print(f'Case {case_id}: {sentence}')
    print('=' * 80)
    
    # 正解データ
    expected = test_data['data'][str(case_id)]['expected']
    expected_main = expected["main_slots"]
    expected_sub = expected["sub_slots"]
    
    # 出力結果
    actual = results['results'][str(case_id)]['analysis_result']
    actual_main = actual["slots"]
    actual_sub = actual["sub_slots"]
    
    print('【メインスロット詳細比較】')
    all_main_slots = set(list(expected_main.keys()) + list(actual_main.keys()))
    for slot in sorted(all_main_slots):
        exp_val = expected_main.get(slot, '(なし)')
        act_val = actual_main.get(slot, '(なし)')
        match = "✓" if exp_val == act_val else "✗"
        print(f'  {slot:4s}: 期待="{exp_val}" | 出力="{act_val}" {match}')
    
    print('\n【サブスロット詳細比較】')
    all_sub_slots = set(list(expected_sub.keys()) + list(actual_sub.keys()))
    for slot in sorted(all_sub_slots):
        exp_val = expected_sub.get(slot, '(なし)')
        act_val = actual_sub.get(slot, '(なし)')
        match = "✓" if exp_val == act_val else "✗"
        print(f'  {slot:8s}: 期待="{exp_val}" | 出力="{act_val}" {match}')
    
    print()
