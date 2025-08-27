#!/usr/bin/env python3
"""
基本5文型と関係節の例文特定スクリプト

final_54_test_data.jsonから基本5文型と関係節の例文を特定し、
それらをグループ化して表示する
"""

import json
import re

def identify_sentence_types():
    """例文のタイプを特定"""
    
    # データ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    basic_five_patterns = []
    relative_clauses = []
    other_patterns = []
    
    for key, case in data['data'].items():
        sentence = case.get('sentence', '')
        expected = case.get('expected', {})
        case_num = int(key)
        
        # 関係節キーワードをチェック
        relative_keywords = ['who', 'which', 'that', 'whom', 'whose', 'where', 'when', 'why', 'how']
        has_relative = any(keyword in sentence.lower() for keyword in relative_keywords)
        
        # サブスロットの存在をチェック
        has_sub_slots = bool(expected.get('sub_slots', {}))
        
        # 基本5文型の条件：シンプルで教科書的な例文
        is_basic_pattern = is_simple_basic_pattern(sentence, expected)
        
        if has_relative or has_sub_slots:
            relative_clauses.append({
                'case': case_num,
                'sentence': sentence,
                'keywords': [kw for kw in relative_keywords if kw in sentence.lower()] if has_relative else ['sub_slots検出']
            })
        elif is_basic_pattern:
            # 真の基本5文型（シンプルで教科書的）
            main_slots = expected.get('main_slots', {})
            basic_five_patterns.append({
                'case': case_num,
                'sentence': sentence,
                'pattern': determine_pattern_type(main_slots)
            })
        else:
            other_patterns.append({
                'case': case_num,
                'sentence': sentence
            })
    
    return basic_five_patterns, relative_clauses, other_patterns

def is_simple_basic_pattern(sentence, expected):
    """シンプルな基本5文型かどうかを判定"""
    
    # 複雑な構造を持つ場合は除外
    if expected.get('sub_slots', {}):
        return False
    
    # 関係代名詞・関係副詞がある場合は除外
    relative_keywords = ['who', 'which', 'that', 'whom', 'whose', 'where', 'when', 'why', 'how']
    if any(keyword in sentence.lower() for keyword in relative_keywords):
        return False
    
    # 受動態や複雑な時制は除外
    passive_indicators = ['was', 'were', 'been', 'being', 'by']
    if any(indicator in sentence.lower() for indicator in passive_indicators):
        return False
    
    # 副詞句や前置詞句が多い場合は除外
    complex_indicators = ['carefully', 'thoroughly', 'successfully', 'dramatically', 'efficiently', 'internationally']
    if any(indicator in sentence.lower() for indicator in complex_indicators):
        return False
    
    # 単語数チェック（基本文型は通常短い）
    word_count = len(sentence.split())
    if word_count > 8:  # 8語を超える場合は複雑とみなす
        return False
    
    # 基本的なS+V構造があるかチェック
    main_slots = expected.get('main_slots', {})
    has_basic_structure = 'S' in main_slots and 'V' in main_slots
    
    return has_basic_structure

def determine_pattern_type(main_slots):
    """基本5文型のパターンを判定"""
    if 'C1' in main_slots:
        return "第2文型 (S+V+C)"
    elif 'O1' in main_slots and 'O2' in main_slots:
        return "第4文型 (S+V+O+O)"
    elif 'O1' in main_slots and 'C1' in main_slots:
        return "第5文型 (S+V+O+C)"
    elif 'O1' in main_slots:
        return "第3文型 (S+V+O)"
    else:
        return "第1文型 (S+V)"

def main():
    print("🎯 基本5文型と関係節の例文特定")
    print("=" * 50)
    
    basic_patterns, relative_clauses, others = identify_sentence_types()
    
    print(f"\n📊 分類結果:")
    print(f"基本5文型: {len(basic_patterns)} ケース")
    print(f"関係節: {len(relative_clauses)} ケース")
    print(f"その他: {len(others)} ケース")
    print(f"総計: {len(basic_patterns) + len(relative_clauses) + len(others)} ケース")
    
    # 基本5文型の詳細
    print(f"\n🔸 基本5文型 ({len(basic_patterns)} ケース):")
    print("-" * 30)
    for item in basic_patterns:
        print(f"  {item['case']:2d}. {item['sentence']} [{item['pattern']}]")
    
    # 関係節の詳細
    print(f"\n🔸 関係節 ({len(relative_clauses)} ケース):")
    print("-" * 30)
    for item in relative_clauses:
        keywords_str = ", ".join(item['keywords']) if item['keywords'] else "sub_slots検出"
        print(f"  {item['case']:2d}. {item['sentence']} [{keywords_str}]")
    
    # テスト範囲の提案
    basic_range = [item['case'] for item in basic_patterns]
    relative_range = [item['case'] for item in relative_clauses]
    
    print(f"\n🎯 テスト実行コマンド:")
    print(f"基本5文型のみ: --range {','.join(map(str, basic_range))}")
    print(f"関係節のみ: --range {','.join(map(str, relative_range))}")
    
    # 連続範囲での実行
    all_target_cases = sorted(basic_range + relative_range)
    if all_target_cases:
        min_case = min(all_target_cases)
        max_case = max(all_target_cases)
        print(f"全対象: --range {min_case}-{max_case} (ただし、対象外も含む)")
        
        # 実際の対象ケース番号を出力
        print(f"対象ケース番号: {all_target_cases}")

if __name__ == "__main__":
    main()
