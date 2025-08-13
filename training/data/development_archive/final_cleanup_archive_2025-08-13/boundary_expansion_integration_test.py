#!/usr/bin/env python3
"""
🔍 統一境界拡張統合効果検証テスト
Grammar Master Controller V2 with Unified Boundary Expansion Integration Test
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
while not os.path.exists(os.path.join(project_root, 'grammar_master_controller_v2.py')):
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

from grammar_master_controller_v2 import GrammarMasterControllerV2
from boundary_expansion_lib import BoundaryExpansionLib

def test_boundary_expansion_integration():
    """統一境界拡張統合効果検証テスト"""
    print("🔬 統一境界拡張統合効果検証テスト")
    print("=" * 70)
    
    try:
        # Initialize Grammar Master Controller V2
        controller = GrammarMasterControllerV2()
        
        # Test sentences that benefit from boundary expansion
        test_cases = [
            {
                "text": "The very tall student quickly read the book.",
                "description": "形容詞・副詞拡張テスト",
                "expected_improvement": "very tall → 1つのS, quickly → 1つのV modifier"
            },
            {
                "text": "She is reading the book on the table.",
                "description": "前置詞句境界拡張",
                "expected_improvement": "on the table → 完全なM1として認識"
            },
            {
                "text": "The student who studies hard will succeed.",
                "description": "関係代名詞境界拡張",
                "expected_improvement": "who studies hard → 完全な修飾句として認識"
            },
            {
                "text": "Having finished the work, he went home.",
                "description": "分詞構文境界拡張",
                "expected_improvement": "Having finished the work → 完全なM1として認識"
            }
        ]
        
        print(f"📊 テスト対象: {len(test_cases)} cases")
        print()
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"【Test {i}】: {test_case['description']}")
            print(f"   文章: \"{test_case['text']}\"")
            print(f"   期待改善: {test_case['expected_improvement']}")
            
            try:
                # Process with integrated boundary expansion
                result = controller.process_sentence(test_case['text'])
                
                if result:
                    print(f"   ✅ 処理成功")
                    print(f"   🚀 使用エンジン: {result.engine_type}")
                    print(f"   📊 抽出スロット数: {len(result.slots)}")
                    
                    # Display slots
                    for slot, content in result.slots.items():
                        print(f"      {slot}: '{content}'")
                    
                    success_count += 1
                else:
                    print(f"   ❌ 処理失敗: No result returned")
                    
            except Exception as e:
                print(f"   ❌ エラー: {e}")
            
            print()
        
        # Summary
        success_rate = (success_count / len(test_cases)) * 100
        print(f"📈 統合効果検証結果:")
        print(f"   成功率: {success_rate:.1f}% ({success_count}/{len(test_cases)})")
        
        if success_rate >= 75:
            print(f"   🌟 統合成功: 境界拡張機能が効果的に動作中")
        elif success_rate >= 50:
            print(f"   ⚠️  部分的成功: 一部改善が必要")
        else:
            print(f"   ❌ 統合課題: 境界拡張統合の見直しが必要")
            
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ 統合テストエラー: {e}")
        return False

def test_direct_boundary_expansion():
    """直接境界拡張ライブラリテスト（比較用）"""
    print("\n🔧 直接境界拡張ライブラリテスト（比較用）")
    print("=" * 50)
    
    try:
        boundary_lib = BoundaryExpansionLib()
        
        test_sentences = [
            "The very tall student quickly read the book.",
            "She is reading the book on the table."
        ]
        
        for sentence in test_sentences:
            print(f"原文: \"{sentence}\"")
            expanded = boundary_lib.expand_span_generic(sentence)
            print(f"拡張: \"{expanded}\"")
            print()
            
    except Exception as e:
        print(f"❌ 直接テストエラー: {e}")

if __name__ == "__main__":
    print("🚀 統一境界拡張統合効果検証テスト開始")
    print()
    
    # Main integration test
    integration_success = test_boundary_expansion_integration()
    
    # Direct comparison test
    test_direct_boundary_expansion()
    
    print("🎯 テスト完了")
    
    if integration_success:
        print("✅ 統一境界拡張統合 - 成功")
        sys.exit(0)
    else:
        print("❌ 統一境界拡張統合 - 要改善")
        sys.exit(1)
