#!/usr/bin/env python3
"""
協調システムでのPrepositionalEngine連携テスト
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_prepositional_coordination():
    """前置詞エンジンとの協調システムをテスト"""
    print("🔍 前置詞エンジン協調システムテスト")
    print("=" * 60)
    
    controller = GrammarMasterControllerV2()
    
    test_cases = [
        # Priority 15 + Prepositional coordination
        "Put the book on the table carefully.",
        
        # Priority 16 + Prepositional coordination  
        "There is a book on the table.",
        
        # 前置詞エンジン単独テスト
        "The book is on the table.",
    ]
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{sentence}'")
        print("-" * 50)
        
        try:
            result = controller.process_sentence(sentence, debug=True)
            print(f"Success: {result.success}")
            print(f"Engine Type: {result.engine_type}")
            print(f"Confidence: {result.confidence}")
            print(f"Slots: {result.slots}")
            
            if result.metadata:
                coordination_info = result.metadata.get('coordination_strategy', 'N/A')
                print(f"Coordination Strategy: {coordination_info}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🏁 協調システムテスト完了")

if __name__ == "__main__":
    test_prepositional_coordination()
