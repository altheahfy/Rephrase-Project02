#!/usr/bin/env python3
"""
whose構文の詳細テスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

def test_whose_clause_accuracy():
    """whose構文の精度テスト"""
    
    # 詳細ログ設定
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')
    
    mapper = DynamicGrammarMapper()
    
    # 様々なwhose構文のテストケース
    whose_test_cases = [
        {
            "sentence": "The woman whose car is blue works here.",
            "description": "基本whose構文 - SVC関係節",
            "expected_pattern": "SV",
            "expected_subject": "The woman whose car is blue",
            "expected_verb": "works",
            "complexity": "基本"
        },
        {
            "sentence": "The man whose daughter studies medicine is proud.",
            "description": "whose + 人物関係 + 動詞",
            "expected_pattern": "SVC",
            "expected_subject": "The man whose daughter studies medicine",
            "expected_verb": "is",
            "expected_complement": "proud",
            "complexity": "中級"
        },
        {
            "sentence": "The house whose roof was damaged needs repair.",
            "description": "whose + 受動態関係節",
            "expected_pattern": "SVO",
            "expected_subject": "The house whose roof was damaged",
            "expected_verb": "needs",
            "expected_object": "repair",
            "complexity": "中級"
        },
        {
            "sentence": "The student whose homework is always perfect gets good grades.",
            "description": "whose + 修飾語付き関係節",
            "expected_pattern": "SVO",
            "expected_subject": "The student whose homework is always perfect",
            "expected_verb": "gets",
            "expected_object": "good grades",
            "complexity": "上級"
        },
        {
            "sentence": "The company whose products are expensive lost customers.",
            "description": "whose + 複数形 + 形容詞",
            "expected_pattern": "SVO",
            "expected_subject": "The company whose products are expensive",
            "expected_verb": "lost",
            "expected_object": "customers",
            "complexity": "上級"
        },
        {
            "sentence": "I know the teacher whose class starts early.",
            "description": "whose構文が目的語位置",
            "expected_pattern": "SVO",
            "expected_subject": "I",
            "expected_verb": "know",
            "expected_object": "the teacher whose class starts early",
            "complexity": "上級"
        }
    ]
    
    print("=== whose構文精度テスト ===\n")
    
    success_count = 0
    total_count = len(whose_test_cases)
    
    for i, test_case in enumerate(whose_test_cases, 1):
        print(f"テスト {i} ({test_case['complexity']}): {test_case['sentence']}")
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
        
        print("-" * 70)
    
    accuracy = (success_count / total_count) * 100
    print(f"\n=== whose構文テスト結果サマリー ===")
    print(f"成功率: {success_count}/{total_count} ({accuracy:.1f}%)")
    print(f"改善が必要なケース: {total_count - success_count}")
    
    return whose_test_cases, success_count, total_count

if __name__ == "__main__":
    test_whose_clause_accuracy()
