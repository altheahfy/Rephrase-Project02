import pandas as pd

df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('🔍 5文型フルセット：100%単語保全の正しい例')
print('=' * 80)

# ex001の詳細分析
ex001 = df[df['例文ID'] == 'ex001']
original = ex001[ex001['原文'].notna()]['原文'].iloc[0] if len(ex001[ex001['原文'].notna()]) > 0 else ''

print(f'原文: {original}')
print()

# M2スロットの完全分解例
m2_data = ex001[ex001['Slot'] == 'M2']
m2_phrase = m2_data[m2_data['SubslotID'].isna()]['SlotPhrase'].iloc[0] if len(m2_data[m2_data['SubslotID'].isna()]) > 0 else ''
print(f'M2スロット原句: "{m2_phrase}"')
print('M2サブスロット分解:')

m2_subslots = ex001[(ex001['Slot'] == 'M2') & (ex001['SubslotID'].notna())]
for _, row in m2_subslots.iterrows():
    subslot_id = row['SubslotID']
    element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
    print(f'  {subslot_id}: "{element}"')

# 単語カバレッジチェック
m2_words = m2_phrase.split()
covered_words = []
for _, row in m2_subslots.iterrows():
    element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
    covered_words.extend(element.split())

print(f'\n原句単語数: {len(m2_words)}')
print(f'カバー単語数: {len(covered_words)}')
print(f'原句単語: {m2_words}')
print(f'カバー単語: {covered_words}')

print()

# O1スロットの完全分解例  
o1_data = ex001[ex001['Slot'] == 'O1']
o1_phrase = o1_data[o1_data['SubslotID'].isna()]['SlotPhrase'].iloc[0] if len(o1_data[o1_data['SubslotID'].isna()]) > 0 else ''
print(f'O1スロット原句: "{o1_phrase}"')
print('O1サブスロット分解:')

o1_subslots = ex001[(ex001['Slot'] == 'O1') & (ex001['SubslotID'].notna())]
for _, row in o1_subslots.iterrows():
    subslot_id = row['SubslotID']
    element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
    print(f'  {subslot_id}: "{element}"')

# 単語カバレッジチェック
o1_words = o1_phrase.split()
o1_covered_words = []
for _, row in o1_subslots.iterrows():
    element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
    o1_covered_words.extend(element.split())

print(f'\n原句単語数: {len(o1_words)}')
print(f'カバー単語数: {len(o1_covered_words)}')
print(f'原句単語: {o1_words}')
print(f'カバー単語: {o1_covered_words}')

print('\n' + '=' * 80)
print('🔍 C1とO1の混在例文の完全分析')
print('=' * 80)

# C1とO1スロットの両方を持つ例文を検索
examples_with_both = []
for example_id in df['例文ID'].unique():
    if pd.isna(example_id):
        continue
    example_data = df[df['例文ID'] == example_id]
    slots = example_data['Slot'].unique()
    if 'C1' in slots and 'O1' in slots:
        examples_with_both.append(example_id)

print(f'C1とO1両方を持つ例文: {examples_with_both[:3]}')

# 最初の例文を詳細分析
if examples_with_both:
    target_id = examples_with_both[0]
    target_data = df[df['例文ID'] == target_id]
    
    original = target_data[target_data['原文'].notna()]['原文'].iloc[0] if len(target_data[target_data['原文'].notna()]) > 0 else ''
    print(f'\n例文ID: {target_id}')
    print(f'原文: {original}')
    
    # C1とO1の分解状況
    for slot in ['C1', 'O1']:
        slot_data = target_data[target_data['Slot'] == slot]
        slot_phrase = slot_data[slot_data['SubslotID'].isna()]['SlotPhrase'].iloc[0] if len(slot_data[slot_data['SubslotID'].isna()]) > 0 else ''
        print(f'\n{slot}スロット原句: "{slot_phrase}"')
        
        subslots = target_data[(target_data['Slot'] == slot) & (target_data['SubslotID'].notna())]
        if len(subslots) > 0:
            print(f'{slot}サブスロット分解:')
            for _, row in subslots.iterrows():
                subslot_id = row['SubslotID']
                element = str(row['SubslotElement']) if pd.notna(row['SubslotElement']) else ''
                print(f'  {subslot_id}: "{element}"')
        else:
            print(f'{slot}サブスロット: なし（単一要素）')
