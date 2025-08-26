#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
be動詞構文のStanza構造を詳細に分析
"""

import stanza

def analyze_be_verb_structure():
    """be動詞構文のStanza依存関係構造を詳細分析"""
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_sentences = [
        "He is happy.",
        "He is a teacher.", 
        "He is under pressure."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*50}")
        print(f"文: {sentence}")
        print(f"{'='*50}")
        
        doc = nlp(sentence)
        sent = doc.sentences[0]
        
        # ROOT特定
        root = None
        for word in sent.words:
            if word.deprel == 'root':
                root = word
                break
        
        print(f"ROOT: {root.text} ({root.upos})")
        print("\n依存関係構造:")
        
        for word in sent.words:
            head_text = "ROOT" if word.head == 0 else sent.words[word.head-1].text
            print(f"  {word.id:2d}: {word.text:12s} <- {head_text:12s} ({word.deprel:10s}) [{word.upos}]")
        
        # 各wordの文字範囲も表示
        print("\n文字範囲:")
        for word in sent.words:
            print(f"  {word.text}: {word.start_char}-{word.end_char} = '{sentence[word.start_char:word.end_char]}'")

if __name__ == "__main__":
    analyze_be_verb_structure()
