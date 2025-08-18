#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを上げてデバッグ出力を抑制
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)

def main():
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    perfect_matches = 0
    total_tested = 0
    
    # Case 43と44のみをテスト
    target_cases = ['43', '44']
    
    for case_id in target_cases:
        if case_id not in test_data:
            continue
            
        case_data = test_data[case_id]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"🧪 Case {case_id}: {sentence}")
        
        try:
            result = mapper.process(sentence)
            
            # 結果比較
            actual_slots = result.get('slots', {})
            actual_sub_slots = result.get('sub_slots', {})
            
            # 期待値の構造を解析
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            print(f"  実際のMスロット: M1='{actual_slots.get('M1', '')}', M2='{actual_slots.get('M2', '')}', M3='{actual_slots.get('M3', '')}'")
            print(f"  期待値: M1='{expected_main.get('M1', '')}', M2='{expected_main.get('M2', '')}', M3='{expected_main.get('M3', '')}'")
            
            # 完全一致チェック
            perfect_match = True
            mismatches = []
            
            # 主スロットチェック
            for key, expected_value in expected_main.items():
                actual_value = actual_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    mismatches.append(f"Main:{key}: '{actual_value}' ≠ '{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    mismatches.append(f"Sub:{key}: '{actual_value}' ≠ '{expected_value}'")
            
            if perfect_match:
                print("   ✅ 完全一致")
                perfect_matches += 1
            else:
                print("   ⚠️  不一致")
                for mismatch in mismatches[:3]:
                    print(f"     {mismatch}")
            
            total_tested += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
            total_tested += 1
        
        print()
    
    print(f"=== 結果 ===")
    print(f"完全一致: {perfect_matches}/{total_tested} ({perfect_matches/total_tested*100:.1f}%)")

if __name__ == "__main__":
    main()
