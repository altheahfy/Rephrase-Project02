#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
句動詞での主語・目的語欠落問題のデバッグ
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine
import spacy

def debug_missing_components():
    print("=== 句動詞での主語・目的語欠落問題のデバッグ ===")
    
    # spaCy直接分析
    nlp = spacy.load("en_core_web_sm")
    sentence = "Could you write it down"
    doc = nlp(sentence)
    
    print(f"Sentence: '{sentence}'")
    print("spaCy token analysis:")
    for token in doc:
        print(f"  {token.text:<8} POS:{token.pos_:<6} DEP:{token.dep_:<8} HEAD:{token.head.text}")
    
    print("\nDependency relationships:")
    for token in doc:
        if token.dep_ == "nsubj":
            print(f"  SUBJECT: {token.text} -> {token.head.text}")
        elif token.dep_ == "dobj": 
            print(f"  DIRECT OBJECT: {token.text} -> {token.head.text}")
        elif token.dep_ == "prt":
            print(f"  PARTICLE: {token.text} -> {token.head.text}")
        elif token.dep_ == "aux":
            print(f"  AUXILIARY: {token.text} -> {token.head.text}")
    
    # パーサー結果
    print("\n" + "="*50)
    parser = RephraseParsingEngine()
    result = parser.analyze_sentence(sentence)
    
    print("Parser result:")
    for slot, data in result.items():
        value = data[0]['value']
        slot_type = data[0].get('type', 'unknown')
        print(f"  {slot}: '{value}' (type: {slot_type})")
    
    print(f"\n❌ Missing components:")
    expected = {"Aux": "Could", "S": "you", "V": "write", "O1": "it", "M2": "down"}
    for slot, expected_value in expected.items():
        if slot not in result:
            print(f"  {slot}: Expected '{expected_value}' - NOT FOUND")
        elif result[slot][0]['value'] != expected_value:
            actual = result[slot][0]['value']
            print(f"  {slot}: Expected '{expected_value}' - Got '{actual}'")

if __name__ == "__main__":
    debug_missing_components()
