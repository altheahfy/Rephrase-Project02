#!/usr/bin/env python3
"""
V2システムのスロット分解機能デバッグ
"""

from basic_five_pattern_handler import BasicFivePatternHandler

def test_basic_handler():
    print("=== BasicFivePatternHandler テスト ===")
    
    handler = BasicFivePatternHandler()
    test_sentences = [
        "The car is red.",
        "I love you.", 
        "Birds fly."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 テスト: '{sentence}'")
        try:
            # processメソッドを使用
            result = handler.process(sentence)
            print(f"   結果タイプ: {type(result)}")
            print(f"   結果: {result}")
            
            if result:
                print(f"   success: {result.get('success', False)}")
                print(f"   main_slots: {result.get('main_slots', {})}")
                print(f"   slots: {result.get('slots', {})}")
                print(f"   全キー: {list(result.keys())}")
            else:
                print("   結果がNoneまたは空")
                
        except Exception as e:
            print(f"   エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_basic_handler()
