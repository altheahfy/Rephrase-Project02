#!/usr/bin/env python3
"""
緊急診断：システムの真の状況を把握
- 各コンポーネントが実際に動作しているか
- どこで問題が発生しているか
- 戻るべき地点の特定
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
from basic_five_pattern_handler import BasicFivePatternHandler
from adverb_handler import AdverbHandler
from relative_clause_handler import RelativeClauseHandler
import json

def emergency_diagnosis():
    """緊急診断を実行"""
    
    print("🚨 緊急診断：システムの真の状況")
    print("=" * 70)
    
    # 1. 各ハンドラーの単体テスト
    print("📊 Step 1: 各ハンドラー単体診断")
    print("-" * 50)
    
    # AdverbHandler単体テスト
    print("\n🔍 AdverbHandler単体テスト:")
    adverb_handler = AdverbHandler()
    adverb_result = adverb_handler.process("I run fast")
    print(f"   入力: 'I run fast'")
    print(f"   成功: {adverb_result.get('success', False)}")
    print(f"   結果: {adverb_result}")
    
    # BasicFivePatternHandler単体テスト
    print("\n🔍 BasicFivePatternHandler単体テスト:")
    five_handler = BasicFivePatternHandler()
    five_result = five_handler.process("The car is red")
    print(f"   入力: 'The car is red'")
    print(f"   成功: {five_result.get('success', False)}")
    print(f"   main_slots: {five_result.get('main_slots', {})}")
    print(f"   slots: {five_result.get('slots', {})}")
    
    # RelativeClauseHandler単体テスト
    print("\n🔍 RelativeClauseHandler単体テスト:")
    collaborators = {'adverb': adverb_handler}
    rel_handler = RelativeClauseHandler(collaborators)
    rel_result = rel_handler.process("The man who runs")
    print(f"   入力: 'The man who runs'")
    print(f"   成功: {rel_result.get('success', False)}")
    print(f"   main_slots: {rel_result.get('main_slots', {})}")
    print(f"   sub_slots: {rel_result.get('sub_slots', {})}")
    
    # 2. CentralController診断
    print(f"\n📊 Step 2: CentralController診断")
    print("-" * 50)
    
    controller = CentralController()
    
    test_cases = [
        ("基本5文型", "The car is red"),
        ("関係節", "The man who runs")
    ]
    
    working_components = []
    broken_components = []
    
    for case_type, sentence in test_cases:
        print(f"\n🔍 {case_type}テスト: '{sentence}'")
        result = controller.process_sentence(sentence)
        
        success = result.get('success', False)
        main_slots = result.get('main_slots', {})
        sub_slots = result.get('sub_slots', {})
        
        print(f"   CentralController成功: {success}")
        print(f"   main_slots: {main_slots}")
        print(f"   sub_slots: {sub_slots}")
        
        # 真の成功判定
        has_meaningful_output = len(main_slots) > 0 or len(sub_slots) > 0
        real_success = success and has_meaningful_output
        
        print(f"   真の成功: {real_success}")
        
        if real_success:
            working_components.append(case_type)
        else:
            broken_components.append(case_type)
    
    # 3. 診断結果と推奨アクション
    print(f"\n📊 Step 3: 診断結果と推奨アクション")
    print("=" * 70)
    
    print(f"✅ 動作中: {working_components}")
    print(f"❌ 故障中: {broken_components}")
    
    # 判定ロジック
    if len(broken_components) == 0:
        print(f"\n🎉 推奨: 現在のシステムで継続")
        print(f"   テスト判定基準のみ修正すれば問題解決")
        return "continue"
        
    elif "基本5文型" in broken_components and "関係節" in broken_components:
        print(f"\n🚨 推奨: 新システム構築開始地点に戻る")
        print(f"   基本機能が全て故障、全面的な見直しが必要")
        return "restart"
        
    elif "基本5文型" in broken_components:
        print(f"\n🔧 推奨: BasicFivePatternHandlerの修正")
        print(f"   基本5文型の修正が最優先")
        return "fix_basic"
        
    else:
        print(f"\n🔧 推奨: 関係節処理の修正")
        print(f"   基本5文型は動作、関係節のみ修正")
        return "fix_relative"

def check_git_history():
    """Git履歴で安全な復帰ポイントを確認"""
    print(f"\n📊 Step 4: Git履歴確認")
    print("-" * 50)
    
    # 最近のコミット履歴を表示
    import subprocess
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                              capture_output=True, text=True, cwd='.')
        print("最近のコミット履歴:")
        print(result.stdout)
    except:
        print("Git履歴の取得に失敗")

if __name__ == "__main__":
    recommended_action = emergency_diagnosis()
    check_git_history()
    
    print(f"\n🎯 最終推奨アクション: {recommended_action}")
    
    if recommended_action == "restart":
        print(f"🔄 新システム構築開始地点への復帰を推奨")
    elif recommended_action == "continue":
        print(f"✅ 現システムでテスト修正のみ実施を推奨")
    else:
        print(f"🔧 部分修正での対応を推奨")
