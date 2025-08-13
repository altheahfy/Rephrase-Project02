#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modal Engine GitHub版テスト
"""

from engines.modal_engine import ModalEngine

def main():
    engine = ModalEngine()

    test_cases = [
        'I can swim.',                  # 能力
        'You must go.',                 # 必要性
        'She will come.',               # 未来/意思
        'He should study.',             # 助言
        'They might be late.',          # 可能性
        'We could help.',               # 可能性/提案
        'I have to work.',              # 半助動詞（義務）
        'She is able to run.',          # 半助動詞（能力）
        'You need to eat.',             # 半助動詞（必要）
        'The cat sits.'                 # 助動詞なし
    ]

    print('=== 🔧 Modal Engine GitHub版機能テスト ===')
    for text in test_cases:
        print(f'\n入力: {text}')
        try:
            result = engine.process(text)
            print(f'結果: {result}')
            
            # スロット内容詳細表示
            for key, value in result.items():
                if key not in ['modal_function', 'certainty_level', 'formality_level']:
                    print(f'  {key}: "{value}"')
        except Exception as e:
            print(f'エラー: {e}')
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
