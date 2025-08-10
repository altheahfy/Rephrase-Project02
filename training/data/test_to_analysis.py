#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spacy

def test_to_analysis():
    """「to+目的格」構文の解析テスト"""
    nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        "You, give it to me straight.",
        "You, give that to him clearly.",
        "She's been married to a nice person."
    ]
    
    for sentence in test_sentences:
        print(f"\n=== Testing: {sentence} ===")
        doc = nlp(sentence)
        
        for token in doc:
            if token.text.lower() == 'to':
                print(f"Token: '{token.text}'")
                print(f"  POS: {token.pos_}")
                print(f"  Tag: {token.tag_}")
                print(f"  Dep: {token.dep_}")
                print(f"  Head: '{token.head.text}' ({token.head.pos_})")
                
                # Children を確認
                children = list(token.children)
                if children:
                    print(f"  Children: {[(child.text, child.dep_) for child in children]}")
                else:
                    print(f"  Children: None")

if __name__ == "__main__":
    test_to_analysis()
