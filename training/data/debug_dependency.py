#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spaCy依存関係解析デバッグ用スクリプト
"""
import spacy

def debug_dependencies(sentence):
    """依存関係を詳細表示"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    print(f"\n🔍 文: {sentence}")
    print("=" * 60)
    
    # ROOT動詞特定
    root_verb = None
    for token in doc:
        if token.dep_ == 'ROOT':
            root_verb = token
            print(f"📌 ROOT動詞: {token.text} (index: {token.i})")
            break
    
    print("\n📋 全トークン詳細:")
    for token in doc:
        print(f"  {token.i:2d}: '{token.text}' | POS: {token.pos_} | DEP: {token.dep_} | HEAD: '{token.head.text}' (index: {token.head.i})")
    
    if root_verb:
        print(f"\n🎯 ROOT動詞 '{root_verb.text}' の子要素:")
        for child in root_verb.children:
            print(f"  - '{child.text}' (dep: {child.dep_}, pos: {child.pos_})")
            
            if child.dep_ in ['nsubj', 'nsubjpass']:
                print(f"    ✅ 主語候補: '{child.text}'")
                print(f"    📖 子要素 (subtree):")
                for desc in child.subtree:
                    print(f"      - '{desc.text}' (dep: {desc.dep_}, pos: {desc.pos_})")

# テストケース
sentences = [
    "The book that I bought is interesting.",
    "The person who knows me is here.", 
    "The students who were studying passed the exam."
]

for sentence in sentences:
    debug_dependencies(sentence)
