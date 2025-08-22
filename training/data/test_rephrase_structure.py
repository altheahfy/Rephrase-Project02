#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# 完全Rephrase準拠構造テスト
test_sentence = 'The car is red.'

mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')
result = mapper.process(test_sentence)

print('=== 完全Rephrase準拠構造 テスト ===')
print('文:', test_sentence)
print('')

print('🔹 従来互換スロット:')
for slot, value in result.get('slots', {}).items():
    if value:
        print('  ' + slot + ':', repr(value))

print('')
print('🔹 完全Rephrase準拠構造:')
if 'rephrase_slots' in result:
    print(f'  rephrase_slots found: {len(result["rephrase_slots"])} entries')
    for i, slot_entry in enumerate(result['rephrase_slots']):
        print(f'  [{i+1}] Slot: {slot_entry["Slot"]}, Text: "{slot_entry["SlotPhrase"]}", Position: {slot_entry["Slot_display_order"]}')
else:
    print('  rephrase_slots not found')

print('')
print('🔹 スロット名修正確認:')
print('  C1スロットが存在するか:', 'C1' in result.get('slots', {}))
print('  旧Cスロットが存在するか:', 'C' in result.get('slots', {}))
