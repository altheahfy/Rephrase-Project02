#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# テスト用の設定
mapper = UnifiedStanzaRephraseMapper()

# テスト文
test_sentence = "The man whose car is red lives here."

print(f"テスト文: {test_sentence}")
print("="*50)

# 処理実行
result = mapper.process(test_sentence)

print("\n" + "="*50)
print("最終結果:")
print(f"S: '{result['S']}'")
print(f"V: '{result['V']}'")
print(f"C1: '{result.get('C1', '')}'")
print(f"C2: '{result.get('C2', '')}'")
print(f"M2: '{result.get('M2', '')}'")
