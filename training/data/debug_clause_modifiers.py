#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節内修飾語の処理問題をデバッグ
"""

from adverb_handler import AdverbHandler
import spacy

# 問題の例文
test_case = "The book which was carefully written by Shakespeare is famous."

print(f"🔧 関係節内修飾語デバッグ: {test_case}")
print("=" * 70)

# Step 1: 副詞ハンドラーの直接処理
adverb_handler = AdverbHandler()
result = adverb_handler.process(test_case)

print(f"\n📍 副詞ハンドラー結果:")
print(f"   分離後テキスト: '{result['separated_text']}'")
print(f"   修飾語スロット: {result['modifier_slots']}")

# Step 2: spaCy解析で構造確認
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_case)

print(f"\n📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, DEP: {token.dep_}, HEAD: {token.head.text})")

# Step 3: 関係節境界の確認
print(f"\n🔍 関係節境界分析:")
which_idx = None
main_verb_idx = None

for i, token in enumerate(doc):
    if token.text.lower() == 'which':
        which_idx = i
        print(f"   which位置: {i}")
    if token.dep_ == 'ROOT':
        main_verb_idx = i
        print(f"   主節動詞: {i}: {token.text}")

if which_idx is not None and main_verb_idx is not None:
    print(f"   関係節範囲: {which_idx} - {main_verb_idx-1}")
    print(f"   主節範囲: {main_verb_idx} - {len(doc)-1}")
    
    # 関係節内の修飾語
    rel_modifiers = []
    main_modifiers = []
    
    for i, token in enumerate(doc):
        if token.pos_ in ['ADV'] or (token.pos_ == 'ADP' and token.text in ['by']):
            if which_idx <= i < main_verb_idx:
                rel_modifiers.append(f"{i}: {token.text}")
            else:
                main_modifiers.append(f"{i}: {token.text}")
    
    print(f"   関係節内修飾語: {rel_modifiers}")
    print(f"   主節修飾語: {main_modifiers}")
