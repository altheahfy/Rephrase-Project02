#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stanza解析結果の詳細確認"""

import stanza

def debug_stanza_analysis():
    """Case 49のStanza解析結果を詳細表示"""
    
    # Stanza初期化
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
    
    sentence = "The team working overtime completed the project successfully yesterday."
    print(f"入力: {sentence}")
    
    doc = nlp(sentence)
    sent = doc.sentences[0]
    
    print(f"\n=== Stanza解析結果 ===")
    for word in sent.words:
        print(f"ID:{word.id:2} text:'{word.text:12}' lemma:'{word.lemma:12}' upos:{word.upos:5} deprel:{word.deprel:12} head:{word.head:2}")
    
    print(f"\n=== 依存関係詳細 ===")
    for word in sent.words:
        if word.head > 0:
            head_word = next(w for w in sent.words if w.id == word.head)
            print(f"{word.text} -> {head_word.text} ({word.deprel})")
    
    print(f"\n=== successfully の関係 ===")
    successfully = next(w for w in sent.words if w.text == "successfully")
    yesterday = next(w for w in sent.words if w.text == "yesterday")
    
    print(f"successfully: id={successfully.id}, head={successfully.head}, deprel={successfully.deprel}")
    print(f"yesterday: id={yesterday.id}, head={yesterday.head}, deprel={yesterday.deprel}")
    
    if successfully.head == yesterday.id:
        print(f"✅ successfully は yesterday の修飾語として認識されています")
    else:
        head_word = next(w for w in sent.words if w.id == successfully.head)
        print(f"✅ successfully の head は {head_word.text} です")

if __name__ == "__main__":
    debug_stanza_analysis()
