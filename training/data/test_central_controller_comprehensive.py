#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央制御機構包括的テスト用スクリプト
全テストケースでの中央制御機構の効果を確認
"""

import json
import argparse
from dynamic_grammar_mapper import DynamicGrammarMapper

# 全テストケース定義
TEST_CASES = {
    1: {
        "sentence": "The car is red.",
        "type": "basic_five_pattern",
        "expected_main": {'S': 'The car', 'V': 'is', 'C1': 'red'},
        "expected_sub": {}
    },
    2: {
        "sentence": "I love you.",
        "type": "basic_five_pattern", 
        "expected_main": {'S': 'I', 'V': 'love', 'O1': 'you'},
        "expected_sub": {}
    },
    3: {
        "sentence": "The man who runs fast is strong.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'strong'},
        "expected_sub": {'sub-s': 'The man who', 'sub-v': 'runs', 'sub-m2': 'fast', '_parent_slot': 'S'}
    },
    4: {
        "sentence": "The book which lies there is mine.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'mine'},
        "expected_sub": {'sub-s': 'The book which', 'sub-v': 'lies', 'sub-m2': 'there', '_parent_slot': 'S'}
    },
    5: {
        "sentence": "The person that works here is kind.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'kind'},
        "expected_sub": {'sub-s': 'The person that', 'sub-v': 'works', 'sub-m2': 'here', '_parent_slot': 'S'}
    },
    6: {
        "sentence": "The book which I bought is expensive.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'expensive'},
        "expected_sub": {'sub-o1': 'The book which', 'sub-s': 'I', 'sub-v': 'bought', '_parent_slot': 'S'}
    },
    7: {
        "sentence": "The man whom I met is tall.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'tall'},
        "expected_sub": {'sub-o1': 'The man whom', 'sub-s': 'I', 'sub-v': 'met', '_parent_slot': 'S'}
    },
    8: {
        "sentence": "The car that he drives is new.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'new'},
        "expected_sub": {'sub-o1': 'The car that', 'sub-s': 'he', 'sub-v': 'drives', '_parent_slot': 'S'}
    },
    9: {
        "sentence": "The car which was crashed is red.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'red'},
        "expected_sub": {'sub-s': 'The car which', 'sub-aux': 'was', 'sub-v': 'crashed', '_parent_slot': 'S'}
    },
    10: {
        "sentence": "The book that was written is famous.",
        "type": "relative_clause",
        "expected_main": {'S': '', 'V': 'is', 'C1': 'famous'},
        "expected_sub": {'sub-s': 'The book that', 'sub-aux': 'was', 'sub-v': 'written', '_parent_slot': 'S'}
    }
}

def compare_slots(actual, expected, slot_type="main"):
    """スロット比較（順序に関係なく）"""
    if not actual and not expected:
        return True
    
    if not actual or not expected:
        return False
    
    # キーと値の完全一致確認
    return actual == expected

def test_single_case(test_id, case_data, verbose=False):
    """単一テストケースの実行"""
    sentence = case_data["sentence"]
    expected_main = case_data["expected_main"]
    expected_sub = case_data["expected_sub"]
    
    if verbose:
        print(f"\n=== Test {test_id}: {sentence} ===")
    
    # 1. 従来システムでのテスト
    mapper_legacy = DynamicGrammarMapper()
    result_legacy = mapper_legacy.analyze_sentence(sentence)
    
    main_legacy = result_legacy.get('main_slots', {})
    sub_legacy = result_legacy.get('sub_slots', {})
    
    main_match_legacy = compare_slots(main_legacy, expected_main, "main")
    sub_match_legacy = compare_slots(sub_legacy, expected_sub, "sub")
    
    if verbose:
        print(f"従来システム:")
        print(f"  main: {main_legacy}")
        print(f"  sub:  {sub_legacy}")
        print(f"  正解: main={main_match_legacy}, sub={sub_match_legacy}")
    
    # 2. 中央制御機構でのテスト
    mapper_central = DynamicGrammarMapper()
    success = mapper_central.enable_central_controller()
    
    if not success:
        if verbose:
            print("❌ 中央制御機構の有効化に失敗")
        return {
            'test_id': test_id,
            'sentence': sentence,
            'legacy_success': main_match_legacy and sub_match_legacy,
            'central_success': False,
            'central_enabled': False
        }
    
    result_central = mapper_central.analyze_sentence(sentence)
    main_central = result_central.get('main_slots', {})
    sub_central = result_central.get('sub_slots', {})
    
    main_match_central = compare_slots(main_central, expected_main, "main")
    sub_match_central = compare_slots(sub_central, expected_sub, "sub")
    
    if verbose:
        print(f"中央制御機構:")
        print(f"  main: {main_central}")
        print(f"  sub:  {sub_central}")
        print(f"  正解: main={main_match_central}, sub={sub_match_central}")
        
        # 結果判定
        if main_match_central and sub_match_central:
            print("🎉 中央制御機構で正解！")
        elif main_match_legacy and sub_match_legacy:
            print("⚠️ 従来システムでも正解")
        else:
            print("❌ 両システムとも不正解")
    
    return {
        'test_id': test_id,
        'sentence': sentence,
        'expected_main': expected_main,
        'expected_sub': expected_sub,
        'legacy_main': main_legacy,
        'legacy_sub': sub_legacy,
        'central_main': main_central,
        'central_sub': sub_central,
        'legacy_success': main_match_legacy and sub_match_legacy,
        'central_success': main_match_central and sub_match_central,
        'central_enabled': True
    }

def test_comprehensive(test_ids=None, verbose=False):
    """包括的テスト実行"""
    if test_ids is None:
        test_ids = list(TEST_CASES.keys())
    
    results = []
    
    print(f"=== 中央制御機構包括的テスト ===")
    print(f"テスト対象: {test_ids}")
    print()
    
    for test_id in test_ids:
        if test_id not in TEST_CASES:
            print(f"⚠️ Test {test_id} は存在しません")
            continue
            
        case_data = TEST_CASES[test_id]
        result = test_single_case(test_id, case_data, verbose)
        results.append(result)
    
    # 結果サマリー
    print("\n=== テスト結果サマリー ===")
    legacy_success_count = sum(1 for r in results if r['legacy_success'])
    central_success_count = sum(1 for r in results if r['central_success'])
    total_tests = len(results)
    
    print(f"総テスト数: {total_tests}")
    print(f"従来システム成功: {legacy_success_count}/{total_tests}")
    print(f"中央制御機構成功: {central_success_count}/{total_tests}")
    
    # 改善効果分析
    improvement_cases = [r for r in results if r['central_success'] and not r['legacy_success']]
    regression_cases = [r for r in results if r['legacy_success'] and not r['central_success']]
    
    if improvement_cases:
        print(f"\n🎉 改善されたテスト ({len(improvement_cases)}件):")
        for r in improvement_cases:
            print(f"  Test {r['test_id']}: {r['sentence']}")
    
    if regression_cases:
        print(f"\n⚠️ 劣化したテスト ({len(regression_cases)}件):")
        for r in regression_cases:
            print(f"  Test {r['test_id']}: {r['sentence']}")
    
    if central_success_count > legacy_success_count:
        print(f"\n✅ 中央制御機構は従来システムより {central_success_count - legacy_success_count}件改善")
    elif central_success_count == legacy_success_count:
        print(f"\n➡️ 中央制御機構と従来システムは同等の性能")
    else:
        print(f"\n❌ 中央制御機構は従来システムより {legacy_success_count - central_success_count}件劣化")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='中央制御機構包括的テスト')
    parser.add_argument('--tests', type=str, help='テスト番号（カンマ区切り、例: 1,2,3）')
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細出力')
    parser.add_argument('--save-results', type=str, help='結果をJSONファイルに保存')
    
    args = parser.parse_args()
    
    # テスト番号解析
    test_ids = None
    if args.tests:
        try:
            test_ids = [int(x.strip()) for x in args.tests.split(',')]
        except ValueError:
            print("❌ テスト番号の形式が正しくありません")
            return
    
    # テスト実行
    results = test_comprehensive(test_ids, args.verbose)
    
    # 結果保存
    if args.save_results:
        with open(args.save_results, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n📁 結果を {args.save_results} に保存しました")

if __name__ == "__main__":
    main()
