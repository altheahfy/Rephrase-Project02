#!/usr/bin/env python3
"""
spaCy品詞分析の詳細確認（依存関係解析なし）
"""

import spacy

def analyze_pos_only():
    nlp = spacy.load('en_core_web_sm')
    
    test_sentence = "The students study hard for exams."
    print(f"テスト文: {test_sentence}")
    
    doc = nlp(test_sentence)
    
    print(f"\nspaCy品詞分析結果（依存関係解析なし）:")
    print("Index | Token    | POS   | Tag   | Lemma   | Shape")
    print("-" * 55)
    
    for i, token in enumerate(doc):
        print(f"{i:5d} | {token.text:8s} | {token.pos_:5s} | {token.tag_:5s} | {token.lemma_:7s} | {token.shape_}")
    
    # 動詞の特定
    print(f"\n動詞の特定:")
    for i, token in enumerate(doc):
        if token.pos_ in ['VERB', 'AUX']:
            print(f"  {i}: {token.text} (POS: {token.pos_}, TAG: {token.tag_})")
    
    # 副詞の特定
    print(f"\n副詞の特定:")
    for i, token in enumerate(doc):
        if token.pos_ == 'ADV':
            print(f"  {i}: {token.text} (POS: {token.pos_}, TAG: {token.tag_})")
    
    # 前置詞の特定
    print(f"\n前置詞の特定:")
    for i, token in enumerate(doc):
        if token.pos_ == 'ADP':
            print(f"  {i}: {token.text} (POS: {token.pos_}, TAG: {token.tag_})")
    
    # 名詞の特定
    print(f"\n名詞の特定:")
    for i, token in enumerate(doc):
        if token.pos_ in ['NOUN', 'PRON', 'PROPN']:
            print(f"  {i}: {token.text} (POS: {token.pos_}, TAG: {token.tag_})")

if __name__ == "__main__":
    analyze_pos_only()
