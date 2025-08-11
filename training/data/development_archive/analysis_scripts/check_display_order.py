#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表示順序確認スクリプト
"""
import pandas as pd

def check_display_order():
    """生成されたExcelファイルの表示順序を確認"""
    print('🔍 生成されたExcelファイルの内容確認')
    print('=' * 60)
    
    # 新しく生成されたファイルを確認
    df = pd.read_excel('display_order_test.xlsx')
    print(f'📊 総行数: {len(df)}行')
    print(f'📋 列名: {list(df.columns)}')
    print()

    # 最初の例文のサブスロット表示順序を確認
    first_sentence = df[df['例文ID'] == 1]
    original_text = first_sentence[first_sentence['原文'].notna()]['原文'].iloc[0] if len(first_sentence[first_sentence['原文'].notna()]) > 0 else "原文なし"
    
    print('🎯 第1例文のサブスロット表示順序確認:')
    print(f'原文: "{original_text}"')

    # Sスロットのサブスロットを表示順序でソート
    s_slot = first_sentence[first_sentence['Slot'] == 'S']
    s_subslots = s_slot[s_slot['SubslotID'].notna()].sort_values('display_order')

    print('\n📝 Sスロット - サブスロット語順確認:')
    for _, row in s_subslots.iterrows():
        print(f'  {row["display_order"]:2.0f}. {row["SubslotID"]:10} = "{row["SubslotElement"]}"')
    print()

    # 語順確認
    expected_tokens = ['The', 'intelligent', 'student', 'was', 'studying', 'English', 'very', 'hard', 'in', 'the', 'library', '.']
    actual_elements = s_subslots['SubslotElement'].tolist()

    print('🎯 語順整合性確認:')
    print(f'期待トークン: {expected_tokens}')
    print(f'実際要素   : {actual_elements}')

    # 表示順序数値確認
    print('\n🔍 表示順序数値詳細:')
    for _, row in s_subslots.iterrows():
        print(f'  {row["SubslotElement"]:12} → display_order = {row["display_order"]}')
        
    print('\n' + '='*60)
    
    # O1スロットも確認
    o1_slot = first_sentence[first_sentence['Slot'] == 'O1']
    o1_subslots = o1_slot[o1_slot['SubslotID'].notna()].sort_values('display_order')
    
    print('📝 O1スロット - サブスロット語順確認:')
    for _, row in o1_subslots.iterrows():
        print(f'  {row["display_order"]:2.0f}. {row["SubslotID"]:10} = "{row["SubslotElement"]}"')
    
    # 第2例文も簡単にチェック
    print('\n🎯 第2例文の語順確認:')
    second_sentence = df[df['例文ID'] == 2]
    s2_slot = second_sentence[second_sentence['Slot'] == 'S']
    s2_subslots = s2_slot[s2_slot['SubslotID'].notna()].sort_values('display_order')
    
    original_text2 = second_sentence[second_sentence['原文'].notna()]['原文'].iloc[0] if len(second_sentence[second_sentence['原文'].notna()]) > 0 else "原文なし"
    print(f'原文: "{original_text2}"')
    
    print('S2スロット語順:')
    for _, row in s2_subslots.iterrows():
        print(f'  {row["display_order"]:2.0f}. {row["SubslotElement"]}')

if __name__ == "__main__":
    check_display_order()
