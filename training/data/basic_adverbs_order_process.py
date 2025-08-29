#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本副詞グループのorder付与プロセス表示
"""

def show_basic_adverbs_order_process():
    """基本副詞グループのorder付与プロセスを詳細表示"""
    
    # 実際のJSONデータから抜粋した例文
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
    
    print("=" * 120)
    print("基本副詞グループ - order付与プロセス")
    print("=" * 120)
    
    # ① 要素列挙フェーズ
    print("\n【① 要素列挙フェーズ】")
    print("各例文から使用されているスロットを抽出:")
    
    all_slots = set()
    for i, data in enumerate(sentences_data, 1):
        slots = data["slots"]
        all_slots.update(slots.keys())
        print(f"例文{i}: {list(slots.keys())}")
    
    unique_slots = sorted(list(all_slots))
    print(f"\n→ 基本副詞グループで使用される全スロット: {unique_slots}")
    print(f"→ スロット数: {len(unique_slots)}列")
    
    # ② 語順配置フェーズ
    print("\n【② 語順配置フェーズ】")
    print("各スロットの語順位置を分析:")
    
    # 各スロットの位置を計算
    slot_positions = {}
    
    for data in sentences_data:
        sentence = data["sentence"]
        slots = data["slots"]
        words = sentence.split()
        
        for slot_name, slot_value in slots.items():
            slot_words = slot_value.split()
            # 最初の単語の位置を探す
            start_pos = None
            for i, word in enumerate(words):
                if word in slot_words[0] or slot_words[0] in word:
                    start_pos = i
                    break
            
            if start_pos is not None:
                if slot_name not in slot_positions:
                    slot_positions[slot_name] = []
                slot_positions[slot_name].append(start_pos)
    
    # 平均位置を計算
    slot_avg_positions = {}
    for slot_name, positions in slot_positions.items():
        avg_pos = sum(positions) / len(positions)
        slot_avg_positions[slot_name] = avg_pos
        print(f"{slot_name}: 位置リスト{positions} → 平均位置 {avg_pos:.1f}")
    
    # 平均位置でソート
    sorted_slots = sorted(slot_avg_positions.items(), key=lambda x: x[1])
    
    print(f"\n→ 平均位置による並び順:")
    for i, (slot_name, avg_pos) in enumerate(sorted_slots, 1):
        print(f"  {i}. {slot_name} (平均位置: {avg_pos:.1f})")
    
    # ③ 最終的なorder付与
    print("\n【③ 最終的なorder付与】")
    print("平均位置順にorderを付与:")
    
    final_order = {}
    for i, (slot_name, avg_pos) in enumerate(sorted_slots, 1):
        final_order[slot_name] = i
        print(f"{slot_name}_{i} (平均位置: {avg_pos:.1f})")
    
    print(f"\n→ 基本副詞グループの固定列構成:")
    ordered_columns = [f"{slot}_{order}" for slot, order in sorted(final_order.items(), key=lambda x: x[1])]
    print(f"   {' | '.join(ordered_columns)}")
    
    # ④ 検証
    print("\n【④ 検証】")
    print("実際の例文での各要素の配置確認:")
    
    for i, data in enumerate(sentences_data[:3], 1):  # 最初の3例文で検証
        sentence = data["sentence"]
        slots = data["slots"]
        print(f"\n例文{i}: {sentence}")
        
        # 各スロットの配置を表示
        placement = [""] * len(sorted_slots)
        for slot_name, slot_value in slots.items():
            order_pos = final_order[slot_name] - 1  # 0-based index
            placement[order_pos] = slot_value
        
        header = " | ".join([f"{slot}_{order}" for slot, order in sorted_slots])
        values = " | ".join([f"{val:<{len(col)}}" for val, col in zip(placement, header.split(" | "))])
        print(f"配置: {values}")

if __name__ == "__main__":
    show_basic_adverbs_order_process()
