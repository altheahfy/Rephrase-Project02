#!/usr/bin/env python3
from central_controller import CentralController

def test_case_141():
    print("=== Case 141 順序付与テスト ===")
    
    controller = CentralController()
    sentence = "If I were rich, I would travel around the world."
    
    result = controller.process_sentence(sentence)
    
    print(f"Success: {result.get('success')}")
    print(f"Main slots: {result.get('main_slots')}")
    print(f"Sub slots: {result.get('sub_slots')}")
    print(f"Ordered slots: {result.get('ordered_slots')}")
    
    return result

if __name__ == "__main__":
    test_case_141()
