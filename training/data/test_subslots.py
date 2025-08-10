#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サブスロット機能の完全テスト
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_complex_sentence_subslots():
    """複文のサブスロット機能をテスト"""
    
    engine = CompleteRephraseParsingEngine()
    
    # テスト文1: 関係詞節
    print("🔍 テスト1: 関係詞節")
    print("=" * 50)
    sentence1 = "The book that I bought yesterday is very interesting."
    result1 = engine.analyze_sentence(sentence1)
    
    print(f"文: {sentence1}")
    print(f"文型: {result1.get('sentence_pattern', '')}")
    print("\n📋 Main Slots:")
    for slot, content in result1['rephrase_slots'].items():
        if content:
            print(f"  {slot}: {content}")
    
    print("\n📋 Sub Structures:")
    for sub in result1.get('sub_structures', []):
        print(f"  Type: {sub['type']}, Verb: {sub['verb']}, Parent: {sub['parent_element']}")
        print("  Sub-slots:")
        for slot, content in sub['sub_slots'].items():
            if content:
                print(f"    {slot}: {content}")
    
    # テスト文2: 副詞節
    print("\n\n🔍 テスト2: 副詞節")
    print("=" * 50)
    sentence2 = "When I arrived at the station quickly, the train had already left."
    result2 = engine.analyze_sentence(sentence2)
    
    print(f"文: {sentence2}")
    print(f"文型: {result2.get('sentence_pattern', '')}")
    print("\n📋 Main Slots:")
    for slot, content in result2['rephrase_slots'].items():
        if content:
            print(f"  {slot}: {content}")
    
    print("\n📋 Sub Structures:")
    for sub in result2.get('sub_structures', []):
        print(f"  Type: {sub['type']}, Verb: {sub['verb']}, Parent: {sub.get('parent_element', 'None')}")
        print("  Sub-slots:")
        for slot, content in sub['sub_slots'].items():
            if content:
                print(f"    {slot}: {content}")
    
    # テスト文3: 複合複文
    print("\n\n🔍 テスト3: 複合複文")
    print("=" * 50)
    sentence3 = "The student who studies hard in the library will pass the exam that is scheduled next week."
    result3 = engine.analyze_sentence(sentence3)
    
    print(f"文: {sentence3}")
    print(f"文型: {result3.get('sentence_pattern', '')}")
    print("\n📋 Main Slots:")
    for slot, content in result3['rephrase_slots'].items():
        if content:
            print(f"  {slot}: {content}")
    
    print("\n📋 Sub Structures:")
    for i, sub in enumerate(result3.get('sub_structures', []), 1):
        print(f"  Sub Structure {i}:")
        print(f"    Type: {sub['type']}, Verb: {sub['verb']}, Parent: {sub.get('parent_element', 'None')}")
        print("    Sub-slots:")
        for slot, content in sub['sub_slots'].items():
            if content:
                print(f"      {slot}: {content}")

if __name__ == "__main__":
    test_complex_sentence_subslots()
