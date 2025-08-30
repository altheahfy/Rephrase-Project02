#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from relative_adverb_handler import RelativeAdverbHandler

def test_failed_cases():
    """失敗した関係副詞ケースをテスト"""
    handler = RelativeAdverbHandler()

    # 失敗した5ケースをテスト
    test_cases = [
        ('The time when everything will change is approaching.', 
         {'S': '', 'Aux': 'is', 'V': 'approaching'}, 
         {'sub-m2': 'The time when', 'sub-s': 'everything', 'sub-aux': 'will', 'sub-v': 'change', '_parent_slot': 'S'}),
        
        ('The moment when he told her the truth changed everything.',
         {'S': '', 'V': 'changed', 'O1': 'everything'},
         {'sub-m2': 'The moment when', 'sub-s': 'he', 'sub-v': 'told', 'sub-o1': 'her', 'sub-o2': 'the truth', '_parent_slot': 'S'}),
         
        ('The reason why she was upset became clear.',
         {'S': '', 'V': 'became', 'C1': 'clear'},
         {'sub-m2': 'The reason why', 'sub-s': 'she', 'sub-aux': 'was', 'sub-v': 'upset', '_parent_slot': 'S'}),
         
        ('The city where we spent our honeymoon is in Italy.',
         {'S': '', 'V': 'is', 'M2': 'in Italy'},
         {'sub-m2': 'The city where', 'sub-s': 'we', 'sub-v': 'spent', 'sub-o1': 'our honeymoon', '_parent_slot': 'S'}),
         
        ('The method how they solved the problem was innovative.',
         {'S': '', 'V': 'was', 'C1': 'innovative'},
         {'sub-m2': 'The method how', 'sub-s': 'they', 'sub-v': 'solved', 'sub-o1': 'the problem', '_parent_slot': 'S'})
    ]

    success_count = 0
    for i, (sentence, expected_main, expected_sub) in enumerate(test_cases, 116):
        print(f'\n=== Case {i}: {sentence} ===')
        result = handler.detect_relative_adverb(sentence)
        
        if result and result.get('success'):
            actual_main = result['main_slots']
            actual_sub = result['sub_slots']
            
            # 主節比較
            main_match = True
            for key, value in expected_main.items():
                if actual_main.get(key) != value:
                    main_match = False
                    break
            
            # 従節比較
            sub_match = True
            for key, value in expected_sub.items():
                if actual_sub.get(key) != value:
                    sub_match = False
                    break
            
            if main_match and sub_match:
                print(f'✅ 成功: {result["relative_adverb"]}')
                success_count += 1
            else:
                print(f'❌ 部分失敗: {result["relative_adverb"]}')
                if not main_match:
                    print(f'   主節不一致: 期待={expected_main}, 実際={actual_main}')
                if not sub_match:
                    print(f'   従節不一致: 期待={expected_sub}, 実際={actual_sub}')
        else:
            print('❌ 失敗: 関係副詞が検出されませんでした')
    
    print(f'\n🎯 結果: {success_count}/5 ケース成功')
    return success_count == 5

if __name__ == '__main__':
    test_failed_cases()
