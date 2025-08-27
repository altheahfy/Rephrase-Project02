#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関係節ハンドラーのmain_continuation問題をデバッグ
"""

import json
from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
from basic_five_pattern_handler import BasicFivePatternHandler

# 問題のケースを詳細分析
test_case = {
    "text": "The book which lies there is mine.",
    "expected_main": "is mine"
}

# ハンドラーの初期化
adverb_handler = AdverbHandler()
five_pattern_handler = BasicFivePatternHandler()

collaborators = {
    'adverb': adverb_handler,
    'five_pattern': five_pattern_handler
}

rel_handler = RelativeClauseHandler(collaborators)

print(f"🔧 main_continuation デバッグ: {test_case['text']}")
print("=" * 60)

# Step 1: spaCy解析を直接確認
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_case['text'])

print("\n📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, DEP: {token.dep_}, HEAD: {token.head.text})")

# ROOT動詞を特定
root_idx = None
for i, token in enumerate(doc):
    if token.dep_ == 'ROOT':
        root_idx = i
        print(f"\n🎯 ROOT動詞: {i}: {token.text}")
        break

# which位置を特定
which_idx = None
for i, token in enumerate(doc):
    if token.text.lower() == 'which':
        which_idx = i
        print(f"🔍 which位置: {i}: {token.text}")
        break

# 関係節範囲を予想
if which_idx is not None and root_idx is not None:
    print(f"\n📍 関係節範囲予想: {which_idx}～{root_idx-1}")
    if root_idx < len(doc):
        main_tokens = [token.text for token in doc[root_idx:]]
        expected_main = " ".join(main_tokens)
        print(f"🎯 期待されるmain_continuation: '{expected_main}'")

# Step 2: 関係節ハンドラーの実際の結果
print("\n" + "="*60)
print("🔧 関係節ハンドラー実行結果:")
result = rel_handler.process(test_case['text'])
print(f"📊 結果: {json.dumps(result, indent=2, ensure_ascii=False)}")

if result.get('main_continuation'):
    print(f"✅ main_continuation: '{result['main_continuation']}'")
else:
    print(f"❌ main_continuation が空またはなし")
