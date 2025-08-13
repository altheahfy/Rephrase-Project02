#!/usr/bin/env python3
"""前置詞句エンジンのデバッグスクリプト"""

from engines.prepositional_phrase_engine import PrepositionalPhraseEngine
import re

def debug_prepositional_engine():
    engine = PrepositionalPhraseEngine()
    test_text = 'The book is on the table.'
    
    print(f"📋 詳細デバッグ: '{test_text}'")
    print("-" * 50)
    
    # 前置詞リストの確認
    print(f"登録されている前置詞数: {len(engine.all_prepositions)}")
    print(f"前置詞 'on' が含まれているか: {'on' in engine.all_prepositions}")
    print(f"前置詞の一部: {list(engine.all_prepositions)[:10]}")
    
    # 直接正規表現テスト
    test_prep = 'on'
    pattern = r'\b' + re.escape(test_prep) + r'\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;)|\s*$)'
    print(f"\n正規表現パターン: {pattern}")
    
    matches = list(re.finditer(pattern, test_text, re.IGNORECASE))
    print(f"正規表現マッチ数: {len(matches)}")
    
    for i, match in enumerate(matches):
        print(f"  マッチ {i+1}: '{match.group(0)}'")
        print(f"  目的語: '{match.group(1)}'")
        print(f"  位置: {match.start()}-{match.end()}")
    
    # extract_prepositional_phrases メソッドのテスト
    print(f"\n📊 extract_prepositional_phrases の結果:")
    phrases = engine.extract_prepositional_phrases(test_text)
    print(f"抽出された前置詞句数: {len(phrases)}")
    
    for i, phrase in enumerate(phrases):
        print(f"  前置詞句 {i+1}: {phrase}")

if __name__ == "__main__":
    debug_prepositional_engine()
