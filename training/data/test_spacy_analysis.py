#!/usr/bin/env python3
"""spaCy解析結果確認テスト"""

import spacy

def test_spacy_analysis():
    nlp = spacy.load("en_core_web_sm")
    
    sentence = "The house where I was born is in Tokyo."
    print(f"文: {sentence}")
    
    doc = nlp(sentence)
    
    print("\n=== spaCy解析結果 ===")
    for token in doc:
        print(f"{token.text:10} | POS: {token.pos_:8} | TAG: {token.tag_:8} | DEP: {token.dep_:12} | HEAD: {token.head.text:10}")
    
    print("\n=== ROOT語検出 ===")
    root_tokens = [token for token in doc if token.dep_ == "ROOT"]
    for root in root_tokens:
        print(f"ROOT語: {root.text} (POS: {root.pos_}, TAG: {root.tag_})")
    
    print("\n=== 関係節検出 ===")
    relcl_tokens = [token for token in doc if token.dep_ == "relcl"]
    for relcl in relcl_tokens:
        print(f"関係節動詞: {relcl.text} (HEAD: {relcl.head.text})")

if __name__ == "__main__":
    test_spacy_analysis()
