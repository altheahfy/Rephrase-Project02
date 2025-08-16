#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
53例文完全整合テストスクリプト
正解データと完全に整合した例文でのシステム動作確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import codecs

def run_53_complete_test():
    """53例文完全整合テスト実行"""
    print("🎯 53例文完全整合テスト開始")
    print("="*60)
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログを最小化
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    # 正解データ読み込み
    with codecs.open('final_54_test_data.json', 'r', 'utf-8') as f:
        test_data = json.load(f)
    
    print(f"📊 テストデータ読み込み完了: {test_data['meta']['total_count']}例文")
    print()
    
    total_tests = 0
    perfect_matches = 0
    partial_matches = 0
    failures = 0
    
    results = []
    
    # 各例文をテスト
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        total_tests += 1
        print(f"🧪 テスト{test_id}: {sentence}")
        
        try:
            # システム実行
            result = mapper.process(sentence)
            
            # 結果取得
            system_slots = result.get('slots', {})
            system_sub_slots = result.get('sub_slots', {})
            
            # 期待値取得
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            # 完全一致チェック
            main_match = check_slots_match(system_slots, expected_main)
            sub_match = check_slots_match(system_sub_slots, expected_sub)
            
            if main_match and sub_match:
                perfect_matches += 1
                status = "✅ 完全一致"
            elif main_match or sub_match:
                partial_matches += 1
                status = "⚠️  部分一致"
            else:
                failures += 1
                status = "❌ 不一致"
            
            print(f"   {status}")
            
            # 詳細表示（不一致の場合）
            if not (main_match and sub_match):
                print("   詳細:")
                print(f"     システム出力: {format_slots(system_slots, system_sub_slots)}")
                print(f"     期待値: {format_slots(expected_main, expected_sub)}")
            
            results.append({
                'test_id': test_id,
                'sentence': sentence,
                'main_match': main_match,
                'sub_match': sub_match,
                'perfect': main_match and sub_match,
                'system_output': {
                    'main_slots': system_slots,
                    'sub_slots': system_sub_slots
                },
                'expected': expected
            })
            
        except Exception as e:
            failures += 1
            print(f"   ❌ エラー: {str(e)}")
            
        print()
    
    # 結果レポート
    print("="*60)
    print("📊 テスト結果レポート")
    print("="*60)
    print(f"総テスト数: {total_tests}")
    print(f"完全一致: {perfect_matches} ({perfect_matches/total_tests*100:.1f}%)")
    print(f"部分一致: {partial_matches} ({partial_matches/total_tests*100:.1f}%)")
    print(f"不一致: {failures} ({failures/total_tests*100:.1f}%)")
    print()
    
    accuracy = perfect_matches / total_tests * 100
    print(f"🎯 完全一致率: {accuracy:.1f}%")
    
    # 詳細レポート保存
    report = {
        'meta': {
            'total_tests': total_tests,
            'perfect_matches': perfect_matches,
            'partial_matches': partial_matches,
            'failures': failures,
            'accuracy': accuracy
        },
        'results': results
    }
    
    with codecs.open('53_complete_test_report.json', 'w', 'utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 詳細レポート保存: 53_complete_test_report.json")
    
    if accuracy >= 90:
        print("🎉 システム動作: 優秀")
    elif accuracy >= 80:
        print("✅ システム動作: 良好")
    elif accuracy >= 70:
        print("⚠️  システム動作: 要改善")
    else:
        print("❌ システム動作: 要修正")
    
    return accuracy

def check_slots_match(system_slots, expected_slots):
    """スロット完全一致チェック"""
    # 空でないスロットのみを比較
    system_filtered = {k: v for k, v in system_slots.items() if v.strip()}
    expected_filtered = {k: v for k, v in expected_slots.items() if v.strip()}
    
    return system_filtered == expected_filtered

def format_slots(main_slots, sub_slots=None):
    """スロット表示フォーマット"""
    result = []
    
    # メインスロット
    for k, v in main_slots.items():
        if v.strip():
            result.append(f"{k}:{v}")
    
    # サブスロット
    if sub_slots:
        for k, v in sub_slots.items():
            if v.strip():
                result.append(f"{k}:{v}")
    
    return "{" + ", ".join(result) + "}"

if __name__ == "__main__":
    run_53_complete_test()
