#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
複数修飾語の検出問題をデバッグ
"""

from adverb_handler import AdverbHandler

# 問題の簡略文
test_text = "The student always succeeds academically ."

print(f"🔧 複数修飾語検出テスト: '{test_text}'")
print("=" * 60)

# 副詞ハンドラーで処理
adverb_handler = AdverbHandler()
result = adverb_handler.process(test_text)

print(f"📊 副詞ハンドラー結果:")
print(f"   成功: {result['success']}")
print(f"   分離文: '{result.get('separated_text', '')}'")
print(f"   修飾語: {result.get('modifiers', {})}")
print(f"   スロット: {result.get('modifier_slots', {})}")

# spaCy解析を確認
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_text)

print(f"\n📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, DEP: {token.dep_}, HEAD: {token.head.text})")

# 期待される結果
print(f"\n🎯 期待される結果:")
print(f"   分離文: 'The student succeeds .'")
print(f"   修飾語スロット: {{'M2': 'always', 'M3': 'academically'}}")

# 手動で修飾語を確認
print(f"\n🔍 修飾語の手動確認:")
for i, token in enumerate(doc):
    if token.pos_ == 'ADV':
        print(f"   {token.text} (位置{i}) -> HEAD: {token.head.text} (位置{token.head.i})")
