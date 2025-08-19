#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Case 49 専用デバッグ"""

import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを詳細に設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_case_49():
    """Case 49 の詳細デバッグ"""
    
    mapper = UnifiedStanzaRephraseMapper()
    sentence = "The team working overtime completed the project successfully yesterday."
    
    print(f"\n=== Case 49 詳細デバッグ ===")
    print(f"入力: {sentence}")
    
    result = mapper.process(sentence)
    
    print(f"\n結果詳細:")
    print(f"  Main slots: {result.get('slots', {})}")
    print(f"  Sub slots: {result.get('sub_slots', {})}")
    print(f"  Patterns: {result.get('grammar_info', {}).get('detected_patterns', [])}")
    
    # 期待値と比較
    expected_main = {'S': '', 'V': 'completed', 'O1': 'the project', 'M2': 'successfully', 'M3': 'yesterday'}
    expected_sub = {'sub-v': 'the team working', 'sub-m2': 'overtime'}
    
    actual_main = result.get('slots', {})
    actual_sub = result.get('sub_slots', {})
    
    print(f"\n比較:")
    print(f"  期待 main: {expected_main}")
    print(f"  実際 main: {actual_main}")
    print(f"  期待 sub:  {expected_sub}")
    print(f"  実際 sub:  {actual_sub}")
    
    # 問題点の特定
    problems = []
    
    # M3の問題
    if actual_main.get('M3') != expected_main.get('M3'):
        problems.append(f"M3不一致: 期待'{expected_main.get('M3')}' != 実際'{actual_main.get('M3')}'")
    
    # sub-vの大文字小文字
    if actual_sub.get('sub-v') != expected_sub.get('sub-v'):
        problems.append(f"sub-v不一致: 期待'{expected_sub.get('sub-v')}' != 実際'{actual_sub.get('sub-v')}'")
    
    if problems:
        print(f"\n問題点:")
        for problem in problems:
            print(f"  ❌ {problem}")
    else:
        print(f"\n✅ 完全一致！")

if __name__ == "__main__":
    debug_case_49()
