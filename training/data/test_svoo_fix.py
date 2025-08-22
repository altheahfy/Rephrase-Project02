#!/usr/bin/env python3
"""
SVOO文型のテスト
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_svoo():
    """SVOO文型の修正をテスト"""
    mapper = DynamicGrammarMapper()
    
    test_sentences = [
        "I gave him a book.",
        "She told me a story.",
        "He bought her flowers."
    ]
    
    for sentence in test_sentences:
        print(f"=== {sentence} ===")
        result = mapper.analyze_sentence(sentence)
        slots = result.get('main_slots', {})
        
        for slot, phrase in slots.items():
            print(f"  {slot}: '{phrase}'")
        print()

if __name__ == "__main__":
    test_svoo()
