#!/usr/bin/env python3
"""AdverbHandler出力形式確認用デバッグスクリプト"""

from adverb_handler import AdverbHandler

def test_adverb_handler():
    """AdverbHandlerの実際の出力形式を確認"""
    handler = AdverbHandler()
    
    test_cases = [
        'who runs fast',
        'The man who runs fast',
        'who works here'
    ]
    
    for test_text in test_cases:
        print(f"\n=== テスト: '{test_text}' ===")
        result = handler.process(test_text)
        print(f"結果: {result}")
        
        if result.get('success'):
            print(f"success: {result['success']}")
            print(f"separated_text: {result.get('separated_text', 'なし')}")
            print(f"modifiers: {result.get('modifiers', 'なし')}")
            
            # M2キーの詳細確認
            modifiers = result.get('modifiers', {})
            if isinstance(modifiers, dict):
                print(f"modifiersのキー: {list(modifiers.keys())}")
                if 'M2' in modifiers:
                    print(f"M2値: '{modifiers['M2']}'")
                else:
                    print("M2キーが存在しません")
            else:
                print(f"modifiersが辞書ではありません: {type(modifiers)}")

if __name__ == "__main__":
    test_adverb_handler()
