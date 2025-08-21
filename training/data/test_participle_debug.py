#!/usr/bin/env python3
"""
ParticiplePattern デバッグ用シンプルテスト
"""

import sys
import os
import stanza

# プロジェクトルートをパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(project_root, 'training', 'data'))

from universal_slot_system.patterns.participle_pattern import ParticiplePattern

# Stanza初期化
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', use_gpu=False)

# ParticiplePattern初期化
participle_pattern = ParticiplePattern()

# テスト文
test_sentence = "The man working overtime is tired"
print(f"テスト文: {test_sentence}")

# Stanza解析
doc = nlp(test_sentence)

# 分詞検出テスト
result = participle_pattern.detect(doc, test_sentence)
print(f"分詞検出結果: {result}")

# トークン詳細表示
print("\nトークン詳細:")
for i, word in enumerate(doc.sentences[0].words):
    print(f"  {i}: '{word.text}' upos={word.upos} feats={word.feats}")
