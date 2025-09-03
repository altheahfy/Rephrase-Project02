#!/usr/bin/env python3
"""
リファクタリング後のテストスクリプト
Phase 1 & Phase 2 の動作確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController

def test_refactored_system():
    """リファクタリング後のシステムテスト"""
    
    print("🔧 リファクタリング後システムテスト開始")
    print("=" * 60)
    
    controller = CentralController()
    
    # Phase 1テスト: データ駆動型早期検出
    phase1_tests = [
        'Imagine if he had studied harder.',
        'Provided that you study hard, you will pass.',
        'As long as you work hard, you will succeed.',
        'If he had known, he would have helped.',
        'Even if it rains, we will go.'
    ]
    
    print("\n📋 Phase 1テスト: データ駆動型早期検出")
    print("-" * 50)
    
    for i, test_sentence in enumerate(phase1_tests, 151):
        print(f"\n🧪 Case {i}: {test_sentence}")
        
        try:
            # 新システム（v2）でテスト
            result_v2 = controller.process_sentence_v2(test_sentence)
            print(f"✅ v2 Success: {result_v2.get('success', False)}")
            
            # 従来システムと比較
            result_v1 = controller.process_sentence(test_sentence)
            print(f"🔄 v1 Success: {result_v1.get('success', False)}")
            
            # 結果比較
            if result_v2.get('success') == result_v1.get('success'):
                print("✅ 互換性確認: OK")
            else:
                print("⚠️ 互換性警告: 結果が異なります")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    # Phase 2テスト: ProcessingContext
    print("\n\n📋 Phase 2テスト: ProcessingContext活用")
    print("-" * 50)
    
    phase2_tests = [
        'The book that he bought is interesting.',
        'Can you tell me what happened?',
        'She studies harder than her brother.'
    ]
    
    for test_sentence in phase2_tests:
        print(f"\n🧪 ProcessingContext: {test_sentence}")
        
        try:
            result = controller.process_sentence_v2(test_sentence)
            print(f"✅ ProcessingContext Success: {result.get('success', False)}")
            
            if result.get('success'):
                grammar_pattern = result.get('grammar_pattern', 'unknown')
                print(f"📝 文法パターン: {grammar_pattern}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 リファクタリングテスト完了")

if __name__ == "__main__":
    test_refactored_system()
