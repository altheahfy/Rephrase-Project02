#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの正しいスロット構成による表形式配置表示
"""

def display_basic_adverbs_real_slots_table():
    """基本副詞グループの正しいスロット構成による表形式配置表示"""
    
    # 実際のJSONデータから抜粋した例文とその分析
    real_data = [
        # 例文1: The cake is being baked by my mother.
        {
            "sentence": "The cake is being baked by my mother.",
            "slots": {
                "S": "The cake",
                "Aux": "is being", 
                "V": "baked",
                "M2": "by my mother"
            }
        },
        # 例文2: The cake was eaten by the children.
        {
            "sentence": "The cake was eaten by the children.",
            "slots": {
                "S": "The cake",
                "Aux": "was",
                "V": "eaten", 
                "M2": "by the children"
            }
        },
        # 例文3: The door was opened by the key.
        {
            "sentence": "The door was opened by the key.",
            "slots": {
                "S": "The door",
                "Aux": "was",
                "V": "opened",
                "M2": "by the key"
            }
        },
        # 例文4: The students study hard for exams.
        {
            "sentence": "The students study hard for exams.",
            "slots": {
                "S": "The students",
                "V": "study",
                "M2": "hard",
                "M3": "for exams"
            }
        },
        # 例文5: The car was repaired last week.
        {
            "sentence": "The car was repaired last week.",
            "slots": {
                "S": "The car", 
                "Aux": "was",
                "V": "repaired",
                "M2": "last week"
            }
        },
        # 例文6: The window was gently opened by the morning breeze.
        {
            "sentence": "The window was gently opened by the morning breeze.",
            "slots": {
                "S": "The window",
                "Aux": "was",
                "V": "opened",
                "M2": "gently",
                "M3": "by the morning breeze"
            }
        },
        # 例文7: The message is being carefully written by the manager.
        {
            "sentence": "The message is being carefully written by the manager.",
            "slots": {
                "S": "The message",
                "Aux": "is being",
                "V": "written",
                "M2": "carefully", 
                "M3": "by the manager"
            }
        },
        # 例文8: The problem was quickly solved by the expert team.
        {
            "sentence": "The problem was quickly solved by the expert team.",
            "slots": {
                "S": "The problem",
                "Aux": "was",
                "V": "solved",
                "M2": "quickly",
                "M3": "by the expert team"
            }
        },
        # 例文9: The building is being constructed very carefully by skilled workers.
        {
            "sentence": "The building is being constructed very carefully by skilled workers.",
            "slots": {
                "S": "The building",
                "Aux": "is being",
                "V": "constructed",
                "M2": "very carefully",
                "M3": "by skilled workers"
            }
        },
        # 例文10: The teacher explains grammar clearly to confused students daily.
        {
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "slots": {
                "S": "The teacher",
                "V": "explains", 
                "O1": "grammar",
                "M1": "clearly",
                "M2": "to confused students",
                "M3": "daily"
            }
        }
    ]
    
    # 実際に使用されているスロット（JSONデータに基づく）
    columns = ["S", "Aux", "V", "O1", "M1", "M2", "M3"]
    
    print("=" * 110)
    print("基本副詞グループ - 正しいスロット構成による表形式配置")
    print("=" * 110)
    
    # ヘッダー行
    header = f"{'group':<12}"
    for col in columns:
        header += f"{col:<15}"
    print(header)
    print("-" * 110)
    
    # 各例文を表形式で表示
    for idx, data in enumerate(real_data, 1):
        # 各列に配置する要素を決定
        row_data = [""] * len(columns)  # 空の行データ
        
        # スロットに基づいて列に配置
        slots = data["slots"]
        
        for i, col in enumerate(columns):
            if col in slots:
                row_data[i] = slots[col]
        
        # 行を表示
        row_str = f"{'adverbs':<12}"
        for cell in row_data:
            row_str += f"{cell:<15}"
        print(row_str)
        
        # 元の例文も表示
        print(f"{'→':<12}{data['sentence']}")
        print()
    
    print("-" * 110)
    
    # 列の説明
    print(f"{'列説明':<12}", end="")
    explanations = [
        "S(主語)",
        "Aux(助動詞)", 
        "V(動詞)",
        "O1(第一目的語)",
        "M1(副詞・方法)",
        "M2(副詞・時間場所)",
        "M3(副詞・追加修飾)"
    ]
    for exp in explanations:
        print(f"{exp:<15}", end="")
    print()
    print()
    
    # 実際に使用されているスロットの集計
    all_slots = set()
    for data in real_data:
        all_slots.update(data["slots"].keys())
    
    print(f"実際に使用されているスロット: {sorted(list(all_slots))}")

if __name__ == "__main__":
    display_basic_adverbs_real_slots_table()
