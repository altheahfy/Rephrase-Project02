#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの表形式配置表示（正しい分析版）
"""

def display_basic_adverbs_correct_table():
    """基本副詞グループの正しい表形式配置表示"""
    
    # 各例文の正確な文法的役割分析
    grammar_analysis = [
        # 例文1: The cake is being baked by my mother.
        {
            "sentence": "The cake is being baked by my mother.",
            "roles": {
                "S": "The cake",
                "Aux": "is being", 
                "V": "baked",
                "Prep": "by",
                "O": "my mother"
            }
        },
        # 例文2: The cake was eaten by the children.
        {
            "sentence": "The cake was eaten by the children.",
            "roles": {
                "S": "The cake",
                "Aux": "was",
                "V": "eaten", 
                "Prep": "by",
                "O": "the children"
            }
        },
        # 例文3: The door was opened by the key.
        {
            "sentence": "The door was opened by the key.",
            "roles": {
                "S": "The door",
                "Aux": "was",
                "V": "opened",
                "Prep": "by", 
                "O": "the key"
            }
        },
        # 例文4: The students study hard for exams.
        {
            "sentence": "The students study hard for exams.",
            "roles": {
                "S": "The students",
                "V": "study",
                "M1": "hard",
                "Prep": "for",
                "O": "exams"
            }
        },
        # 例文5: The car was repaired last week.
        {
            "sentence": "The car was repaired last week.",
            "roles": {
                "S": "The car", 
                "Aux": "was",
                "V": "repaired",
                "M2": "last week"
            }
        },
        # 例文6: The window was gently opened by the morning breeze.
        {
            "sentence": "The window was gently opened by the morning breeze.",
            "roles": {
                "S": "The window",
                "Aux": "was",
                "M1": "gently",
                "V": "opened",
                "Prep": "by",
                "O": "the morning breeze"
            }
        },
        # 例文7: The message is being carefully written by the manager.
        {
            "sentence": "The message is being carefully written by the manager.",
            "roles": {
                "S": "The message",
                "Aux": "is being",
                "M1": "carefully", 
                "V": "written",
                "Prep": "by",
                "O": "the manager"
            }
        },
        # 例文8: The problem was quickly solved by the expert team.
        {
            "sentence": "The problem was quickly solved by the expert team.",
            "roles": {
                "S": "The problem",
                "Aux": "was",
                "M1": "quickly",
                "V": "solved",
                "Prep": "by", 
                "O": "the expert team"
            }
        },
        # 例文9: The building is being constructed very carefully by skilled workers.
        {
            "sentence": "The building is being constructed very carefully by skilled workers.",
            "roles": {
                "S": "The building",
                "Aux": "is being",
                "V": "constructed",
                "M1": "very carefully",
                "Prep": "by",
                "O": "skilled workers"
            }
        },
        # 例文10: The teacher explains grammar clearly to confused students daily.
        {
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "roles": {
                "S": "The teacher",
                "V": "explains", 
                "O1": "grammar",
                "M1": "clearly",
                "Prep": "to",
                "O2": "confused students",
                "M2": "daily"
            }
        }
    ]
    
    # 固定order（先ほどの結果から）
    columns = ["S_1", "Aux_2", "O1_3", "V_4", "M1_5", "Prep_6", "M2_7", "O_8", "O2_9"]
    
    print("=" * 140)
    print("基本副詞グループ - 表形式配置（正しい分析版）")
    print("=" * 140)
    
    # ヘッダー行
    header = f"{'group':<12}"
    for col in columns:
        header += f"{col:<15}"
    print(header)
    print("-" * 140)
    
    # 各例文を表形式で表示
    for idx, analysis in enumerate(grammar_analysis, 1):
        # 各列に配置する要素を決定
        row_data = [""] * len(columns)  # 空の行データ
        
        # 役割に基づいて列に配置
        roles = analysis["roles"]
        
        if "S" in roles:
            row_data[0] = roles["S"]  # S_1
        if "Aux" in roles:
            row_data[1] = roles["Aux"]  # Aux_2
        if "O1" in roles:
            row_data[2] = roles["O1"]  # O1_3
        if "V" in roles:
            row_data[3] = roles["V"]  # V_4
        if "M1" in roles:
            row_data[4] = roles["M1"]  # M1_5
        if "Prep" in roles:
            row_data[5] = roles["Prep"]  # Prep_6
        if "M2" in roles:
            row_data[6] = roles["M2"]  # M2_7
        if "O" in roles:
            row_data[7] = roles["O"]  # O_8
        if "O2" in roles:
            row_data[8] = roles["O2"]  # O2_9
        
        # 行を表示
        row_str = f"{'adverbs':<12}"
        for cell in row_data:
            row_str += f"{cell:<15}"
        print(row_str)
        
        # 元の例文も表示
        print(f"{'→':<12}{analysis['sentence']}")
        print()
    
    print("-" * 140)
    
    # 列の説明
    print(f"{'列説明':<12}", end="")
    explanations = [
        "S(主語)",
        "Aux(助動詞)", 
        "O1(第一目的語)",
        "V(動詞)",
        "M1(副詞)",
        "Prep(前置詞)",
        "M2(時間副詞)",
        "O(目的語)",
        "O2(第二目的語)"
    ]
    for exp in explanations:
        print(f"{exp:<15}", end="")
    print()

if __name__ == "__main__":
    display_basic_adverbs_correct_table()
