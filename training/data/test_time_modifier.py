#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
時間修飾語分離のテスト
特に "He left New York a few days ago." の分解をテスト
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_time_modifier_separation():
    """時間修飾語分離のテスト"""
    engine = RephraseParsingEngine()
    
    test_cases = [
        {
            'sentence': "He left New York a few days ago.",
            'expected': {
                'S': 'He',
                'V': 'left',
                'O1': 'New York',
                'M3': 'a few days ago'
            }
        },
        {
            'sentence': "I visited Tokyo yesterday.",
            'expected': {
                'S': 'I',
                'V': 'visited',
                'O1': 'Tokyo',
                'M3': 'yesterday'
            }
        },
        {
            'sentence': "She finished her work two hours ago.",
            'expected': {
                'S': 'She',
                'V': 'finished',
                'O1': 'her work',
                'M3': 'two hours ago'
            }
        },
        {
            'sentence': "They will meet us next week.",
            'expected': {
                'S': 'They',
                'Aux': 'will',
                'V': 'meet',
                'O1': 'us',
                'M3': 'next week'
            }
        }
    ]
    
    print("=== 時間修飾語分離テスト ===")
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"\n--- テスト {i}: {sentence} ---")
        
        # 解析実行
        result = engine.analyze_sentence(sentence)
        
        print("解析結果:")
        for slot, candidates in result.items():
            if candidates:
                value = candidates[0]['value']
                print(f"  {slot}: {value}")
        
        print("期待値:")
        for slot, value in expected.items():
            print(f"  {slot}: {value}")
        
        # 結果確認
        success = True
        for slot, expected_value in expected.items():
            if slot not in result or not result[slot]:
                print(f"❌ {slot} スロットが見つかりません")
                success = False
            elif result[slot][0]['value'] != expected_value:
                actual = result[slot][0]['value']
                print(f"❌ {slot}: 期待値='{expected_value}', 実際='{actual}'")
                success = False
            else:
                print(f"✅ {slot}: '{expected_value}' 正解")
        
        if success:
            print("🎉 テスト成功!")
        else:
            print("💥 テスト失敗")

if __name__ == "__main__":
    test_time_modifier_separation()
