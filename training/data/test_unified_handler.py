#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# テスト文
sentence = 'The doctor who works carefully saves lives successfully'
print(f'🧪 テスト文: {sentence}')

# 統合ハンドラーでテスト
mapper = UnifiedStanzaRephraseMapper()
result = mapper.process(sentence)

print(f'🔍 統合ハンドラー結果:')
print(f'  slots: {result.get("slots", {})}')
print(f'  sub_slots: {result.get("sub_slots", {})}')
print(f'  grammar_info: {result.get("grammar_info", {})}')
print(f'  detected_patterns: {result.get("grammar_info", {}).get("detected_patterns", [])}')

# メタ情報
meta = result.get('meta', {})
print(f'\n🔍 メタ情報:')
print(f'  active_handlers: {meta.get("active_handlers", 0)}')
print(f'  processing_time: {meta.get("processing_time", 0)}秒')
