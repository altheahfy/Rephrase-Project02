#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spaCyの品詞認識結果を確認するデバッグスクリプト
"""

import spacy

def debug_spacy_parsing(text):
    """spaCyの品詞認識結果をデバッグ表示"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print(f"\n=== '{text}' の解析結果 ===")
    for i, token in enumerate(doc):
        print(f"{i}: '{token.text}' -> POS: {token.pos_}, DEP: {token.dep_}, HEAD: '{token.head.text}'")
    print()

if __name__ == "__main__":
    test_phrases = [
        "The fact that he came",
        "The idea that we discussed"
    ]
    
    for phrase in test_phrases:
        debug_spacy_parsing(phrase)
