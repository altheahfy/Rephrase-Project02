#!/usr/bin/env python3
"""
失敗ケース8件の詳細デバッグスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def debug_failed_cases():
    """失敗している8ケースを個別デバッグ"""
    
    # 失敗ケースリスト（ケース20除く）
    failed_cases = [1, 2, 3, 4, 5, 6, 8, 35, 46, 47]  # テスト結果から失敗したケース
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    controller = CentralController()
    
    for case_id in failed_cases:
        case_key = str(case_id)
        if case_key not in test_data:
            continue
            
        case_info = test_data[case_key]
        sentence = case_info['sentence']
        expected = case_info['expected']
        
        print(f"\n🔍 ケース{case_id}デバッグ: '{sentence}'")
        print("=" * 80)
        
        # 実行
        try:
            actual = controller.process_sentence(sentence)
            
            print(f"📊 期待値:")
            print(f"  main_slots: {expected.get('main_slots', {})}")
            print(f"  sub_slots: {expected.get('sub_slots', {})}")
            
            print(f"📊 実際結果:")
            print(f"  main_slots: {actual.get('main_slots', {})}")
            print(f"  sub_slots: {actual.get('sub_slots', {})}")
            
            # 差分チェック
            main_match = expected.get('main_slots', {}) == actual.get('main_slots', {})
            
            # sub_slots比較（_parent_slotは除外）
            exp_sub = expected.get('sub_slots', {})
            act_sub = actual.get('sub_slots', {})
            exp_sub_filtered = {k: v for k, v in exp_sub.items() if k != '_parent_slot'}
            act_sub_filtered = {k: v for k, v in act_sub.items() if k != '_parent_slot'}
            sub_match = exp_sub_filtered == act_sub_filtered
            
            print(f"\n🎯 判定:")
            print(f"  main_slots一致: {'✅' if main_match else '❌'}")
            print(f"  sub_slots一致: {'✅' if sub_match else '❌'}")
            
            if not main_match:
                print(f"  main_slots差分:")
                for key in set(expected.get('main_slots', {}).keys()) | set(actual.get('main_slots', {}).keys()):
                    exp_val = expected.get('main_slots', {}).get(key, '<欠如>')
                    act_val = actual.get('main_slots', {}).get(key, '<欠如>')
                    if exp_val != act_val:
                        print(f"    {key}: 期待='{exp_val}' vs 実際='{act_val}'")
            
            if not sub_match:
                print(f"  sub_slots差分:")
                for key in set(exp_sub_filtered.keys()) | set(act_sub_filtered.keys()):
                    exp_val = exp_sub_filtered.get(key, '<欠如>')
                    act_val = act_sub_filtered.get(key, '<欠如>')
                    if exp_val != act_val:
                        print(f"    {key}: 期待='{exp_val}' vs 実際='{act_val}'")
            
        except Exception as e:
            print(f"💥 エラー: {str(e)}")

if __name__ == "__main__":
    debug_failed_cases()
