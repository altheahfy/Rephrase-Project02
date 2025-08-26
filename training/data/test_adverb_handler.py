#!/usr/bin/env python3
"""
AdverbHandler テストスクリプト
"""

import sys
sys.path.append('.')

from adverb_handler import AdverbHandler

def test_adverb_handler():
    """AdverbHandler の基本テスト"""
    handler = AdverbHandler()
    
    # テストケース
    test_cases = [
        "The man runs fast",
        "The book lies there", 
        "The person works here",
        "He runs very quickly",
        "She sings beautifully at home",
        "They work hard every day"
    ]
    
    print("🚀 AdverbHandler テスト開始")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 テストケース {i}: {text}")
        result = handler.process(text)
        
        if result['success']:
            print(f"✅ 成功")
            print(f"   分離後: {result['separated_text']}")
            print(f"   修飾語: {result['modifiers']}")
            print(f"   動詞位置: {result['verb_positions']}")
        else:
            print(f"❌ 失敗: {result['error']}")
    
    print("\n" + "=" * 50)
    print("🏁 AdverbHandler テスト終了")

if __name__ == "__main__":
    test_adverb_handler()
