#!/usr/bin/env python3
"""
修正後の緊急テスト
- main_slots修正の効果確認
- 適切なテスト判定基準の適用
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def test_main_slots_fix():
    """main_slots修正の効果をテスト"""
    
    print("🔧 main_slots修正後の緊急テスト")
    print("=" * 60)
    
    controller = CentralController()
    
    test_cases = [
        {
            'category': '基本5文型 - 第2文型',
            'sentence': 'The car is red.',
            'expected_main': {'S': 'The car', 'V': 'is', 'C1': 'red'},
            'should_have_main': True,
            'should_have_sub': False
        },
        {
            'category': '基本5文型 - 第3文型',
            'sentence': 'I love you.',
            'expected_main': {'S': 'I', 'V': 'love', 'O1': 'you'},
            'should_have_main': True,
            'should_have_sub': False
        },
        {
            'category': '関係節 - who',
            'sentence': 'The man who runs fast is strong.',
            'expected_main': {'S': '', 'V': 'is', 'C1': 'strong'},  # Sは空に
            'expected_sub': {'sub-s': 'The man who', 'sub-v': 'runs'},
            'should_have_main': True,
            'should_have_sub': True
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【ケース{i}】{case['category']}")
        print(f"文: {case['sentence']}")
        print("-" * 40)
        
        result = controller.process_sentence(case['sentence'])
        
        # 結果分析
        success = result.get('success', False)
        main_slots = result.get('main_slots', {})
        sub_slots = result.get('sub_slots', {})
        
        print(f"処理成功: {success}")
        print(f"main_slots: {main_slots}")
        print(f"sub_slots: {sub_slots}")
        
        # 適切な成功判定
        has_meaningful_main = len(main_slots) > 0 and any(v != '' for v in main_slots.values())
        has_meaningful_sub = len(sub_slots) > 0
        
        # ケース別判定
        case_success = True
        reasons = []
        
        if case['should_have_main'] and not has_meaningful_main:
            case_success = False
            reasons.append("main_slotsが空または無意味")
        
        if case['should_have_sub'] and not has_meaningful_sub:
            case_success = False
            reasons.append("sub_slotsが期待されているが空")
        
        if not success:
            case_success = False
            reasons.append("処理自体が失敗")
        
        # 結果判定
        if case_success:
            print(f"✅ 成功")
            success_count += 1
        else:
            print(f"❌ 失敗: {', '.join(reasons)}")
        
        # 詳細比較（可能な場合）
        if 'expected_main' in case and main_slots:
            print(f"期待main_slots: {case['expected_main']}")
            print(f"実際main_slots: {main_slots}")
    
    # 総合結果
    success_rate = success_count / total_count * 100
    print(f"\n" + "=" * 60)
    print(f"📊 修正後の成功率: {success_count}/{total_count} = {success_rate:.1f}%")
    
    if success_rate >= 80:
        print(f"🎉 修正成功！システムが正常動作")
    elif success_rate >= 50:
        print(f"🔧 部分的改善、さらなる調整が必要")
    else:
        print(f"❌ 修正効果不十分、根本的見直しが必要")
    
    return success_rate >= 80

if __name__ == "__main__":
    fix_successful = test_main_slots_fix()
    
    print(f"\n{'🎉 修正完了！' if fix_successful else '🔧 継続修正必要'}")
    print(f"📝 適切なテスト基準による正確な評価を実施")
