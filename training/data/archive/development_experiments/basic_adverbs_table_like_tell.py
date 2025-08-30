#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの実際の配置を表形式で表示（tellグループ形式）
"""

def display_basic_adverbs_table_like_tell():
    """基本副詞グループを画像と同じ表形式で表示"""
    
    # 実際のJSONデータから正確に抜粋
    real_examples = [
        # 基本副詞グループの例文
        {"sentence": "The cake is being baked by my mother.", "slots": {"S": "The cake", "Aux": "is being", "V": "baked", "M2": "by my mother"}},
        {"sentence": "The cake was eaten by the children.", "slots": {"S": "The cake", "Aux": "was", "V": "eaten", "M2": "by the children"}},
        {"sentence": "The door was opened by the key.", "slots": {"S": "The door", "Aux": "was", "V": "opened", "M2": "by the key"}},
        {"sentence": "The students study hard for exams.", "slots": {"S": "The students", "V": "study", "M2": "hard", "M3": "for exams"}},
        {"sentence": "The car was repaired last week.", "slots": {"S": "The car", "Aux": "was", "V": "repaired", "M2": "last week"}},
        {"sentence": "The window was gently opened by the morning breeze.", "slots": {"S": "The window", "Aux": "was", "V": "opened", "M2": "gently", "M3": "by the morning breeze"}},
        {"sentence": "The teacher explains grammar clearly to confused students daily.", "slots": {"S": "The teacher", "V": "explains", "O1": "grammar", "M1": "clearly", "M2": "to confused students", "M3": "daily"}}
    ]
    
    # order付与結果（先ほどの計算結果）
    # S_1 | Aux_2 | O1_3 | V_4 | M2_5 | M1_6 | M3_7
    
    print("=" * 140)
    print("基本副詞グループ - 実際の配置表（tellグループ形式）")
    print("=" * 140)
    
    # ヘッダー行1（番号）
    print(f"{'':12}", end="")
    for i in range(1, 8):
        print(f"①{'':5} " if i==1 else f"{'②' if i==2 else '③' if i==3 else '④' if i==4 else '⑤' if i==5 else '⑥' if i==6 else '⑦'}{'':5} ", end="")
    print()
    
    # ヘッダー行2（列名）
    headers = ["S-1", "Aux-2", "O1-3", "V-4", "M2-5", "M1-6", "M3-7"]
    print(f"{'group':<12}", end="")
    for header in headers:
        print(f"{header:<12}", end="")
    print()
    
    # セパレーター
    print("-" * 140)
    
    # 各例文を表示
    for example in real_examples:
        slots = example["slots"]
        
        # 各列に配置する要素を決定
        row_data = [""] * 7  # 7列
        
        # スロットを正しい列に配置
        if "S" in slots:
            row_data[0] = slots["S"]      # S-1
        if "Aux" in slots:
            row_data[1] = slots["Aux"]    # Aux-2
        if "O1" in slots:
            row_data[2] = slots["O1"]     # O1-3
        if "V" in slots:
            row_data[3] = slots["V"]      # V-4
        if "M2" in slots:
            row_data[4] = slots["M2"]     # M2-5
        if "M1" in slots:
            row_data[5] = slots["M1"]     # M1-6
        if "M3" in slots:
            row_data[6] = slots["M3"]     # M3-7
        
        # 行を表示
        print(f"{'adverbs':<12}", end="")
        for cell in row_data:
            print(f"{cell:<12}", end="")
        print()
    
    print()
    print("-" * 140)
    
    # 最後に列の説明
    print(f"{'':12}", end="")
    explanations = ["S_1", "Aux_2", "O1_3", "V_4", "M2_5", "M1_6", "M3_7"]
    for exp in explanations:
        print(f"{exp:<12}", end="")
    print()
    
    print("\n列説明:")
    print("S_1: 主語")
    print("Aux_2: 助動詞")  
    print("O1_3: 第一目的語")
    print("V_4: 動詞")
    print("M2_5: 副詞・時間場所")
    print("M1_6: 副詞・方法")
    print("M3_7: 副詞・追加修飾")

if __name__ == "__main__":
    display_basic_adverbs_table_like_tell()
