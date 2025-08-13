#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
受動態エンジン機能テスト
"""

from engines.passive_voice_engine import PassiveVoiceEngine

def main():
    engine = PassiveVoiceEngine()

    test_cases = [
        'The book was written by him.',         # by句付き受動態
        'The house was built.',                 # by句なし受動態
        'The work is being done.',              # 進行受動態
        'The project will be completed.',       # 未来受動態
        'The letter has been sent.',            # 完了受動態
        'The cat is fed.',                      # 短い受動態
        'They are loved by everyone.',          # 複数主語受動態
        'The cake was eaten by the children.',  # 複数動作主
        'The cat sits.',                        # 受動態なし（能動態）
        'I write a book.'                       # 受動態なし（能動態）
    ]

    print('=== 🔄 受動態エンジン機能テスト ===')
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
