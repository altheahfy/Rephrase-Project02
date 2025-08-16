#!/usr/bin/env python3
"""
最終完璧性検証テスト
この超複雑文を本当に100%完璧に分解できているか確認
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def final_perfection_test():
    """最終完璧性検証"""
    
    print("="*80)
    print("🏆 最終完璧性検証テスト")
    print("="*80)
    
    # システム初期化
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()
    
    # 超複雑文
    complex_sentence = 'That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential.'
    
    print(f"📝 対象文: {complex_sentence}")
    print()
    
    # 処理実行
    result = integrator.process(complex_sentence)
    main_slots = result.get('slots', {})
    sub_slot_results = decomposer.decompose_complex_slots(main_slots)
    
    print("🎯 完璧な分解結果:")
    print()
    
    # 期待値の完全定義
    perfect_structure = {
        'M1': {
            'type': 'word',
            'content': 'That afternoon at the crucial point in the presentation',
            'sub_slots': None
        },
        'S': {
            'type': 'clause',
            'content': '',  # 空であるべき
            'sub_slots': {
                'sub_S': 'the manager who',
                'sub_Aux': 'had',
                'sub_M2': 'recently',
                'sub_V': 'taken',
                'sub_O1': 'charge of the project'
            }
        },
        'Aux': {
            'type': 'word',
            'content': 'had to',
            'sub_slots': None
        },
        'V': {
            'type': 'word',
            'content': 'make',
            'sub_slots': None
        },
        'O1': {
            'type': 'word',
            'content': 'the committee responsible for implementation',
            'sub_slots': None
        },
        'C2': {
            'type': 'phrase',
            'content': '',  # 空であるべき
            'sub_slots': {
                'sub_V': 'deliver',
                'sub_O1': 'the final proposal',
                'sub_M3': 'flawlessly'
            }
        },
        'M2': {
            'type': 'clause',
            'content': '',  # 空であるべき
            'sub_slots': {
                'sub_M1': 'even though',
                'sub_S': 'he',
                'sub_V': 'was',
                'sub_M2': 'under intense pressure'
            }
        },
        'M3': {
            'type': 'clause',
            'content': '',  # 空であるべき
            'sub_slots': {
                'sub_M1': 'so',
                'sub_S': 'the outcome',
                'sub_Aux': 'would',
                'sub_V': 'reflect',
                'sub_O1': 'their full potential'
            }
        }
    }
    
    # 完璧性検証
    total_perfect = 0
    total_checks = 0
    
    for slot_name, expected in perfect_structure.items():
        print(f"📌 {slot_name}スロット ({expected['type']}):")
        slot_perfect = 0
        slot_checks = 0
        
        # 上位スロット内容チェック
        actual_content = main_slots.get(slot_name, '').strip()
        expected_content = expected['content']
        
        if actual_content == expected_content:
            print(f"  ✅ 上位内容: {'空' if not expected_content else expected_content}")
            slot_perfect += 1
        else:
            print(f"  ❌ 上位内容: 期待「{expected_content}」→ 実際「{actual_content}」")
        slot_checks += 1
        
        # サブスロットチェック
        if expected['sub_slots']:
            if slot_name in sub_slot_results:
                actual_subs = sub_slot_results[slot_name][0].sub_slots
                for sub_key, sub_expected in expected['sub_slots'].items():
                    sub_actual = actual_subs.get(sub_key, '')
                    if sub_actual == sub_expected:
                        print(f"  ✅ {sub_key}: {sub_expected}")
                        slot_perfect += 1
                    else:
                        print(f"  ❌ {sub_key}: 期待「{sub_expected}」→ 実際「{sub_actual}」")
                    slot_checks += 1
            else:
                print(f"  ❌ サブスロット: 未検出")
                slot_checks += len(expected['sub_slots'])
        
        slot_accuracy = (slot_perfect / slot_checks) * 100
        print(f"  📈 {slot_name}正確性: {slot_accuracy:.1f}% ({slot_perfect}/{slot_checks})")
        print()
        
        total_perfect += slot_perfect
        total_checks += slot_checks
    
    # 最終評価
    final_accuracy = (total_perfect / total_checks) * 100
    
    print("="*80)
    print(f"🎯 最終結果: {final_accuracy:.1f}% ({total_perfect}/{total_checks})")
    
    if final_accuracy == 100.0:
        print()
        print("🎉🎉🎉 ABSOLUTELY PERFECT! 🎉🎉🎉")
        print("✨ この超複雑文を100%完璧に分解しました！")
        print("🚀 メイン+サブスロットの完璧な階層構造を実現！")
        print("🏆 これは本当にとてつもない技術的成果です！")
        print()
        print("📊 達成した技術的突破:")
        print("  • 使役動詞構文の完全処理")
        print("  • 関係詞節の完璧なサブスロット分解")
        print("  • 複数副詞節の正確な分離")
        print("  • 補語句の詳細構造解析")
        print("  • 上位/サブスロットの正しい階層化")
        return True
    else:
        print("⚠️ まだ完璧ではありません。")
        return False

if __name__ == "__main__":
    final_perfection_test()
