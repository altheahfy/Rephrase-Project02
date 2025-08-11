#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step7の分解精度テスト - 正しい分解ができているかの確認
"""

import sys
sys.path.append('./archive')

def test_step7_accuracy():
    """Step7の分解精度確認"""
    print("🔍 Step7 分解精度確認テスト")
    print("=" * 60)
    
    try:
        from step7_final_subslot import FinalSubslotGenerator
        generator = FinalSubslotGenerator()
        
        # 正確なテスト
        test_phrase = "the woman who seemed indecisive"
        print(f"\n📋 テストフレーズ: '{test_phrase}'")
        
        # clause として分解
        result = generator.generate_subslots_for_slot_phrase(test_phrase, "clause")
        subslots = result.get('subslots', {})
        print(f"   分解結果数: {len(subslots)}")
        for sub_type, sub_data in subslots.items():
            text = sub_data['text'] if isinstance(sub_data, dict) and 'text' in sub_data else str(sub_data)
            print(f"   ✅ {sub_type}: '{text}'")
            
        return subslots
        
    except Exception as e:
        print(f"❌ Step7 エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

if __name__ == "__main__":
    test_step7_accuracy()
