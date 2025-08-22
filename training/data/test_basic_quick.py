#!/usr/bin/env python3
"""
基本5文型テスト（簡易版）
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

def test_basic_patterns():
    """基本5文型のテスト"""
    
    logging.basicConfig(level=logging.WARNING)  # ログを簡潔に
    
    mapper = DynamicGrammarMapper()
    
    basic_cases = [
        ("The car is red.", "SVC"),
        ("I love you.", "SVO"), 
        ("Birds fly.", "SV"),
        ("I gave him a book.", "SVOO"),
        ("They made her happy.", "SVOC")
    ]
    
    print("=== 基本5文型テスト ===\n")
    
    success_count = 0
    
    for sentence, expected in basic_cases:
        result = mapper.analyze_sentence(sentence)
        actual = result.get('pattern_detected', 'UNKNOWN')
        
        if actual == expected:
            print(f"✅ {sentence} → {actual}")
            success_count += 1
        else:
            print(f"❌ {sentence} → {actual} (期待: {expected})")
    
    accuracy = (success_count / len(basic_cases)) * 100
    print(f"\n基本5文型精度: {success_count}/{len(basic_cases)} ({accuracy:.1f}%)")
    
    return success_count == len(basic_cases)

if __name__ == "__main__":
    test_basic_patterns()
