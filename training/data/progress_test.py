#!/usr/bin/env python3
from step13_o1_subslot_new import O1SubslotGenerator

def main():
    gen = O1SubslotGenerator()
    
    test_cases = [
        ('making her crazy for him', 'clause'),
        ('to make the project successful', 'phrase'), 
        ('running very fast in the park', 'phrase'),
        ('books on the table in the library', 'word'),
        ('students studying abroad this year', 'phrase'),
        # sub-s（主語スロット）テスト用追加
        ('that he is studying hard', 'clause'),
        ('who studies English daily', 'clause'),
        ('which is on the table', 'clause'),
        ('what happened yesterday', 'clause'),
        # O1O2構造テスト用追加
        ('give him a book', 'phrase'),  # sub-o2: him, sub-o1: a book
        ('giving him a book', 'phrase'),  # sub-o2: him, sub-o1: a book
        ('send her the letter', 'phrase'),  # sub-o2: her, sub-o1: the letter
        ('becoming very tired', 'phrase'),  # sub-c1: tired
    ]
    
    print('=== 現在の完全性テスト結果 ===\n')
    
    for i, (text, phrase_type) in enumerate(test_cases, 1):
        print(f'{i}. "{text}"')
        try:
            result = gen.generate_o1_subslots(text, phrase_type)
            subslot_count = len(result)
            subslots_display = ', '.join([f'{k}:"{v["text"]}"' for k, v in result.items()])
            print(f'   ✅ {subslot_count}サブスロット: {subslots_display}')
        except Exception as e:
            print(f'   ❌ エラー: {e}')
        print()

if __name__ == "__main__":
    main()
