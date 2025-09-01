#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def test_case_143():
    """Test Case 143: I wish I had more time"""
    
    controller = CentralController()
    
    sentence = "I wish I had more time"
    case_number = 143
    
    print(f"🎯 Testing Case {case_number}")
    print(f"Sentence: {sentence}")
    print("="*50)
    
    result = controller.process_sentence(sentence)
    
    print(f"\nResult: {result}")
    
    # Expected sub-slots
    expected_sub_o1 = "more time"
    actual_sub_o1 = result.get("sub_slots", {}).get("sub-o1", "")
    
    print(f"\nExpected sub-o1: '{expected_sub_o1}'")
    print(f"Actual sub-o1: '{actual_sub_o1}'")
    
    if actual_sub_o1 == expected_sub_o1:
        print("✅ PASS: Phrase extraction successful!")
    else:
        print("❌ FAIL: Phrase extraction mismatch!")
    
    return result

if __name__ == "__main__":
    test_case_143()
