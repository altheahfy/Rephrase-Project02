#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの表形式配置表示
"""

import json

def display_basic_adverbs_table():
    """基本副詞グループの表形式配置表示"""
    
    # データファイル読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # basic_adverbsグループを抽出
    basic_adverbs_data = []
    for key, item in data['data'].items():
        if item.get('grammar_category') == 'basic_adverbs':
            sentence = item['sentence']
            words = sentence.replace('?', '').replace('.', '').split()
            basic_adverbs_data.append({
                'sentence': sentence,
                'words': words
            })
    
    # 固定order（先ほどの結果から）
    columns = [
        "Det_1",        # 冠詞
        "Aux_2",        # 助動詞 
        "Aux2_3",       # 進行形助動詞
        "V_4",          # 動詞
        "M1_middle_5",  # 副詞・文中
        "M2_time_6",    # 時間副詞
        "Prep_7",       # 前置詞
        "M1_end_8"      # 副詞・文末
    ]
    
    print("=" * 120)
    print("基本副詞グループ - 表形式配置")
    print("=" * 120)
    
    # ヘッダー行
    header = f"{'group':<12}"
    for i, col in enumerate(columns, 1):
        header += f"{col:<15}"
    print(header)
    print("-" * 120)
    
    # 各例文を表形式で表示（最初の10例文）
    for idx, data_item in enumerate(basic_adverbs_data[:10]):
        words = data_item['words']
        sentence = data_item['sentence']
        
        # 各列に配置する要素を決定
        row_data = [""] * len(columns)  # 空の行データ
        
        for pos, word in enumerate(words):
            # 文法的役割に基づいて列を決定
            if word in ['The', 'the']:
                if row_data[0] == "":  # Det_1
                    row_data[0] = word
            elif word in ['is', 'was', 'were']:
                if row_data[1] == "":  # Aux_2
                    row_data[1] = word
            elif word in ['being']:
                if row_data[2] == "":  # Aux2_3
                    row_data[2] = word
            elif word.lower() in ['study', 'baked', 'eaten', 'opened', 'repaired', 'written', 'solved', 'constructed', 'explains']:
                if row_data[3] == "":  # V_4
                    row_data[3] = word
            elif word.lower() in ['hard', 'carefully', 'quickly', 'clearly', 'gently', 'very']:
                if pos != len(words) - 1:  # 文末でない場合
                    if row_data[4] == "":  # M1_middle_5
                        row_data[4] = word
                else:  # 文末の場合
                    if row_data[7] == "":  # M1_end_8
                        row_data[7] = word
            elif word.lower() in ['daily']:
                if row_data[7] == "":  # M1_end_8
                    row_data[7] = word
            elif word.lower() in ['yesterday', 'today', 'last']:
                if row_data[5] == "":  # M2_time_6
                    row_data[5] = word
            elif word.lower() in ['week'] and pos > 0 and words[pos-1].lower() == 'last':
                if row_data[5] == "":  # M2_time_6
                    row_data[5] = f"last {word}"
            elif word in ['by']:
                if row_data[6] == "":  # Prep_7
                    row_data[6] = word
        
        # 行を表示
        row_str = f"{'adverbs':<12}"
        for cell in row_data:
            row_str += f"{cell:<15}"
        print(row_str)
    
    print("-" * 120)
    
    # 列の説明
    print(f"{'列説明':<12}", end="")
    explanations = [
        "Det(冠詞)",
        "Aux(助動詞)", 
        "Aux2(進行)",
        "V(動詞)",
        "M1_mid(副詞中)",
        "M2_time(時間)",
        "Prep(前置詞)",
        "M1_end(副詞末)"
    ]
    for exp in explanations:
        print(f"{exp:<15}", end="")
    print()

if __name__ == "__main__":
    display_basic_adverbs_table()
