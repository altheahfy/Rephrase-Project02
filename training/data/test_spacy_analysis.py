#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
spaCyベース解析のテスト
時間修飾語の適切な分離をテスト
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_spacy_analysis():
    """spaCyベース解析のテスト"""
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
            'sentence': "She visited Tokyo last week.",
            'expected': {
                'S': 'She',
                'V': 'visited',
                'O1': 'Tokyo',
                'M3': 'last week'
            }
        },
        {
            'sentence': "They will arrive tomorrow.",
            'expected': {
                'S': 'They',
                'Aux': 'will',
                'V': 'arrive',
                'M3': 'tomorrow'
            }
        },
        {
            'sentence': "I studied English for two hours.",
            'expected': {
                'S': 'I',
                'V': 'studied',
                'O1': 'English',
                'M3': 'for two hours'
            }
        }
    ]
    
    print("=== spaCyベース解析テスト ===")
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"\n--- テスト {i}: {sentence} ---")
        
        # 解析実行
        result = engine.analyze_sentence(sentence)
        
        print("解析結果:")
        for slot, candidates in result.items():
            if candidates:
                if isinstance(candidates, list):
                    values = [item['value'] for item in candidates]
                    print(f"  {slot}: {values}")
                else:
                    print(f"  {slot}: {candidates}")
        
        print("期待値:")
        for slot, value in expected.items():
            print(f"  {slot}: {value}")
        
        # 結果確認
        success = True
        for slot, expected_value in expected.items():
            if slot not in result or not result[slot]:
                print(f"❌ {slot} スロットが見つかりません")
                success = False
            else:
                # リスト形式の場合は最初の値を取得
                if isinstance(result[slot], list):
                    actual_values = [item['value'] for item in result[slot]]
                    if expected_value in actual_values:
                        print(f"✅ {slot}: '{expected_value}' 正解")
                    else:
                        print(f"❌ {slot}: 期待値='{expected_value}', 実際={actual_values}")
                        success = False
                else:
                    actual = result[slot]
                    if actual == expected_value:
                        print(f"✅ {slot}: '{expected_value}' 正解")
                    else:
                        print(f"❌ {slot}: 期待値='{expected_value}', 実際='{actual}'")
                        success = False
        
        if success:
            print("🎉 テスト成功!")
        else:
            print("💥 テスト失敗")

if __name__ == "__main__":
    test_spacy_analysis()
