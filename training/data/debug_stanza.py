#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza
import json

# Stanza初期化
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')

# テスト文
sentence = "The man whose car is red lives here."

print(f"Testing sentence: {sentence}")
print("="*50)

# Stanza解析
doc = nlp(sentence)

# 詳細出力
for sent in doc.sentences:
    print("Token詳細:")
    for word in sent.words:
        print(f"  ID:{word.id:2} Text:'{word.text}' Lemma:'{word.lemma}' UPOS:{word.upos} XPOS:{word.xpos} Head:{word.head} Deprel:{word.deprel}")
    
    print("\nROOT語の特定:")
    root_words = [w for w in sent.words if w.deprel == 'root']
    for root in root_words:
        print(f"  ROOT: '{root.text}' (ID:{root.id}, UPOS:{root.upos}, XPOS:{root.xpos})")
    
    print("\n'man'と'lives'の詳細:")
    for word in sent.words:
        if word.text.lower() in ['man', 'lives']:
            print(f"  '{word.text}': ID={word.id}, UPOS={word.upos}, XPOS={word.xpos}, Deprel={word.deprel}, Head={word.head}")
