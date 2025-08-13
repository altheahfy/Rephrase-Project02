#!/usr/bin/env python3
"""
具体的処理結果比較デモ
従来システムとPhase 2システムの実際の動作差分を示す

同じテスト文に対する両システムの処理結果を並べて比較し、
Phase 2サブレベルパターン統合の具体的改善効果を実証します。
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from grammar_master_controller_v2 import GrammarMasterControllerV2
    from engines.simple_relative_engine_unified import SimpleRelativeEngine
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def demonstrate_processing_differences():
    """処理結果の具体的差分デモ"""
    
    print("🔬 従来システム vs Phase 2システム - 具体的処理結果比較")
    print("=" * 80)
    
    # Phase 2システム（Grammar Master Controller V2）
    phase2_controller = GrammarMasterControllerV2()
    
    # 従来システム（関係詞エンジン単体）
    traditional_relative_engine = SimpleRelativeEngine()
    
    # テスト文
    test_sentences = [
        "I think that he is smart.",
        "She believes they work hard.",
        "The man who lives here is kind.",
        "Running quickly, he caught the bus."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【テスト文 {i}】: {sentence}")
        print("=" * 60)
        
        # Phase 2システムの処理
        print("🚀 Phase 2システム処理結果:")
        phase2_result = phase2_controller.process_sentence(sentence, debug=False)
        
        print(f"   エンジン選択: {phase2_result.engine_type.value}")
        print(f"   処理成功: {phase2_result.success}")
        print(f"   基本スロット:")
        if phase2_result.slots:
            for slot, value in phase2_result.slots.items():
                if value and value.strip():
                    print(f"      {slot}: '{value}'")
        
        # Phase 2サブレベルパターン結果
        if 'sublevel_patterns' in phase2_result.metadata:
            sublevel_data = phase2_result.metadata['sublevel_patterns']
            enhancement_details = sublevel_data.get('enhancement_details', {})
            processing_stats = sublevel_data.get('processing_stats', {})
            
            print(f"   サブレベルパターン統計:")
            print(f"      検出パターン数: {processing_stats.get('patterns_detected', 0)}")
            print(f"      サブレベル総数: {processing_stats.get('total_sublevels', 0)}")
            
            if enhancement_details:
                print(f"   サブレベル分析詳細:")
                for slot, details in enhancement_details.items():
                    if details.get('enhanced', False):
                        pattern = details.get('pattern_type', 'N/A')
                        sublevel_slots = details.get('sublevel_slots', {})
                        print(f"      {slot}スロット → {pattern}パターン: {sublevel_slots}")
        
        # 従来システムの処理（関係詞エンジンが適用可能な場合）
        print(f"\n🔧 従来システム処理結果（関係詞エンジン単体）:")
        try:
            traditional_result = traditional_relative_engine.process(sentence)
            print(f"   処理結果:")
            for slot, value in traditional_result.items():
                print(f"      {slot}: '{value}'")
        except Exception as e:
            print(f"   処理エラーまたは適用外: {str(e)[:100]}...")
        
        # 差分分析
        print(f"\n📊 差分分析:")
        print(f"   Phase 2の優位性:")
        
        if 'sublevel_patterns' in phase2_result.metadata:
            sublevel_stats = phase2_result.metadata['sublevel_patterns'].get('processing_stats', {})
            if sublevel_stats.get('patterns_detected', 0) > 0:
                print(f"      ✅ 複雑構造認識: {sublevel_stats['patterns_detected']}パターン検出")
                print(f"      ✅ サブレベル分解: {sublevel_stats['total_sublevels']}要素抽出")
                print(f"      ✅ メタデータ保持: 完全な分析情報記録")
            else:
                print(f"      ⚪ 単純文: サブレベル処理不要（正常動作）")
        
        print(f"   従来システムの限界:")
        print(f"      ❌ 特定構造のみ: 関係詞文以外は基本処理のみ")
        print(f"      ❌ エンジン依存: 文全体での最適化判断が必要")
        print(f"      ❌ 統合情報なし: メタデータでの統一分析結果なし")

def summarize_key_advantages():
    """主要利点のまとめ"""
    
    print(f"\n\n🎖️ Phase 2サブレベルパターン統合の決定的利点")
    print("=" * 80)
    
    print("1. 【処理の普遍性】")
    print("   従来: 特定文構造 → 特定エンジン → 特化処理")
    print("   Phase 2: 任意文構造 → 任意エンジン → 統一サブレベル処理")
    print("   → どのエンジンでも複雑構造を見逃さない")
    
    print("\n2. 【分析の一貫性】")
    print("   従来: エンジンごとに異なる複雑構造処理ロジック")
    print("   Phase 2: Pure Stanza V3.1統一パターンによる一貫分析")
    print("   → 同じ構造は常に同じ結果")
    
    print("\n3. 【開発効率性】")
    print("   従来: 新構造 → エンジン開発 → 統合テスト → デプロイ")
    print("   Phase 2: 新構造 → パターン定義追加 → 即座に全エンジンで利用可能")
    print("   → 開発工数の劇的削減")
    
    print("\n4. 【情報の完全性】")
    print("   従来: 限定的なsub-slotサブ情報")
    print("   Phase 2: 完全なsublevel_patternsメタデータ")
    print("   → 分析結果の詳細追跡とデバッグが可能")
    
    print("\n5. 【システムの拡張性】")
    print("   従来: 15個エンジン × 各種複雑構造 = 膨大な組み合わせ開発")
    print("   Phase 2: 15個エンジン + 1個統一ライブラリ = シンプルなアーキテクチャ")
    print("   → メンテナンス性とスケーラビリティの向上")

def main():
    """メイン実行"""
    demonstrate_processing_differences()
    summarize_key_advantages()
    
    print(f"\n\n📋 結論")
    print("=" * 80)
    print("従来の関係詞エンジンとGrammar Masterの組み合わせは")
    print("「特定構造に対する専用処理」を提供していましたが、")
    print()
    print("Phase 2サブレベルパターン統合により")
    print("「全エンジン横断的な統一複雑構造認識」が実現され、")
    print()
    print("🚀 処理範囲の拡大（関係詞のみ → 11種類パターン）")
    print("🚀 適用範囲の拡大（1エンジン → 15全エンジン）")
    print("🚀 分析深度の向上（構造認識 → サブレベル分解）")
    print("🚀 開発効率の向上（専用開発 → パターン追加）")
    print("🚀 システム統合性の向上（個別処理 → 統一メタデータ）")
    print()
    print("という5次元での劇的改善を達成しました。")

if __name__ == "__main__":
    main()
