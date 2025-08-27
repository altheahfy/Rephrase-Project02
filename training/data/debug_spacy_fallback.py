#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spaCy誤判定対処法のデバッグ：ケース12
設計仕様書の例2に基づく分析
"""

import spacy
from central_controller import CentralController

# 問題のケース
test_case = "The man whose car is red lives here."

print(f"🔧 spaCy誤判定デバッグ: {test_case}")
print("=" * 60)

# Step 1: spaCy解析を詳細確認
nlp = spacy.load('en_core_web_sm')
doc = nlp(test_case)

print("📊 spaCy解析結果:")
for i, token in enumerate(doc):
    print(f"  {i}: {token.text} (POS: {token.pos_}, TAG: {token.tag_}, DEP: {token.dep_}, HEAD: {token.head.text})")

# Step 2: livesの品詞判定確認
lives_token = None
for token in doc:
    if token.text.lower() == 'lives':
        lives_token = token
        break

if lives_token:
    print(f"\n🎯 'lives'の判定:")
    print(f"  POS: {lives_token.pos_} (期待: VERB)")
    print(f"  TAG: {lives_token.tag_} (期待: VBZ)")
    print(f"  DEP: {lives_token.dep_} (期待: ROOT)")
    
    if lives_token.pos_ != 'VERB':
        print(f"  ❌ spaCy誤判定検出: livesを{lives_token.pos_}として判定")
    else:
        print(f"  ✅ spaCy正しい判定: livesをVERBとして判定")

# Step 3: hereの品詞判定確認
here_token = None
for token in doc:
    if token.text.lower() == 'here':
        here_token = token
        break

if here_token:
    print(f"\n🎯 'here'の判定:")
    print(f"  POS: {here_token.pos_} (期待: ADV)")
    print(f"  TAG: {here_token.tag_}")
    print(f"  DEP: {here_token.dep_}")
    print(f"  HEAD: {here_token.head.text}")

# Step 4: 中央管理システムの実際の処理結果
print("\n" + "="*60)
print("🔧 中央管理システム処理結果:")
controller = CentralController()
result = controller.process(test_case)
print(f"📊 結果: {result}")

# Step 5: 設計仕様書の対処法適用提案
print("\n" + "="*60)
print("🎯 設計仕様書対処法適用:")
print("1. システム警戒: spaCy誤判定を検出")
print("2. 複数候補準備: lives_名詞 vs lives_動詞")
print("3. 文法破綻チェック: 上位スロットの整合性検証")
print("4. 最適候補選択: 文法的に成立する候補を採用")
