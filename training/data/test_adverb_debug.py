#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdverbHandler詳細テスト
"""

from adverb_handler import AdverbHandler
import spacy

# テスト文
test_sentence = "We would visit Paris every summer."

# AdverbHandlerテスト
print("=== AdverbHandler詳細テスト ===")
handler = AdverbHandler()
result = handler.process(test_sentence)

print(f'Success: {result["success"]}')
if result['success']:
    print(f'Separated text: "{result["separated_text"]}"')
    print(f'Modifiers: {result["modifiers"]}')
    print(f'Modifier slots: {result["modifier_slots"]}')
else:
    print(f'Error: {result["error"]}')

# spaCy詳細分析
print("\n=== spaCy詳細分析 ===")
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_sentence)

for i, token in enumerate(doc):
    print(f"{i}: '{token.text}' - POS: {token.pos_}, TAG: {token.tag_}, DEP: {token.dep_}, HEAD: {token.head.text}")

# 修飾語候補の検出
print("\n=== 修飾語候補の検出 ===")
for token in doc:
    if token.pos_ == 'ADV':
        print(f"副詞検出: {token.text}")
    elif token.pos_ == 'NOUN' and token.dep_ in ['npadvmod', 'tmod']:
        print(f"名詞的副詞検出: {token.text} (dep: {token.dep_})")
    elif token.text.lower() in ['every', 'summer']:
        print(f"キーワード検出: {token.text} - POS: {token.pos_}, DEP: {token.dep_}")

# 動詞修飾語の詳細チェック
print("\n=== 動詞修飾語の詳細チェック ===")
verb_idx = None
for i, token in enumerate(doc):
    if token.pos_ == 'VERB':
        verb_idx = i
        print(f"動詞発見: {token.text} (index: {i})")
        break

if verb_idx is not None:
    print(f"\n動詞後の解析 (index {verb_idx+1} から):")
    i = verb_idx + 1
    while i < len(doc):
        token = doc[i]
        print(f"  {i}: '{token.text}' - POS: {token.pos_}, DEP: {token.dep_}")
        
        # 時間表現チェック
        if token.text.lower() in ['every', 'each', 'last', 'next', 'this', 'that'] and i + 1 < len(doc):
            next_token = doc[i + 1]
            time_nouns = ['day', 'week', 'month', 'year', 'morning', 'afternoon', 'evening', 'night', 'time', 'moment', 'summer']
            print(f"    時間表現候補: '{token.text} {next_token.text}' - next_token in time_nouns: {next_token.text.lower() in time_nouns}")
        
        i += 1
