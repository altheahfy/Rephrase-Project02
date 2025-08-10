#!/usr/bin/env python3
from step13_o1_subslot_new import O1SubslotGenerator

def main():
    gen = O1SubslotGenerator()
    
    test_cases = [
        ('making her crazy for him', 'clause'),
        ('to make the project successful', 'phrase'), 
        ('running very fast in the park', 'phrase'),
        ('books on the table in the library', 'word'),
        ('students studying abroad this year', 'phrase')
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
