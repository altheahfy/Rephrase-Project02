"""
個別エンジン vs 協調システム品質劣化の原因分析
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_engine_architecture_problems():
    """マルチエンジン協調システムの設計問題分析"""
    print("🔍 マルチエンジン協調システム 設計問題分析\n")
    
    # Basic Five Pattern Engineを直接テスト
    print("=" * 70)
    print("📊 個別エンジン vs 協調システム 品質比較")
    print("=" * 70)
    
    try:
        # 1. 個別エンジン直接テスト
        print("🧪 テスト1: Basic Five Pattern Engine 直接実行")
        
        from engines.basic_five_pattern_engine import BasicFivePatternEngine
        basic_engine = BasicFivePatternEngine()
        
        test_sentences = [
            "The cat sits.",
            "They made him captain.", 
            "She is beautiful.",
            "I love you.",
            "He gave me a book."
        ]
        
        print("📋 個別エンジン結果:")
        direct_results = {}
        
        for sentence in test_sentences:
            result = basic_engine.process_sentence(sentence)
            direct_results[sentence] = result
            print(f"  '{sentence}' → {result}")
        
        print("\n" + "-" * 50)
        
        # 2. 協調システム経由テスト
        print("🧪 テスト2: 協調システム経由実行")
        
        from grammar_master_controller_v2 import GrammarMasterControllerV2
        controller = GrammarMasterControllerV2()
        
        print("📋 協調システム結果:")
        coordination_results = {}
        
        for sentence in test_sentences:
            result = controller.process_sentence(sentence, debug=False)
            coordination_results[sentence] = result.slots if result and result.slots else {}
            print(f"  '{sentence}' → {result.slots if result and result.slots else 'FAILED'}")
        
        print("\n" + "=" * 70)
        print("🔍 品質劣化原因分析")
        print("=" * 70)
        
        # 3. 品質劣化ポイント特定
        problems = []
        
        for sentence in test_sentences:
            direct = direct_results.get(sentence, {})
            coordinated = coordination_results.get(sentence, {})
            
            print(f"\n📊 '{sentence}':")
            print(f"  個別エンジン: {direct}")
            print(f"  協調システム: {coordinated}")
            
            # 主要な違いを検出
            if direct and coordinated:
                # スロット内容の比較
                for slot, value in direct.items():
                    coord_value = coordinated.get(slot, "")
                    if value != coord_value:
                        problem = f"スロット'{slot}': '{value}' → '{coord_value}'"
                        problems.append(problem)
                        print(f"  ❌ 劣化: {problem}")
                        
                # 余分なスロット
                extra_slots = set(coordinated.keys()) - set(direct.keys())
                if extra_slots:
                    problem = f"余分なスロット: {extra_slots}"
                    problems.append(problem)
                    print(f"  ⚠️ 余分: {problem}")
                    
                # 欠けているスロット
                missing_slots = set(direct.keys()) - set(coordinated.keys())
                if missing_slots:
                    problem = f"欠けているスロット: {missing_slots}"
                    problems.append(problem)
                    print(f"  ❌ 欠損: {problem}")
            
            elif direct and not coordinated:
                problems.append(f"協調システムが完全失敗: '{sentence}'")
                print(f"  ❌ 完全失敗: 協調システムが結果を返せず")
                
        print("\n" + "=" * 70)
        print("📋 システム設計の根本問題")
        print("=" * 70)
        
        if problems:
            print("🚨 品質劣化の根本原因:")
            for i, problem in enumerate(problems[:10], 1):  # 最初の10個まで
                print(f"  {i}. {problem}")
                
            print("\n🤔 マルチエンジン協調システムの構造的問題:")
            print("  1. 境界拡張ライブラリが原文を改変している")
            print("  2. 複数エンジンの結果をマージする際にデータが汚染される")
            print("  3. 協調戦略がエンジン本来の能力を阻害している")
            print("  4. 中央制御システムがボトルネックになっている")
            
            print("\n💡 理論的な解決アプローチ:")
            print("  A. 単一最適エンジン方式：最適エンジン1つだけを使用")
            print("  B. パイプライン方式：エンジンを順番に適用（協調ではなく）") 
            print("  C. 境界拡張の無効化：原文をそのまま使用")
            print("  D. 個別エンジン復帰：協調システムを廃止")
            
        else:
            print("✅ 品質劣化は検出されませんでした")
            print("協調システムは正常に機能しています")
            
    except Exception as e:
        print(f"❌ 分析エラー: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_engine_architecture_problems()
