#!/usr/bin/env python3
"""
関係節処理の精度向上テスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
import json

def test_relative_clause_accuracy():
    """関係節処理の精度テスト"""
    
    # 詳細ログ設定
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')
    
    mapper = DynamicGrammarMapper()
    
    # より複雑な関係節テストケース
    test_cases = [
        {
            "sentence": "The man who runs fast is strong.",
            "expected_pattern": "SVC",
            "expected_subject": "The man who runs fast",
            "expected_verb": "is",
            "expected_complement": "strong",
            "description": "主格関係代名詞who - 単純SV関係節"
        },
        {
            "sentence": "The car which is red looks nice.",
            "expected_pattern": "SVC", 
            "expected_subject": "The car which is red",
            "expected_verb": "looks",
            "expected_complement": "nice",
            "description": "主格関係代名詞which - SVC関係節"
        },
        {
            "sentence": "The book that I read was interesting.",
            "expected_pattern": "SVC",
            "expected_subject": "The book that I read", 
            "expected_verb": "was",
            "expected_complement": "interesting",
            "description": "目的格関係代名詞that - SVO関係節"
        },
        {
            "sentence": "The woman whose car is blue works here.",
            "expected_pattern": "SV",
            "expected_subject": "The woman whose car is blue",
            "expected_verb": "works",
            "description": "所有格関係代名詞whose"
        },
        {
            "sentence": "The place where I live is quiet.",
            "expected_pattern": "SVC",
            "expected_subject": "The place where I live",
            "expected_verb": "is", 
            "expected_complement": "quiet",
            "description": "関係副詞where"
        },
        {
            "sentence": "I know the man who teaches English.",
            "expected_pattern": "SVO",
            "expected_subject": "I",
            "expected_verb": "know",
            "expected_object": "the man who teaches English",
            "description": "関係節が目的語位置"
        }
    ]
    
    print("=== 関係節精度向上テスト ===\n")
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"テスト {i}: {test_case['sentence']}")
        print(f"説明: {test_case['description']}")
        
        result = mapper.analyze_sentence(test_case['sentence'])
        
        # 詳細分析
        actual_pattern = result.get('pattern_detected', 'UNKNOWN')
        actual_slots = result.get('Slot', [])
        actual_phrases = result.get('SlotPhrase', [])
        
        print(f"📊 実際の結果:")
        print(f"  文型: {actual_pattern}")
        print(f"  スロット: {actual_slots}")
        print(f"  フレーズ: {actual_phrases}")
        
        print(f"🎯 期待される結果:")
        print(f"  文型: {test_case['expected_pattern']}")
        if 'expected_subject' in test_case:
            print(f"  主語: {test_case['expected_subject']}")
        if 'expected_verb' in test_case:
            print(f"  動詞: {test_case['expected_verb']}")
        if 'expected_complement' in test_case:
            print(f"  補語: {test_case['expected_complement']}")
        if 'expected_object' in test_case:
            print(f"  目的語: {test_case['expected_object']}")
        
        # 精度評価
        pattern_correct = actual_pattern == test_case['expected_pattern']
        
        if pattern_correct:
            print("✅ 文型認識: 正確")
            success_count += 1
        else:
            print("❌ 文型認識: 不正確")
        
        print("-" * 60)
    
    accuracy = (success_count / total_count) * 100
    print(f"\n=== テスト結果サマリー ===")
    print(f"成功率: {success_count}/{total_count} ({accuracy:.1f}%)")
    print(f"改善が必要なケース: {total_count - success_count}")
    
    return test_cases, success_count, total_count

if __name__ == "__main__":
    test_relative_clause_accuracy()
