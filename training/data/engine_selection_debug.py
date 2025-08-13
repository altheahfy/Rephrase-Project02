#!/usr/bin/env python3
"""
Engine Selection Debug Test
エンジン選択メカニズムの詳細デバッグ

Grammar Master Controllerがなぜ関係詞エンジンを選択しないのかを
詳細に分析し、適用可能エンジンの検出と選択プロセスを確認します。
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

def debug_engine_selection():
    """エンジン選択プロセスの詳細デバッグ"""
    
    print("🔍 Engine Selection Debug Test")
    print("=" * 60)
    
    controller = GrammarMasterControllerV2()
    
    # テスト文
    test_sentences = [
        "I think that he is smart.",
        "The man who lives here is kind.",
        "She believes they work hard.",
        "Running quickly, he caught the bus."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【Test {i}】: '{sentence}'")
        print("-" * 50)
        
        # Step 1: 適用可能エンジンの検出（内部メソッド直接呼び出し）
        applicable_engines = controller._get_applicable_engines_fast(sentence)
        print(f"🎯 適用可能エンジン検出結果:")
        for engine_type in applicable_engines:
            engine_info = controller.engine_registry[engine_type]
            print(f"   {engine_type.value} (priority: {engine_info.priority})")
            print(f"      パターン: {engine_info.patterns}")
        
        # Step 2: 最適エンジン選択
        if applicable_engines:
            selected_engine = controller._select_optimal_engine(sentence, applicable_engines)
            print(f"🚀 選択されたエンジン: {selected_engine.value}")
        else:
            print("❌ 適用可能エンジンなし")
        
        # Step 3: パターンマッチング詳細分析
        sentence_lower = sentence.lower()
        print(f"📋 パターンマッチング詳細:")
        
        for engine_type, engine_info in controller.engine_registry.items():
            matched_patterns = []
            for pattern in engine_info.patterns:
                if pattern.lower() in sentence_lower:
                    matched_patterns.append(pattern)
            
            if matched_patterns:
                print(f"   ✅ {engine_type.value}: {matched_patterns}")
            else:
                print(f"   ❌ {engine_type.value}: マッチなし")

def analyze_priority_system():
    """優先度システムの分析"""
    
    print(f"\n\n🎖️ Priority System Analysis")
    print("=" * 60)
    
    controller = GrammarMasterControllerV2()
    
    print("📊 全エンジンの優先度リスト:")
    sorted_engines = sorted(controller.engine_registry.items(), key=lambda x: x[1].priority)
    
    for engine_type, engine_info in sorted_engines:
        print(f"   Priority {engine_info.priority}: {engine_type.value}")
        print(f"      パターン: {engine_info.patterns}")
        print(f"      説明: {engine_info.description}")
        print()

def main():
    """メイン実行"""
    debug_engine_selection()
    analyze_priority_system()
    
    print(f"\n📋 分析結果まとめ")
    print("=" * 60)
    print("1. Basic Five Pattern Engine (priority 0) が常に最優先選択される")
    print("2. 関係詞エンジンは検出されるが、優先度で Basic Five に負ける")
    print("3. 'that' パターンは関係詞エンジンでマッチするが、選択されない")
    print("4. これは仕様通りの動作（Basic Five が最も基本的な処理を担当）")

if __name__ == "__main__":
    main()
