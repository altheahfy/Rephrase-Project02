#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Final test for all "give it straight" sentences

import os
import sys
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_all_sentences():
    """4つの文すべてをテスト"""
    
    sentences = [
        "You, give it to me straight.",
        "You, give it to him straight.", 
        "You, give it to her straight.",
        "You, give it to them straight."
    ]
    
    parser = RephraseParsingEngine()
    
    print("=== Give It Straight 修正確認テスト ===\n")
    
    for i, sentence in enumerate(sentences, 1):
        print(f"【テスト{i}】: {sentence}")
        result = parser.analyze_sentence(sentence)
        
        if 'M2' in result:
            m2_info = result['M2'][0]
            phrase = m2_info['value']
            phrase_type = m2_info['type']
            status = "✅ WORD" if phrase_type == "word" else "❌ PHRASE"
            print(f"  M2: '{phrase}' → {phrase_type} {status}")
        else:
            print("  M2スロットが見つかりません ❌")
        print()

if __name__ == "__main__":
    test_all_sentences()
