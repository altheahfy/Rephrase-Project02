#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_parsing():
    # パーサーテスト - 最終確認
    parser = RephraseParsingEngine()
    
    # テスト1: haven't構文
    result = parser.analyze_sentence("I haven't seen you for a long time")
    print("=== Final Test Results ===")
    print("Sentence: I haven't seen you for a long time")
    print("Parsed components:")
    for slot, data in result.items():
        value = data[0]['value']
        print(f"  {slot}: '{value}'")

    print()
    
    # テスト2: 命令文
    result2 = parser.analyze_sentence("You, give it to me straight")
    print("=== Additional Test ===")
    print("Sentence: You, give it to me straight")
    print("Parsed components:")
    for slot, data in result2.items():
        value = data[0]['value']
        print(f"  {slot}: '{value}'")

if __name__ == "__main__":
    test_parsing()
