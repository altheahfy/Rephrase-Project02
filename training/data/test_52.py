#!/usr/bin/env python3
import sys
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログ設定
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')

# Test 52の文
sentence = "The documents being reviewed thoroughly will be approved soon."

# マッパー初期化
mapper = UnifiedStanzaRephraseMapper()

# 処理実行
result = mapper.process(sentence)

print("=" * 60)
print("Test 52結果:")
print(f"文: {sentence}")
print(f"実際の出力: {result}")
print("=" * 60)
