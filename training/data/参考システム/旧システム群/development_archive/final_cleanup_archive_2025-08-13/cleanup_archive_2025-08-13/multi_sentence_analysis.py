#!/usr/bin/env python3
"""
Multi-Sentence Slot Analysis Test
複数文のスロット分析とサブレベルパターン検出テスト

Phase 2テストケースの実際の検出結果を確認し、
期待値を正しく設定するために実際のパターンを調査します。
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from grammar_master_controller_v2 import GrammarMasterControllerV2
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def analyze_multiple_sentences():
    """複数文の実際のスロット分析とサブレベルパターン検出"""
    print("🔬 Multi-Sentence Slot Analysis Test")
    print("=" * 60)
    
    controller = GrammarMasterControllerV2()
    
    # テストケース
    test_sentences = [
        "I think that he is smart.",
        "She believes that they work hard.",
        "The man who lives next door is kind.",
        "The book that I read yesterday was interesting.",
        "When it rains, I stay home.",
        "Running quickly, he caught the bus.",
        "The cat under the table is sleeping.",
        "This book is more interesting than that one."
    ]
    
    print("\n🧪 Analyzing actual slot extraction and sublevel patterns:")
    print("-" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【Test {i}】: {sentence}")
        
        # 処理実行（デバッグモードoff）
        result = controller.process_sentence(sentence, debug=False)
        
        print(f"   Engine: {result.engine_type.value}")
        print(f"   Success: {result.success}")
        
        # スロット情報表示
        if result.slots:
            print(f"   📋 Extracted Slots:")
            for slot, value in result.slots.items():
                if value and value.strip():
                    print(f"      {slot}: '{value}'")
        
        # サブレベルパターン処理結果確認
        if 'sublevel_patterns' in result.metadata:
            sublevel_data = result.metadata['sublevel_patterns']
            enhancement_details = sublevel_data.get('enhancement_details', {})
            processing_stats = sublevel_data.get('processing_stats', {})
            
            if processing_stats.get('patterns_detected', 0) > 0:
                print(f"   🔍 Sublevel Patterns Detected:")
                for slot, details in enhancement_details.items():
                    if details.get('enhanced', False):
                        pattern = details.get('pattern_type', 'N/A')
                        sublevel_slots = details.get('sublevel_slots', {})
                        print(f"      {slot}: {pattern} → {sublevel_slots}")
            else:
                print(f"   ❌ No sublevel patterns detected")
        else:
            print(f"   ⚠️  No sublevel pattern metadata")
    
    # 最終統計
    final_stats = controller.get_processing_stats()
    print(f"\n📊 Final Processing Statistics:")
    print(f"   Total Requests: {final_stats['total_requests']}")
    print(f"   Boundary Expansions: {final_stats.get('boundary_expansions_applied', 0)}")
    print(f"   Sublevel Patterns: {final_stats.get('sublevel_patterns_applied', 0)}")
    print(f"   Success Rate: {final_stats['success_rate_percent']}%")

if __name__ == "__main__":
    analyze_multiple_sentences()
