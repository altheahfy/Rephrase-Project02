#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

# Auxスロット完全デバッグテスト
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)

text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

doc = nlp(text)
sent = doc.sentences[0]

# ROOT動詞を特定
root_verb = None
for word in sent.words:
    if word.deprel == 'root':
        root_verb = word
        break

print(f"📌 ROOT動詞: '{root_verb.text}' (id={root_verb.id})")

# この場合、"had to make"構造では：
# - "had"がROOT (助動詞的役割)
# - "to make"がxcomp (実際の動詞句)

aux_parts = []

# 1. ROOT動詞がモーダル/助動詞として機能している場合
if root_verb.text.lower() in ['had', 'has', 'have', 'will', 'would', 'can', 'could', 'may', 'might', 'must', 'should']:
    aux_parts.append(root_verb.text)
    print(f"  → ROOT助動詞検出: '{root_verb.text}'")

# 2. ROOT動詞の助動詞を探す
for word in sent.words:
    if word.head == root_verb.id and word.deprel == 'aux':
        aux_parts.append(word.text)
        print(f"  → aux検出: '{word.text}'")

# 3. xcompのmarkも探す
for word in sent.words:
    if word.head == root_verb.id and word.deprel == 'xcomp':
        print(f"xcomp: '{word.text}' (id={word.id})")
        for child in sent.words:
            if child.head == word.id and child.deprel == 'mark':
                aux_parts.append(child.text)
                print(f"  → mark検出: '{child.text}'")

print(f"\n📍 Aux parts: {aux_parts}")
aux_text = ' '.join(aux_parts)
print(f"📍 Aux結果: '{aux_text}'")
print(f"正解: 'had to'")
print(f"一致: {aux_text == 'had to'}")
