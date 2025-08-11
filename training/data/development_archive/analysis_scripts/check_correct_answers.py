#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

# 正解データの読み込み
df = pd.read_excel('例文入力元_分解結果_v2_20250810_113552.xlsx')

# ex001の正解データを確認
ex001_data = df[df['例文ID'] == 'ex001']
print('🎯 ex001の正解データ:')
print('=' * 60)

# Sスロットの正解
s_slot_data = ex001_data[ex001_data['Slot'] == 'S']
print('📋 Sスロット正解:')
for _, row in s_slot_data.iterrows():
    if pd.notna(row['SubslotID']) and pd.notna(row['SubslotElement']):
        print(f'  {row["SubslotID"]:8} : "{row["SubslotElement"]}"')

print()

# M2スロットの正解
m2_slot_data = ex001_data[ex001_data['Slot'] == 'M2']
print('📋 M2スロット正解:')
for _, row in m2_slot_data.iterrows():
    if pd.notna(row['SubslotID']) and pd.notna(row['SubslotElement']):
        print(f'  {row["SubslotID"]:8} : "{row["SubslotElement"]}"')

print()

# O1スロットの正解
o1_slot_data = ex001_data[ex001_data['Slot'] == 'O1']
print('📋 O1スロット正解:')
for _, row in o1_slot_data.iterrows():
    if pd.notna(row['SubslotID']) and pd.notna(row['SubslotElement']):
        print(f'  {row["SubslotID"]:8} : "{row["SubslotElement"]}"')

print()

# M3スロットの正解
m3_slot_data = ex001_data[ex001_data['Slot'] == 'M3']
print('📋 M3スロット正解:')
for _, row in m3_slot_data.iterrows():
    if pd.notna(row['SubslotID']) and pd.notna(row['SubslotElement']):
        print(f'  {row["SubslotID"]:8} : "{row["SubslotElement"]}"')
