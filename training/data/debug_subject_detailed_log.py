#!/usr/bin/env python3
"""
主語検出失敗の原因特定
"""

import sys
import os
sys.path.append('.')

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def debug_subject_detection():
    mapper = DynamicGrammarMapper()
    
    # テスト文
    text = "She quickly runs to school."
    result = mapper.analyze_sentence(text)
    
    print(f"\n=== 解析結果 ===")
    for role, assignments in result.items():
        if assignments:
            print(f"{role}: {assignments}")

if __name__ == "__main__":
    debug_subject_detection()
