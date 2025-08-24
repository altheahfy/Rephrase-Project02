#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def analyze_complement_vs_adverb_issues():
    """補語(C1)と副詞(M3)の誤分類問題を分析"""
    
    print('=== 補語vs副詞の誤分類問題分析 ===')
    
    # 問題例文の詳細分析
    test_cases = [
        {
            'id': 9,
            'sentence': 'The car which was crashed is red.',
            'issue': 'red → C1 (補語) であるべきなのに M3 として期待されている',
            'correct_analysis': {
                'main': {'S': '', 'V': 'is', 'C1': 'red'},
                'sub': {'sub-s': 'The car which', 'sub-aux': 'was', 'sub-v': 'crashed', '_parent_slot': 'S'}
            }
        },
        {
            'id': 10,
            'sentence': 'The book that was written is famous.',
            'issue': 'famous → C1 (補語) であるべきなのに M3 として期待されている',
            'correct_analysis': {
                'main': {'S': '', 'V': 'is', 'C1': 'famous'},
                'sub': {'sub-s': 'The book that', 'sub-aux': 'was', 'sub-v': 'written', '_parent_slot': 'S'}
            }
        }
    ]
    
    print('🔍 分析結果:')
    for case in test_cases:
        print(f"\nTest {case['id']}: {case['sentence']}")
        print(f"問題: {case['issue']}")
        print(f"正解分析:")
        print(f"  main: {case['correct_analysis']['main']}")
        print(f"  sub:  {case['correct_analysis']['sub']}")
    
    print('\n🎯 結論:')
    print('現在の中央制御機構は正しく動作している！')
    print('問題は期待値設定が文法的に不正確であること。')
    print('"is red", "is famous" → SVC文型 (S + V + C1)')
    print('これらは副詞ではなく補語として処理するのが正解。')
    
    print('\n🚀 次のステップ:')
    print('1. 期待値データの修正（C1として設定）')
    print('2. 真の副詞配置問題の特定と修正')
    print('3. より複雑な副詞配置パターンのテスト追加')

if __name__ == "__main__":
    analyze_complement_vs_adverb_issues()
