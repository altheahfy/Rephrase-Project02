#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修正前後の比較テスト（絵文字なし版）
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def simple_test():
    print("修正前後比較テスト")
    print("=" * 50)
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data_obj = json.load(f)
    
    test_data = test_data_obj['data']
    
    # マッパー初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    total = 0
    perfect = 0
    failed_cases = []
    
    # Case 32を含む重要なケースのみテスト
    important_cases = [21, 23, 24, 25, 26, 32, 37, 38, 39]
    
    for case_str, case_data in test_data.items():
        case_num = int(case_str)
        if case_num not in important_cases:
            continue
            
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"\nCase {case_num}: {sentence}")
        
        result = mapper.process(sentence)
        actual_slots = result.get('slots', {})
        actual_sub_slots = result.get('sub_slots', {})
        
        # 完全一致判定
        is_perfect = (actual_slots == expected.get('main_slots', {}) and 
                     actual_sub_slots == expected.get('sub_slots', {}))
        
        total += 1
        if is_perfect:
            perfect += 1
            print(f"  OK: 完全一致")
        else:
            failed_cases.append(case_num)
            print(f"  FAIL: 不一致")
            print(f"    期待: slots={expected.get('main_slots', {})}, sub_slots={expected.get('sub_slots', {})}")
            print(f"    実際: slots={actual_slots}, sub_slots={actual_sub_slots}")
    
    accuracy = (perfect/total)*100 if total > 0 else 0
    print(f"\n結果:")
    print(f"完全一致: {perfect}/{total} = {accuracy:.1f}%")
    print(f"失敗ケース: {failed_cases}")

if __name__ == "__main__":
    simple_test()
