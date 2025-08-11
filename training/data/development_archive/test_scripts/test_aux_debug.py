#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

# Auxスロットデバッグテスト
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

# Auxスロット関連の単語をチェック
aux_parts = []

print("\n=== 全単語の依存関係 ===")
for word in sent.words:
    if word.head == root_verb.id:
        print(f"単語: '{word.text}' deprel={word.deprel} head={word.head}")
        if word.deprel == 'aux':
            aux_parts.append(word.text)
            print(f"  → aux検出: '{word.text}'")

# xcompのmarkも探す
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
