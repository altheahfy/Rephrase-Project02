#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple 53-test runner without Unicode issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def run_simple_test():
    """簡潔な53テスト実行"""
    print("53例文テスト開始")
    print("="*50)
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    
    # テストデータ読み込み
    try:
        with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("ERROR: final_54_test_data.json not found")
        return
    
    print(f"テストデータ読み込み完了: {test_data['meta']['total_count']}例文")
    print()
    
    # テスト実行
    results = []
    perfect_count = 0
    partial_count = 0
    fail_count = 0
    
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"Test{test_id}: {sentence}")
        
        try:
            # システム実行
            result = mapper.process(sentence)
            system_main = result.get('slots', {})
            system_sub = result.get('sub_slots', {})
            
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            # 比較
            main_match = system_main == expected_main
            sub_match = system_sub == expected_sub
            
            if main_match and sub_match:
                status = "PERFECT"
                perfect_count += 1
            elif main_match or sub_match:
                status = "PARTIAL"
                partial_count += 1
            else:
                status = "FAIL"
                fail_count += 1
            
            print(f"  Status: {status}")
            if status != "PERFECT":
                print(f"  System: {system_main} | {system_sub}")
                print(f"  Expected: {expected_main} | {expected_sub}")
            
            results.append({
                'test_id': test_id,
                'status': status,
                'sentence': sentence
            })
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            fail_count += 1
            results.append({
                'test_id': test_id,
                'status': 'ERROR',
                'sentence': sentence
            })
        
        print()
    
    # 結果レポート
    total = len(test_data['data'])
    accuracy = (perfect_count / total) * 100
    
    print("="*50)
    print("テスト結果レポート")
    print("="*50)
    print(f"総テスト数: {total}")
    print(f"完全一致: {perfect_count} ({perfect_count/total*100:.1f}%)")
    print(f"部分一致: {partial_count} ({partial_count/total*100:.1f}%)")
    print(f"不一致: {fail_count} ({fail_count/total*100:.1f}%)")
    print()
    print(f"完全一致率: {accuracy:.1f}%")
    
    # 改善ターゲット出力
    failures = [r for r in results if r['status'] == 'FAIL']
    if failures:
        print()
        print("改善対象:")
        for f in failures[:5]:  # 最初の5件のみ
            print(f"  Test{f['test_id']}: {f['sentence']}")

if __name__ == "__main__":
    run_simple_test()
