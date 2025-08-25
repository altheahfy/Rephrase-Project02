#!/usr/bin/env python3
"""
比較級・最上級ハンドラーの簡単なテスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def quick_test():
    mapper = DynamicGrammarMapper()
    
    # テスト: 比較級
    sentence = "This book is bigger than that one."
    result = mapper.analyze_sentence(sentence)
    
    print("=== 比較級テスト ===")
    print(f"文: {sentence}")
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"unified_handlers: {result.get('unified_handlers', {})}")
    
    # より具体的な確認
    if 'unified_handlers' in result:
        handlers = result['unified_handlers']
        if 'handler_contributions' in handlers:
            comp_handler = handlers['handler_contributions'].get('comparative_superlative')
            print(f"比較級ハンドラー結果: {comp_handler}")
    
    print()

if __name__ == "__main__":
    quick_test()
