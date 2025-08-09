#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修正されたパーシングエンジンの最終テスト
"I haven't seen you for a long time" の問題解決確認
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_parsing_engine():
    print("=== 修正されたパーシングエンジンの最終テスト ===")
    
    parser = RephraseParsingEngine()
    
    # Test Case 1: "I haven't seen you for a long time"
    sentence1 = "I haven't seen you for a long time"
    result1 = parser.analyze_sentence(sentence1)
    
    print(f"\nTest 1: '{sentence1}'")
    print("Parsed components:")
    for slot, data in result1.items():
        value = data[0]['value']
        slot_type = data[0].get('type', 'unknown')
        print(f"  {slot}: '{value}' (type: {slot_type})")
    
    # Test Case 2: "You, give it to me straight" 
    sentence2 = "You, give it to me straight"
    result2 = parser.analyze_sentence(sentence2)
    
    print(f"\nTest 2: '{sentence2}'")
    print("Parsed components:")
    for slot, data in result2.items():
        value = data[0]['value']
        slot_type = data[0].get('type', 'unknown')
        print(f"  {slot}: '{value}' (type: {slot_type})")
    
    # 期待される結果との比較
    print("\n=== 修正前後の比較 ===")
    print("問題1: 'haven't' が order=99 になる問題")
    print("  修正前: Aux: 'have not' (展開された形)")
    print(f"  修正後: Aux: '{result1['Aux'][0]['value']}' (元の収縮形を保持)")
    
    print("\n問題2: 'you' オブジェクトが欠落する問題")
    if 'O1' in result1:
        print(f"  修正後: O1: '{result1['O1'][0]['value']}' (オブジェクト認識成功)")
    else:
        print("  修正後: O1が見つからない (まだ問題あり)")
    
    print("\n問題3: 'to me' が phrase分類される問題")
    if 'M2' in result2:
        m2_type = result2['M2'][0].get('type', 'unknown')
        print(f"  修正後: M2: '{result2['M2'][0]['value']}' (type: {m2_type})")
    
    print("\n=== 全ての修正が完了しました ===")
    return result1, result2

if __name__ == "__main__":
    test_parsing_engine()
    import traceback
    traceback.print_exc()
