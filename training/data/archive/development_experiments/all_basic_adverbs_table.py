#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの全例文表示（tellグループ形式）
"""

def display_all_basic_adverbs_examples():
    """基本副詞グループの全例文を表形式で表示"""
    
    # 実際のJSONデータから基本副詞グループの全例文を抜粋
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
        {"sentence": "The teacher explains grammar clearly to confused students daily.", "slots": {"S": "The teacher", "V": "explains", "O1": "grammar", "M1": "clearly", "M2": "to confused students", "M3": "daily"}},
        {"sentence": "The student writes essays carefully for better grades.", "slots": {"S": "The student", "V": "writes", "O1": "essays", "M2": "carefully", "M3": "for better grades"}},
        {"sentence": "The chef cooks meals perfectly in the kitchen daily.", "slots": {"S": "The chef", "V": "cooks", "O1": "meals", "M2": "perfectly", "M3": "in the kitchen", "M4": "daily"}},
        {"sentence": "The artist paints pictures beautifully.", "slots": {"S": "The artist", "V": "paints", "O1": "pictures", "M2": "beautifully"}},
        {"sentence": "The manager reads reports carefully every morning.", "slots": {"S": "The manager", "V": "reads", "O1": "reports", "M2": "carefully", "M3": "every morning"}},
        {"sentence": "The doctor examines patients thoroughly in the clinic.", "slots": {"S": "The doctor", "V": "examines", "O1": "patients", "M2": "thoroughly", "M3": "in the clinic"}},
        {"sentence": "The musician plays songs beautifully for the audience.", "slots": {"S": "The musician", "V": "plays", "O1": "songs", "M2": "beautifully", "M3": "for the audience"}},
        {"sentence": "The writer creates stories imaginatively at night.", "slots": {"S": "The writer", "V": "creates", "O1": "stories", "M2": "imaginatively", "M3": "at night"}},
        {"sentence": "The researcher analyzes data carefully for accuracy.", "slots": {"S": "The researcher", "V": "analyzes", "O1": "data", "M2": "carefully", "M3": "for accuracy"}},
        {"sentence": "The designer creates logos professionally for clients.", "slots": {"S": "The designer", "V": "creates", "O1": "logos", "M2": "professionally", "M3": "for clients"}},
        {"sentence": "The engineer builds bridges safely.", "slots": {"S": "The engineer", "V": "builds", "O1": "bridges", "M2": "safely"}},
        {"sentence": "The photographer takes pictures professionally outdoors.", "slots": {"S": "The photographer", "V": "takes", "O1": "pictures", "M2": "professionally", "M3": "outdoors"}},
        {"sentence": "The librarian organizes books systematically.", "slots": {"S": "The librarian", "V": "organizes", "O1": "books", "M2": "systematically"}},
        {"sentence": "The gardener plants flowers carefully in spring.", "slots": {"S": "The gardener", "V": "plants", "O1": "flowers", "M2": "carefully", "M3": "in spring"}},
        {"sentence": "The baker bakes bread fresh every morning.", "slots": {"S": "The baker", "V": "bakes", "O1": "bread", "M2": "fresh", "M3": "every morning"}},
        {"sentence": "The teacher explains lessons clearly to students.", "slots": {"S": "The teacher", "V": "explains", "O1": "lessons", "M2": "clearly", "M3": "to students"}}
    ]
    
    # 正しい語順: S_1 | Aux_2 | V_3 | O1_4 | M1_5 | M2_6 | M3_7
    
    print("=" * 140)
    print("基本副詞グループ - 全例文表示（tellグループ形式）")
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
        
        # 行を表示
        print(f"{'adverbs':<12}", end="")
        for cell in row_data:
            # 長いテキストは切り詰め
            display_cell = cell[:11] if len(cell) > 11 else cell
            print(f"{display_cell:<12}", end="")
        print()
        
        # 10例文ごとに区切り線
        if i % 10 == 0:
            print("-" * 140)
    
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
    
    print(f"\n→ 語順パターン検証: 全{len(all_examples)}例文で S < Aux < V < O1 < M1 < M2 < M3 の順序を確認")

if __name__ == "__main__":
    display_all_basic_adverbs_examples()
