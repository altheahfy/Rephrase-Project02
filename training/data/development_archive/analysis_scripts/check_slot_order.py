import pandas as pd

df = pd.read_excel('display_order_test.xlsx')

# 第1例文の上位スロットの表示順序を確認
first_sentence = df[df['例文ID'] == 'ex001']
upper_slots = first_sentence[first_sentence['SubslotID'].isna()]

print('🎯 第1例文の上位スロット表示順序確認:')
print('Slot | Slot_display_order')
print('-' * 25)
for _, row in upper_slots.iterrows():
    print(f'{row["Slot"]:4} | {row["Slot_display_order"]}')

print('\n問題: 全部のSlot_display_orderが1になっている！')
print('正しくは: 原文の語順に応じて、S=1, O1=2, M1=3, etc... のようになるべき')
