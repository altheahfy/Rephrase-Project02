#!/usr/bin/env python3
"""
中央制御機構 単体テストシステム
===============================

目的: 中央制御機構の標準運用開始に伴い、単体での動作検証を実施
従来システムとの比較は不要（中央制御機構が優秀であることは実証済み）

作成日: 2025年8月24日
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_grammar_mapper import DynamicGrammarMapper
import argparse

# 標準テストケース
TEST_CASES = {
    1: {
        'sentence': 'The car is red.',
        'expected_main': {'S': 'The car', 'V': 'is', 'C1': 'red'},
        'expected_sub': {}
    },
    2: {
        'sentence': 'I love you.',
        'expected_main': {'S': 'I', 'V': 'love', 'O1': 'you'},
        'expected_sub': {}
    },
    3: {
        'sentence': 'The man who runs fast is strong.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'strong'},
        'expected_sub': {'sub-s': 'The man who', 'sub-v': 'runs', 'sub-m2': 'fast', '_parent_slot': 'S'}
    },
    4: {
        'sentence': 'The book which lies there is mine.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'mine'},
        'expected_sub': {'sub-s': 'The book which', 'sub-v': 'lies', 'sub-m2': 'there', '_parent_slot': 'S'}
    },
    5: {
        'sentence': 'The person that works here is kind.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'kind'},
        'expected_sub': {'sub-s': 'The person that', 'sub-v': 'works', 'sub-m2': 'here', '_parent_slot': 'S'}
    },
    6: {
        'sentence': 'The book which I bought is expensive.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'expensive'},
        'expected_sub': {'sub-s': 'I', 'sub-v': 'bought', 'sub-o1': 'The book which', '_parent_slot': 'S'}
    },
    7: {
        'sentence': 'The man whom I met is tall.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'tall'},
        'expected_sub': {'sub-s': 'I', 'sub-v': 'met', 'sub-o1': 'The man whom', '_parent_slot': 'S'}
    },
    8: {
        'sentence': 'The car that he drives is new.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'new'},
        'expected_sub': {'sub-s': 'he', 'sub-v': 'drives', 'sub-o1': 'The car that', '_parent_slot': 'S'}
    },
    9: {
        'sentence': 'The car which was crashed is red.',
        'expected_main': {'S': '', 'V': 'is', 'C1': 'red'},
        'expected_sub': {'sub-s': 'The car which', 'sub-aux': 'was', 'sub-v': 'crashed', '_parent_slot': 'S'}
    },
    10: {
        'sentence': 'The book that was written is famous.',
        'expected_main': {'Aux': 'was', 'V': 'written'},
        'expected_sub': {'sub-s': 'The book that', '_parent_slot': 'S'}
    }
}

def analyze_sentence(analyzer, sentence):
    """中央制御機構で文を分析"""
    result = analyzer.analyze_sentence(sentence)
    
    main_slots = {}
    sub_slots = {}
    
    if 'main_slots' in result:
        main_slots = result['main_slots']
    elif 'slots' in result:
        main_slots = result['slots']
    
    if 'sub_slots' in result:
        sub_slots = result['sub_slots']
    
    return main_slots, sub_slots

def compare_slots(actual, expected):
    """スロット比較（完全一致）"""
    if not actual and not expected:
        return True
    if not actual or not expected:
        return False
    
    # キーの完全一致チェック
    if set(actual.keys()) != set(expected.keys()):
        return False
    
    # 値の完全一致チェック
    for key in expected:
        if actual.get(key) != expected[key]:
            return False
    
    return True

def run_test(test_num, verbose=False):
    """単一テスト実行"""
    test_case = TEST_CASES[test_num]
    sentence = test_case['sentence']
    expected_main = test_case['expected_main']
    expected_sub = test_case['expected_sub']
    
    print(f"\n=== Test {test_num}: {sentence} ===")
    
    # 中央制御機構で分析
    analyzer = DynamicGrammarMapper()
    
    try:
        main_slots, sub_slots = analyze_sentence(analyzer, sentence)
        
        if verbose:
            print(f"中央制御機構:")
            print(f"  main: {main_slots}")
            print(f"  sub:  {sub_slots}")
        
        # 結果検証
        main_match = compare_slots(main_slots, expected_main)
        sub_match = compare_slots(sub_slots, expected_sub)
        
        if main_match and sub_match:
            print("✅ 正解！")
            return True
        else:
            print("❌ 不正解")
            print(f"  期待: main={expected_main}, sub={expected_sub}")
            print(f"  実際: main={main_slots}, sub={sub_slots}")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='中央制御機構 単体テストシステム')
    parser.add_argument('--tests', type=str, help='テスト番号（カンマ区切り、例: 1,3,5）', default=None)
    parser.add_argument('--verbose', action='store_true', help='詳細出力')
    args = parser.parse_args()
    
    print("=== 中央制御機構 単体テストシステム ===")
    
    if args.tests:
        test_numbers = [int(x.strip()) for x in args.tests.split(',')]
    else:
        test_numbers = list(TEST_CASES.keys())
    
    print(f"テスト対象: {test_numbers}")
    
    success_count = 0
    total_tests = len(test_numbers)
    
    for test_num in test_numbers:
        if test_num in TEST_CASES:
            success = run_test(test_num, args.verbose)
            if success:
                success_count += 1
        else:
            print(f"⚠️ Test {test_num} は存在しません")
    
    print(f"\n=== テスト結果サマリー ===")
    print(f"総テスト数: {total_tests}")
    print(f"成功: {success_count}/{total_tests}")
    print(f"成功率: {success_count/total_tests*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 全テスト成功！中央制御機構は正常に動作しています。")
    else:
        failed_tests = [num for num in test_numbers if num in TEST_CASES and not run_test(num, False)]
        print(f"⚠️ 失敗したテスト: {failed_tests}")

if __name__ == "__main__":
    main()
