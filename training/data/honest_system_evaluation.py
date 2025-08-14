#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現在のシステム実態調査 - 正直なテスト
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

def test_current_system_honestly():
    """現在のシステムの正直な性能評価"""
    
    print("🔍 現在のシステム実態調査")
    print("=" * 60)
    
    # エンジン初期化
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    decomposer = SubSlotDecomposer()
    
    # 基本テストケース（段階的に複雑化）
    test_cases = [
        # Level 1: 超基本文
        "I study English.",
        "The cat sat.",
        "She is happy.",
        
        # Level 2: 基本関係詞節
        "The book that I bought is good.",
        "The person who called me was John.",
        "The car which we saw was red.",
        
        # Level 3: 時間・条件節
        "When I arrived, he was sleeping.",
        "If it rains, we will stay home.",
        "Before she left, she called me.",
        
        # Level 4: 使役動詞
        "I made him study English.",
        "She let me use her car.",
        "He had me clean the room.",
        
        # Level 5: 複合構文
        "I think that he is smart.",
        "Having finished homework, I went out.",
        "The man walking there is my father.",
        
        # Level 6: 超複雑（前任者テストケース）
        "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    ]
    
    results = {
        "success": [],
        "partial": [],
        "failure": []
    }
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {sentence} ---")
        
        try:
            # メインスロット分解
            main_result = integrator.process(sentence)
            main_slots = main_result.get('slots', {})
            print(f"✅ メインスロット: {main_slots}")
            
            # サブスロット分解（正しいインターフェース使用）
            sub_results = decomposer.decompose_complex_slots(main_slots)
            if any(sub_results.values()):
                print(f"✅ サブスロット: {sub_results}")
                results["success"].append((i, sentence))
            else:
                print(f"⚠️ サブスロットなし")
                results["partial"].append((i, sentence))
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            results["failure"].append((i, sentence))
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 実態調査結果")
    print("=" * 60)
    
    total = len(test_cases)
    success = len(results["success"])
    partial = len(results["partial"])
    failure = len(results["failure"])
    
    print(f"🏆 完全成功: {success}/{total} ({success/total*100:.1f}%)")
    print(f"⚠️ 部分成功: {partial}/{total} ({partial/total*100:.1f}%)")
    print(f"❌ 完全失敗: {failure}/{total} ({failure/total*100:.1f}%)")
    
    print(f"\n🎯 真の成功率: {(success+partial)/total*100:.1f}%")
    
    if failure:
        print(f"\n❌ 失敗したケース:")
        for idx, sentence in results["failure"]:
            print(f"  {idx}: {sentence}")

if __name__ == "__main__":
    test_current_system_honestly()
