#!/usr/bin/env python3
"""final_54_test_data.jsonのM配置問題4ケース確認"""

import json

# 正しい正解データを読み込み
with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

results = test_data.get('data', {})

# 問題のあった4ケースを確認
problem_cases = ['32', '34', '37', '38']

print('🔍 final_54_test_data.json の M配置問題4ケース確認')
print('=' * 70)

for case_id in problem_cases:
    if case_id in results:
        case_data = results[case_id]
        sentence = case_data.get('sentence', case_id)
        expected_main = case_data.get('expected', {}).get('main_slots', {})
        expected_sub = case_data.get('expected', {}).get('sub_slots', {})
        
        print(f'\n📝 Case {case_id}: {sentence}')
        print('   正解Main M-slots:')
        for slot in ['M1', 'M2', 'M3']:
            value = expected_main.get(slot, '')
            print(f'     {slot}: "{value}"')
        
        print('   正解Sub M-slots:')
        for slot in ['sub-m1', 'sub-m2', 'sub-m3']:
            value = expected_sub.get(slot, '')
            if value:
                print(f'     {slot}: "{value}"')
        
        # 修飾語分析
        print('   🔍 修飾語分析:')
        if case_id == '32':
            print('     候補: "quickly", "yesterday", "smoothly" (3個)')
            print('     個数+位置ルール期待値: M1=quickly, M2=yesterday, M3=smoothly')
        elif case_id == '34':
            print('     候補: "diligently", "always", "academically" (3個)')
            print('     個数+位置ルール期待値: M1=diligently, M2=always, M3=academically')
        elif case_id == '37':
            print('     候補: "gently", "by the morning breeze" (2個)')
            print('     個数+位置ルール期待値: M1=gently, M3=by the morning breeze')
        elif case_id == '38':
            print('     候補: "carefully", "by the manager" (2個)')
            print('     個数+位置ルール期待値: M1=carefully, M3=by the manager')
    else:
        print(f'\nCase {case_id}: Not found')
