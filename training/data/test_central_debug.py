#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

# CentralController初期化
controller = CentralController()

# テスト文
text = "He seems to have finished his work."

print(f"🔍 CentralController分析テスト: '{text}'")
print("=" * 60)

# 1. 文法パターン検出
patterns = controller.analyze_grammar_structure(text)
print(f"📊 検出された文法パターン: {patterns}")

# 2. 実際の処理
result = controller.process_sentence(text)
print(f"📊 処理結果: {result}")
