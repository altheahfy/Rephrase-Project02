#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
動名詞ケース専用fast_testスクリプト
ケース171-200のみをテスト
"""

import json
import sys
sys.path.append('.')

from central_controller import CentralController

def test_gerund_cases():
    """動名詞ケース（171-200）のみをテスト"""
    
    # テストデータの読み込み
    try:
        with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("❌ テストデータファイルが見つかりません")
        return False
    
    controller = CentralController()
    
    # 動名詞テストケース（171-200）を抽出
    gerund_test_cases = {}
    for case_id, case_data in test_data['data'].items():
        case_num = int(case_id)
        if 171 <= case_num <= 175:  # 最初の5ケースだけテスト
            gerund_test_cases[case_id] = case_data
    
    print(f"🧪 動名詞ケーステスト開始: {len(gerund_test_cases)}ケース")
    print("=" * 80)
    
    success_count = 0
    total_count = len(gerund_test_cases)
    
    for case_id, case_data in gerund_test_cases.items():
        sentence = case_data['sentence']
        expected = case_data['expected']
        v_group_key = case_data.get('V_group_key', 'test')
        grammar_category = case_data.get('grammar_category', 'unknown')
        
        print(f"\n📝 ケース {case_id}: {grammar_category}")
        print(f"   例文: '{sentence}'")
        print(f"   V_group_key: {v_group_key}")
        
        # CentralController でテスト実行
        try:
            result = controller.process_sentence(sentence)
            
            print(f"📊 実行結果:")
            print(f"   success: {result.get('success', False)}")
            print(f"   main_slots: {result.get('main_slots', {})}")
            print(f"   sub_slots: {result.get('sub_slots', {})}")
            print(f"   primary_handler: {result.get('metadata', {}).get('primary_handler', 'unknown')}")
            
            if result.get('success', False):
                success_count += 1
                print(f"✅ 成功")
            else:
                print(f"❌ 失敗: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 最終結果: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")

if __name__ == "__main__":
    test_gerund_cases()
