#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節ハンドラーのmain_continuation作成をデバッグ
"""

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
from basic_five_pattern_handler import BasicFivePatternHandler

# 問題のケース
test_case = "The student who studies diligently always succeeds academically."

print(f"🔧 関係節ハンドラーmain_continuation作成デバッグ")
print(f"📝 元の文: '{test_case}'")
print("=" * 80)

# 協力者を設定
adverb_handler = AdverbHandler()
five_pattern_handler = BasicFivePatternHandler()
collaborators = {
    'adverb': adverb_handler,
    'five_pattern': five_pattern_handler
}

# 関係節ハンドラーを初期化
rel_handler = RelativeClauseHandler(collaborators)

# 処理実行
result = rel_handler.process(test_case)

print(f"📊 関係節ハンドラー結果:")
print(f"   成功: {result['success']}")
print(f"   先行詞: '{result.get('antecedent', '')}'")
print(f"   主節継続: '{result.get('main_continuation', '')}'")
print(f"   サブスロット: {result.get('sub_slots', {})}")

# 期待される主節継続
expected_main = "always succeeds academically ."
print(f"\n🎯 期待される主節継続: '{expected_main}'")

# spaCy解析を直接確認
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_case)

print(f"\n📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, DEP: {token.dep_}, HEAD: {token.head.text})")

# ROOT動詞位置の確認
root_idx = None
for i, token in enumerate(doc):
    if token.dep_ == 'ROOT':
        root_idx = i
        print(f"\n🎯 ROOT動詞: {i}: {token.text}")
        break

if root_idx:
    main_tokens = [token.text for token in doc[root_idx:]]
    actual_main = " ".join(main_tokens)
    print(f"🔍 ROOT以降のトークン: '{actual_main}'")
