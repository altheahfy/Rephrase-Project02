#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import logging

def test_53_safe():
    # Suppress verbose logs
    logging.basicConfig(level=logging.ERROR)
    
    # Load test data
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    perfect_count = 0
    partial_count = 0
    fail_count = 0
    
    for test_id in range(1, 54):  # Tests 1-53
        test_case = test_data['data'][str(test_id)]
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        # Process sentence
        result = mapper.process(sentence)
        
        # Extract results
        main_result = result.get('slots', {})
        sub_result = result.get('sub_slots', {})
        
        # Extract expected
        main_expected = expected['main_slots']
        sub_expected = expected['sub_slots']
        
        # Compare results
        main_match = (main_result == main_expected)
        sub_match = (sub_result == sub_expected)
        
        if main_match and sub_match:
            status = "PERFECT"
            perfect_count += 1
        elif main_match or sub_match:
            status = "PARTIAL" 
            partial_count += 1
        else:
            status = "FAIL"
            fail_count += 1
        
        print(f"Test{test_id}: {status}")
    
    total = perfect_count + partial_count + fail_count
    accuracy = (perfect_count / total) * 100
    
    print(f"\nResults Summary:")
    print(f"Perfect: {perfect_count}/{total} ({perfect_count/total*100:.1f}%)")
    print(f"Partial: {partial_count}/{total} ({partial_count/total*100:.1f}%)")
    print(f"Failed: {fail_count}/{total} ({fail_count/total*100:.1f}%)")
    print(f"Overall Accuracy: {accuracy:.1f}%")

if __name__ == "__main__":
    test_53_safe()
