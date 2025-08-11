#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

# テスト用の簡単なM1修正テスト
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

# obl:unmarkedを探す
for word in sent.words:
    if word.head == root_verb.id and word.deprel == 'obl:unmarked':
        # 依存関係ツリーの終端を探す
        max_end = word.end_char
        
        def find_children_end(word_id):
            global max_end
            for w in sent.words:
                if w.head == word_id:
                    max_end = max(max_end, w.end_char)
                    find_children_end(w.id)
        
        find_children_end(word.id)
        
        m1_text = text[:max_end].strip().rstrip(',').strip()
        print(f"📍 M1検出: '{m1_text}'")
        print(f"正解: 'that afternoon at the crucial point in the presentation'")
        print(f"一致: {m1_text.lower() == 'that afternoon at the crucial point in the presentation'}")
        break
