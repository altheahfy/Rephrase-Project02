import pandas as pd
import os

# Excelファイルの読み込み
file_path = r'c:\Users\yurit\Downloads\Rephraseプロジェクト20250529\完全トレーニングUI完成フェーズ３\project-root\Rephrase-Project\training\data\絶対順序考察.xlsx'

print('ファイル存在確認:', os.path.exists(file_path))

# データ読み込み
df = pd.read_excel(file_path)
print('データ形状:', df.shape)

# 空ではないセルのみを表示
print('\n=== 空ではないデータのみ表示 ===')
for i, row in df.iterrows():
    non_empty = []
    for j, value in enumerate(row.values):
        if pd.notna(value) and str(value).strip() != '':
            non_empty.append(f'列{j}: {value}')
    if non_empty:
        print(f'行{i}: {", ".join(non_empty)}')
