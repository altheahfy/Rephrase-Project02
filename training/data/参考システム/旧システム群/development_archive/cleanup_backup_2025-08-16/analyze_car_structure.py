#!/usr/bin/env python3
"""The car parked outside 構造解析"""

import stanza

def analyze_car_parked():
    print("The car parked outside 構造解析")
    
    nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')
    
    sentence = "The car parked outside is mine."
    doc = nlp(sentence)
    
    print(f"Sentence: {sentence}")
    print("\n=== STANZA DEPENDENCY ANALYSIS ===")
    
    for sent in doc.sentences:
        for word in sent.words:
            print(f"ID: {word.id:2d} | Text: {word.text:10s} | Head: {word.head:2d} | Deprel: {word.deprel:15s} | POS: {word.upos}")
    
    print("\n=== LOOKING FOR RELATIVE CLAUSES ===")
    for sent in doc.sentences:
        for word in sent.words:
            if word.deprel in ['acl:relcl', 'acl', 'amod']:
                print(f"  Found: {word.text} ({word.deprel}) -> head: {word.head}")
                head_word = None
                for w in sent.words:
                    if w.id == word.head:
                        head_word = w
                        break
                if head_word:
                    print(f"    Head word: {head_word.text}")

if __name__ == "__main__":
    analyze_car_parked()
