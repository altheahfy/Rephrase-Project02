#!/usr/bin/env python3
"""
基本5文型テストケース特定スクリプト
"""
import json

def analyze_basic_patterns():
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    basic_tests = []
    relative_tests = []
    passive_tests = []
    
    for test_id, test_case in data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        # 分析条件
        has_sub_slots = len(expected.get('sub_slots', {})) > 0
        has_relatives = any(word in sentence.lower() for word in ['who', 'which', 'that', 'whom', 'whose'])
        has_passive_words = any(pattern in sentence.lower() for pattern in ['was ', 'were ', 'is ', 'are ', 'been ', 'being '])
        has_by_phrase = 'by ' in sentence.lower()
        
        # カテゴリ分類
        if has_relatives:
            relative_tests.append({'id': int(test_id), 'sentence': sentence})
        elif has_passive_words and (has_by_phrase or 'crashed' in sentence or 'written' in sentence or 'sent' in sentence or 'built' in sentence or 'baked' in sentence):
            passive_tests.append({'id': int(test_id), 'sentence': sentence})
        else:
            # 基本5文型
            basic_tests.append({
                'id': int(test_id),
                'sentence': sentence,
                'pattern': _get_pattern_type(expected['main_slots']),
                'main_slots': expected['main_slots']
            })

    print(f'=== テストケース分類結果 ===')
    print(f'基本5文型: {len(basic_tests)}件')
    print(f'関係節: {len(relative_tests)}件')
    print(f'受動態: {len(passive_tests)}件')
    print()
    
    print('=== 基本5文型テストケース ===')
    for test in sorted(basic_tests, key=lambda x: x['id']):
        print(f"Test {test['id']}: {test['sentence']} [{test['pattern']}]")
    
    print()
    print('=== 基本5文型テストID一覧 ===')
    basic_ids = sorted([test['id'] for test in basic_tests])
    print(f"基本5文型IDs: {set(basic_ids)}")
    
    return basic_tests, relative_tests, passive_tests

def _get_pattern_type(main_slots):
    """文型を判定"""
    slots = set(main_slots.keys())
    if 'O2' in slots:
        return 'SVOO'  # 第4文型
    elif 'O1' in slots and 'C1' in slots:
        return 'SVOC'  # 第5文型
    elif 'O1' in slots:
        return 'SVO'   # 第3文型
    elif 'C1' in slots:
        return 'SVC'   # 第2文型
    else:
        return 'SV'    # 第1文型

if __name__ == "__main__":
    analyze_basic_patterns()
