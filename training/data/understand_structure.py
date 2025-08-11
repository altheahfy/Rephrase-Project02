import pandas as pd

# 既存の5文型フルセットを確認
df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')

print('🔍 既存5文型フルセット: 上位スロットとサブスロットの構造')
print('=' * 60)

# 第1例文を詳しく確認  
first_example = df[df['例文ID'] == 1]
original_text = first_example[first_example['原文'].notna()]['原文'].iloc[0] if len(first_example[first_example['原文'].notna()]) > 0 else "原文なし"

print(f'例文: {original_text}')
print()

# 上位スロット行（SubslotIDが空の行）
upper_slots = first_example[first_example['SubslotID'].isna()]
print('📋 上位スロット行:')
print('Slot | Slot_display_order')
print('-' * 25)
for _, row in upper_slots.iterrows():
    print(f'{row["Slot"]:4} | {row["Slot_display_order"]}')

print()

# サブスロット行（SubslotIDがあるの行）の最初の10行
subslot_rows = first_example[first_example['SubslotID'].notna()].head(10)
print('📋 サブスロット行（最初の10行）:')
print('Slot | SubslotID | SubslotElement | display_order')
print('-' * 50)
for _, row in subslot_rows.iterrows():
    print(f'{row["Slot"]:4} | {row["SubslotID"]:9} | {row["SubslotElement"]:12} | {row["display_order"]}')
