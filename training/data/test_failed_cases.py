#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def test_failed_cases():
    """Test the 5 failed cases"""
    
    controller = CentralController()
    
    failed_cases = [
        (141, "Should you need help, please call me."),
        (147, "Unless you study hard, you won't pass the exam."),
        (148, "As if I didn't know that already."),
        (151, "But for your help, I would have failed."),
        (152, "Without your support, we couldn't have succeeded.")
    ]
    
    for case_num, sentence in failed_cases:
        print(f"\n🎯 Testing Case {case_num}")
        print(f"Sentence: {sentence}")
        print("="*60)
        
        try:
            result = controller.process_sentence(sentence)
            if result.get('success', False):
                print("✅ SUCCESS")
                print(f"Main slots: {result.get('main_slots', {})}")
                print(f"Sub slots: {result.get('sub_slots', {})}")
            else:
                print("❌ FAILED")
                print(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    test_failed_cases()
