#!/usr/bin/env python3
"""
上位スロット分解問題の調査
なぜmain_slotsが空になっているのかを詳細調査
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def investigate_main_slots_issue():
    """上位スロット分解問題を調査"""
    
    print("🔍 上位スロット分解問題の詳細調査")
    print("=" * 70)
    
    controller = CentralController()
    
    # 問題のケースを詳細調査
    test_cases = [
        {
            'name': 'Phase 1 - 第2文型',
            'sentence': 'The car is red.',
            'expected_main': {'S': 'The car', 'V': 'is', 'C': 'red'}
        },
        {
            'name': 'Phase 1 - 第3文型', 
            'sentence': 'I love you.',
            'expected_main': {'S': 'I', 'V': 'love', 'O': 'you'}
        },
        {
            'name': 'Phase 2 - 関係節',
            'sentence': 'The man who runs fast is strong.',
            'expected_main': {'S': '', 'V': 'is', 'C': 'strong'}  # Sは空（sub-slots存在）
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【調査{i}】{case['name']}")
        print(f"文: {case['sentence']}")
        print(f"期待されるメインスロット: {case['expected_main']}")
        print("-" * 50)
        
        # 実際の処理実行と詳細確認
        result = controller.process_sentence(case['sentence'])
        
        print(f"🔍 実際の結果:")
        print(f"   success: {result.get('success', False)}")
        print(f"   main_slots: {result.get('main_slots', {})}")
        print(f"   sub_slots: {result.get('sub_slots', {})}")
        print(f"   詳細結果の keys: {list(result.keys())}")
        
        # main_slotsが空の理由を推測
        main_slots = result.get('main_slots', {})
        if not main_slots:
            print(f"❌ 問題: main_slotsが空です")
            
            # 可能な原因
            if result.get('sub_slots'):
                print(f"   💡 推測: 関係節処理でSスロットが意図的に空にされている可能性")
            else:
                print(f"   💡 推測: 基本5文型処理で全くスロット分解されていない")
        else:
            print(f"✅ main_slotsが正常に取得されています")
    
    print(f"\n" + "=" * 70)
    print(f"🎯 問題の分析結果")
    print("=" * 70)
    print(f"1. Phase 1（基本5文型）: main_slotsが全く分解されていない")
    print(f"2. Phase 2（関係節）: 仕様により意図的にSスロットを空にしている")
    print(f"3. 根本原因: 基本5文型ハンドラーが正しく動作していない可能性")

def test_basic_five_pattern_directly():
    """BasicFivePatternHandlerを直接テスト"""
    print(f"\n🔧 BasicFivePatternHandler直接テスト")
    print("-" * 50)
    
    try:
        from basic_five_pattern_handler import BasicFivePatternHandler
        
        handler = BasicFivePatternHandler()
        test_sentence = "The car is red."
        
        print(f"テスト文: {test_sentence}")
        result = handler.process(test_sentence)
        
        print(f"直接テスト結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get('slots'):
            print(f"✅ BasicFivePatternHandlerは正常動作")
        else:
            print(f"❌ BasicFivePatternHandlerに問題あり")
            
    except Exception as e:
        print(f"❌ BasicFivePatternHandler直接テストでエラー: {e}")

if __name__ == "__main__":
    investigate_main_slots_issue()
    test_basic_five_pattern_directly()
