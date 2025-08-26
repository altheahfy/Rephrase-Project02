#!/usr/bin/env python3
"""
緊急修正: 正しいテストシステム
- 偽陽性を排除
- 実際の機能状況を正確に把握
- 厳格な成功判定基準
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def emergency_real_test():
    """緊急：実際の状況把握"""
    
    print("🚨 緊急事態：正しいテスト実行")
    print("=" * 80)
    print("❌ これまでのテストは信用できません")
    print("✅ 厳格な基準で再評価します")
    print("=" * 80)
    
    controller = CentralController()
    
    # 最も基本的なケース
    basic_tests = [
        {
            'sentence': 'The car is red.',
            'expected_pattern': '第2文型',
            'must_have_main_slots': ['S', 'V', 'C'],
            'expected_main': {'S': 'The car', 'V': 'is', 'C': 'red'}
        },
        {
            'sentence': 'I love you.',
            'expected_pattern': '第3文型', 
            'must_have_main_slots': ['S', 'V', 'O'],
            'expected_main': {'S': 'I', 'V': 'love', 'O': 'you'}
        }
    ]
    
    print("📊 厳格な基準でのテスト")
    print("-" * 60)
    
    real_success_count = 0
    
    for i, test in enumerate(basic_tests, 1):
        print(f"\n【テスト{i}】{test['expected_pattern']}")
        print(f"文: {test['sentence']}")
        print(f"必須main_slots: {test['must_have_main_slots']}")
        
        # 処理実行
        result = controller.process_sentence(test['sentence'])
        
        # 厳格な判定
        processing_success = result.get('success', False)
        main_slots = result.get('main_slots', {})
        
        print(f"処理success: {processing_success}")
        print(f"実際main_slots: {main_slots}")
        
        # 真の成功判定
        has_required_slots = all(slot in main_slots for slot in test['must_have_main_slots'])
        slots_not_empty = len(main_slots) > 0
        real_success = processing_success and has_required_slots and slots_not_empty
        
        print(f"必須スロット存在: {has_required_slots}")
        print(f"スロット非空: {slots_not_empty}")
        print(f"🎯 真の成功: {real_success}")
        
        if real_success:
            real_success_count += 1
            print(f"✅ 実際に成功")
        else:
            print(f"❌ 実際は失敗")
            
            # 失敗理由の詳細
            if not processing_success:
                print(f"   理由: 処理自体が失敗")
            elif not slots_not_empty:
                print(f"   理由: main_slotsが空")
            elif not has_required_slots:
                missing = [s for s in test['must_have_main_slots'] if s not in main_slots]
                print(f"   理由: 必須スロット欠損 {missing}")
    
    # 厳しい現実
    real_success_rate = real_success_count / len(basic_tests) * 100
    
    print(f"\n" + "=" * 80)
    print(f"🚨 厳格基準による真の結果")
    print("=" * 80)
    print(f"📊 真の成功率: {real_success_count}/{len(basic_tests)} = {real_success_rate:.1f}%")
    
    if real_success_rate == 0:
        print(f"❌ 完全失敗：基本機能が全く動いていません")
        print(f"🚨 緊急修正が必要です")
    elif real_success_rate < 50:
        print(f"🔧 重大な問題：大部分の機能が動いていません")
    else:
        print(f"✅ 部分的成功：まだ改善の余地があります")
    
    return real_success_rate

def identify_root_cause():
    """根本原因の特定"""
    
    print(f"\n🔍 根本原因の特定")
    print("-" * 40)
    
    controller = CentralController()
    result = controller.process_sentence("The car is red.")
    
    print(f"詳細な処理結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # CentralControllerの処理フローを追跡
    print(f"\n🔍 処理フロー分析:")
    print(f"1. 修飾語分離は動作している（出力に表示）")
    print(f"2. 関係節検出も動作している") 
    print(f"3. しかしmain_slotsが空 → 5文型処理が失敗している可能性")

if __name__ == "__main__":
    real_rate = emergency_real_test()
    identify_root_cause()
    
    print(f"\n🚨 緊急事態報告:")
    print(f"📊 これまでの「100%成功」報告は完全に間違いでした")
    print(f"📊 実際の成功率: {real_rate:.1f}%")
    print(f"🔧 immediate修正が必要です")
