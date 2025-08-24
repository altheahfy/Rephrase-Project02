#!/usr/bin/env python3
"""
受動態ハンドラー基本テスト（無限ループ回避）
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_basic_passive_voice():
    """受動態ハンドラーの基本テスト"""
    mapper = DynamicGrammarMapper()

    # 単純な受動態テスト文
    test_sentence = 'The book was written.'
    
    print(f'📝 テスト文: {test_sentence}')
    
    # 直接的なハンドラーテスト（analyze_sentence回避）
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(test_sentence)
        
        # 受動態ハンドラーを直接テスト
        result = mapper._handle_passive_voice(test_sentence, doc, {})
        print(f'🎯 受動態ハンドラー結果: {result}')
        
    except Exception as e:
        print(f'❌ エラー: {e}')

if __name__ == '__main__':
    test_basic_passive_voice()
