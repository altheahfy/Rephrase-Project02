#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step15の分解精度テスト
昨日の開発途中で正しく動作していたかを確認
"""

import sys
sys.path.append('./archive')

def test_step15_accuracy():
    """Step15の分解精度確認"""
    print("🔍 Step15 分解精度確認テスト")
    print("=" * 60)
    
    try:
        from step15_enhanced_universal import EnhancedUniversalSubslotGenerator
        generator = EnhancedUniversalSubslotGenerator()
        
        # 正しい5文型の例文構造で個別テスト
        test_cases = {
            "S": "the woman who seemed indecisive",
            "M1": "this morning",
            "O1": "that he had been trying to avoid Tom",
            "M3": "because he was afraid of hurting her feelings"
        }
        
        for slot_name, phrase in test_cases.items():
            print(f"\n📋 {slot_name}スロット: '{phrase}'")
            try:
                result = generator.generate_subslots_for_slot(slot_name, phrase)
                print(f"   分解結果数: {len(result)}")
                for sub_type, sub_data in result.items():
                    print(f"   ✅ {sub_type}: '{sub_data['text']}'")
            except Exception as e:
                print(f"   ❌ エラー: {str(e)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Step15インポートエラー: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {str(e)}")
        return False

if __name__ == "__main__":
    test_step15_accuracy()
