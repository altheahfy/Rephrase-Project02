#!/usr/bin/env python3
"""副詞ハンドラーが実行されているか確認"""

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# Case 37で詳細デバッグ
sentence = "The window was gently opened by the morning breeze."

print(f'🔍 副詞ハンドラー実行確認: {sentence}')
print('=' * 60)

# ログレベルをDEBUGに設定
mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')

# 副詞ハンドラーが実際に呼び出されているか確認
print('アクティブハンドラー:', mapper.list_active_handlers())

# 個別ハンドラーテスト
print('\n🧪 個別ハンドラーテスト:')
doc = mapper.nlp(sentence)
main_sentence = doc.sentences[0]

# 副詞ハンドラーを直接呼び出し
print('副詞ハンドラー直接実行:')
adverb_result = mapper._handle_adverbial_modifier(main_sentence, {'slots': {}, 'sub_slots': {}})
print('副詞ハンドラー結果:', adverb_result)

print('\n🔧 統合処理実行:')
result = mapper.process(sentence)
print('統合処理結果:')
slots = result.get('slots', {})
print('Main M-slots:')
for slot in ['M1', 'M2', 'M3']:
    value = slots.get(slot, '')
    if value:
        print(f'  {slot}: "{value}"')
