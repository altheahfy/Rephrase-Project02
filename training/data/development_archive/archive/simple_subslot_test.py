#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡単なサブスロットテスト
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def simple_test():
    print("=== 簡単なサブスロットテスト ===\n")
    
    engine = CompleteRephraseParsingEngine()
    
    sentence = 'The boy who plays soccer is my friend.'
    print(f"テスト文: {sentence}")
    
    result = engine.analyze_sentence(sentence)
    
    print("\n=== 結果の完全構造 ===")
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    simple_test()
