#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
spaCyベース句動詞自動検出システムのテスト
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_spacy_based_phrasal_verbs():
    print("=== spaCyベース句動詞自動検出システムテスト ===")
    
    parser = RephraseParsingEngine()
    
    test_cases = [
        # 分離可能句動詞 - 非分離型
        "Write down the sentence",
        "Turn off the light",
        "Look up the word",
        "Put on your shoes",
        "Take off your coat",
        
        # 分離可能句動詞 - 分離型  
        "Write the sentence down",
        "Turn the light off", 
        "Look the word up",
        "Put your shoes on",
        "Take your coat off",
        
        # 呼びかけ付き句動詞
        "You, write the sentence down",
        "John, turn off the light",
        
        # より複雑な例
        "Please write down all the important information",
        "Can you turn the music down?",
    ]
    
    for sentence in test_cases:
        print(f"\n--- '{sentence}' ---")
        result = parser.analyze_sentence(sentence)
        
        if result:
            print("Parsed components:")
            for slot, data in result.items():
                value = data[0]['value']
                slot_type = data[0].get('type', 'unknown')
                print(f"  {slot}: '{value}' (type: {slot_type})")
                
            # 期待される構造: V + O1 + M2 (particle)
            has_verb = 'V' in result
            has_object = 'O1' in result
            has_particle = 'M2' in result and any('phrasal_verb_particle' in str(d) for d in result['M2'])
            
            if has_verb and has_particle:
                print("  ✅ 句動詞構造検出成功")
                if has_object:
                    print("  ✅ 目的語も正しく分離")
            else:
                print("  ❌ 句動詞検出失敗")
        else:
            print("  ❌ 解析失敗")

if __name__ == "__main__":
    test_spacy_based_phrasal_verbs()
