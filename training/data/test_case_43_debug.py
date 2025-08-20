#!/usr/bin/env python3
"""
Case 43副詞重複エラーの解析
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_case_43():
    """Case 43: She very carefully planned the surprise party."""
    
    # Initialize mapper
    mapper = UnifiedStanzaRephraseMapper()
    
    # Test sentence
    sentence = "She very carefully planned the surprise party."
    print(f"=== Case 43分析 ===")
    print(f"文: {sentence}")
    
    # Process
    result = mapper.process(sentence)
    
    print(f"実際結果: {result}")
    
    # Expected result
    expected = {
        "S": "She",
        "V": "planned", 
        "O": "the surprise party",
        "M2": "very carefully"  # Should be combined, not duplicated
    }
    
    print(f"期待結果: {expected}")
    
    # Check for issue
    main_slots = {k:v for k,v in result.items() if not k.startswith('sub-')}
    
    # Look for M1/M2 duplication
    if 'M1' in main_slots and 'M2' in main_slots:
        m1_val = main_slots['M1']
        m2_val = main_slots['M2']
        print(f"副詞重複検出: M1='{m1_val}', M2='{m2_val}'")
        
        # Check if there's word overlap
        m1_words = set(m1_val.split())
        m2_words = set(m2_val.split())
        overlap = m1_words & m2_words
        if overlap:
            print(f"重複語彙: {overlap}")
    
    return result

if __name__ == "__main__":
    test_case_43()
