#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 1: spaCy依存構造解析の基礎確認
=====================================
パターンマッチングから脱却し、構造解析ベースでの分析を学ぶ
"""

import spacy

def analyze_sentence_structure(text):
    """文の依存構造を詳細分析"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print(f"=== 文: '{text}' ===")
    print(f"文長: {len(doc)} tokens")
    print()
    
    print("【Token分析】")
    for token in doc:
        print(f"Token: '{token.text}' | POS: {token.pos_} | Dep: {token.dep_} | Head: '{token.head.text}'")
    
    print()
    print("【依存関係の構造】")
    for token in doc:
        if token.dep_ != "punct":  # 句読点は除外
            children = list(token.children)
            children_text = [child.text for child in children]
            print(f"'{token.text}' ({token.dep_}) → children: {children_text}")
    
    print()
    print("【ROOTからの構造】")
    root = [token for token in doc if token.dep_ == "ROOT"][0]
    print(f"ROOT: '{root.text}' (POS: {root.pos_})")
    
    # 主語
    subjects = [child for child in root.children if child.dep_ in ["nsubj", "nsubjpass"]]
    if subjects:
        print(f"主語: {[s.text for s in subjects]}")
    
    # 目的語
    objects = [child for child in root.children if child.dep_ in ["dobj", "iobj"]]
    if objects:
        print(f"目的語: {[o.text for o in objects]}")
    
    # 助動詞
    aux = [child for child in root.children if child.dep_ in ["aux", "auxpass"]]
    if aux:
        print(f"助動詞: {[a.text for a in aux]}")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    # シンプルな例文から始める
    test_sentences = [
        "The manager works.",
        "The manager had worked.", 
        "The manager who works is here."
    ]
    
    for sentence in test_sentences:
        analyze_sentence_structure(sentence)
