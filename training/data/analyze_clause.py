#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節の構造分析
"""

import spacy

def analyze_clause_structure(text):
    """関係節の構造を詳しく分析"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print(f"=== 分析: '{text}' ===")
    print("Token分析:")
    for token in doc:
        print(f"  '{token.text}' | POS: {token.pos_} | Tag: {token.tag_} | Dep: {token.dep_} | Head: '{token.head.text}'")
    
    print("\n依存関係:")
    for token in doc:
        children = list(token.children)
        if children:
            children_text = [f"'{child.text}'({child.dep_})" for child in children]
            print(f"  '{token.text}' → {children_text}")
    
    print("\nROOT検索:")
    roots = [token for token in doc if token.dep_ == "ROOT"]
    for root in roots:
        print(f"  ROOT: '{root.text}' (POS: {root.pos_}, Tag: {root.tag_})")
    
    print("\n関係節(relcl)検索:")
    relcls = [token for token in doc if token.dep_ == "relcl"]
    for relcl in relcls:
        print(f"  RELCL: '{relcl.text}' (POS: {relcl.pos_}, Head: '{relcl.head.text}')")
        children = list(relcl.children)
        if children:
            children_text = [f"'{child.text}'({child.dep_})" for child in children]
            print(f"    Children: {children_text}")

if __name__ == "__main__":
    analyze_clause_structure("the manager who had recently taken charge of the project")
