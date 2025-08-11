#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

# Stanza初期化
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')

# テスト文
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print(f"🎯 デバッグ開始: '{text[:50]}...'")

# 解析
doc = nlp(text)
sent = doc.sentences[0]

print("\n=== 文字位置デバッグ ===")
print(f"全文: '{text}'")
print(f"文長: {len(text)}")

# ROOT動詞を特定
root_verb = None
for word in sent.words:
    if word.deprel == 'root':
        root_verb = word
        break

print(f"📌 ROOT動詞: '{root_verb.text}' (id={root_verb.id})")

# 主語を特定
subject_word = None
for word in sent.words:
    if word.head == root_verb.id and word.deprel == 'nsubj':
        subject_word = word
        break

if subject_word:
    print(f"📌 主語単語: '{subject_word.text}' (start_char={subject_word.start_char}, end_char={subject_word.end_char})")
    
    # 文頭から主語開始まで
    m1_candidate = text[:subject_word.start_char]
    print(f"📌 M1候補（主語開始まで）: '{m1_candidate}'")
    print(f"📌 M1候補長さ: {len(m1_candidate)}")
    
    # カンマと空白を除去
    m1_cleaned = m1_candidate.strip().rstrip(',').strip()
    print(f"📌 M1清掃後: '{m1_cleaned}'")
    
    print(f"📌 正解: 'that afternoon at the crucial point in the presentation'")
    print(f"📌 一致: {m1_cleaned.lower() == 'that afternoon at the crucial point in the presentation'}")
