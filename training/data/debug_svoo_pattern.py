#!/usr/bin/env python3
"""
SVOO文型のデバッグ
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def debug_svoo_pattern():
    """SVOO文型の問題を詳細分析"""
    mapper = DynamicGrammarMapper()
    
    problem_sentences = [
        "I gave him a book.",
        "She told me a story.", 
        "He bought her flowers."
    ]
    
    for sentence in problem_sentences:
        print(f"=== {sentence} ===")
        result = mapper.analyze_sentence(sentence)
        
        # 詳細なトークン分析
        doc = mapper.nlp(sentence)
        print("🔍 トークン解析:")
        for i, token in enumerate(doc):
            print(f"  {i}: '{token.text}' (pos={token.pos_}, tag={token.tag_})")
        
        # 文型判定
        print(f"\n📊 検出文型: {result.get('pattern_detected', 'UNKNOWN')}")
        
        # 認識結果
        print("\n📋 認識結果:")
        slots = result.get('main_slots', {})
        for slot, phrase in slots.items():
            print(f"  {slot}: '{phrase}'")
        
        print("-" * 50)

if __name__ == "__main__":
    debug_svoo_pattern()
