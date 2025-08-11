import pandas as pd

# 正解データを読み込み
df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('=== 正解データ構造確認 ===')
print('列名:', list(df.columns))
print(f'データ行数: {len(df)}')

print('\n=== ex007の正解データ ===')
ex007_data = df[df['例文ID'] == 'ex007']
for _, row in ex007_data.iterrows():
    slot = row['Slot']
    subslot_id = row['SubslotID'] if pd.notna(row['SubslotID']) else ''
    subslot_element = row['SubslotElement'] if pd.notna(row['SubslotElement']) else ''
    print(f'Slot={slot:<3} | SubslotID={subslot_id:<10} | SubslotElement="{subslot_element}"')
