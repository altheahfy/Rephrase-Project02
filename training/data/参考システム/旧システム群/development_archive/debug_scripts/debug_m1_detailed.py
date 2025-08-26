#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

# Stanza初期化
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')

# テスト文
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print(f"🎯 詳細デバッグ開始")

# 解析
doc = nlp(text)
sent = doc.sentences[0]

# 全単語をチェック
print("\n=== 全単語の位置情報 ===")
for i, word in enumerate(sent.words):
    print(f"{i+1:2}: '{word.text}' (start={word.start_char}, end={word.end_char}) head={word.head} deprel={word.deprel}")

print(f"\n=== 文字位置からテキスト切り出し確認 ===")
print(f"0-53: '{text[0:53]}'")  # 'presentation'まで
print(f"0-55: '{text[0:55]}'")  # 'presentation,'まで
print(f"0-61: '{text[0:61]}'")  # 'presentation, the 'まで

print(f"\n正解: 'that afternoon at the crucial point in the presentation'")
print(f"位置53まで切り出し: '{text[0:53]}'")
print(f"位置53まで一致: {text[0:53].lower() == 'that afternoon at the crucial point in the presentation'}")
