#!/usr/bin/env python3
"""
上位スロットの中身確認テスト
サブスロットがある場合、上位スロットは空であるべき
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def test_upper_slot_emptiness():
    """上位スロットが正しく空になっているかテスト"""
    
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()

    complex_sentence = 'That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential.'

    print('=== 📋 上位スロット中身確認テスト ===')

    # メインスロット分解
    result = integrator.process(complex_sentence)
    main_slots = result.get('slots', {})

    # サブスロット分解
    sub_slot_results = decomposer.decompose_complex_slots(main_slots)

    print('\n🔍 現在の状態分析:')

    # サブスロットがあるスロット
    slots_with_subs = ['S', 'C2', 'M2', 'M3']
    issues = []

    print('\n1️⃣ サブスロットがあるスロット（上位は空であるべき）:')
    for slot in slots_with_subs:
        has_sub_slots = slot in sub_slot_results
        main_content = main_slots.get(slot, '').strip()
        
        print(f'\n📌 {slot}スロット:')
        print(f'  サブスロット有無: {"有" if has_sub_slots else "無"}')
        print(f'  上位スロット内容: "{main_content}"')
        
        if has_sub_slots and main_content:
            print(f'  ❌ 問題: サブスロットがあるのに上位に内容が残っている')
            issues.append(f'{slot}スロットの上位を空にする')
        elif has_sub_slots and not main_content:
            print(f'  ✅ 正常: サブスロット有、上位空')
        elif not has_sub_slots:
            print(f'  ⚠️ サブスロット未実装')

    # サブスロットがないスロット
    print('\n2️⃣ サブスロットがないスロット（上位に内容があるべき）:')
    slots_without_subs = ['M1', 'Aux', 'V', 'O1']
    
    for slot in slots_without_subs:
        main_content = main_slots.get(slot, '').strip()
        print(f'  {slot}: "{main_content}" (正常: 内容有)')

    # 問題の要約
    print(f'\n📊 問題の要約:')
    if issues:
        print(f'❌ 修正が必要な箇所: {len(issues)}個')
        for issue in issues:
            print(f'  - {issue}')
    else:
        print(f'✅ すべて正常: 上位/サブスロットの関係が正しく設定されています')

    return len(issues) == 0

if __name__ == "__main__":
    test_upper_slot_emptiness()
