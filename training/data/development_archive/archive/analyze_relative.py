#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節の詳細構造分析
"""

import spacy

def analyze_relative_clause_structure(text):
    """関係節の詳細構造分析"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print(f"=== 分析: '{text}' ===")
    print("Token詳細分析:")
    for i, token in enumerate(doc):
        print(f"  {i}: '{token.text}' | POS: {token.pos_} | Tag: {token.tag_} | Dep: {token.dep_} | Head: '{token.head.text}' (index: {token.head.i})")
    
    print("\n依存関係ツリー:")
    for token in doc:
        children = list(token.children)
        if children:
            children_info = [f"'{child.text}'({child.dep_}, i:{child.i})" for child in children]
            print(f"  '{token.text}'(i:{token.i}) → {children_info}")

if __name__ == "__main__":
    test_cases = [
        "the manager who had recently taken charge of the project",
        "a pencil that I bought yesterday"
    ]
    
    for case in test_cases:
        analyze_relative_clause_structure(case)
        print()
