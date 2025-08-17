#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smoothlyの配置問題を詳細分析
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def analyze_smoothly_issue():
    """smoothlyの配置問題を分析"""
    
    # 期待値データを読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # 類似の副詞配置例を検索
    similar_cases = []
    
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        main_slots = expected.get('main_slots', {})
        
        # 動詞後の様態副詞を含む例文を検索
        if any(adv in sentence.lower() for adv in ['smoothly', 'carefully', 'quickly', 'successfully', 'efficiently']):
            similar_cases.append({
                'test_id': test_id,
                'sentence': sentence,
                'main_slots': main_slots
            })
    
    print("様態副詞の配置パターン分析")
    print("="*60)
    
    for case in similar_cases:
        print(f"Test{case['test_id']}: {case['sentence']}")
        m_slots = {k: v for k, v in case['main_slots'].items() if k.startswith('M')}
        print(f"  M配置: {m_slots}")
        print()

if __name__ == "__main__":
    analyze_smoothly_issue()
