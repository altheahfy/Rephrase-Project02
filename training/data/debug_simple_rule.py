#!/usr/bin/env python3
"""副詞ハンドラーのデバッグ - シンプルルールが呼び出されているか確認"""

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# Case 37で詳細デバッグ
sentence = "The window was gently opened by the morning breeze."

print(f'🔍 副詞ハンドラー詳細デバッグ: {sentence}')
print('=' * 60)

mapper = UnifiedStanzaRephraseMapper()
result = mapper.process(sentence)

print('\n実際の結果:')
slots = result.get('slots', {})
sub_slots = result.get('sub_slots', {})

print('Main M-slots:')
for slot in ['M1', 'M2', 'M3']:
    value = slots.get(slot, '')
    if value:
        print(f'  {slot}: "{value}"')

print('期待値: M2="gently", M3="by the morning breeze" (2個ルール)')
print()
print('問題: まだM1/M2配置になっている → シンプルルール一括処理が機能していない可能性')
