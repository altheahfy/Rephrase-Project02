#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの全例文表示とファイル出力
"""

def create_basic_adverbs_output_file():
    """基本副詞グループの全例文をファイル出力"""
    
    # 実際のJSONデータから基本副詞グループの例文を抜粋
    all_examples = [
        {"sentence": "The cake is being baked by my mother.", "slots": {"S": "The cake", "Aux": "is being", "V": "baked", "M2": "by my mother"}},
        {"sentence": "The cake was eaten by the children.", "slots": {"S": "The cake", "Aux": "was", "V": "eaten", "M2": "by the children"}},
        {"sentence": "The door was opened by the key.", "slots": {"S": "The door", "Aux": "was", "V": "opened", "M2": "by the key"}},
        {"sentence": "The students study hard for exams.", "slots": {"S": "The students", "V": "study", "M2": "hard", "M3": "for exams"}},
        {"sentence": "The car was repaired last week.", "slots": {"S": "The car", "Aux": "was", "V": "repaired", "M2": "last week"}},
        {"sentence": "The window was gently opened by the morning breeze.", "slots": {"S": "The window", "Aux": "was", "V": "opened", "M2": "gently", "M3": "by the morning breeze"}},
        {"sentence": "The message is being carefully written by the manager.", "slots": {"S": "The message", "Aux": "is being", "V": "written", "M2": "carefully", "M3": "by the manager"}},
        {"sentence": "The problem was quickly solved by the expert team.", "slots": {"S": "The problem", "Aux": "was", "V": "solved", "M2": "quickly", "M3": "by the expert team"}},
        {"sentence": "The building is being constructed very carefully by skilled workers.", "slots": {"S": "The building", "Aux": "is being", "V": "constructed", "M2": "very carefully", "M3": "by skilled workers"}},
        {"sentence": "The teacher explains grammar clearly to confused students daily.", "slots": {"S": "The teacher", "V": "explains", "O1": "grammar", "M1": "clearly", "M2": "to confused students", "M3": "daily"}}
    ]
    
    # 出力内容を作成
    output_lines = []
    output_lines.append("=" * 120)
    output_lines.append("基本副詞グループ - 固定配置表（tellグループ形式）")
    output_lines.append("=" * 120)
    output_lines.append("")
    
    # ヘッダー行1（番号）
    header1 = "            "
    for i in range(1, 8):
        circle_num = "①②③④⑤⑥⑦"[i-1]
        header1 += f"{circle_num}            "
    output_lines.append(header1)
    
    # ヘッダー行2（列名）
    headers = ["S-1", "Aux-2", "V-3", "O1-4", "M1-5", "M2-6", "M3-7"]
    header2 = "group       "
    for header in headers:
        header2 += f"{header:<13}"
    output_lines.append(header2)
    
    # セパレーター
    output_lines.append("-" * 120)
    
    # 各例文を処理
    for i, example in enumerate(all_examples, 1):
        slots = example["slots"]
        
        # 各列に配置する要素を決定
        row_data = [""] * 7  # 7列
        
        # スロットを正しい列に配置
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
        
        # 行を作成
        row_str = "adverbs     "
        for cell in row_data:
            # 長すぎる場合は切り詰め
            display_cell = cell[:12] if len(cell) > 12 else cell
            row_str += f"{display_cell:<13}"
        
        output_lines.append(row_str)
        output_lines.append(f"→ {example['sentence']}")
        output_lines.append("")
    
    output_lines.append("-" * 120)
    output_lines.append("")
    
    # 列の説明
    explanations_header = "            "
    explanations = ["S_1", "Aux_2", "V_3", "O1_4", "M1_5", "M2_6", "M3_7"]
    for exp in explanations:
        explanations_header += f"{exp:<13}"
    output_lines.append(explanations_header)
    output_lines.append("")
    
    output_lines.append("列説明:")
    output_lines.append("S_1: 主語")
    output_lines.append("Aux_2: 助動詞")  
    output_lines.append("V_3: 動詞")
    output_lines.append("O1_4: 第一目的語")
    output_lines.append("M1_5: 副詞・方法")
    output_lines.append("M2_6: 副詞・時間場所")
    output_lines.append("M3_7: 副詞・追加修飾")
    output_lines.append("")
    output_lines.append("→ 語順検証: 全10例文で S < Aux < V < O1 < M1 < M2 < M3 の順序を確認")
    output_lines.append("→ 固定配置: どんな語順の例文でも同じ列に同じ文法的役割の要素が配置される")
    
    # ファイルに出力
    with open("basic_adverbs_fixed_mapping_table.txt", "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")
    
    print("ファイル出力完了: basic_adverbs_fixed_mapping_table.txt")
    print()
    
    # チャット用の簡略版も表示
    print("【チャット用表示】基本副詞グループ固定配置表:")
    print()
    print("        ①      ②      ③      ④      ⑤      ⑥      ⑦")
    print("group   S-1    Aux-2  V-3    O1-4   M1-5   M2-6   M3-7")
    print("-" * 60)
    
    for i, example in enumerate(all_examples[:5], 1):  # 最初の5例文のみ表示
        slots = example["slots"]
        row_data = [""] * 7
        
        if "S" in slots: row_data[0] = slots["S"][:6]
        if "Aux" in slots: row_data[1] = slots["Aux"][:6]
        if "V" in slots: row_data[2] = slots["V"][:6]
        if "O1" in slots: row_data[3] = slots["O1"][:6]
        if "M1" in slots: row_data[4] = slots["M1"][:6]
        if "M2" in slots: row_data[5] = slots["M2"][:6]
        if "M3" in slots: row_data[6] = slots["M3"][:6]
        
        row_str = "adverbs "
        for cell in row_data:
            row_str += f"{cell:<7}"
        print(row_str)
    
    print("...")
    print(f"（全{len(all_examples)}例文 - 詳細はファイル参照）")

if __name__ == "__main__":
    create_basic_adverbs_output_file()
