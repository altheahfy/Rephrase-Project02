#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

# 正解データの読み込み
df = pd.read_excel('例文入力元_分解結果_v2_20250810_113552.xlsx')

print('🎯 データ詳細調査:')
print('=' * 60)

# 例文IDの確認
unique_ids = df['例文ID'].unique()
print(f'📋 存在する例文ID: {unique_ids}')
print()

# ex001が存在する場合の全データ
if 'ex001' in unique_ids:
    ex001_all = df[df['例文ID'] == 'ex001']
    print('📋 ex001の全データ (最初の10行):')
    print(ex001_all[['Slot', 'SubslotID', 'SubslotElement']].head(10))
else:
    # 最初の例文IDを使用
    first_id = unique_ids[0] if len(unique_ids) > 0 else None
    if first_id:
        print(f'📋 代わりに {first_id} の全データ (最初の10行):')
        first_data = df[df['例文ID'] == first_id]
        print(first_data[['Slot', 'SubslotID', 'SubslotElement']].head(10))

print()
print('📋 全体のSlot分布:')
print(df['Slot'].value_counts())
