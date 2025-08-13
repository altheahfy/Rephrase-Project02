#!/usr/bin/env python3
"""
Grammar Master Controller v2 成功率測定ツール
各エンジンの実際の処理精度を測定
"""

from grammar_master_controller_v2 import GrammarMasterControllerV2
from rephrase_slot_validator import RephraseSlotValidator

def test_engine_success_rates():
    """エンジン成功率の測定"""
    
    controller = GrammarMasterControllerV2()
    validator = RephraseSlotValidator()
    
    # エンジン別テストケース
    test_cases = {
        'basic_five': [
            "I go.",
            "She likes cats.",
            "He is tall.",
            "They gave me a book.",
            "We made him happy."
        ],
        'modal': [
            "I can swim.",
            "She must go.",
            "They should study.",
            "We will help.",
            "You may enter."
        ],
        'progressive': [
            "I am running.",
            "She was sleeping.",
            "They are playing.",
            "We were working.",
            "He is studying."
        ],
        'conjunction': [
            "I go because she asked.",
            "Although it rains, we play.",
            "Since you're here, let's start.",
            "While she works, I rest.",
            "If it's sunny, we'll go."
        ],
        'passive': [
            "The book was written by him.",
            "The car is being repaired.",
            "The house was built yesterday.",
            "The letter has been sent.",
            "The work will be finished."
        ],
        'prepositional': [
            "The cat is on the table.",
            "We met at school.",
            "She lives in Tokyo.",
            "They go by car.",
            "The book is under the desk."
        ]
    }
    
    results = {}
    
    print("🔍 エンジン成功率測定開始...\n")
    
    for engine_category, sentences in test_cases.items():
        print(f"📊 {engine_category.upper()} エンジンテスト:")
        
        success_count = 0
        valid_slot_count = 0
        
        for sentence in sentences:
            try:
                # 処理実行
                result = controller.process_sentence(sentence, debug=False)
                
                # 成功判定
                if result.success:
                    success_count += 1
                    
                    # スロット構造検証
                    is_valid, errors, warnings = validator.validate_slots(result.slots)
                    if is_valid:
                        valid_slot_count += 1
                        print(f"  ✅ '{sentence}' → {result.slots}")
                    else:
                        print(f"  ⚠️ '{sentence}' → スロット構造エラー: {errors}")
                else:
                    print(f"  ❌ '{sentence}' → 処理失敗: {result.error}")
                    
            except Exception as e:
                print(f"  💥 '{sentence}' → 例外: {e}")
        
        success_rate = (success_count / len(sentences)) * 100
        valid_rate = (valid_slot_count / len(sentences)) * 100
        
        results[engine_category] = {
            'success_rate': success_rate,
            'valid_rate': valid_rate,
            'total_tests': len(sentences),
            'successful': success_count,
            'valid_slots': valid_slot_count
        }
        
        print(f"  📈 成功率: {success_rate:.1f}% ({success_count}/{len(sentences)})")
        print(f"  📋 有効スロット率: {valid_rate:.1f}% ({valid_slot_count}/{len(sentences)})")
        print()
    
    # 総合結果
    print("=" * 60)
    print("📊 総合成功率レポート")
    print("=" * 60)
    
    for engine, stats in results.items():
        print(f"{engine:15s}: 成功率 {stats['success_rate']:5.1f}% | 有効率 {stats['valid_rate']:5.1f}%")
    
    # 平均成功率
    avg_success = sum(stats['success_rate'] for stats in results.values()) / len(results)
    avg_valid = sum(stats['valid_rate'] for stats in results.values()) / len(results)
    
    print("-" * 60)
    print(f"平均成功率: {avg_success:.1f}%")
    print(f"平均有効率: {avg_valid:.1f}%")
    
    return results

if __name__ == "__main__":
    test_engine_success_rates()
