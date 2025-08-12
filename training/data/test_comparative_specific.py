#!/usr/bin/env python3
"""
比較倒置の特定テスト - couldn't 問題の解決
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.inversion_engine import InversionEngine

def test_comparative_inversion_specific():
    """比較倒置の詳細テスト"""
    print("🔥 比較倒置 couldn't 問題修正テスト")
    
    try:
        engine = InversionEngine()
        print("✅ 初期化完了")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return
    
    test_sentence = "Such was his anger that he couldn't speak."
    print(f"\n🎯 テスト対象: {test_sentence}")
    
    try:
        result = engine.process(test_sentence)
        
        if result:
            print(f"✅ 処理成功")
            
            print(f"  📋 上位スロット:")
            for key, value in result.items():
                if not key.startswith('sub-') and key not in ['metadata', 'tense_type']:
                    print(f"    {key}: '{value}'")
            
            print(f"  📋 サブスロット:")
            for key, value in result.items():
                if key.startswith('sub-'):
                    print(f"    {key}: '{value}'")
            
            # 期待値との詳細比較
            print(f"\n🔍 詳細検証:")
            
            # 上位スロット期待値
            expected_upper = {
                'M1': 'Such was his anger that',
                'S': 'he',
                'Aux': "couldn't",  # 重要: 縮約形のまま
                'V': 'speak'        # 重要: 実際の動詞
            }
            
            # サブスロット期待値
            expected_sub = {
                'sub-c1': 'such',
                'sub-v': 'was',
                'sub-s': 'his anger',
                'sub-m2': 'that'
            }
            
            # 上位スロット検証
            all_correct = True
            for exp_key, exp_value in expected_upper.items():
                actual_value = result.get(exp_key)
                if actual_value == exp_value:
                    print(f"    ✅ 上位 {exp_key}: '{actual_value}' = 期待値")
                else:
                    print(f"    ❌ 上位 {exp_key}: '{actual_value}' ≠ 期待値 '{exp_value}'")
                    all_correct = False
            
            # サブスロット検証
            for exp_key, exp_value in expected_sub.items():
                actual_value = result.get(exp_key)
                if actual_value == exp_value:
                    print(f"    ✅ サブ {exp_key}: '{actual_value}' = 期待値")
                else:
                    print(f"    ❌ サブ {exp_key}: '{actual_value}' ≠ 期待値 '{exp_value}'")
                    all_correct = False
            
            if all_correct:
                print(f"\n🎉 完璧！全てのスロット配置が正しい")
            else:
                print(f"\n🔧 まだ改善の余地あり")
                
        else:
            print("❌ 処理失敗: 結果が空です")
            
    except Exception as e:
        print(f"❌ 処理エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comparative_inversion_specific()
