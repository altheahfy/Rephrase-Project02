#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
動名詞ハンドラー専用テストスクリプト
新規追加されたテストケース（171-195）での動作検証
"""

import json
import sys
from gerund_handler import GerundHandler

def test_gerund_handler():
    """動名詞ハンドラーのテスト実行"""
    # テストデータの読み込み
    try:
        with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("❌ テストデータファイルが見つかりません")
        return False
    
    handler = GerundHandler()
    
    # 動名詞テストケース（171-195）を抽出
    gerund_test_cases = {}
    for case_id, case_data in test_data['data'].items():
        case_num = int(case_id)
        if 171 <= case_num <= 195:
            gerund_test_cases[case_id] = case_data
    
    print(f"🧪 動名詞ハンドラーテスト開始: {len(gerund_test_cases)}ケース")
    print("=" * 80)
    
    success_count = 0
    total_count = len(gerund_test_cases)
    detailed_results = []
    
    for case_id, case_data in gerund_test_cases.items():
        sentence = case_data['sentence']
        expected = case_data['expected']
        expected_main = expected['main_slots']
        v_group_key = case_data.get('V_group_key', 'test')
        grammar_category = case_data.get('grammar_category', 'unknown')
        
        print(f"\n📝 ケース {case_id}: {grammar_category}")
        print(f"   例文: '{sentence}'")
        
        # ハンドラー実行
        result = handler.handle(sentence, v_group_key)
        
        if result['success']:
            # 期待値との比較
            actual_main = result['main_slots']
            
            # スロット比較
            main_match = compare_slots(actual_main, expected_main)
            
            if main_match:
                print(f"   ✅ 成功: スロット分解正確")
                success_count += 1
                status = "✅ PASS"
            else:
                print(f"   ⚠️  期待値不一致:")
                print(f"      期待値: {expected_main}")
                print(f"      実際値: {actual_main}")
                status = "⚠️ MISMATCH"
            
            detailed_results.append({
                'case_id': case_id,
                'sentence': sentence,
                'category': grammar_category,
                'status': status,
                'expected': expected_main,
                'actual': actual_main
            })
        else:
            print(f"   ❌ 失敗: {result.get('reason', 'Unknown error')}")
            detailed_results.append({
                'case_id': case_id,
                'sentence': sentence,
                'category': grammar_category,
                'status': "❌ FAIL",
                'expected': expected_main,
                'actual': {},
                'error': result.get('reason', 'Unknown error')
            })
    
    print("\n" + "=" * 80)
    print(f"🏆 テスト結果サマリー: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    # カテゴリ別成功率
    categories = {}
    for result in detailed_results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'success': 0}
        categories[cat]['total'] += 1
        if result['status'] == "✅ PASS":
            categories[cat]['success'] += 1
    
    print("\n📊 カテゴリ別成功率:")
    for cat, stats in categories.items():
        rate = stats['success'] / stats['total'] * 100
        print(f"   {cat}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
    
    # 失敗ケースの詳細表示
    failures = [r for r in detailed_results if r['status'] != "✅ PASS"]
    if failures:
        print(f"\n❌ 失敗・不一致ケース詳細 ({len(failures)}件):")
        for failure in failures:
            print(f"   ケース {failure['case_id']}: {failure['sentence']}")
            print(f"      期待値: {failure['expected']}")
            if 'actual' in failure:
                print(f"      実際値: {failure['actual']}")
            if 'error' in failure:
                print(f"      エラー: {failure['error']}")
    
    return success_count == total_count

def compare_slots(actual, expected):
    """スロット比較（期待値との一致確認）"""
    # 空文字列とNoneを同等に扱う
    def normalize_value(value):
        return "" if value is None else str(value)
    
    # 両方のキーを取得
    all_keys = set(actual.keys()) | set(expected.keys())
    
    for key in all_keys:
        actual_val = normalize_value(actual.get(key, ""))
        expected_val = normalize_value(expected.get(key, ""))
        
        if actual_val != expected_val:
            return False
    
    return True

if __name__ == "__main__":
    success = test_gerund_handler()
    sys.exit(0 if success else 1)
