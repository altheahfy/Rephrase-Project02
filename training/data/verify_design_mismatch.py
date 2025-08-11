import pandas as pd

# 5文型フルセットとRephraseルールの整合性確認
df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('=== 5文型フルセット全体構造 ===')
print(f'総データ行数: {len(df)}')
print(f'総例文数: {df["例文ID"].nunique()}')

print('\n=== 例文ID一覧 ===')
ex_ids = df['例文ID'].unique()
for ex_id in sorted(ex_ids):
    if pd.notna(ex_id):
        print(f'  {ex_id}')

print('\n=== スロット分布 ===')
slot_counts = df['Slot'].value_counts()
print(slot_counts)

print('\n=== ex007の詳細構造確認 ===')
ex007_data = df[df['例文ID'] == 'ex007']
print(f'ex007データ行数: {len(ex007_data)}')

print('\nex007の各スロット内訳:')
for slot in ex007_data['Slot'].unique():
    slot_rows = ex007_data[ex007_data['Slot'] == slot]
    print(f'\n{slot}スロット ({len(slot_rows)}行):')
    for _, row in slot_rows.iterrows():
        phrase = row['SlotPhrase']
        subslot = row['SubslotID'] if pd.notna(row['SubslotID']) else 'main'
        element = row['SubslotElement'] if pd.notna(row['SubslotElement']) else phrase
        print(f'  {subslot}: "{element}"')

print('\n=== 他の例文との比較 ===')
for ex_id in ['ex001', 'ex002', 'ex003']:
    if ex_id in ex_ids:
        ex_data = df[df['例文ID'] == ex_id]
        slot_types = ex_data['Slot'].unique()
        print(f'{ex_id}: {list(slot_types)}')
