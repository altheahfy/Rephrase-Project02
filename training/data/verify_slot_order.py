import pandas as pd

df = pd.read_excel('slot_order_fixed.xlsx')

# 上位スロットの表示順序を確認
first_sentence = df[df['例文ID'] == 'ex001']
upper_slots = first_sentence[first_sentence['SubslotID'].isna()]

print('🎯 修正後の上位スロット表示順序:')
print('原文: "The intelligent student was studying English very hard in the library."')
print()
print('Slot | Slot_display_order')
print('-' * 30)

# 表示順序でソート
sorted_slots = upper_slots.sort_values('Slot_display_order')
for _, row in sorted_slots.iterrows():
    print(f'{row["Slot"]:4} | {row["Slot_display_order"]:15}')

print()
print('🔍 語順解析:')
print('原文トークン位置: The(0) intelligent(1) student(2) was(3) studying(4) English(5) very(6) hard(7) in(8) the(9) library(10)')
print('各スロットの最初のトークン位置に基づく順序になっているはずです。')
