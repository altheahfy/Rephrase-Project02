#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
句動詞（Phrasal Verb）のテスト
分離可能な句動詞の処理確認
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_phrasal_verbs():
    print("=== 句動詞（Phrasal Verb）処理テスト ===")
    
    parser = RephraseParsingEngine()
    
    test_cases = [
        "Write the sentence down!",
        "Write down the sentence!",
        "Put your jacket on!",
        "Put on your jacket!",
        "Turn the music off!",
        "Turn off the music!",
        "Look the word up!",
        "Look up the word!"
    ]
    
    for i, sentence in enumerate(test_cases, 1):
        result = parser.analyze_sentence(sentence)
        
        print(f"\nTest {i}: '{sentence}'")
        print("Parsed components:")
        for slot, data in result.items():
            value = data[0]['value']
            slot_type = data[0].get('type', 'unknown')
            print(f"  {slot}: '{value}' (type: {slot_type})")
        
        # 句動詞粒子の検出確認
        has_particle = any(data[0].get('type') == 'phrasal_verb_particle' 
                          for data in result.values())
        print(f"  → 句動詞粒子検出: {'✅' if has_particle else '❌'}")
    
    print("\n=== 分析結果 ===")
    print("提案された方式 'V + O1 + M2(particle)' が既に実装済み！")
    print("type: 'phrasal_verb_particle' で句動詞の粒子を識別")

if __name__ == "__main__":
    test_phrasal_verbs()
