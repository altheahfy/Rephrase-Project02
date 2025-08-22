#!/usr/bin/env python3
"""
関係節処理の詳細デバッグ
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

def debug_relative_clause():
    """関係節処理の詳細をデバッグ"""
    
    # より詳細なログ設定
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(message)s'
    )
    
    mapper = DynamicGrammarMapper()
    sentence = "The man who runs fast is strong."
    
    print(f"🔍 解析対象: '{sentence}'")
    print("=" * 60)
    
    # spaCy解析
    doc = mapper.nlp(sentence)
    tokens = mapper._extract_tokens(doc)
    
    print("📊 spaCyトークン解析:")
    for i, token in enumerate(tokens):
        print(f"  {i}: '{token['text']}' (POS:{token['pos']}, DEP:{token['dep']}, HEAD:{token['head']})")
    
    print("\n🧠 関係節検出:")
    relative_info = mapper._detect_relative_clause(tokens, sentence)
    print(f"  検出結果: {relative_info}")
    
    print("\n🔧 文法解析結果:")
    result = mapper.analyze_sentence(sentence)
    print(f"  文型: {result.get('pattern_detected', 'UNKNOWN')}")
    print(f"  スロット: {result['Slot']}")
    print(f"  フレーズ: {result['SlotPhrase']}")

if __name__ == "__main__":
    debug_relative_clause()
