#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ケース34のalways検出問題をデバッグ
"""

from adverb_handler import AdverbHandler

# 問題の簡略文をテスト
test_text = "The student succeeds academically ."

print(f"🔧 簡略文での副詞検出テスト: '{test_text}'")
print("=" * 60)

# 副詞ハンドラーで処理
adverb_handler = AdverbHandler()
result = adverb_handler.process(test_text)

print(f"📊 副詞ハンドラー結果:")
print(f"   成功: {result['success']}")
print(f"   分離文: '{result.get('separated_text', '')}'")
print(f"   修飾語: {result.get('modifiers', {})}")
print(f"   スロット: {result.get('modifier_slots', {})}")

# spaCy解析を直接確認
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_text)

print(f"\n📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, DEP: {token.dep_})")

# alwaysが元文のどこにあるかを確認
original = "The student who studies diligently always succeeds academically."
print(f"\n🔍 元の文: '{original}'")
doc_orig = nlp(original)
for i, token in enumerate(doc_orig):
    if token.text.lower() == 'always':
        print(f"   always位置: {i} (POS: {token.pos_}, DEP: {token.dep_})")
        print(f"   前後: '{doc_orig[i-1].text}' -> 'always' -> '{doc_orig[i+1].text}'")
