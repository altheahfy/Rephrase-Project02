#!/usr/bin/env python3
"""
spaCy依存関係の詳細分析
"""

import spacy

def analyze_spacy_dependencies():
    nlp = spacy.load("en_core_web_sm")
    
    sentences = [
        "That afternoon, she gave him a book.",
        "She teaches English to students every morning."
    ]
    
    for sentence in sentences:
        print(f"\n=== 例文: {sentence} ===")
        doc = nlp(sentence)
        
        for token in doc:
            print(f"{token.text:12} | {token.pos_:6} | {token.dep_:10} | {token.head.text:10}")
        
        print("\n📍 目的語関係の分析:")
        for token in doc:
            if token.dep_ in ["dobj", "iobj", "pobj"]:
                print(f"  {token.dep_}: '{token.text}' (head: {token.head.text})")

if __name__ == "__main__":
    analyze_spacy_dependencies()
