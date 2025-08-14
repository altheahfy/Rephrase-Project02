#!/usr/bin/env python3
"""
Priority 15 ImperativeEngine デバッグテスト

空の結果を返す問題を特定するためのデバッグスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from engines.imperative_engine import ImperativeEngine

def debug_imperative_engine():
    """Priority 15 ImperativeEngine の詳細デバッグ"""
    print("🔍 Priority 15 ImperativeEngine デバッグテスト")
    print("=" * 60)
    
    # エンジン初期化
    try:
        engine = ImperativeEngine()
        print("✅ ImperativeEngine 初期化成功")
    except Exception as e:
        print(f"❌ ImperativeEngine 初期化失敗: {e}")
        return
    
    test_cases = [
        "Go!",
        "Don't go!",
        "Give me the book.",
        "Put the book on the table carefully."
    ]
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{sentence}'")
        print("-" * 40)
        
        # Step 1: 基本チェック
        is_applicable = engine._is_imperative_candidate(sentence)
        print(f"Step 1 - is_imperative_candidate: {is_applicable}")
        
        if not is_applicable:
            print("❌ 基本チェックで除外された")
            continue
            
        # Step 2: フルプロセス実行
        try:
            result = engine.process(sentence, debug=True)
            print(f"Step 2 - プロセス結果:")
            print(f"  Success: {result.success}")
            print(f"  Confidence: {result.confidence}")
            print(f"  Slots: {result.slots}")
            print(f"  Error: {result.error}")
            print(f"  Processing Time: {result.processing_time:.4f}s")
            
            if result.metadata:
                print(f"  Metadata: {result.metadata}")
                
        except Exception as e:
            print(f"❌ プロセス実行エラー: {e}")
            import traceback
            traceback.print_exc()
            
        # Step 3: フォールバック分析テスト
        try:
            fallback_slots = engine._fallback_slot_analysis(sentence)
            print(f"Step 3 - フォールバック分析: {fallback_slots}")
        except Exception as e:
            print(f"❌ フォールバック分析エラー: {e}")
            
        # Step 4: 信頼度計算テスト
        try:
            confidence = engine._calculate_confidence(result.slots if 'result' in locals() else {}, sentence)
            print(f"Step 4 - 信頼度計算: {confidence}")
        except Exception as e:
            print(f"❌ 信頼度計算エラー: {e}")
    
    print("\n🏁 デバッグ完了")

if __name__ == "__main__":
    debug_imperative_engine()
