#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
spaCyの句動詞認識能力をテスト
"""

import spacy

def test_spacy_phrasal_verbs():
    print("=== spaCyの句動詞認識テスト ===")
    
    # Load English model
    nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        "Write down the sentence",
        "Write the sentence down", 
        "Turn off the light",
        "Turn the light off",
        "Look up the word",
        "Look the word up",
        "Put on your shoes",
        "Put your shoes on",
        "Take off your coat",
        "Take your coat off"
    ]
    
    for sentence in test_sentences:
        print(f"\n--- '{sentence}' ---")
        doc = nlp(sentence)
        
        # Token analysis
        for token in doc:
            print(f"  {token.text:<12} POS:{token.pos_:<6} TAG:{token.tag_:<6} DEP:{token.dep_:<8} HEAD:{token.head.text}")
        
        # Dependency tree visualization
        print("  Dependencies:")
        for token in doc:
            if token.dep_ == "prt":  # particle
                print(f"    ✓ PARTICLE DETECTED: {token.text} -> {token.head.text}")
            elif token.pos_ == "ADP" and token.dep_ == "prep":
                print(f"    • PREPOSITION: {token.text}")
        
        # Compound detection
        compounds = []
        for token in doc:
            if token.dep_ == "prt" and token.head.pos_ == "VERB":
                compounds.append(f"{token.head.text} {token.text}")
        
        if compounds:
            print(f"    🎯 PHRASAL VERB: {', '.join(compounds)}")
        else:
            print(f"    ❌ No phrasal verb detected")

if __name__ == "__main__":
    test_spacy_phrasal_verbs()
