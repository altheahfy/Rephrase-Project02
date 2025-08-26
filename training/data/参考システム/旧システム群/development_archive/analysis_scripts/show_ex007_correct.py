import pandas as pd

# 5文型フルセットからex007の正解データを読み取り
df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
ex007 = df[df['例文ID'] == 'ex007']

print('=== ex007 全10スロット上位要素確認 ===')

# 全10スロットをチェック
all_slots = ['M1', 'S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M2', 'M3']

for slot in all_slots:
    slot_data = ex007[ex007['Slot'] == slot]
    if len(slot_data) > 0:
        print(f'\n✅ {slot}スロット:')
        # main要素（上位スロット）を最初に表示
        main_data = slot_data[pd.isna(slot_data['SubslotID'])]
        if len(main_data) > 0:
            main_element = main_data.iloc[0]['SlotPhrase']
            print(f'  📋 main      : "{main_element}"')
        
        # sub要素を表示
        sub_data = slot_data[pd.notna(slot_data['SubslotID'])]
        for _, row in sub_data.iterrows():
            subslot = row['SubslotID']
            element = row['SubslotElement'] if pd.notna(row['SubslotElement']) else row['SlotPhrase']
            print(f'     {subslot:<10}: "{element}"')
    else:
        print(f'\n❌ {slot}スロット: データなし')
