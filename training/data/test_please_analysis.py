#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
spaCy解析による「please」の品詞・依存関係確認
"""

import spacy

def analyze_please_sentences():
    """pleaseを含む文のspaCy解析確認"""
    # spaCyモデル読み込み
    nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        "Help me, please.",
        "Call her back, please.",
        "Come here quickly, please.",
        "Give it to him, please.",
    ]
    
    print("=== spaCy解析：「please」の品詞・依存関係確認 ===\n")
    
    for sentence in test_sentences:
        print(f"📝 例文: '{sentence}'")
        doc = nlp(sentence)
        
        for token in doc:
            if token.text.lower() == 'please':
                print(f"  🔍 「please」詳細:")
                print(f"    - token.text: {token.text}")
                print(f"    - token.lemma_: {token.lemma_}")
                print(f"    - token.pos_: {token.pos_}")
                print(f"    - token.tag_: {token.tag_}")
                print(f"    - token.dep_: {token.dep_}")
                print(f"    - token.head: {token.head}")
                print(f"    - token.i (位置): {token.i}")
                
        print(f"  📊 全tokens: {[(t.text, t.pos_, t.dep_) for t in doc]}")
        print()

if __name__ == "__main__":
    analyze_please_sentences()
