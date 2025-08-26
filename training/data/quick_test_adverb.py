#!/usr/bin/env python3
"""AdverbHandler動作確認テスト"""

from adverb_handler import AdverbHandler

def test_adverb_handler():
    handler = AdverbHandler()
    test_cases = ['who runs fast', 'which I bought']

    for test in test_cases:
        result = handler.process(test)
        status = '✅' if result.get('success') else '❌'
        print(f'{status} "{test}" -> success: {result.get("success")}')
        if not result.get('success'):
            print(f'    エラー: {result.get("error")}')

if __name__ == "__main__":
    test_adverb_handler()
