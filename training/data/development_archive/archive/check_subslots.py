import pandas as pd

df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

# サブスロットデータの実際の構造を確認
subslots = df[pd.notna(df['SubslotID'])].head(15)
print('=== サブスロットデータサンプル ===')
for _, row in subslots.iterrows():
    print(f'例文ID: {row["例文ID"]}, SubslotID: {row["SubslotID"]}, Element: "{row["SubslotElement"]}", Order: {row["Slot_display_order"]}')

print('\n=== 例文ex007の詳細構造 ===')
ex007 = df[df['例文ID'] == 'ex007'].sort_values('display_order')
for _, row in ex007.iterrows():
    if pd.notna(row['Slot']):
        print(f'MAIN: {row["Slot"]}[{row["PhraseType"]}] = "{row["SlotPhrase"]}" (order:{row["Slot_display_order"]})')
    elif pd.notna(row['SubslotID']):
        print(f'  SUB: {row["SubslotID"]} = "{row["SubslotElement"]}"')
