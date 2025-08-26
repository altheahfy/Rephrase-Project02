#!/usr/bin/env python3
"""
テストスクリプトの問題分析
- main_slotsが空なのに成功判定している問題
- テストの検証が不十分な問題を特定
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def analyze_test_problems():
    """テストスクリプトの問題を分析"""
    
    print("🚨 テストスクリプト問題分析")
    print("=" * 60)
    
    controller = CentralController()
    
    # 基本5文型で検証
    basic_cases = [
        {
            'sentence': 'The car is red.',
            'expected_main': {'S': 'The car', 'V': 'is', 'C': 'red'},
            'pattern': '第2文型 SVC'
        },
        {
            'sentence': 'I love you.',
            'expected_main': {'S': 'I', 'V': 'love', 'O': 'you'},
            'pattern': '第3文型 SVO'
        },
        {
            'sentence': 'I gave him a book.',
            'expected_main': {'S': 'I', 'V': 'gave', 'O1': 'him', 'O2': 'a book'},
            'pattern': '第4文型 SVOO'
        }
    ]
    
    print("📊 基本5文型でのmain_slots検証")
    print("-" * 40)
    
    for i, case in enumerate(basic_cases, 1):
        print(f"\n【ケース{i}】{case['pattern']}")
        print(f"文: {case['sentence']}")
        print(f"期待main_slots: {case['expected_main']}")
        
        result = controller.process_sentence(case['sentence'])
        actual_main = result.get('main_slots', {})
        success = result.get('success', False)
        
        print(f"実際main_slots: {actual_main}")
        print(f"処理success判定: {success}")
        
        # 真の成功判定
        main_slots_empty = len(actual_main) == 0
        should_have_main = True  # 基本5文型なら必須
        
        print(f"🚨 問題分析:")
        print(f"   main_slotsが空: {main_slots_empty}")
        print(f"   main_slots必要: {should_have_main}")
        print(f"   真の成功: {not main_slots_empty and success}")
        
        if main_slots_empty and success:
            print(f"   ❌ 偽陽性: main_slots空なのに成功判定")
        elif not main_slots_empty and success:
            print(f"   ✅ 正常: main_slotsもあり成功")
        else:
            print(f"   ❌ 失敗: 処理自体が失敗")
    
    print(f"\n" + "=" * 60)
    print(f"🚨 テストスクリプトの重大な問題")
    print("=" * 60)
    print(f"❌ 1. success=Trueだけで判定している")
    print(f"❌ 2. main_slotsの中身を検証していない")
    print(f"❌ 3. 空のmain_slotsでも成功扱いしている")
    print(f"❌ 4. 実際のスロット内容と期待値を比較していない")
    print(f"❌ 5. 偽陽性（false positive）を見逃している")
    
    return True

def create_proper_test():
    """適切なテストスクリプトの作成"""
    
    print(f"\n🔧 適切なテスト判定の例")
    print("-" * 40)
    
    controller = CentralController()
    sentence = "The car is red."
    result = controller.process_sentence(sentence)
    
    # 現在の判定（問題のある判定）
    current_judgment = result.get('success', False)
    print(f"現在の判定: {current_judgment} (success フラグのみ)")
    
    # 適切な判定
    success = result.get('success', False)
    main_slots = result.get('main_slots', {})
    has_meaningful_main = len(main_slots) > 0
    
    proper_judgment = success and has_meaningful_main
    print(f"適切な判定: {proper_judgment} (success + main_slots内容)")
    
    print(f"\n💡 修正すべきポイント:")
    print(f"   1. success=True かつ main_slotsに内容がある")
    print(f"   2. 期待されるスロット構造と実際の構造を比較")
    print(f"   3. 空のスロットは失敗として扱う")
    print(f"   4. 詳細なエラーメッセージを提供")

if __name__ == "__main__":
    analyze_test_problems()
    create_proper_test()
    
    print(f"\n🚨 結論: テストスクリプトが問題を隠蔽している")
    print(f"📝 修正必要: 適切な成功判定基準の実装")
