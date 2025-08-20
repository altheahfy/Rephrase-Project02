#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def calculate_accuracy(expected, actual):
    """Calculate accuracy between expected and actual results"""
    total_slots = 0
    matching_slots = 0
    
    # Check main slots
    for slot in ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2']:
        total_slots += 1
        expected_val = expected.get('main_slots', {}).get(slot, '')
        actual_val = actual.get('slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    # Check sub slots
    for slot in ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2']:
        total_slots += 1
        expected_val = expected.get('sub_slots', {}).get(slot, '')
        actual_val = actual.get('sub_slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    return matching_slots / total_slots if total_slots > 0 else 0.0

def test_case_28():
    """Test case 28 specifically"""
    
    # Load test data
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Get case 28
    test_case = test_data['data']['28']
    sentence = test_case['sentence']
    expected = test_case['expected']
    
    print(f"Testing case 28: {sentence}")
    print(f"Expected:")
    print(f"  Main slots: {expected['main_slots']}")
    print(f"  Sub-slots: {expected['sub_slots']}")
    
    # Initialize mapper
    mapper = UnifiedStanzaRephraseMapper()
    
    # Process sentence
    actual = mapper.process(sentence)
    
    print(f"Actual:")
    print(f"  Slots: {actual['slots']}")
    print(f"  Sub-slots: {actual['sub_slots']}")
    
    # Calculate accuracy
    accuracy = calculate_accuracy(expected, actual)
    
    print(f"Accuracy: {accuracy:.3f} ({accuracy:.1%})")
    
    # Detailed comparison
    print("\nDetailed comparison:")
    for slot in ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2']:
        expected_val = expected.get('main_slots', {}).get(slot, '')
        actual_val = actual.get('slots', {}).get(slot, '')
        match = "✓" if expected_val == actual_val else "✗"
        print(f"  {slot}: {expected_val} -> {actual_val} {match}")
        
    for slot in ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2']:
        expected_val = expected.get('sub_slots', {}).get(slot, '')
        actual_val = actual.get('sub_slots', {}).get(slot, '')
        match = "✓" if expected_val == actual_val else "✗"
        print(f"  {slot}: {expected_val} -> {actual_val} {match}")

if __name__ == "__main__":
    test_case_28()
