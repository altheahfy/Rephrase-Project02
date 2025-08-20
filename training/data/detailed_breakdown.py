#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# データ読み込み
with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

with open('batch_results_fixed.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Case 12を詳細分析
case_id = 12
sentence = "The man whose car is red lives here."

print("=" * 80)
print(f"文: {sentence}")
print("=" * 80)

print("\n【文の分解】")
print("原文: The man whose car is red lives here.")
print("構造:")
print("  主文: The man ... lives here")
print("  関係節: whose car is red")

print("\n【期待される分解結果】")
expected = test_data['data'][str(case_id)]['expected']
print("メインスロット:")
for slot, value in expected['main_slots'].items():
    print(f"  {slot} = '{value}'")
print("サブスロット:")
for slot, value in expected['sub_slots'].items():
    print(f"  {slot} = '{value}'")

print("\n【実際の分解結果】")
actual = results['results'][str(case_id)]['analysis_result']
print("メインスロット:")
for slot, value in actual['slots'].items():
    print(f"  {slot} = '{value}'")
print("サブスロット:")
for slot, value in actual['sub_slots'].items():
    print(f"  {slot} = '{value}'")

print("\n【どの単語がどのスロットに入っているか】")
print("期待:")
print("  S (主語) = '' (空)")
print("  V (動詞) = 'lives'")
print("  M2 (修飾語) = 'here'")
print("  sub-s (関係節主語) = 'The man whose car'")
print("  sub-v (関係節動詞) = 'is'")
print("  sub-c1 (関係節補語) = 'red'")

print("\n実際:")
print("  S (主語) = '' (空)")
print("  V (動詞) = 'lives'")
print("  C1 (補語) = 'red lives' ← 余分")
print("  M2 (修飾語) = 'here'")
print("  sub-s (関係節主語) = 'The man whose car'")
print("  sub-v (関係節動詞) = 'is'")
print("  sub-c1 (関係節補語) = 'red'")
