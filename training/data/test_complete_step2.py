#!/usr/bin/env python3
"""
Complete Rephrase Parsing Engine - Step 2 テスト
時間表現とSVOO構造の詳細検証
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_step2_improvements():
    engine = CompleteRephraseParsingEngine()
    
    print("🧪 Complete Engine Step 2: 複雑文構造テスト")
    print("=" * 50)
    
    test_cases = [
        {
            "id": 1,
            "sentence": "He left New York a few days ago.",
            "focus": "時間表現の完全抽出",
            "expected": {
                "S": "He",
                "V": "left", 
                "O1": "New York",
                "M3": "a few days ago"  # 時間修飾語
            }
        },
        {
            "id": 2,
            "sentence": "That afternoon, she gave him a book.",
            "focus": "SVOO構造 + 時間表現",
            "expected": {
                "S": "she",
                "V": "gave",
                "O1": "him",      # 間接目的語
                "O2": "a book",   # 直接目的語
                "M3": "That afternoon"  # 時間修飾語
            }
        },
        {
            "id": 3,
            "sentence": "I can't afford it today.",
            "focus": "助動詞縮約 + 時間表現",
            "expected": {
                "S": "I",
                "Aux": "cannot",  # 縮約形展開
                "V": "afford",
                "O1": "it",
                "M3": "today"     # 時間修飾語
            }
        },
        {
            "id": 4,
            "sentence": "She teaches English to students every morning.",
            "focus": "SVO + 前置詞句（副詞）+ 時間修飾",
            "expected": {
                "S": "She",
                "V": "teaches",
                "O1": "English",         # 直接目的語
                "M2": "to students",     # 副詞的修飾語（前置詞句）
                "M3": "every morning"    # 時間修飾語
            }
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n=== Step 2 テスト {test['id']}: {test['focus']} ===")
        print(f"例文: {test['sentence']}")
        print(f"期待値: {test['expected']}")
        
        result = engine.analyze_sentence(test['sentence'])
        
        print(f"📊 実際の結果:")
        extracted = {}
        for slot_type, values in result['main_slots'].items():
            if values:
                extracted[slot_type] = [v['value'] for v in values]
        
        print(f"  抽出結果: {extracted}")
        print(f"  文型: {result.get('sentence_type', 'unknown')}")
        
        # 期待値との比較
        matches = 0
        total = len(test['expected'])
        
        for expected_slot, expected_value in test['expected'].items():
            actual_values = extracted.get(expected_slot, [])
            if any(expected_value.lower() in str(val).lower() for val in actual_values):
                print(f"  ✅ {expected_slot}: '{expected_value}' → 検出済み")
                matches += 1
            else:
                print(f"  ❌ {expected_slot}: '{expected_value}' → 未検出")
        
        accuracy = (matches / total) * 100 if total > 0 else 0
        print(f"  🎯 精度: {accuracy:.1f}% ({matches}/{total})")
        
        results.append({
            'test_id': test['id'],
            'accuracy': accuracy,
            'matches': matches,
            'total': total
        })
        
        print("=" * 50)
    
    # 全体サマリー
    overall_matches = sum(r['matches'] for r in results)
    overall_total = sum(r['total'] for r in results)
    overall_accuracy = (overall_matches / overall_total) * 100 if overall_total > 0 else 0
    
    print(f"\n🏆 Step 2 全体結果:")
    print(f"  総合精度: {overall_accuracy:.1f}% ({overall_matches}/{overall_total})")
    print(f"  改善必要項目数: {overall_total - overall_matches}")
    
    return results

if __name__ == "__main__":
    test_step2_improvements()
