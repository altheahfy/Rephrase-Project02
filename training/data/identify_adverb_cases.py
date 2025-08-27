#!/usr/bin/env python3
"""
副詞ケース特定スクリプト
基本5文型の中で副詞を含むケースのみを特定
"""

import json
import re

def identify_adverb_cases():
    """基本5文型の中で副詞を含むケースを特定"""
    
    # データ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 副詞リスト（よく使われる副詞）
    adverbs = [
        'carefully', 'quickly', 'slowly', 'quietly', 'loudly', 'clearly',
        'hard', 'well', 'fast', 'early', 'late', 'often', 'always', 'never',
        'sometimes', 'usually', 'daily', 'yesterday', 'today', 'tomorrow',
        'here', 'there', 'everywhere', 'anywhere', 'nowhere',
        'very', 'quite', 'really', 'extremely', 'completely', 'totally'
    ]
    
    basic_with_adverbs = []
    
    for key, case in data['data'].items():
        sentence = case.get('sentence', '')
        expected = case.get('expected', {})
        case_num = int(key)
        
        # 関係代名詞・関係副詞がある場合は除外
        relative_keywords = ['who', 'which', 'that', 'whom', 'whose', 'where', 'when', 'why', 'how']
        has_relative = any(keyword in sentence.lower() for keyword in relative_keywords)
        
        # サブスロットの存在をチェック（関係節除外）
        has_sub_slots = bool(expected.get('sub_slots', {}))
        
        # 受動態や複雑な構造を除外
        passive_indicators = ['was', 'were', 'been', 'being', 'by']
        has_passive = any(indicator in sentence.lower() for indicator in passive_indicators)
        
        # 複雑な修飾語を除外
        complex_indicators = ['internationally', 'dramatically', 'efficiently', 'successfully']
        has_complex = any(indicator in sentence.lower() for indicator in complex_indicators)
        
        # 基本構造チェック
        main_slots = expected.get('main_slots', {})
        has_basic_structure = 'S' in main_slots and 'V' in main_slots
        
        # 副詞チェック
        has_adverb = any(adverb in sentence.lower() for adverb in adverbs)
        
        # 基本5文型 + 副詞のみの条件
        if (has_basic_structure and has_adverb and 
            not has_relative and not has_sub_slots and 
            not has_passive and not has_complex and
            len(sentence.split()) <= 10):  # 複雑すぎない
            
            found_adverbs = [adv for adv in adverbs if adv in sentence.lower()]
            basic_with_adverbs.append({
                'case': case_num,
                'sentence': sentence,
                'adverbs': found_adverbs,
                'pattern': determine_pattern_type(main_slots)
            })
    
    return basic_with_adverbs

def determine_pattern_type(main_slots):
    """基本5文型のパターンを判定"""
    if 'C1' in main_slots:
        return "第2文型 (S+V+C)"
    elif 'O1' in main_slots and 'O2' in main_slots:
        return "第4文型 (S+V+O+O)"
    elif 'O1' in main_slots and 'C2' in main_slots:
        return "第5文型 (S+V+O+C)"
    elif 'O1' in main_slots:
        return "第3文型 (S+V+O)"
    else:
        return "第1文型 (S+V)"

def main():
    print("🎯 副詞を含む基本5文型の例文特定")
    print("=" * 50)
    
    adverb_cases = identify_adverb_cases()
    
    print(f"\n📊 副詞を含む基本5文型: {len(adverb_cases)} ケース")
    
    if adverb_cases:
        print("\n🔸 副詞を含む基本5文型:")
        print("-" * 50)
        for item in adverb_cases:
            adverbs_str = ", ".join(item['adverbs'])
            print(f"  {item['case']:2d}. {item['sentence']} [{item['pattern']}] 副詞: {adverbs_str}")
        
        # テスト用の範囲を生成
        case_numbers = [item['case'] for item in adverb_cases]
        print(f"\n🎯 副詞ハンドラーテスト用コマンド:")
        print(f"python fast_test.py {','.join(map(str, case_numbers))}")
    else:
        print("\n❌ 条件に合致する副詞ケースが見つかりませんでした")

if __name__ == "__main__":
    main()
