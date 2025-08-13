#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
関係代名詞エンジン機能テスト
"""

from engines.simple_relative_engine import SimpleRelativeEngine

def main():
    engine = SimpleRelativeEngine()

    test_cases = [
        'The book that I read is good.',        # 限定用法
        'The man who lives there is tall.',     # 主格関係代名詞
        'The car which I bought is red.',       # 目的格関係代名詞
        'The house where I live is big.',       # 関係副詞
        'My friend, who is a doctor, helps me.', # 非限定用法（コンマ有り）
        'The cat sits.',                        # 関係代名詞なし
        'The woman that works here is kind.'    # that関係代名詞
    ]

    print('=== 👥 関係代名詞エンジン機能テスト ===')
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
