#!/usr/bin/env python3
"""否定形助動詞のトークナイゼーション確認テスト"""

import spacy

# spaCy初期化
nlp = spacy.load('en_core_web_sm')

# テスト文
test_sentence = "Don't touch that button!"

print(f"📝 テスト文: {test_sentence}")
print()

# spaCy処理
doc = nlp(test_sentence)

print("🔍 spaCyトークン分析:")
for i, token in enumerate(doc):
    print(f"  {i}: '{token.text}' - POS: {token.pos_} - TAG: {token.tag_} - DEP: {token.dep_}")

print()
print("🔍 直接比較テスト:")
dont_word = "don't"
for token in doc:
    token_lower = token.text.lower()
    print(f"  Token: '{token.text}' -> lower: '{token_lower}'")
    print(f"    don't: {token_lower == dont_word}")
    print(f"    do: {token_lower == 'do'}")
    print()
