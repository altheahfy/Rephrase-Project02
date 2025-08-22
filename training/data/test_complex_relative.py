#!/usr/bin/env python3
"""
より複雑な関係節テストケース
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

def test_complex_relative_clauses():
    """より複雑な関係節のテスト"""
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    
    mapper = DynamicGrammarMapper()
    
    # より複雑なテストケース
    complex_cases = [
        {
            "sentence": "The student who studies hard every day gets good grades.",
            "description": "長い関係節 - 修飾語を含む",
            "expected_pattern": "SVO"
        },
        {
            "sentence": "The house that we bought last year is very expensive.",
            "description": "目的格関係代名詞 + 時間修飾語",
            "expected_pattern": "SVC"
        },
        {
            "sentence": "The teacher whose students always pass the exam is popular.",
            "description": "whose + 複雑な関係節",
            "expected_pattern": "SVC"
        },
        {
            "sentence": "The city where my parents live is beautiful.",
            "description": "関係副詞where + 所有代名詞",
            "expected_pattern": "SVC"
        },
        {
            "sentence": "He told me the story that everyone knows.",
            "description": "SVOO構文 + 関係節目的語",
            "expected_pattern": "SVOO"
        },
        {
            "sentence": "She made the cake that tastes delicious.",
            "description": "SVO構文 + 関係節目的語",
            "expected_pattern": "SVO"
        }
    ]
    
    print("=== 複雑な関係節テスト ===\n")
    
    success_count = 0
    total_count = len(complex_cases)
    
    for i, test_case in enumerate(complex_cases, 1):
        print(f"テスト {i}: {test_case['sentence']}")
        print(f"説明: {test_case['description']}")
        
        result = mapper.analyze_sentence(test_case['sentence'])
        
        actual_pattern = result.get('pattern_detected', 'UNKNOWN')
        pattern_correct = actual_pattern == test_case['expected_pattern']
        
        print(f"📊 実際: {actual_pattern} | 期待: {test_case['expected_pattern']}")
        
        if pattern_correct:
            print("✅ 成功")
            success_count += 1
        else:
            print("❌ 失敗")
            print(f"  スロット: {result.get('Slot', [])}")
            print(f"  フレーズ: {result.get('SlotPhrase', [])}")
        
        print("-" * 50)
    
    accuracy = (success_count / total_count) * 100
    print(f"\n=== 複雑関係節テスト結果 ===")
    print(f"成功率: {success_count}/{total_count} ({accuracy:.1f}%)")
    
    return success_count, total_count

if __name__ == "__main__":
    test_complex_relative_clauses()
