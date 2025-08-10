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
        ('give him a book', 'phrase'),  # sub-o1: him, sub-o2: a book
        ('giving him a book', 'phrase'),  # sub-o1: him, sub-o2: a book
        ('send her the letter', 'phrase'),  # sub-o1: her, sub-o2: the letter
        ('becoming very tired', 'phrase'),  # sub-c2: tired
        # 第5文型SVOC構造テスト用追加
        ('I saw her cry', 'phrase'),  # sub-s: I, sub-v: saw, sub-o1: her, sub-c1: cry
        ('I found it interesting', 'phrase'),  # sub-s: I, sub-v: found, sub-o1: it, sub-c1: interesting
        ('They made him happy', 'phrase'),  # sub-s: They, sub-v: made, sub-o1: him, sub-c1: happy
        ('She kept the door open', 'phrase'),  # sub-s: She, sub-v: kept, sub-o1: the door, sub-c1: open
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
