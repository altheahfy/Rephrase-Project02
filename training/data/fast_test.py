#!/usr/bin/env python3
"""
高速テストシステム - 簡潔版
最小限のログで高速実行
"""

import json
import sys
import os
from pathlib import Path

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

def load_test_data():
    """テストデータ読み込み"""
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def run_fast_test(case_range=None, output_results=False, output_file=None):
    """高速テスト実行 - 分解結果出力対応"""
    # データ読み込み
    data = load_test_data()
    test_cases = data['data']
    
    # central_controller インポート
    from central_controller import CentralController
    controller = CentralController()
    
    # 対象ケース決定
    if case_range:
        if '-' in case_range:
            start, end = map(int, case_range.split('-'))
            target_cases = [str(i) for i in range(start, end + 1) if str(i) in test_cases]
        elif ',' in case_range:
            target_cases = [c.strip() for c in case_range.split(',') if c.strip() in test_cases]
        else:
            target_cases = [case_range] if case_range in test_cases else []
    else:
        target_cases = list(test_cases.keys())
    
    print(f"🎯 分解結果出力実行: {len(target_cases)} ケース")
    
    results = {}
    success = 0
    failed = 0
    
    for case_id in target_cases:
        case_data = test_cases[case_id]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        try:
            # 実行
            actual = controller.process_sentence(sentence)
            
            # 期待値との比較
            is_match = compare_simple(expected, actual)
            
            # 分解結果を保存
            results[f"case_{case_id}"] = {
                "sentence": sentence,
                "expected": expected,
                "actual": actual,
                "match": is_match
            }
            
            if is_match:
                if output_results:
                    print(f"\n✅ case_{case_id}: 一致")
                    print(f"例文: {sentence}")
                    print(f"分解結果:")
                    print(json.dumps(actual, ensure_ascii=False, indent=2))
                else:
                    print(f"✅ case_{case_id}: {sentence}")
                success += 1
            else:
                if output_results:
                    print(f"\n❌ case_{case_id}: 不一致")
                    print(f"例文: {sentence}")
                    print(f"実際: {actual.get('main_slots', {})}")
                    print(f"期待: {expected.get('main_slots', {})}")
                else:
                    print(f"❌ case_{case_id}: {sentence}")
                failed += 1
                
        except Exception as e:
            results[f"case_{case_id}"] = {
                "sentence": sentence,
                "expected": expected,
                "error": str(e),
                "match": False
            }
            print(f"💥 case_{case_id}: {str(e)}")
            failed += 1
    
    success_rate = (success / len(target_cases) * 100) if len(target_cases) > 0 else 0
    print(f"\n📊 処理完了: {success}成功 / {failed}失敗 / {len(target_cases)}総計 ({success_rate:.1f}%)")
    
    # ファイル出力
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"� 分解結果を保存: {output_file}")
    
    return results

def compare_simple(expected, actual):
    """簡易比較"""
    if 'error' in actual:
        return False
        
    # メインスロット比較のみ
    exp_main = expected.get('main_slots', {})
    act_main = actual.get('main_slots', {})
    
    return exp_main == act_main

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='分解結果出力システム')
    parser.add_argument('range', nargs='?', help='対象ケース範囲 (例: 1-10, 1,2,3, 35)')
    parser.add_argument('--output', '-o', help='分解結果の出力ファイル名')
    parser.add_argument('--show', '-s', action='store_true', help='コンソールに詳細表示')
    
    args = parser.parse_args()
    
    # デフォルトの出力ファイル名
    output_file = args.output
    if not output_file and args.range:
        output_file = f"decomposition_results_{args.range.replace(',', '_').replace('-', '_')}.json"
    elif not output_file:
        output_file = "decomposition_results_all.json"
    
    results = run_fast_test(args.range, args.show, output_file)
    
    print(f"📁 分解結果を保存しました: {output_file}")
