#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
部分カバレッジ問題のデバッグ
"""

import spacy
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

nlp = spacy.load("en_core_web_sm")

def analyze_partial_coverage(phrase):
    """部分カバレッジケースの詳細分析"""
    doc = nlp(phrase)
    print(f"\n=== '{phrase}' の詳細分析 ===")
    print(f"トークン数: {len(doc)}")
    
    print(f"\n【トークン詳細】")
    for token in doc:
        print(f"[{token.i}] '{token.text}':")
        print(f"    POS: {token.pos_}")
        print(f"    TAG: {token.tag_}")
        print(f"    DEP: {token.dep_}")
        print(f"    HEAD: '{token.head.text}' (index: {token.head.i})")
        print(f"    CHILDREN: {[child.text for child in token.children]}")
        print()

if __name__ == "__main__":
    # 問題のあるケースを分析
    test_cases = [
        "the big red car that must have been made very carefully",
        "making her crazy for him"
    ]
    
    for phrase in test_cases:
        analyze_partial_coverage(phrase)
        print("="*80)
