#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
eatグループの固定マッピング作成
7つの要素を例文の語順に配置し、重ならないように位置を決める
"""

def create_eat_group_mapping():
    # eatグループの7つの要素
    elements = [
        "What",     # O1 (wh疑問詞位置)
        "will",     # Aux (助動詞)
        "you",      # S (主語)
        "eat",      # V (動詞)
        "there",    # M2 (場所副詞、通常位置)
        "sushi",    # O1 (目的語、通常位置)
        "How"       # M2 (wh疑問副詞位置)
    ]
    
    print("=== eatグループ 7要素の語順配置 ===")
    print("要素リスト:", elements)
    print()
    
    # 例文での語順を考慮した配置
    # 1. What will you eat there? - What(1) will(2) you(3) eat(4) there(5)
    # 2. How will you eat sushi there? - How(1) will(2) you(3) eat(4) sushi(5) there(6)
    # 3. You will eat sushi there. - You(1) will(2) eat(3) sushi(4) there(5)
    
    # 語順に基づく配置（重ならないように）
    fixed_mapping = {
        1: "What",    # wh疑問詞は文頭
        2: "How",     # wh疑問副詞も文頭（Whatと同じ位置だが別例文）
        3: "will",    # 助動詞
        4: "you",     # 主語
        5: "eat",     # 動詞
        6: "sushi",   # 目的語（通常位置）
        7: "there"    # 場所副詞（通常位置）
    }
    
    print("=== 固定マッピング（重複なし配置）===")
    for pos, element in fixed_mapping.items():
        print(f"位置{pos}: {element}")
    
    print()
    print("=== 各例文での配置確認 ===")
    
    # 例文1: What will you eat there?
    sentence1 = ["What", "will", "you", "eat", "there"]
    print("例文1: What will you eat there?")
    print("語順:", sentence1)
    
    # 例文2: How will you eat sushi there?
    sentence2 = ["How", "will", "you", "eat", "sushi", "there"]
    print("例文2: How will you eat sushi there?")
    print("語順:", sentence2)
    
    # 例文3: You will eat sushi there.
    sentence3 = ["You", "will", "eat", "sushi", "there"]
    print("例文3: You will eat sushi there.")
    print("語順:", sentence3)
    
    return fixed_mapping

if __name__ == "__main__":
    mapping = create_eat_group_mapping()
