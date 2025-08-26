#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import time
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
    partial_matches = 0
    total_tested = 0
    failed_cases = []
    mismatch_details = []
    
    print("53ケース完全テスト実行")
    print("=" * 60)
    
    # 1から53まで全ケースをテスト
    for case_id in range(1, 54):
        case_str = str(case_id)
        if case_str not in test_data:
            print(f"Case {case_id}: データなし (スキップ)")
            continue
            
        case_data = test_data[case_str]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        print(f"Case {case_id}: {sentence}")
        
        try:
            # タイムアウト対策
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
                    mismatches.append(f"Main-{key}: '{actual_value}' ≠ '{expected_value}'")
            
            # サブスロットチェック  
            for key, expected_value in expected_sub.items():
                actual_value = actual_sub_slots.get(key, '')
                if str(actual_value) != str(expected_value):
                    perfect_match = False
                    mismatches.append(f"Sub-{key}: '{actual_value}' ≠ '{expected_value}'")
            
            if perfect_match:
                print("  ✅ 完全一致")
                perfect_matches += 1
            elif len(mismatches) <= 2:  # 軽微な不一致
                print("  ⚠️  部分一致")
                for mismatch in mismatches[:2]:
                    print(f"    {mismatch}")
                partial_matches += 1
                mismatch_details.append(f"Case {case_id}: " + ", ".join(mismatches[:2]))
            else:  # 重大な不一致
                print("  ❌ 重大な不一致")
                for mismatch in mismatches[:3]:
                    print(f"    {mismatch}")
                failed_cases.append(case_id)
                mismatch_details.append(f"Case {case_id}: " + ", ".join(mismatches[:3]))
            
            total_tested += 1
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            failed_cases.append(case_id)
            total_tested += 1
        
        # 処理間隔（システム負荷軽減）
        time.sleep(0.05)
        
        # 10ケースごとに進捗表示
        if case_id % 10 == 0:
            current_accuracy = perfect_matches / total_tested * 100 if total_tested > 0 else 0
            print(f"  --- {case_id}ケース完了 (現在の精度: {current_accuracy:.1f}%) ---")
    
    # 最終結果
    print("\n" + "=" * 60)
    print(f"📊 最終結果")
    print(f"完全一致: {perfect_matches}/{total_tested} ({perfect_matches/total_tested*100:.1f}%)")
    print(f"部分一致: {partial_matches}/{total_tested} ({partial_matches/total_tested*100:.1f}%)")
    print(f"失敗: {len(failed_cases)}/{total_tested} ({len(failed_cases)/total_tested*100:.1f}%)")
    
    # 詳細サマリー
    overall_success = perfect_matches + partial_matches
    print(f"総合成功率: {overall_success}/{total_tested} ({overall_success/total_tested*100:.1f}%)")
    
    if failed_cases:
        print(f"\n❌ 失敗ケース: {failed_cases}")
    
    if mismatch_details and len(mismatch_details) <= 10:
        print(f"\n⚠️  主な不一致詳細:")
        for detail in mismatch_details[:10]:
            print(f"  {detail}")

if __name__ == "__main__":
    main()
