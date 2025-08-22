#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# デバッグ用のカスタム実装
test_sentence = 'The car is red.'

try:
    mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')
    result = mapper.process(test_sentence)
    
    print('=== デバッグ結果 ===')
    print('文:', test_sentence)
    print('')
    
    print('🔹 result構造:')
    for key in result.keys():
        print(f'  {key}: {type(result[key])}')
    
    print('')
    print('🔹 スロット詳細:')
    if 'slots' in result:
        for slot, value in result['slots'].items():
            if value:
                print(f'  {slot}: "{value}"')
    
    print('')
    print('🔹 rephrase_slots存在チェック:')
    print(f'  存在するか: {"rephrase_slots" in result}')
    if 'rephrase_slots' in result:
        print(f'  エントリ数: {len(result["rephrase_slots"])}')
        for i, entry in enumerate(result['rephrase_slots']):
            print(f'    [{i+1}] {entry["Slot"]}: "{entry["SlotPhrase"]}" (pos: {entry["Slot_display_order"]})')
    
    print('')
    print('🔹 grammar_info.human_corrections:')
    if 'grammar_info' in result and 'human_corrections' in result['grammar_info']:
        for correction in result['grammar_info']['human_corrections']:
            print(f'  タイプ: {correction.get("type")}')
            print(f'  パターン: {correction.get("pattern_type")}')
            print(f'  確信度: {correction.get("confidence")}')
            
except Exception as e:
    print(f'エラー: {e}')
    import traceback
    traceback.print_exc()
