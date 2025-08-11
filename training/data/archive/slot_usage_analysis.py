#!/usr/bin/env python3
from step13_o1_subslot_new import O1SubslotGenerator

def analyze_slot_usage():
    gen = O1SubslotGenerator()
    
    test_cases = [
        ('making her crazy for him', 'clause'),
        ('to make the project successful', 'phrase'), 
        ('running very fast in the park', 'phrase'),
        ('books on the table in the library', 'word'),
        ('students studying abroad this year', 'phrase'),
        ('that he is studying hard', 'clause'),
        ('who studies English daily', 'clause'),
        ('which is on the table', 'clause'),
        ('what happened yesterday', 'clause'),
        ('give him a book', 'phrase'),
        ('giving him a book', 'phrase'),
        ('send her the letter', 'phrase'),
        ('becoming very tired', 'phrase'),
    ]
    
    # 全10スロット
    all_slots = [
        'sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 
        'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux'
    ]
    
    slot_usage = {slot: 0 for slot in all_slots}
    total_tests = len(test_cases)
    
    print('=== 10スロット活用状況分析 ===\n')
    
    for i, (text, phrase_type) in enumerate(test_cases, 1):
        try:
            result = gen.generate_o1_subslots(text, phrase_type)
            used_slots = list(result.keys())
            
            print(f'{i:2d}. "{text}"')
            print(f'    使用スロット({len(used_slots)}): {", ".join(used_slots)}')
            
            # 使用回数カウント
            for slot in used_slots:
                if slot in slot_usage:
                    slot_usage[slot] += 1
            print()
        except Exception as e:
            print(f'{i:2d}. "{text}" - エラー: {e}\n')
    
    print('=== スロット使用統計 ===')
    print(f'総テストケース数: {total_tests}')
    print()
    
    used_count = 0
    for slot in all_slots:
        usage_rate = (slot_usage[slot] / total_tests) * 100
        status = "✅活用中" if slot_usage[slot] > 0 else "❌未使用"
        print(f'{slot:8s}: {slot_usage[slot]:2d}/{total_tests} ({usage_rate:5.1f}%) {status}')
        if slot_usage[slot] > 0:
            used_count += 1
    
    print()
    overall_rate = (used_count / len(all_slots)) * 100
    print(f'総合活用率: {used_count}/{len(all_slots)} ({overall_rate:.1f}%)')
    
    # 未使用スロットの詳細
    unused_slots = [slot for slot in all_slots if slot_usage[slot] == 0]
    if unused_slots:
        print(f'\n未使用スロット: {", ".join(unused_slots)}')
    else:
        print('\n🎉 全スロット活用達成！')

if __name__ == "__main__":
    analyze_slot_usage()
