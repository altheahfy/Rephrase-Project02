#!/usr/bin/env python3
"""
Grammar Master Controller経由でのPriority 15, 16テスト

直接エンジンと協調システム経由の結果比較
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from engines.imperative_engine import ImperativeEngine
from engines.existential_there_engine import ExistentialThereEngine
from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_controller_vs_direct():
    """直接エンジン vs 協調システム比較テスト"""
    print("🔍 直接エンジン vs Grammar Master Controller比較テスト")
    print("=" * 70)
    
    # エンジン初期化
    print("\n📋 エンジン初期化...")
    try:
        imperative_engine = ImperativeEngine()
        existential_engine = ExistentialThereEngine()
        controller = GrammarMasterControllerV2()
        print("✅ 全エンジン初期化成功")
    except Exception as e:
        print(f"❌ 初期化失敗: {e}")
        return
    
    test_cases = [
        # Priority 15 テスト
        ("Go!", "IMPERATIVE"),
        ("Don't go!", "IMPERATIVE"),
        ("Give me the book.", "IMPERATIVE"),
        ("Put the book on the table carefully.", "IMPERATIVE"),
        
        # Priority 16 テスト
        ("There is a book on the table.", "EXISTENTIAL_THERE"),
        ("There are many students.", "EXISTENTIAL_THERE"),
        ("There will be a party tonight.", "EXISTENTIAL_THERE"),
        ("There have been several complaints recently.", "EXISTENTIAL_THERE"),
    ]
    
    for i, (sentence, expected_engine) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{sentence}'")
        print(f"期待エンジン: {expected_engine}")
        print("-" * 50)
        
        # 直接エンジンテスト
        if expected_engine == "IMPERATIVE":
            direct_result = imperative_engine.process(sentence, debug=False)
            print(f"直接エンジン結果:")
            print(f"  Success: {direct_result.success}")
            print(f"  Confidence: {direct_result.confidence}")
            print(f"  Slots: {direct_result.slots}")
        else:  # EXISTENTIAL_THERE
            direct_result = existential_engine.process(sentence)
            print(f"直接エンジン結果:")
            print(f"  Success: {direct_result['success']}")
            print(f"  Confidence: {direct_result['confidence']}")
            print(f"  Slots: {direct_result['slots']}")
        
        # 協調システムテスト
        try:
            controller_result = controller.process_sentence(sentence, debug=True)
            print(f"協調システム結果:")
            print(f"  Success: {controller_result.success}")
            print(f"  Confidence: {controller_result.confidence}")
            print(f"  Slots: {controller_result.slots}")
            print(f"  Engine Type: {controller_result.engine_type}")
            
            if hasattr(controller_result, 'metadata'):
                print(f"  Metadata: {controller_result.metadata}")
                
        except Exception as e:
            print(f"❌ 協調システムエラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🏁 比較テスト完了")

if __name__ == "__main__":
    test_controller_vs_direct()
