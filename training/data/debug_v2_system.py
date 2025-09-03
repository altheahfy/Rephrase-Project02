#!/usr/bin/env python3
"""
V2システムのprocess_sentenceメソッドを直接テスト
"""

from central_controller_v2 import CentralControllerV2

def test_v2_system():
    print("=== V2システム直接テスト ===")
    
    controller_v2 = CentralControllerV2()
    test_sentences = [
        "The car is red.",
        "I love you.",
        "Birds fly."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 テスト: '{sentence}'")
        try:
            result = controller_v2.process_sentence(sentence)
            print(f"   結果: {result}")
            print(f"   main_slots: {result.get('main_slots', {})}")
            print(f"   sub_slots: {result.get('sub_slots', {})}")
        except Exception as e:
            print(f"   エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_v2_system()
