#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_vocative_parsing():
    """呼びかけ文の解析テスト"""
    engine = CompleteRephraseParsingEngine()
    
    test_sentences = [
        "You, give it to me straight.",
        "You, give that to him clearly.",
        "You, give this to her honestly.",
        "You, give them to us directly."
    ]
    
    for sentence in test_sentences:
        print(f"\n=== Testing: {sentence} ===")
        result = engine.analyze_sentence(sentence)
        
        if 'slots' in result:
            print("スロット解析結果:")
            for slot_type, slot_data in result['slots'].items():
                print(f"  {slot_type}: {slot_data}")
        else:
            print("解析失敗:", result)

if __name__ == "__main__":
    test_vocative_parsing()
