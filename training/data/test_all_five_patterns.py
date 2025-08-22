#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# 全5文型のテストケース
test_cases = [
    {'sentence': 'The car is red.', 'expected': 'SVC', 'description': '第3文型 SVC'},
    {'sentence': 'I love you.', 'expected': 'SVO', 'description': '第3文型 SVO'}, 
    {'sentence': 'He runs.', 'expected': 'SV', 'description': '第1文型 SV'},
    {'sentence': 'I gave him a book.', 'expected': 'SVOO', 'description': '第4文型 SVOO'},
    {'sentence': 'We made him happy.', 'expected': 'SVOC', 'description': '第5文型 SVOC'}
]

mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')

print('=== 全5文型認識テスト ===')
print('')

for i, test_case in enumerate(test_cases, 1):
    sentence = test_case['sentence']
    expected = test_case['expected']
    description = test_case['description']
    
    print(f'【テスト {i}】{description}')
    print(f'文: "{sentence}"')
    
    try:
        result = mapper.process(sentence)
        
        # 認識された文型を確認
        detected_pattern = None
        if 'grammar_info' in result and 'human_corrections' in result['grammar_info']:
            for correction in result['grammar_info']['human_corrections']:
                if correction.get('type') == 'basic_five_pattern':
                    detected_pattern = correction.get('pattern_type')
                    break
        
        # スロット結果
        slots = result.get('slots', {})
        rephrase_slots = result.get('rephrase_slots', [])
        
        print(f'認識パターン: {detected_pattern or "未認識"} (期待: {expected})')
        print(f'認識成功: {"✅" if detected_pattern == expected else "❌"}')
        
        if slots:
            print('スロット:')
            for slot, value in slots.items():
                if value:
                    print(f'  {slot}: "{value}"')
        
        if rephrase_slots:
            print('Rephrase構造:')
            for entry in rephrase_slots:
                print(f'  {entry["Slot"]}: "{entry["SlotPhrase"]}" (pos: {entry["Slot_display_order"]})')
        
        print('')
        
    except Exception as e:
        print(f'❌ エラー: {e}')
        print('')

print('=== テスト完了 ===')
