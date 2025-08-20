#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# Load test data to identify specific failing cases
with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# Let's look at the simple cases first that had 81% accuracy
case_1 = test_data['data']['1']
case_2 = test_data['data']['2']

print("=== 低精度ケースの分析 ===")
print(f"Case 1: {case_1['sentence']}")
print(f"  Expected main slots: {case_1['expected']['main_slots']}")
print(f"  Expected sub slots: {case_1['expected']['sub_slots']}")
print()

print(f"Case 2: {case_2['sentence']}")
print(f"  Expected main slots: {case_2['expected']['main_slots']}")
print(f"  Expected sub slots: {case_2['expected']['sub_slots']}")
print()

# Look at a couple of the 87% cases too
case_50 = test_data['data']['50']
case_51 = test_data['data']['51']

print("=== 87%精度ケースの分析 ===")
print(f"Case 50: {case_50['sentence']}")
print(f"  Expected main slots: {case_50['expected']['main_slots']}")
print(f"  Expected sub slots: {case_50['expected']['sub_slots']}")
print()

print(f"Case 51: {case_51['sentence']}")
print(f"  Expected main slots: {case_51['expected']['main_slots']}")
print(f"  Expected sub slots: {case_51['expected']['sub_slots']}")
print()

print("次の優先順位:")
print("1. Case 1,2 (シンプルな文で81%精度) - 基本的な問題の可能性")
print("2. Case 50,51 (分詞構文で87%精度) - より複雑な構文問題")
