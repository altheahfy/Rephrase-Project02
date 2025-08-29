#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用システムテスト（新しいシンプル実装）
"""

from absolute_order_manager_universal import AbsoluteOrderManagerUniversal

def test_tell_group():
    """
    tellグループのテスト
    """
    print("🧪 Testing Tell Group")
    
    # tellグループ母集団
    tell_sentences = [
        {
            "sentence": "What did he tell her at the store?",
            "slots": {"O2": "What", "Aux": "did", "S": "he", "V": "tell", "O1": "her", "M2": "at the store"}
        },
        {
            "sentence": "Did he tell her a secret there?", 
            "slots": {"Aux": "Did", "S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M2": "there"}
        },
        {
            "sentence": "Where did you tell me a story?",
            "slots": {"M2": "Where", "Aux": "did", "S": "you", "V": "tell", "O1": "me", "O2": "a story"}
        },
        {
            "sentence": "Did I tell him a truth in the kitchen?",
            "slots": {"Aux": "Did", "S": "I", "V": "tell", "O1": "him", "O2": "a truth", "M2": "in the kitchen"}
        }
    ]
    
    manager = AbsoluteOrderManagerUniversal()
    
    # テストケース1: What疑問詞
    print("\n📋 Test Case 1: What did he tell her at the store?")
    test_slots = {"O2": "What", "Aux": "did", "S": "he", "V": "tell", "O1": "her", "M2": "at the store"}
    result = manager.process_group(tell_sentences, test_slots)
    expected = {'O2': 2, 'Aux': 3, 'S': 4, 'V': 5, 'O1': 6, 'M2': 8}
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print(f"Match: {'✅' if result == expected else '❌'}")
    
    # テストケース2: 標準文
    print("\n📋 Test Case 2: Did he tell her a secret there?")
    test_slots = {"Aux": "Did", "S": "he", "V": "tell", "O1": "her", "O2": "a secret", "M2": "there"}
    result = manager.process_group(tell_sentences, test_slots)
    expected = {'Aux': 3, 'S': 4, 'V': 5, 'O1': 6, 'O2': 7, 'M2': 8}
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print(f"Match: {'✅' if result == expected else '❌'}")
    
    # テストケース3: Where疑問詞
    print("\n📋 Test Case 3: Where did you tell me a story?")
    test_slots = {"M2": "Where", "Aux": "did", "S": "you", "V": "tell", "O1": "me", "O2": "a story"}
    result = manager.process_group(tell_sentences, test_slots)
    expected = {'M2': 1, 'Aux': 3, 'S': 4, 'V': 5, 'O1': 6, 'O2': 7}
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print(f"Match: {'✅' if result == expected else '❌'}")

def test_simple_group():
    """
    シンプルなグループのテスト（gaveグループ相当）
    """
    print("\n\n🧪 Testing Simple Group (gave-style)")
    
    # シンプルなグループ母集団
    simple_sentences = [
        {
            "sentence": "She gave him money",
            "slots": {"S": "She", "V": "gave", "O1": "him", "O2": "money"}
        },
        {
            "sentence": "I gave you a book",
            "slots": {"S": "I", "V": "gave", "O2": "a book", "O1": "you"}
        }
    ]
    
    manager = AbsoluteOrderManagerUniversal()
    
    print("\n📋 Test Case: She gave him money")
    test_slots = {"S": "She", "V": "gave", "O1": "him", "O2": "money"}
    result = manager.process_group(simple_sentences, test_slots)
    expected = {'S': 1, 'V': 2, 'O1': 3, 'O2': 4}
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print(f"Match: {'✅' if result == expected else '❌'}")

if __name__ == "__main__":
    test_tell_group()
    test_simple_group()
