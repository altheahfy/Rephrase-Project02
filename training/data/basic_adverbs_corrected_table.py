#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの正しい表形式配置（修正版）
"""

def display_basic_adverbs_corrected_table():
    """基本副詞グループの正しい語順による表形式配置"""
    
    # 実際のJSONデータから例文を抜粋
    real_examples = [
        {"sentence": "The cake is being baked by my mother.", "slots": {"S": "The cake", "Aux": "is being", "V": "baked", "M2": "by my mother"}},
        {"sentence": "The cake was eaten by the children.", "slots": {"S": "The cake", "Aux": "was", "V": "eaten", "M2": "by the children"}},
        {"sentence": "The door was opened by the key.", "slots": {"S": "The door", "Aux": "was", "V": "opened", "M2": "by the key"}},
        {"sentence": "The students study hard for exams.", "slots": {"S": "The students", "V": "study", "M2": "hard", "M3": "for exams"}},
        {"sentence": "The car was repaired last week.", "slots": {"S": "The car", "Aux": "was", "V": "repaired", "M2": "last week"}},
        {"sentence": "The window was gently opened by the morning breeze.", "slots": {"S": "The window", "Aux": "was", "V": "opened", "M2": "gently", "M3": "by the morning breeze"}},
        {"sentence": "The teacher explains grammar clearly to confused students daily.", "slots": {"S": "The teacher", "V": "explains", "O1": "grammar", "M1": "clearly", "M2": "to confused students", "M3": "daily"}}
    ]
    
    # 正しい語順: S_1 | Aux_2 | V_3 | O1_4 | M1_5 | M2_6 | M3_7
    
    print("=" * 140)
    print("基本副詞グループ - 正しい語順による配置表（修正版）")
    print("=" * 140)
    
    # ヘッダー行1（番号）
    print(f"{'':12}", end="")
    for i in range(1, 8):
        circle_num = "①②③④⑤⑥⑦"[i-1]
        print(f"{circle_num}{'':11}", end="")
    print()
    
    # ヘッダー行2（列名）
    headers = ["S-1", "Aux-2", "V-3", "O1-4", "M1-5", "M2-6", "M3-7"]
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
        
        # スロットを正しい列に配置（修正後の順序）
        if "S" in slots:
            row_data[0] = slots["S"]      # S-1
        if "Aux" in slots:
            row_data[1] = slots["Aux"]    # Aux-2
        if "V" in slots:
            row_data[2] = slots["V"]      # V-3
        if "O1" in slots:
            row_data[3] = slots["O1"]     # O1-4
        if "M1" in slots:
            row_data[4] = slots["M1"]     # M1-5
        if "M2" in slots:
            row_data[5] = slots["M2"]     # M2-6
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
    explanations = ["S_1", "Aux_2", "V_3", "O1_4", "M1_5", "M2_6", "M3_7"]
    for exp in explanations:
        print(f"{exp:<12}", end="")
    print()
    
    print("\n列説明:")
    print("S_1: 主語")
    print("Aux_2: 助動詞")  
    print("V_3: 動詞")
    print("O1_4: 第一目的語")
    print("M1_5: 副詞・方法")
    print("M2_6: 副詞・時間場所")
    print("M3_7: 副詞・追加修飾")
    
    print(f"\n→ 正しい語順: S < Aux < V < O1 < M1 < M2 < M3")

if __name__ == "__main__":
    display_basic_adverbs_corrected_table()
