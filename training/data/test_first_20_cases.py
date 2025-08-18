#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを上げて出力を抑制
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)

def main():
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)
        test_data = full_data['data']
    
    mapper = UnifiedStanzaRephraseMapper()
    
    perfect_matches = 0
    total_tested = 0
    
    print("53ケース精度確認テスト（最初の20ケース）")
    print("=" * 50)
    
    # 最初の20ケースをテスト
    for case_id in range(1, 21):
        case_str = str(case_id)
        if case_str not in test_data:
            continue
            
        case_data = test_data[case_str]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"Case {case_id}: {sentence}")
        
        try:
            result = mapper.process(sentence)
            
            # 結果比較
            actual_slots = result.get('slots', {})
            actual_sub_slots = result.get('sub_slots', {})
            
            # 期待値の構造を解析
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            # 完全一致チェック
            perfect_match = True
            mismatches = []
            
            # 主スロットチェック
            for key, expected_value in expected_main.items():
                actual_value = actual_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    mismatches.append(f"{key}: '{actual_value}' ≠ '{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    mismatches.append(f"Sub-{key}: '{actual_value}' ≠ '{expected_value}'")
            
            if perfect_match:
                print("  ✅ 完全一致")
                perfect_matches += 1
            else:
                print("  ⚠️  不一致")
                for mismatch in mismatches[:2]:  # 最大2つまで表示
                    print(f"    {mismatch}")
            
            total_tested += 1
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            total_tested += 1
        
        # 処理を軽くするため短い間隔を入れる
        import time
        time.sleep(0.01)
    
    print("\n" + "=" * 50)
    print(f"結果: {perfect_matches}/{total_tested} 完全一致 ({perfect_matches/total_tested*100:.1f}%)")

if __name__ == "__main__":
    main()
