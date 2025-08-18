#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを上げて出力を抑制
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)

def analyze_failed_cases():
    # 失敗ケースのID
    failed_cases = [49, 50, 51, 52]
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)
        test_data = full_data['data']
    
    mapper = UnifiedStanzaRephraseMapper()
    
    print("🔍 失敗ケース詳細分析")
    print("=" * 80)
    
    for case_id in failed_cases:
        case_str = str(case_id)
        if case_str not in test_data:
            continue
            
        case_data = test_data[case_str]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"\n📋 Case {case_id}: {sentence}")
        print("-" * 60)
        
        try:
            result = mapper.process(sentence)
            
            # 結果比較
            actual_slots = result.get('slots', {})
            actual_sub_slots = result.get('sub_slots', {})
            
            # 期待値の構造を解析
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            print("🎯 期待値:")
            print("  Main slots:")
            for key, value in expected_main.items():
                print(f"    {key}: '{value}'")
            print("  Sub slots:")
            for key, value in expected_sub.items():
                print(f"    {key}: '{value}'")
            
            print("\n📤 実際の出力:")
            print("  Main slots:")
            for key, value in actual_slots.items():
                if value:  # 空でない値のみ表示
                    print(f"    {key}: '{value}'")
            print("  Sub slots:")
            for key, value in actual_sub_slots.items():
                if value:  # 空でない値のみ表示
                    print(f"    {key}: '{value}'")
            
            print("\n❌ 不一致詳細:")
            # 主スロットチェック
            for key, expected_value in expected_main.items():
                actual_value = actual_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    print(f"  Main-{key}: 実際='{actual_value}' ≠ 期待='{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    print(f"  Sub-{key}: 実際='{actual_value}' ≠ 期待='{expected_value}'")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    print("\n" + "=" * 80)
    print("🎯 100％達成への道筋:")
    print("1. Case 49: 分詞構文の目的語・副詞処理")
    print("2. Case 50-51: 分詞構文での主語・副詞スロット配置") 
    print("3. Case 52: 分詞構文での助動詞処理")
    print("4. 分詞構文専用ハンドラーの実装が必要な可能性")

if __name__ == "__main__":
    analyze_failed_cases()
