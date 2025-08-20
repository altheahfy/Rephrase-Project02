#!/usr/bin/env python3
"""
Case 13, 14のwhose構文copula問題の詳細分析
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_case_13_14():
    """Case 13: The student whose book I borrowed is smart."""
    """Case 14: The woman whose dog barks is my neighbor."""
    
    # Initialize mapper
    mapper = UnifiedStanzaRephraseMapper()
    
    # Test cases
    test_cases = [
        {
            "id": 13,
            "sentence": "The student whose book I borrowed is smart.",
            "expected": {
                "S": "",
                "V": "is", 
                "C1": "smart"
            },
            "expected_sub": {
                "sub-s": "The student whose book",
                "sub-o1": "I", 
                "sub-v": "borrowed"
            }
        },
        {
            "id": 14,
            "sentence": "The woman whose dog barks is my neighbor.",
            "expected": {
                "S": "",
                "V": "is",
                "C1": "my neighbor"  
            },
            "expected_sub": {
                "sub-s": "The woman whose dog",
                "sub-v": "barks"
            }
        }
    ]
    
    for case in test_cases:
        print(f"=== Case {case['id']} 分析 ===")
        print(f"文: {case['sentence']}")
        
        # Process
        result = mapper.process(case['sentence'])
        
        actual_main = result['slots']
        actual_sub = result['sub_slots']
        
        print(f"実際メイン: {actual_main}")
        print(f"実際サブ: {actual_sub}")
        print(f"期待メイン: {case['expected']}")
        print(f"期待サブ: {case['expected_sub']}")
        
        # Check V and C1 slots specifically
        actual_v = actual_main.get('V', '(not present)')
        actual_c1 = actual_main.get('C1', '(not present)')
        expected_v = case['expected'].get('V', '(not present)')
        expected_c1 = case['expected'].get('C1', '(not present)')
        
        print(f"V比較: 実際='{actual_v}' vs 期待='{expected_v}' ({'✓' if actual_v == expected_v else '✗'})")
        print(f"C1比較: 実際='{actual_c1}' vs 期待='{expected_c1}' ({'✓' if actual_c1 == expected_c1 else '✗'})")
        
        print()

if __name__ == "__main__":
    test_case_13_14()
