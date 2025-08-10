#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同格that節のhe, we問題をデバッグするスクリプト
"""

import spacy

def debug_that_clause_processing(text):
    """同格that節の詳細処理をデバッグ"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print(f"\n=== '{text}' のデバッグ ===")
    for i, token in enumerate(doc):
        print(f"{i}: '{token.text}' -> POS: {token.pos_}, DEP: {token.dep_}, HEAD: '{token.head.text}'")
    
    # that検出
    that_token = None
    for token in doc:
        if token.text.lower() == "that":
            if token.dep_ in ["acl", "ccomp", "mark", "dobj"] or (token.pos_ == "SCONJ"):
                that_token = token
                print(f"✓ that検出: インデックス {that_token.i}")
                break
    
    if not that_token:
        print("✗ that節未検出")
        return
        
    # 名詞句検出
    noun_phrase_tokens = []
    main_noun = None
    for token in doc:
        if token.i < that_token.i:
            if token.pos_ in ["NOUN", "PROPN"]:
                main_noun = token
                print(f"✓ 主名詞検出: '{main_noun.text}' インデックス {main_noun.i}")
            elif token.pos_ == "DET" and not noun_phrase_tokens:
                noun_phrase_tokens.append(token)
                print(f"✓ 冠詞検出: '{token.text}' インデックス {token.i}")
    
    if main_noun:
        if noun_phrase_tokens:
            noun_phrase_tokens.append(main_noun)
        else:
            noun_phrase_tokens = [main_noun]
    
    print(f"✓ 名詞句: {[t.text for t in noun_phrase_tokens]}")
    
    # that節内動詞検出
    that_clause_verb = None
    that_clause_subj = None
    
    for token in doc:
        if token.i > that_token.i and token.pos_ == "VERB":
            that_clause_verb = token
            print(f"✓ that節内動詞検出: '{that_clause_verb.text}' インデックス {that_clause_verb.i}")
            # その動詞の主語を探す
            subjects = [child for child in token.children if child.dep_ == "nsubj"]
            if subjects:
                that_clause_subj = subjects[0]
                print(f"✓ that節内主語検出: '{that_clause_subj.text}' インデックス {that_clause_subj.i}")
            else:
                print("✗ that節内主語未検出")
                # 依存構造を詳細表示
                print("動詞の子要素:")
                for child in token.children:
                    print(f"  - '{child.text}' DEP: {child.dep_}")
            break
    
    if not that_clause_verb:
        print("✗ that節内動詞未検出")
    
    print("-" * 50)

if __name__ == "__main__":
    test_cases = [
        "The fact that he came",
        "The idea that we discussed"
    ]
    
    for case in test_cases:
        debug_that_clause_processing(case)
