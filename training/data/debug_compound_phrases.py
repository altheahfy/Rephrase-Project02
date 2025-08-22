#!/usr/bin/env python3
"""
複合名詞句認識のデバッグ
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def debug_compound_phrases():
    """複合名詞句の問題を詳細分析"""
    mapper = DynamicGrammarMapper()
    
    problem_sentences = [
        "He became a doctor.",
        "I gave him a book.", 
        "She told me a story."
    ]
    
    for sentence in problem_sentences:
        print(f"=== {sentence} ===")
        result = mapper.analyze_sentence(sentence)
        
        # 詳細なトークン分析
        doc = mapper.nlp(sentence)
        print("🔍 トークン解析:")
        for i, token in enumerate(doc):
            print(f"  {i}: '{token.text}' (pos={token.pos_}, tag={token.tag_})")
        
        # 認識結果
        print("\n📊 認識結果:")
        slots = result.get('main_slots', {})
        for slot, phrase in slots.items():
            print(f"  {slot}: '{phrase}'")
        
        # 配列形式の詳細
        print(f"\n🗂️  Slot配列: {result.get('Slot', [])}")
        print(f"   SlotPhrase配列: {result.get('SlotPhrase', [])}")
        
        print("-" * 50)

if __name__ == "__main__":
    debug_compound_phrases()
