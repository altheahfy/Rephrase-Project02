#!/usr/bin/env python3
"""AdverbHandler の各種ケーステスト"""

from adverb_handler import AdverbHandler

def test_adverb_handler():
    """副詞ハンドラーの課題となるケースをテスト"""
    handler = AdverbHandler()

    test_cases = [
        'who runs fast',           # 成功例
        'which lies there',        # 成功例  
        'that works here',         # 成功例
        'which I bought',          # 修飾語なし（正常）
        'whom I met',              # 修飾語なし（正常）
        'that he drives',          # 修飾語なし（正常）
    ]

    print('=== AdverbHandler 100%テスト ===')
    success_count = 0
    
    for i, test in enumerate(test_cases, 1):
        result = handler.process(test)
        status = '✅' if result.get('success') else '❌'
        print(f'{i:2d}. {status} "{test}"')
        
        if result.get('success'):
            success_count += 1
            modifiers = result.get('modifiers', {})
            if modifiers:
                print(f'     修飾語: {modifiers}')
            else:
                print(f'     修飾語なし（期待通り）')
        else:
            print(f'     エラー: {result.get("error", "不明")}')
        print()
    
    print(f'成功率: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)')

if __name__ == "__main__":
    test_adverb_handler()
