#!/usr/bin/env python3
"""
expectedデータから正しい例文を再構築
"""

import json
from datetime import datetime

def reconstruct_sentence_from_expected(expected_data):
    """expectedデータから例文を再構築"""
    main_slots = expected_data.get('main_slots', {})
    sub_slots = expected_data.get('sub_slots', {})
    
    # スロット順序: M1, S, Aux, M2, V, C1, O1, O2, C2, M3
    slot_order = ['M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']
    
    # メインスロットから例文構築
    parts = []
    for slot in slot_order:
        if slot in main_slots and main_slots[slot].strip():
            parts.append(main_slots[slot].strip())
    
    # サブスロットがある場合は追加（簡易版）
    if sub_slots:
        sub_parts = []
        for sub_key in sorted(sub_slots.keys()):
            if sub_slots[sub_key].strip():
                sub_parts.append(sub_slots[sub_key].strip())
        if sub_parts:
            parts.extend(sub_parts)
    
    # 文を結合
    sentence = ' '.join(parts)
    
    # 最後にピリオド追加（必要な場合）
    if sentence and not sentence.endswith('.'):
        sentence += '.'
    
    return sentence

def fix_all_sentences():
    """全ての例文をexpectedから修正"""
    
    # データベース読み込み
    with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    correct_answers = data['correct_answers']
    
    print("正解データベースの例文修正中...")
    modified_count = 0
    
    for num, item in correct_answers.items():
        expected = item['expected']
        current_sentence = item['sentence']
        
        # expectedから正しい例文を構築
        reconstructed_sentence = reconstruct_sentence_from_expected(expected)
        
        if reconstructed_sentence and reconstructed_sentence != current_sentence:
            print(f"例文{num}:")
            print(f"  修正前: '{current_sentence}'")
            print(f"  修正後: '{reconstructed_sentence}'")
            print(f"  Expected: {expected['main_slots']}")
            print()
            
            # 修正適用
            correct_answers[num]['sentence'] = reconstructed_sentence
            correct_answers[num]['timestamp'] = datetime.now().isoformat()
            
            modified_count += 1
    
    if modified_count > 0:
        # ファイル保存
        with open('expected_results_progress.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {modified_count}件の例文を修正しました。")
    else:
        print("修正が必要な例文はありませんでした。")

if __name__ == "__main__":
    fix_all_sentences()
