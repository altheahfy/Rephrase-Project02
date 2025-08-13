#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
接続詞エンジン機能テスト
"""

from engines.stanza_based_conjunction_engine import StanzaBasedConjunctionEngine

def main():
    engine = StanzaBasedConjunctionEngine()

    test_cases = [
        'I study because I want to learn.',
        'If it rains, I will stay home.',
        'She left before he arrived.',
        'I will go unless you stop me.',
        'The cat sits.',  # 接続詞なしケース
        'Although it was difficult, I finished the task.'
    ]

    print('=== 🔗 接続詞エンジン機能テスト ===')
    for text in test_cases:
        print(f'\n入力: {text}')
        try:
            result = engine.process(text)
            print(f'結果: {result}')
            
            # スロット内容詳細表示
            for key, value in result.items():
                print(f'  {key}: "{value}"')
        except Exception as e:
            print(f'エラー: {e}')

if __name__ == "__main__":
    main()
