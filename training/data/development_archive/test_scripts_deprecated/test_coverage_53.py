#!/usr/bin/env python3
"""53ケース完全カバレッジテスト（修正版対応）"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import traceback
from datetime import datetime

def test_53_cases_coverage():
    """53ケース全体のカバレッジを測定"""
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    results = test_data.get('data', {})
    
    mapper = UnifiedStanzaRephraseMapper()
    
    total_cases = 0
    perfect_matches = 0
    partial_matches = 0
    failures = 0
    errors = 0
    
    print("53ケース完全カバレッジテスト開始")
    print("=" * 60)
    print(f"開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for case_id, case_data in results.items():
        total_cases += 1
        sentence = case_data.get('sentence', case_id)
        expected = case_data.get('expected', {})
        
        print(f"🧪 Case {case_id}: {sentence}")
        
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
            partial_match = False
            mismatches = []
            
            # 主スロットチェック
            for key, expected_value in expected_main.items():
                actual_value = actual_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    partial_match = True
                    mismatches.append(f"Main:{key}: '{actual_value}' ≠ '{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    partial_match = True
                    mismatches.append(f"Sub:{key}: '{actual_value}' ≠ '{expected_value}'")
            
            if perfect_match:
                print("   ✅ 完全一致")
                perfect_matches += 1
            elif partial_match:
                print("   ⚠️  部分一致")
                for mismatch in mismatches[:2]:  # 最大2つまで表示
                    print(f"     {mismatch}")
                partial_matches += 1
            else:
                print("   ❌ 不一致")
                failures += 1
                
        except Exception as e:
            print(f"   🔥 エラー: {e}")
            # print(f"     {traceback.format_exc()}")
            errors += 1
        
        # 10ケースごとに進捗表示
        if total_cases % 10 == 0:
            current_accuracy = (perfect_matches / total_cases) * 100
            print(f"\n📊 進捗 {total_cases}/53: 完全一致率 {current_accuracy:.1f}%\n")
    
    # 最終結果
    print("\n" + "=" * 60)
    print("📊 53ケース完全カバレッジ結果")
    print("=" * 60)
    print(f"✅ 完全一致: {perfect_matches} ケース")
    print(f"⚠️  部分一致: {partial_matches} ケース")  
    print(f"❌ 不一致: {failures} ケース")
    print(f"🔥 エラー: {errors} ケース")
    print(f"📝 総ケース数: {total_cases}")
    print()
    print(f"🎯 完全一致率: {perfect_matches}/{total_cases} = {(perfect_matches/total_cases)*100:.1f}%")
    print(f"📈 部分成功率: {(perfect_matches+partial_matches)}/{total_cases} = {((perfect_matches+partial_matches)/total_cases)*100:.1f}%")
    print()
    print(f"完了時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 目標達成状況
    if perfect_matches == 53:
        print("🎉 目標達成！53/53 = 100%完全一致！")
    elif perfect_matches >= 45:
        print(f"🔥 優秀！あと{53-perfect_matches}ケースで100%達成！")
    elif perfect_matches >= 40:
        print(f"⭐ 良好！あと{53-perfect_matches}ケースで100%達成！")
    else:
        print(f"🚀 継続改善中...目標まであと{53-perfect_matches}ケース")

if __name__ == "__main__":
    test_53_cases_coverage()
