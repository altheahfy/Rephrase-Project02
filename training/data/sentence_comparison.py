#!/usr/bin/env python3
"""
例文照合スクリプト - 元例文、custom_test.py、正解データベースを比較
"""

import json

# アタッチメントの元例文リスト（original_54_sentences.md から）
ORIGINAL_SENTENCES = [
    "I love you.",
    "She reads books.", 
    "The cat sleeps.",
    "He gives me a book.",
    "I find it interesting.",
    "The flowers are beautiful.",
    "I eat breakfast every morning.",
    "She studies English twice a week.",
    "He visits his grandmother on Sundays.",
    "We go to the beach in summer.",
    "They play tennis after school.",
    "She is going to visit Paris next month.",
    "He has finished his homework.",
    "I went to the store and bought some milk.",
    "She was tired, but she continued working.",
    "Although it was raining, we went for a walk.",
    "Because he was late, he missed the train.",
    "If it rains, I stay home.",
    "She acts as if she knows everything.",
    "The students study hard for exams.",
    "The person that works here is kind.",
    "The car which was parked outside is mine.",
    "The house where I was born is old.",
    "The day when we met was sunny.",
    "The reason why he left is unclear.",
    "The man whose car was stolen called the police.",
    "I know the person that you mentioned.",
    "The book which I read was fascinating.",
    "The place where we lived was peaceful.",
    "The time when you called was perfect.",
    "The woman whose idea won the contest is my sister.",
    "I like the movie that you recommended.",
    "The restaurant where we ate was expensive.",
    "The moment when I realized the truth was shocking.",
    "The man who is standing there is my father.",
    "The girl whom I met yesterday is very smart.",
    "The house that we visited last week is for sale.",
    "The teacher whose class I attended was excellent.",
    "I am running quickly to catch the bus.",
    "She sings beautifully at the concert.",
    "The dog barks loudly in the yard.",
    "He works diligently on his project.",
    "They dance gracefully at the party.",
    "The window was broken.",
    "The letter was written by John.",
    "The house was built in 1990.",
    "The book was written by a famous author.",
    "The cake is being baked by my mother.",
    "The cake was eaten by the children.",
    "The door was opened by the key.",
    "The message was sent yesterday.",
    "The car was repaired last week.",
    "The book was published in 2020.",
    "The room was cleaned this morning."
]

# custom_test.pyから例文抽出
def extract_from_custom_test():
    """custom_test.pyから例文を抽出"""
    sentences = []
    try:
        with open('custom_test.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 例文リスト部分を抽出（簡易的な方法）
        lines = content.split('\n')
        in_sentences = False
        for line in lines:
            line = line.strip()
            if 'your_test_sentences = [' in line:
                in_sentences = True
                continue
            if in_sentences:
                if line == ']' or line == '],':
                    break
                if line.startswith('"') and line.endswith('",'):
                    sentence = line[1:-2]  # 前後の"と",を除去
                    sentences.append(sentence)
                elif line.startswith('"') and line.endswith('"'):
                    sentence = line[1:-1]  # 前後の"を除去
                    sentences.append(sentence)
        
        return sentences
    except Exception as e:
        print(f"custom_test.py読み込みエラー: {e}")
        return []

# 正解データベースから例文抽出
def extract_from_expected_results():
    """正解データベースから例文を抽出"""
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sentences = []
        correct_answers = data.get('correct_answers', {})
        
        for i in range(1, 55):  # 1-54
            key = str(i)
            if key in correct_answers:
                sentence = correct_answers[key].get('sentence', '')
                sentences.append(sentence)
            else:
                sentences.append('[データなし]')
        
        return sentences
    except Exception as e:
        print(f"正解データベース読み込みエラー: {e}")
        return []

def compare_all():
    """3つのソースを比較"""
    print("📊 例文比較 - 元例文 vs custom_test.py vs 正解データベース")
    print("=" * 80)
    
    custom_sentences = extract_from_custom_test()
    expected_sentences = extract_from_expected_results()
    
    print(f"元例文数: {len(ORIGINAL_SENTENCES)}")
    print(f"custom_test.py例文数: {len(custom_sentences)}")
    print(f"正解データベース例文数: {len(expected_sentences)}")
    print()
    
    max_len = max(len(ORIGINAL_SENTENCES), len(custom_sentences), len(expected_sentences))
    
    matches_original_custom = 0
    matches_original_expected = 0
    matches_custom_expected = 0
    
    for i in range(max_len):
        original = ORIGINAL_SENTENCES[i] if i < len(ORIGINAL_SENTENCES) else '[なし]'
        custom = custom_sentences[i] if i < len(custom_sentences) else '[なし]'
        expected = expected_sentences[i] if i < len(expected_sentences) else '[なし]'
        
        # 一致確認
        orig_custom_match = original == custom
        orig_expected_match = original == expected
        custom_expected_match = custom == expected
        
        if orig_custom_match: matches_original_custom += 1
        if orig_expected_match: matches_original_expected += 1
        if custom_expected_match: matches_custom_expected += 1
        
        # 不一致のみ表示
        if not (orig_custom_match and orig_expected_match and custom_expected_match):
            print(f"例文{i+1:2d}:")
            print(f"  元     : {original}")
            print(f"  custom : {custom}")
            print(f"  正解DB : {expected}")
            print(f"  一致   : 元-custom:{orig_custom_match}, 元-正解:{orig_expected_match}, custom-正解:{custom_expected_match}")
            print()
    
    print("=" * 80)
    print(f"📈 一致統計:")
    print(f"  元例文 ↔ custom_test.py  : {matches_original_custom}/{max_len} ({matches_original_custom/max_len*100:.1f}%)")
    print(f"  元例文 ↔ 正解データベース: {matches_original_expected}/{max_len} ({matches_original_expected/max_len*100:.1f}%)")
    print(f"  custom ↔ 正解データベース: {matches_custom_expected}/{max_len} ({matches_custom_expected/max_len*100:.1f}%)")

if __name__ == "__main__":
    compare_all()
