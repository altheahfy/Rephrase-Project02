"""
🔍 統合エンジン vs 既存15エンジン性能比較テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from engines.basic_five_complete import BasicFivePatternEngine
import time

def performance_comparison_test():
    """性能比較テスト"""
    print("🔍 統合エンジン vs 既存15エンジン性能比較")
    print("=" * 70)
    
    # エンジン初期化
    print("⚙️ エンジン初期化中...")
    
    print("  📈 統合エンジン初期化...")
    unified_engine = SimpleUnifiedRephraseSlotIntegrator()
    
    print("  🔧 既存Basic Five Pattern Engine初期化...")
    basic_engine = BasicFivePatternEngine()
    
    # テスト文例
    test_sentences = [
        "I study English.",
        "She is a teacher.",
        "There are many students.",
        "I think that he is right.",
        "The letter was written by John.",
        "Yesterday, I carefully finished my work early.",
        "He gave me a book.",
        "We made him captain.",
        "Children are playing in the park.",
        "What did you buy?"
    ]
    
    print("🧪 性能比較テスト開始")
    print("=" * 70)
    
    unified_times = []
    basic_times = []
    unified_results = []
    basic_results = []
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト {i}: {sentence}")
        
        # 統合エンジンテスト
        start_time = time.time()
        unified_result = unified_engine.process(sentence)
        unified_time = time.time() - start_time
        unified_times.append(unified_time)
        unified_results.append(unified_result)
        
        # 既存エンジンテスト
        start_time = time.time()
        basic_result = basic_engine.process_sentence(sentence)
        basic_time = time.time() - start_time
        basic_times.append(basic_time)
        basic_results.append(basic_result)
        
        # 結果表示
        print(f"  🚀 統合エンジン ({unified_time:.4f}s):")
        if 'error' not in unified_result:
            filled_slots = {k: v for k, v in unified_result['slots'].items() if v}
            print(f"     スロット数: {len(filled_slots)}")
            for slot, content in list(filled_slots.items())[:3]:
                print(f"     {slot}: '{content}'")
        else:
            print(f"     エラー: {unified_result['error']}")
        
        print(f"  🔧 既存エンジン ({basic_time:.4f}s):")
        if basic_result and basic_result.get('processed'):
            print(f"     パターン: {basic_result['pattern']}")
            print(f"     信頼度: {basic_result['confidence']:.2f}")
            slots = basic_result.get('slots', {})
            for slot, content in list(slots.items())[:3]:
                print(f"     {slot}: '{content}'")
        else:
            print("     未処理/エラー")
    
    # 総合比較
    print(f"\n" + "=" * 70)
    print("📊 総合性能比較:")
    print(f"  🚀 統合エンジン:")
    print(f"     平均処理時間: {sum(unified_times)/len(unified_times):.4f}s")
    print(f"     成功処理数: {sum(1 for r in unified_results if 'error' not in r)}/{len(test_sentences)}")
    
    print(f"  🔧 既存エンジン:")
    print(f"     平均処理時間: {sum(basic_times)/len(basic_times):.4f}s")
    print(f"     成功処理数: {sum(1 for r in basic_results if r and r.get('processed'))}/{len(test_sentences)}")
    
    print(f"\n🎯 結論:")
    unified_success_rate = sum(1 for r in unified_results if 'error' not in r) / len(test_sentences)
    basic_success_rate = sum(1 for r in basic_results if r and r.get('processed')) / len(test_sentences)
    
    if unified_success_rate > basic_success_rate:
        print(f"  ✅ 統合エンジンの方が高精度 ({unified_success_rate:.1%} vs {basic_success_rate:.1%})")
    else:
        print(f"  ⚠️ 既存エンジンも競争力あり ({basic_success_rate:.1%} vs {unified_success_rate:.1%})")
    
    avg_unified_time = sum(unified_times)/len(unified_times)
    avg_basic_time = sum(basic_times)/len(basic_times)
    
    if avg_unified_time < avg_basic_time:
        print(f"  ⚡ 統合エンジンの方が高速 ({avg_unified_time:.4f}s vs {avg_basic_time:.4f}s)")
    else:
        print(f"  🐌 既存エンジンの方が高速 ({avg_basic_time:.4f}s vs {avg_unified_time:.4f}s)")

if __name__ == "__main__":
    performance_comparison_test()
