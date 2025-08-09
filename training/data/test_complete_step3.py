#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompleteRephraseParsingEngine Step 3テスト: 100%精度達成確認
正しいRephraseルール解釈に基づく最終テスト
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_step3_complete():
    """Step 3: 100%精度達成テスト"""
    print("🧪 Complete Engine Step 3: 100%精度達成テスト")
    print("=" * 50)
    
    engine = CompleteRephraseParsingEngine()
    
    # Step 3テストケース: 複雑な構造の完全網羅
    test_cases = [
        # 1. 基本5文型の完璧な処理
        {
            "sentence": "The man runs quickly every morning.",
            "expected": {
                "S": "The man", "V": "runs", "M2": "quickly", "M3": "every morning"
            },
            "description": "第1文型 + 副詞修飾語"
        },
        # 2. 真のSVOO構造（両方名詞）
        {
            "sentence": "My teacher gave me good advice.",
            "expected": {
                "S": "My teacher", "V": "gave", "O1": "me", "O2": "good advice"
            },
            "description": "真のSVOO構造：両目的語が名詞"
        },
        # 3. SVO + 前置詞句（副詞修飾語）
        {
            "sentence": "She explained the problem to her colleague clearly.",
            "expected": {
                "S": "She", "V": "explained", "O1": "the problem", 
                "M2": "to her colleague", "M3": "clearly"
            },
            "description": "SVO + 前置詞句副詞修飾語"
        },
        # 4. 複雑な時間表現
        {
            "sentence": "Last night at 10 PM, he finished his homework.",
            "expected": {
                "S": "he", "V": "finished", "O1": "his homework", "M3": "Last night at 10 PM"
            },
            "description": "複合時間表現"
        },
        # 5. 助動詞 + 動詞 + 複数修飾語
        {
            "sentence": "I will definitely visit you tomorrow morning.",
            "expected": {
                "S": "I", "Aux": "will", "V": "visit", "O1": "you", 
                "M2": "definitely", "M3": "tomorrow morning"
            },
            "description": "助動詞 + 複数修飾語"
        }
    ]
    
    total_elements = 0
    correct_elements = 0
    test_results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n=== Step 3 テスト {i}: {test['description']} ===")
        print(f"例文: {test['sentence']}")
        print(f"期待値: {test['expected']}")
        
        # パース実行
        result = engine.analyze_sentence(test['sentence'])
        
        # 結果検証（Step 2と同じ形式に変換）
        test_correct = 0
        test_total = 0
        element_results = {}
        
        # main_slotsから値を取得する関数
        def extract_value(result_dict, element):
            if 'main_slots' in result_dict and element in result_dict['main_slots']:
                slot_data = result_dict['main_slots'][element]
                if slot_data and isinstance(slot_data, list) and len(slot_data) > 0:
                    return slot_data[0].get('value', '')
            return None
        
        for element, expected_value in test['expected'].items():
            test_total += 1
            total_elements += 1
            
            actual_value = extract_value(result, element)
            if actual_value == expected_value:
                test_correct += 1
                correct_elements += 1
                element_results[element] = f"✅ {element}: '{expected_value}' → 検出済み"
            elif actual_value:
                element_results[element] = f"❌ {element}: 期待='{expected_value}', 実際='{actual_value}'"
            else:
                element_results[element] = f"❌ {element}: '{expected_value}' → 未検出"
        
        # テスト結果表示
        test_accuracy = (test_correct / test_total) * 100
        print(f"📊 実際の結果:")
        print(f"  抽出結果: {result}")
        for element_result in element_results.values():
            print(f"  {element_result}")
        print(f"  🎯 精度: {test_accuracy:.1f}% ({test_correct}/{test_total})")
        
        test_results.append({
            "test_id": i,
            "description": test['description'],
            "accuracy": test_accuracy,
            "correct": test_correct,
            "total": test_total
        })
        print("=" * 50)
    
    # 全体結果
    overall_accuracy = (correct_elements / total_elements) * 100
    print(f"\n🏆 Step 3 全体結果:")
    print(f"  総合精度: {overall_accuracy:.1f}% ({correct_elements}/{total_elements})")
    
    if overall_accuracy >= 100.0:
        print("🎉 **100%精度達成！CompleteRephraseParsingEngine完成！**")
    else:
        print(f"  改善必要項目数: {total_elements - correct_elements}")
        failed_tests = [t for t in test_results if t['accuracy'] < 100.0]
        if failed_tests:
            print("  改善が必要なテスト:")
            for test in failed_tests:
                print(f"    - テスト{test['test_id']}: {test['description']} ({test['accuracy']:.1f}%)")
    
    return overall_accuracy >= 100.0

if __name__ == "__main__":
    test_step3_complete()
