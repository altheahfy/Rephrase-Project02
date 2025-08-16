#!/usr/bin/env python3
"""
正解データベースの例文フィールドを修正
expectedに対応する正しい例文に書き換える
"""

import json
from datetime import datetime

def fix_expected_database():
    """正解データベースのsentenceフィールドを修正"""
    
    # データベース読み込み
    with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    correct_answers = data['correct_answers']
    
    # 修正対象の例文を特定（expectedから逆算）
    fixes = {}
    
    for num, item in correct_answers.items():
        expected = item['expected']['main_slots']
        current_sentence = item['sentence']
        
        # expectedから正しい例文を推測
        correct_sentence = None
        
        # パターン1: S + V + C1 (第2文型)
        if 'S' in expected and 'V' in expected and 'C1' in expected and len(expected) == 3:
            if expected['V'] == 'is' and expected['S'] == 'The car' and expected['C1'] == 'red':
                correct_sentence = "The car is red."
        
        # パターン2: S + V + O1 (第3文型)
        elif 'S' in expected and 'V' in expected and 'O1' in expected and len(expected) == 3:
            if expected['S'] == 'I' and expected['V'] == 'love' and expected['O1'] == 'you':
                correct_sentence = "I love you."
        
        # 他のパターンも追加可能
        
        if correct_sentence and correct_sentence != current_sentence:
            fixes[num] = {
                'old': current_sentence,
                'new': correct_sentence,
                'expected': expected
            }
            print(f"例文{num}: '{current_sentence}' → '{correct_sentence}'")
    
    # 修正を適用
    if fixes:
        print(f"\n{len(fixes)}件の修正を適用します。")
        
        for num, fix in fixes.items():
            correct_answers[num]['sentence'] = fix['new']
            # タイムスタンプ更新
            correct_answers[num]['timestamp'] = datetime.now().isoformat()
            correct_answers[num]['notes'] = correct_answers[num].get('notes', '') + " [例文修正済み]"
        
        # ファイル保存
        with open('expected_results_progress.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ 正解データベース修正完了")
    else:
        print("修正が必要な項目はありません。")

if __name__ == "__main__":
    fix_expected_database()
