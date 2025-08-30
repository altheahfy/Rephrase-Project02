#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正版actionグループテスト
文頭副詞と文中副詞の位置別分離をテスト
"""

import json
from adverb_position_analyzer import AdverbPositionAnalyzer

def test_action_group():
    """actionグループの修正版テスト"""
    print("🚀 修正版actionグループ副詞位置分析テスト")
    
    # actionグループの例文データ（手動抽出）
    action_sentences = [
        {
            'sentence': 'She sings beautifully.',
            'slots': {'S': 'She', 'V': 'sings', 'M2': 'beautifully'}
        },
        {
            'sentence': 'We always eat breakfast together.',
            'slots': {'S': 'We', 'V': 'eat', 'O1': 'breakfast', 'M1': 'always', 'M2': 'together'}
        },
        {
            'sentence': 'The cat quietly sat on the mat.',
            'slots': {'S': 'The cat', 'V': 'sat', 'M1': 'quietly', 'M2': 'on the mat'}
        },
        {
            'sentence': 'She carefully reads books.',
            'slots': {'S': 'She', 'V': 'reads', 'O1': 'books', 'M2': 'carefully'}
        },
        {
            'sentence': 'They run fast.',
            'slots': {'S': 'They', 'V': 'run', 'M2': 'fast'}
        },
        {
            'sentence': 'Actually, she works very hard.',
            'slots': {'S': 'she', 'V': 'works', 'M1': 'Actually', 'M2': 'very hard'}
        },
        {
            'sentence': 'Every morning, he jogs slowly in the park.',
            'slots': {'S': 'he', 'V': 'jogs', 'M1': 'Every morning', 'M2': 'slowly', 'M3': 'in the park'}
        }
    ]
    
    analyzer = AdverbPositionAnalyzer()
    
    print(f"\n📚 actionグループ例文 ({len(action_sentences)}件):")
    for i, data in enumerate(action_sentences, 1):
        print(f"  {i}. {data['sentence']}")
        print(f"     スロット: {data['slots']}")
    
    # 修正版で処理
    results = analyzer.process_adverb_group('action_fixed', action_sentences)
    
    # 結果を保存
    output_file = 'action_group_fixed_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 修正版結果を {output_file} に保存しました")
    
    # 結果の確認
    print(f"\n📊 修正版actionグループ結果:")
    for i, result in enumerate(results, 1):
        print(f"例文{i}: {result['sentence']}")
        print(f"順序: {result['ordered_slots']}")
        print()

if __name__ == "__main__":
    test_action_group()
