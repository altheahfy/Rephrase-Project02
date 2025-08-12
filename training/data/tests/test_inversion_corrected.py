#!/usr/bin/env python3
"""
修正した倒置構文エンジンのテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.inversion_engine import InversionEngine

def test_corrected_inversion():
    """修正後の倒置エンジンテスト"""
    print("🔥 修正した倒置構文エンジン テスト")
    
    try:
        engine = InversionEngine()
        print("✅ 初期化完了")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return
    
    test_cases = [
        {
            'name': '副詞句倒置',
            'sentence': 'On the table lay a book.',
            'expected_upper': {'M2': 'On the table', 'V': 'lay', 'S': 'a book'},
            'expected_sub': {'sub-m2': 'On the table', 'sub-v': 'lay', 'sub-s': 'a book'}
        },
        {
            'name': '条件倒置',
            'sentence': 'Had I known, I would have come.',
            'expected_upper': {'M1': 'Had I known', 'S': 'I', 'Aux': 'would have', 'V': 'come'},
            'expected_sub': {'sub-aux': 'had', 'sub-s': 'I', 'sub-v': 'known'}
        },
        {
            'name': '比較倒置',
            'sentence': 'Such was his anger that he couldn\'t speak.',
            'expected_upper': {'M1': 'Such was his anger that', 'S': 'he', 'Aux': 'couldn\'t', 'V': 'speak'},
            'expected_sub': {'sub-c1': 'such', 'sub-v': 'was', 'sub-s': 'his anger', 'sub-m2': 'that'}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test_case['name']}")
        print(f"入力: {test_case['sentence']}")
        
        try:
            result = engine.process(test_case['sentence'])
            
            if result:
                print(f"✅ 処理成功")
                
                print(f"  📋 上位スロット:")
                upper_slots = {}
                for key, value in result.items():
                    if not key.startswith('sub-') and key not in ['metadata', 'tense_type']:
                        print(f"    {key}: '{value}'")
                        upper_slots[key] = value
                
                print(f"  📋 サブスロット:")
                sub_slots = {}
                for key, value in result.items():
                    if key.startswith('sub-'):
                        print(f"    {key}: '{value}'")
                        sub_slots[key] = value
                
                # 期待値との比較
                print(f"  🔍 検証結果:")
                expected_upper = test_case.get('expected_upper', {})
                expected_sub = test_case.get('expected_sub', {})
                
                upper_match = True
                for exp_key, exp_value in expected_upper.items():
                    if upper_slots.get(exp_key) != exp_value:
                        print(f"    ❌ 上位 {exp_key}: 期待='{exp_value}', 実際='{upper_slots.get(exp_key)}'")
                        upper_match = False
                
                sub_match = True
                for exp_key, exp_value in expected_sub.items():
                    if sub_slots.get(exp_key) != exp_value:
                        print(f"    ❌ サブ {exp_key}: 期待='{exp_value}', 実際='{sub_slots.get(exp_key)}'")
                        sub_match = False
                
                if upper_match and sub_match:
                    print(f"    ✅ 全てのスロット配置が正しい")
                
            else:
                print("❌ 処理失敗: 結果が空です")
                
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 修正テスト完了")

if __name__ == "__main__":
    test_corrected_inversion()
