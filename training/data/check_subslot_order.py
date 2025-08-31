#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サブスロットの辞書キー順序を確認
"""

import json

with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Case 43の関係節例文を確認
case_43 = data['data']['43']
print('例文:', case_43['sentence'])
print('サブスロット辞書:')
sub_slots = case_43['expected']['sub_slots']
for i, (key, value) in enumerate(sub_slots.items(), 1):
    if not key.startswith('_'):  # _parent_slotを除外
        print(f'  {i}. {key}: "{value}"')

print('\n辞書のキー順序:')
keys = [k for k in sub_slots.keys() if not k.startswith('_')]
print('  ', keys)

# Case 46も確認（語順が異なる例）
print('\n--- Case 46 ---')
case_46 = data['data']['46']
print('例文:', case_46['sentence'])
print('サブスロット辞書:')
sub_slots_46 = case_46['expected']['sub_slots']
for i, (key, value) in enumerate(sub_slots_46.items(), 1):
    if not key.startswith('_'):
        print(f'  {i}. {key}: "{value}"')

print('\n辞書のキー順序:')
keys_46 = [k for k in sub_slots_46.keys() if not k.startswith('_')]
print('  ', keys_46)

print('\n🔍 重要な気づき:')
print('- Case 43:', keys)
print('- Case 46:', keys_46)
print('- 順序が異なることが確認できます')
