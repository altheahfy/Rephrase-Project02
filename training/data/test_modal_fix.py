#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
助動詞縮約形修正のテスト
特に "I can't afford it" の分解をテスト
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_modal_contractions():
    """助動詞縮約形のテスト"""
    engine = RephraseParsingEngine()
    
    test_cases = [
        {
            'sentence': "I can't afford it.",
            'expected': {
                'S': 'I',
                'Aux': "can't", 
                'V': 'afford',
                'O1': 'it'
            }
        },
        {
            'sentence': "She won't come.",
            'expected': {
                'S': 'She',
                'Aux': "won't",
                'V': 'come'
            }
        },
        {
            'sentence': "They couldn't understand.",
            'expected': {
                'S': 'They',
                'Aux': "couldn't",
                'V': 'understand'
            }
        }
    ]
    
    print("=== 助動詞縮約形テスト ===")
    
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
    test_modal_contractions()
