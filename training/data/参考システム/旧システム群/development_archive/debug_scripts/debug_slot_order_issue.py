import pandas as pd

df = pd.read_excel('step16_complete_final.xlsx')

# 第1例文の上位スロットの表示順序を確認
first_sentence = df[df['例文ID'] == 'ex001']
upper_slots = first_sentence[first_sentence['SubslotID'].isna()]

print('🚨 問題確認: 第1例文の上位スロット表示順序')
print('="The intelligent student was studying English very hard in the library."')
print()
print('Slot | Slot_display_order | 期待値')
print('-' * 50)

# 表示順序でソート
for _, row in upper_slots.iterrows():
    expected = "原文の語順に応じて異なる値であるべき"
    print(f'{row["Slot"]:4} | {row["Slot_display_order"]:15} | {expected}')

print()
print('🎯 正しい理解:')
print('- 同一例文内で各上位スロットは**異なる**Slot_display_order値を持つべき')
print('- 例: S=1, O1=2, C1=3, M1=4... のように原文の語順で番号付け')
print('- 現状: 全て同じ値になっている = 問題！')
