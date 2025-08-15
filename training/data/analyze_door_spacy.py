#!/usr/bin/env python3
"""The door opened slowly creaked loudly spaCy解析"""

import spacy

def analyze_door_spacy():
    print("The door opened slowly creaked loudly spaCy解析")
    
    nlp = spacy.load("en_core_web_sm")
    
    sentence = "The door opened slowly creaked loudly."
    doc = nlp(sentence)
    
    print(f"Sentence: {sentence}")
    print("\n=== SPACY DEPENDENCY ANALYSIS ===")
    
    for token in doc:
        print(f"Text: {token.text:10s} | Head: {token.head.text:10s} | Dep: {token.dep_:15s} | POS: {token.pos_:8s} | Tag: {token.tag_}")
    
    print("\n=== LOOKING FOR RELATIVE CLAUSES ===")
    for token in doc:
        if token.dep_ in ['relcl', 'acl', 'ccomp', 'xcomp']:
            print(f"  Found: {token.text} ({token.dep_}) -> head: {token.head.text}")
    
    print("\n=== SUBJECTS AND VERBS ===")
    subjects = [token for token in doc if token.dep_ in ['nsubj', 'nsubjpass', 'csubj']]
    verbs = [token for token in doc if token.pos_ == 'VERB']
    
    print(f"Subjects: {[s.text for s in subjects]}")
    print(f"Verbs: {[v.text for v in verbs]}")
    
    print("\n=== NOUN CHUNKS ===")
    for chunk in doc.noun_chunks:
        print(f"  Chunk: '{chunk.text}' | Root: {chunk.root.text} | Dep: {chunk.root.dep_}")

if __name__ == "__main__":
    analyze_door_spacy()
