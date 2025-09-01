#!/usr/bin/env python3
from noun_clause_handler import NounClauseHandler

def test_complete_process():
    print("=== Case 119 Complete Process Test ===")
    
    handler = NounClauseHandler()
    sentence = "It depends on if you agree."
    
    print(f"Target: '{sentence}'")
    
    result = handler.process(sentence)
    
    print(f"\n=== Complete Process Result ===")
    print(f"Success: {result.get('success')}")
    print(f"Main slots: {result.get('main_slots')}")
    print(f"Sub slots: {result.get('sub_slots')}")
    
    # Expected structure check
    expected_main = {"S": "It", "V": "depends", "M2": ""}
    expected_sub = {"sub-s": "on if you", "sub-v": "agree", "_parent_slot": "M2"}
    
    print(f"\n=== Expected vs Actual ===")
    print(f"Expected main: {expected_main}")
    print(f"Expected sub: {expected_sub}")
    
    return result

if __name__ == "__main__":
    test_complete_process()
