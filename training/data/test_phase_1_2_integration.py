#!/usr/bin/env python3
"""
Phase 1.2文型認識機能の動作確認テスト
"""
from dynamic_grammar_mapper import DynamicGrammarMapper

def test_sentence_type_integration():
    """文型認識機能の統合テスト"""
    
    mapper = DynamicGrammarMapper()
    
    test_sentences = [
        "The car is red.",          # statement
        "What did you buy?",        # wh_question  
        "Are you coming?",          # yes_no_question
        "I love you."               # statement
    ]
    
    print("=== Phase 1.2 文型認識機能統合テスト ===\n")
    
    for sentence in test_sentences:
        result = mapper.analyze_sentence(sentence)
        
        sentence_type = result.get('sentence_type', 'unknown')
        confidence = result.get('sentence_type_confidence', 0.0)
        
        print(f"📝 '{sentence}'")
        print(f"   文型: {sentence_type}")
        print(f"   信頼度: {confidence:.2f}")
        print(f"   認識スロット: {result.get('Slot', {})}")
        print()

if __name__ == "__main__":
    test_sentence_type_integration()
