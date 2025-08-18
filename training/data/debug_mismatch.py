#!/usr/bin/env python3
"""修正済み正解データと実際の結果を比較"""

import json
import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# 修正済み正解データを確認
with open('batch_results_complete.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

results = test_data.get('results', {})

# 問題のケースの正解データを確認
problem_cases = ['32', '37', '38']

print('🔍 修正済み正解データ vs 実際の結果')
print('=' * 60)

mapper = UnifiedStanzaRephraseMapper()

for case_id in problem_cases:
    if case_id in results:
        case_data = results[case_id]
        sentence = case_data.get('sentence', case_id)
        expected_main = case_data.get('expected', {}).get('main_slots', {})
        expected_sub = case_data.get('expected', {}).get('sub_slots', {})
        
        print(f'\nCase {case_id}: {sentence}')
        print('  📝 修正済み正解データ:')
        print('    Main M-slots:')
        for slot in ['M1', 'M2', 'M3']:
            value = expected_main.get(slot, '')
            if value:
                print(f'      {slot}: "{value}"')
        print('    Sub M-slots:')
        for slot in ['sub-m1', 'sub-m2', 'sub-m3']:
            value = expected_sub.get(slot, '')
            if value:
                print(f'      {slot}: "{value}"')
        
        # 実際の処理結果
        result = mapper.process(sentence)
        actual_slots = result.get('slots', {})
        actual_sub_slots = result.get('sub_slots', {})
        
        print('  🤖 実際の処理結果:')
        print('    Main M-slots:')
        for slot in ['M1', 'M2', 'M3']:
            value = actual_slots.get(slot, '')
            if value:
                print(f'      {slot}: "{value}"')
        print('    Sub M-slots:')
        for slot in ['sub-m1', 'sub-m2', 'sub-m3']:
            value = actual_sub_slots.get(slot, '')
            if value:
                print(f'      {slot}: "{value}"')
        
        # 不一致を確認
        print('  ❗ 不一致点:')
        mismatches = []
        for slot in ['M1', 'M2', 'M3']:
            expected = expected_main.get(slot, '')
            actual = actual_slots.get(slot, '')
            if str(expected) != str(actual):
                mismatches.append(f'Main:{slot}: "{actual}" ≠ "{expected}"')
        
        for slot in ['sub-m1', 'sub-m2', 'sub-m3']:
            expected = expected_sub.get(slot, '')
            actual = actual_sub_slots.get(slot, '')
            if str(expected) != str(actual):
                mismatches.append(f'Sub:{slot}: "{actual}" ≠ "{expected}"')
        
        if mismatches:
            for mismatch in mismatches:
                print(f'    {mismatch}')
        else:
            print('    ✅ 完全一致')
