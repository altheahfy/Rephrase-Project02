#!/usr/bin/env python3
"""
簡単な関係節テスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

# デバッグログを有効化
logging.basicConfig(level=logging.DEBUG)

def test_relative_clause():
    mapper = DynamicGrammarMapper()
    
    test_sentences = [
        "The man who runs fast is strong.",
        "The car which is red looks nice.",
        "The book that I read was interesting."
    ]
    
    print("=== 関係節テスト ===")
    
    for sentence in test_sentences:
        print(f"\n📝 テスト文: '{sentence}'")
        result = mapper.analyze_sentence(sentence)
        
        print(f"✅ 文型: {result.get('pattern_detected', 'UNKNOWN')}")
        print(f"📊 スロット: {result['Slot']}")
        print(f"📄 フレーズ: {result['SlotPhrase']}")
        print(f"🎯 信頼度: {result.get('confidence', 0.0)}")
        print("-" * 50)

if __name__ == "__main__":
    test_relative_clause()
