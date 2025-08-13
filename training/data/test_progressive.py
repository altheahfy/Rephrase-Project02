#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
進行形エンジン機能テスト
"""

from engines.progressive_tenses_engine import ProgressiveTensesEngine

def main():
    engine = ProgressiveTensesEngine()

    test_cases = [
        'I am eating breakfast.',           # 現在進行形
        'She is reading a book.',           # 現在進行形（三人称）
        'They are playing soccer.',         # 現在進行形（複数）
        'He was writing a letter.',         # 過去進行形
        'We were watching TV.',             # 過去進行形（複数）
        'I will be traveling tomorrow.',    # 未来進行形
        'She has been studying.',           # 現在完了進行形
        'They had been working.',           # 過去完了進行形
        'I am being tested.',               # 受動進行形
        'The cat sits.',                    # 進行形なし
        'I eat breakfast every day.'        # 進行形なし（習慣）
    ]

    print('=== 🔄 進行形エンジン機能テスト ===')
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
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
