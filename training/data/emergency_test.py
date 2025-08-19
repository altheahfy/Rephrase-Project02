#!/usr/bin/env python3
"""
全53例文での緊急精度テスト
修正による影響を確認するための包括的テスト
"""

import json
import time
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def run_full_accuracy_test():
    """全53例文での精度テスト実行"""
    print("🚨 緊急精度テスト開始 - 全53例文")
    
    # テストデータ読み込み
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_tests': 0,
        'successes': 0,
        'failures': 0,
        'accuracy': 0.0,
        'failed_cases': [],
        'details': {}
    }
    
    print(f"📊 テスト対象: {len(test_data['data'])}例文")
    
    for case_id, case_data in test_data['data'].items():
        if case_id.isdigit():  # 数字のケースのみ処理
            case_num = int(case_id)
            if case_num > 53:
                continue
                
            sentence = case_data['sentence']
            expected = case_data['expected']
            
            print(f"⏳ Case {case_id}: {sentence[:50]}...")
            
            try:
                # 処理実行
                result = mapper.process(sentence)
                
                # 結果比較
                main_match = result.get('main_slots', {}) == expected['main_slots']
                sub_match = result.get('sub_slots', {}) == expected['sub_slots']
                
                is_success = main_match and sub_match
                
                results['total_tests'] += 1
                if is_success:
                    results['successes'] += 1
                    print(f"  ✅ Case {case_id}: 成功")
                else:
                    results['failures'] += 1
                    results['failed_cases'].append(case_id)
                    print(f"  ❌ Case {case_id}: 失敗")
                    
                    # 失敗詳細
                    failure_detail = {
                        'sentence': sentence,
                        'expected_main': expected['main_slots'],
                        'actual_main': result.get('main_slots', {}),
                        'expected_sub': expected['sub_slots'],
                        'actual_sub': result.get('sub_slots', {}),
                        'main_match': main_match,
                        'sub_match': sub_match
                    }
                    results['details'][case_id] = failure_detail
                    
            except Exception as e:
                print(f"  💥 Case {case_id}: エラー - {e}")
                results['failures'] += 1
                results['failed_cases'].append(case_id)
                results['total_tests'] += 1
    
    # 精度計算
    if results['total_tests'] > 0:
        results['accuracy'] = (results['successes'] / results['total_tests']) * 100
    
    # 結果サマリー
    print(f"\n📈 テスト結果サマリー:")
    print(f"  総テスト数: {results['total_tests']}")
    print(f"  成功: {results['successes']}")
    print(f"  失敗: {results['failures']}")
    print(f"  精度: {results['accuracy']:.2f}%")
    
    if results['failed_cases']:
        print(f"  失敗ケース: {', '.join(results['failed_cases'])}")
    
    # 結果保存
    output_file = f"emergency_test_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 詳細結果保存: {output_file}")
    
    # 過去結果との比較示唆
    print(f"\n🔍 過去の基準精度:")
    print(f"  - Case 49-52 分詞構文: 100% (修正後)")
    print(f"  - 従来の関係詞節: 通常95%以上")
    print(f"  - 基本五文型: 通常98%以上")
    
    if results['accuracy'] < 90:
        print(f"\n⚠️ 精度低下検出: {results['accuracy']:.2f}% < 90%")
        print(f"修正のRevertを検討する必要があります。")
        
        # 特に問題のあるケースを詳細表示
        if len(results['failed_cases']) <= 10:
            print(f"\n🔧 失敗ケース詳細:")
            for case_id in results['failed_cases'][:5]:  # 最初の5件
                if case_id in results['details']:
                    detail = results['details'][case_id]
                    print(f"\nCase {case_id}: {detail['sentence']}")
                    print(f"  期待main: {detail['expected_main']}")
                    print(f"  実際main: {detail['actual_main']}")
                    print(f"  期待sub:  {detail['expected_sub']}")
                    print(f"  実際sub:  {detail['actual_sub']}")
    
    return results

if __name__ == "__main__":
    run_full_accuracy_test()
