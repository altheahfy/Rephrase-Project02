#!/usr/bin/env python3
"""
改善前後比較テスト
- 協力アプローチ化による具体的な改善を数値で示す
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def before_after_comparison():
    """改善前後の比較テスト"""
    
    print("📊 Phase 2 関係節処理 - 改善前後比較")
    print("=" * 70)
    
    # 協力者セットアップ
    adverb_handler = AdverbHandler()
    collaborators = {
        'adverb': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # 重要な改善ケース
    critical_cases = [
        {
            'id': 4,
            'sentence': "The book which lies there is mine.",
            'expected_sub_m2': 'there',
            'issue_before': 'which関係節でsub-m2修飾語が取得されていなかった'
        },
        {
            'id': 5, 
            'sentence': "The person that works here is kind.",
            'expected_sub_m2': 'here',
            'issue_before': 'that関係節でsub-m2修飾語が取得されていなかった'
        }
    ]
    
    print("🎯 改善対象ケース分析")
    print("-" * 70)
    
    all_success = True
    
    for case in critical_cases:
        print(f"\n📝 ケース{case['id']}: {case['sentence']}")
        print(f"❌ 改善前の問題: {case['issue_before']}")
        print(f"✅ 期待されるsub-m2: '{case['expected_sub_m2']}'")
        
        # 実際の処理実行
        result = rel_handler.process(case['sentence'])
        
        # 結果検証
        success = result.get('success', False)
        sub_slots = result.get('sub_slots', {})
        actual_sub_m2 = sub_slots.get('sub-m2', '')
        
        print(f"🔧 処理結果:")
        print(f"   成功: {success}")
        print(f"   実際のsub-m2: '{actual_sub_m2}'")
        
        # 検証
        if actual_sub_m2 == case['expected_sub_m2']:
            print(f"🎉 改善成功！期待値と一致")
        else:
            print(f"❌ 改善失敗：期待'{case['expected_sub_m2']}' → 実際'{actual_sub_m2}'")
            all_success = False
    
    print(f"\n" + "=" * 70)
    print(f"📊 改善成果総合評価")
    print(f"=" * 70)
    
    if all_success:
        print(f"🎉 協力アプローチ化完全成功！")
        print(f"✅ すべての対象ケースで期待されるsub-m2修飾語を正確に取得")
        print(f"🚀 Phase 2関係節処理の品質が大幅向上")
        
        # 技術的改善ポイント
        print(f"\n🔧 技術的改善ポイント:")
        print(f"   1. _process_which協力アプローチ版への完全置換")
        print(f"   2. AdverbHandler連携による修飾語情報統合")
        print(f"   3. 協力者キー両対応（'adverb'/'AdverbHandler'）")
        print(f"   4. spaCy解析結果の適切な活用")
        
    else:
        print(f"🔧 部分的改善：さらなる調整が必要")
    
    return all_success

def detailed_slot_analysis():
    """詳細なスロット構造分析"""
    print(f"\n🔍 詳細スロット構造分析")
    print("=" * 50)
    
    adverb_handler = AdverbHandler()
    collaborators = {'adverb': adverb_handler}
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    test_sentence = "The book which lies there is mine."
    result = rel_handler.process(test_sentence)
    
    print(f"📝 例文: {test_sentence}")
    print(f"📊 完全な処理結果:")
    
    # JSONを見やすく表示
    print(json.dumps(result, indent=3, ensure_ascii=False))

if __name__ == "__main__":
    success = before_after_comparison()
    detailed_slot_analysis()
    
    print(f"\n{'🎉 協力アプローチ化による改善完了！' if success else '🔧 継続改善が必要'}")
