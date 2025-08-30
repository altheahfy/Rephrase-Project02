#!/usr/bin/env python3
"""
AbsoluteOrderManager修正版テスト
Cases 83-86（tellグループ）の検証
"""

import json
from absolute_order_manager_group_fixed import AbsoluteOrderManager

def test_tell_group_cases():
    """tellグループ（Cases 83-86）のテスト実行"""
    
    # 期待値データ読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # AbsoluteOrderManager初期化
    order_manager = AbsoluteOrderManager()
    
    # tellグループのテストケース
    tell_cases = ['83', '84', '85', '86']
    
    print("🎯 AbsoluteOrderManager 修正版テスト")
    print("=" * 60)
    
    success_count = 0
    total_count = len(tell_cases)
    
    for case_id in tell_cases:
        case_data = test_data['data'][case_id]
        sentence = case_data['sentence']
        expected_order = case_data['absolute_order']
        main_slots = case_data['expected']['main_slots']
        wh_word = case_data.get('wh_word')
        
        print(f"\n📋 Case {case_id}: {sentence}")
        print(f"🔍 wh_word: {wh_word}")
        print(f"📊 Expected: {expected_order}")
        
        # AbsoluteOrderManager実行
        try:
            result = order_manager.apply_absolute_order(
                slots=main_slots,
                v_group_key="tell", 
                wh_word=wh_word
            )
            
            # 結果を辞書形式に変換
            actual_order = {}
            for item in result:
                actual_order[item['slot']] = item['absolute_position']
            
            print(f"📈 Actual:   {actual_order}")
            
            # 比較
            is_match = actual_order == expected_order
            
            if is_match:
                print("✅ MATCH")
                success_count += 1
            else:
                print("❌ MISMATCH")
                print("🔍 Differences:")
                for slot in set(list(expected_order.keys()) + list(actual_order.keys())):
                    exp_pos = expected_order.get(slot, "なし")
                    act_pos = actual_order.get(slot, "なし")
                    if exp_pos != act_pos:
                        print(f"  - {slot}: Expected={exp_pos}, Actual={act_pos}")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print(f"\n📊 結果: {success_count}/{total_count} ケース成功")
    print(f"📈 成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 全テスト成功！修正完了")
    else:
        print("⚠️  修正が必要です")

if __name__ == "__main__":
    test_tell_group_cases()
