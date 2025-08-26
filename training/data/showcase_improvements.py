#!/usr/bin/env python3
"""
成果確認用正規テスト
- 協力アプローチ化前後の比較
- 具体的な改善内容の明示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def test_improvement_showcase():
    """改善成果を分かりやすく表示"""
    
    print("🎯 Phase 2 関係節処理 - 協力アプローチ化成果テスト")
    print("=" * 60)
    
    # 協力者セットアップ
    adverb_handler = AdverbHandler()
    collaborators = {
        'adverb': adverb_handler,  # CentralControllerと同じキー
        'AdverbHandler': adverb_handler  # 直接テスト用キー
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # テストケース（改善対象）
    test_cases = [
        {
            'id': 4,
            'sentence': "The book which lies there is mine.",
            'focus': 'which関係節でのsub-m2修飾語取得',
            'improvement': '_process_which協力アプローチ化'
        },
        {
            'id': 5,
            'sentence': "The person that works here is kind.",
            'focus': 'that関係節でのsub-m2修飾語取得',
            'improvement': 'AdverbHandler連携による修飾語情報統合'
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for case in test_cases:
        print(f"\n📝 ケース{case['id']}: {case['sentence']}")
        print(f"🎯 改善目標: {case['focus']}")
        print(f"🔧 実装内容: {case['improvement']}")
        print("-" * 50)
        
        # 関係節処理実行
        result = rel_handler.process(case['sentence'])
        
        # 結果分析
        success = result.get('success', False)
        sub_slots = result.get('sub_slots', {})
        has_sub_m2 = 'sub-m2' in sub_slots
        
        print(f"✅ 処理成功: {success}")
        print(f"🔧 sub-m2存在: {has_sub_m2}")
        
        if has_sub_m2:
            sub_m2_value = sub_slots['sub-m2']
            print(f"📍 sub-m2値: '{sub_m2_value}'")
            print("🎉 修飾語取得成功！")
            success_count += 1
        else:
            print("❌ 修飾語取得失敗")
        
        # サブスロット構造確認
        print(f"📊 サブスロット構造:")
        for key, value in sub_slots.items():
            if key != '_parent_slot':
                print(f"   {key}: '{value}'")
    
    print(f"\n" + "=" * 60)
    print(f"📊 改善成果サマリー")
    print(f"=" * 60)
    print(f"🎯 対象ケース: {total_count}")
    print(f"✅ 修飾語取得成功: {success_count}")
    print(f"📈 修飾語取得成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print(f"🎉 協力アプローチ化による修飾語取得 100% 達成！")
        return True
    else:
        print(f"🔧 さらなる改善が必要")
        return False

def test_adverb_handler_standalone():
    """AdverbHandler単体での100%精度を確認"""
    print(f"\n🔍 AdverbHandler単体性能確認")
    print("=" * 40)
    
    adverb_handler = AdverbHandler()
    
    test_sentences = [
        "The man runs fast",
        "She speaks clearly", 
        "which lies there",
        "that works here",
        "I played yesterday"
    ]
    
    success_count = 0
    for sentence in test_sentences:
        result = adverb_handler.process(sentence)
        success = result.get('success', False)
        print(f"'{sentence}' → {success}")
        if success:
            success_count += 1
    
    print(f"AdverbHandler成功率: {success_count}/{len(test_sentences)} = {success_count/len(test_sentences)*100:.1f}%")

if __name__ == "__main__":
    # メイン成果テスト
    main_success = test_improvement_showcase()
    
    # AdverbHandler確認
    test_adverb_handler_standalone()
    
    print(f"\n{'🎉 協力アプローチ化成功！' if main_success else '🔧 継続改善中'}")
