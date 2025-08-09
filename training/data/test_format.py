#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simplified test for parsing engine return format

import os
import sys
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_return_format():
    """パーサーの戻り値形式を確認"""
    
    parser = RephraseParsingEngine()
    sentence = "You, give it to me straight."
    
    print(f"テスト文: {sentence}")
    print("-" * 50)
    
    result = parser.analyze_sentence(sentence)
    
    print(f"戻り値の型: {type(result)}")
    print(f"戻り値: {result}")
    
    if isinstance(result, dict):
        print("\n辞書形式の戻り値:")
        for key, value in result.items():
            print(f"  {key}: {value} (type: {type(value)})")

if __name__ == "__main__":
    test_return_format()
