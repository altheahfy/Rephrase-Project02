#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループの語順再分析（正確版）
"""

def reanalyze_basic_adverbs_word_order():
    """基本副詞グループの語順を正確に再分析"""
    
    # 実際のJSONデータから例文を抜粋
    sentences_data = [
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
    
    print("=" * 100)
    print("基本副詞グループ - 語順位置の詳細分析")
    print("=" * 100)
    
    # 各例文での単語位置を詳しく分析
    for i, data in enumerate(sentences_data, 1):
        sentence = data["sentence"]
        slots = data["slots"]
        words = sentence.split()
        
        print(f"\n例文{i}: {sentence}")
        print(f"単語リスト: {words}")
        print("スロット位置:")
        
        for slot_name, slot_value in slots.items():
            # スロットの値の最初の単語を探す
            slot_words = slot_value.split()
            first_word = slot_words[0]
            
            # 最初の単語の位置を探す
            position = None
            for j, word in enumerate(words):
                if first_word.lower() in word.lower() or word.lower() in first_word.lower():
                    position = j
                    break
            
            print(f"  {slot_name}: '{slot_value}' → 位置 {position}")
        print("-" * 50)
    
    # 特に注目すべき例文10の詳細分析
    print("\n【重要】例文10の詳細分析:")
    sentence10 = "The teacher explains grammar clearly to confused students daily."
    words10 = sentence10.split()
    print(f"例文: {sentence10}")
    print(f"単語位置: {[(i, word) for i, word in enumerate(words10)]}")
    
    slots10 = {"S": "The teacher", "V": "explains", "O1": "grammar", "M1": "clearly", "M2": "to confused students", "M3": "daily"}
    print("\n正しい語順位置:")
    print(f"S 'The teacher' → 位置 0-1")
    print(f"V 'explains' → 位置 2") 
    print(f"O1 'grammar' → 位置 3")
    print(f"M1 'clearly' → 位置 4")
    print(f"M2 'to confused students' → 位置 5-7")
    print(f"M3 'daily' → 位置 8")
    
    print("\n→ 正しい語順: S < V < O1 < M1 < M2 < M3")
    
    # 修正された平均位置計算
    print("\n【修正後】各スロットの平均位置:")
    slot_positions = {}
    
    for data in sentences_data:
        sentence = data["sentence"]
        slots = data["slots"]
        words = sentence.split()
        
        for slot_name, slot_value in slots.items():
            slot_words = slot_value.split()
            first_word = slot_words[0]
            
            position = None
            for j, word in enumerate(words):
                if first_word.lower() in word.lower() or word.lower() in first_word.lower():
                    position = j
                    break
            
            if position is not None:
                if slot_name not in slot_positions:
                    slot_positions[slot_name] = []
                slot_positions[slot_name].append(position)
    
    # 平均位置を計算して表示
    slot_avg_positions = {}
    for slot_name, positions in slot_positions.items():
        avg_pos = sum(positions) / len(positions)
        slot_avg_positions[slot_name] = avg_pos
        print(f"{slot_name}: {positions} → 平均位置 {avg_pos:.1f}")
    
    # 正しい順序で並び替え
    sorted_slots = sorted(slot_avg_positions.items(), key=lambda x: x[1])
    
    print(f"\n→ 修正後の正しい順序:")
    for i, (slot_name, avg_pos) in enumerate(sorted_slots, 1):
        print(f"  {slot_name}_{i} (平均位置: {avg_pos:.1f})")

if __name__ == "__main__":
    reanalyze_basic_adverbs_word_order()
