import pandas as pd

# 正解データを読み込み
df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('=== ex007の全スロット正解データ ===')
ex007_data = df[df['例文ID'] == 'ex007']

# スロット別に整理
slots = {}
for _, row in ex007_data.iterrows():
    slot = row['Slot']
    subslot_id = row['SubslotID'] if pd.notna(row['SubslotID']) else ''
    subslot_element = row['SubslotElement'] if pd.notna(row['SubslotElement']) else ''
    
    if slot not in slots:
        slots[slot] = {}
    
    if subslot_id:
        slots[slot][subslot_id] = subslot_element

# スロット別表示
for slot_name in ['M1', 'S', 'Aux', 'V', 'O1', 'C2', 'M2', 'M3']:
    if slot_name in slots:
        print(f'\n📋 {slot_name}スロット正解:')
        slot_data = slots[slot_name]
        if slot_data:
            for subslot, value in slot_data.items():
                if value:
                    print(f'  {subslot:10}: "{value}"')
        else:
            print('  (空)')
    else:
        print(f'\n📋 {slot_name}スロット正解: (なし)')

print('\n' + '='*50)
