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

def run_fast_test(case_range=None):
    """高速テスト実行"""
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
    
    print(f"🎯 高速テスト実行: {len(target_cases)} ケース")
    
    success = 0
    failed = 0
    
    for case_id in target_cases:
        case_data = test_cases[case_id]
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        try:
            # 実行
            actual = controller.process_sentence(sentence)
            
            # 簡易比較
            if compare_simple(expected, actual):
                print(f"✅ {case_id}")
                success += 1
            else:
                print(f"❌ {case_id}")
                failed += 1
                
        except Exception as e:
            print(f"💥 {case_id}: {str(e)[:50]}...")
            failed += 1
    
    print(f"\n📊 結果: {success}成功 / {failed}失敗 / {len(target_cases)}総計 ({success/len(target_cases)*100:.1f}%)")

def compare_simple(expected, actual):
    """簡易比較"""
    if 'error' in actual:
        return False
        
    # メインスロット比較のみ
    exp_main = expected.get('main_slots', {})
    act_main = actual.get('main_slots', {})
    
    return exp_main == act_main

if __name__ == "__main__":
    case_range = sys.argv[1] if len(sys.argv) > 1 else None
    run_fast_test(case_range)
