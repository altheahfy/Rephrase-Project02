#!/usr/bin/env python3
"""Case-by-case順次テスト"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_cases_sequentially():
    """Case 1から順番にテスト"""
    
    # テストデータ読み込み
    with open('batch_results_complete.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # データ構造確認
    print(f"データ構造: {type(test_data)}")
    if isinstance(test_data, dict):
        print(f"キー: {list(test_data.keys())}")
        results = test_data.get('results', [])
        # 最初の要素を確認
        if results:
            first_key = list(results.keys())[0]
            print(f"最初のエントリ構造: {results[first_key].keys()}")
        test_cases = list(results.items())[:50]  # 最初の50ケース
    else:
        test_cases = test_data[:10]
    
    mapper = UnifiedStanzaRephraseMapper()
    
    passed = 0
    failed = 0
    
    print("🎯 Case-by-Case順次テスト開始")
    print("=" * 60)
    
    for i, (case_id, case_data) in enumerate(test_cases, 1):  # 最初の10ケースから開始
        sentence = case_data.get('sentence', case_id)  # 実際の文を取得
        expected = case_data.get('expected', case_data.get('expected_result', {}))
        
        print(f"\n🧪 Case {i}: {sentence}")
        
        try:
            result = mapper.process(sentence)
            
            # 結果比較
            actual_slots = result.get('slots', {})
            actual_sub_slots = result.get('sub_slots', {})
            
            # 完全一致チェック
            slots_match = True
            mismatches = []
            
            # 期待値の構造を解析
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            # 主スロットチェック
            for key, expected_value in expected_main.items():
                actual_value = actual_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    slots_match = False
                    mismatches.append(f"{key}: '{actual_value}' ≠ '{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    slots_match = False
                    mismatches.append(f"{key}: '{actual_value}' ≠ '{expected_value}'")
            
            if slots_match:
                print("   ✅ 完全一致")
                passed += 1
            else:
                print("   ❌ 不一致")
                for mismatch in mismatches:
                    print(f"     {mismatch}")
                failed += 1
                
        except Exception as e:
            print(f"   🔥 エラー: {e}")
            failed += 1
    
    print(f"\n📊 結果サマリー (Case 1-10):")
    print(f"✅ 完全一致: {passed}")
    print(f"❌ 不一致: {failed}")
    print(f"🎯 成功率: {passed}/{passed+failed} = {passed/(passed+failed)*100:.1f}%" if passed+failed > 0 else "N/A")

if __name__ == "__main__":
    test_cases_sequentially()
