#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def test_central_controller_relative_adverbs():
    """CentralController経由で関係副詞をテスト"""
    controller = CentralController()

    # 失敗した関係副詞5ケースをテスト
    test_cases = [
        'The time when everything will change is approaching.',
        'The moment when he told her the truth changed everything.',
        'The reason why she was upset became clear.',
        'The city where we spent our honeymoon is in Italy.',
        'The method how they solved the problem was innovative.'
    ]

    success_count = 0
    for i, sentence in enumerate(test_cases, 116):
        print(f'\n=== Case {i}: {sentence} ===')
        try:
            result = controller.process_sentence(sentence)
            if result.get('success'):
                print(f'✅ 成功')
                main_slots = result.get('main_slots', {})
                sub_slots = result.get('sub_slots', {})
                print(f'主節: {main_slots}')
                print(f'従節: {sub_slots}')
                success_count += 1
            else:
                print(f'❌ 失敗: {result}')
        except Exception as e:
            print(f'❌ 例外: {e}')
    
    print(f'\n🎯 結果: {success_count}/5 ケース成功')
    return success_count == 5

if __name__ == '__main__':
    test_central_controller_relative_adverbs()
