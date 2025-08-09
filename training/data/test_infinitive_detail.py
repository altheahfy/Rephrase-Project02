#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_infinitive_detection():
    engine = CompleteRephraseParsingEngine()
    
    test_sentence = 'I want to play tennis.'
    
    print(f'\n=== 不定詞の名詞的用法詳細テスト: {test_sentence} ===')
    
    # spaCy分析を手動で実行
    doc = engine.nlp(test_sentence)
    
    print("\n🔍 spaCy 依存関係分析:")
    for token in doc:
        print(f"  {token.text} [{token.pos_}] ({token.dep_}) <- {token.head.text}")
        if token.children:
            children = [child.text for child in token.children]
            print(f"    children: {children}")
    
    # 不定詞検出テスト
    test_phrase = "to play tennis"
    is_infinitive = engine._is_infinitive_as_noun(test_phrase, doc)
    print(f"\n🔍 不定詞の名詞的用法判定: '{test_phrase}' → {is_infinitive}")
    
    # 動詞含有テスト
    contains_verb = engine._contains_verb(test_phrase, doc)
    print(f"🔍 動詞含有判定: '{test_phrase}' → {contains_verb}")
    
    # 完全な解析実行
    print("\n🔍 完全解析結果:")
    result = engine.analyze_sentence(test_sentence)
    
    if result and 'main_slots' in result:
        main_slots = result['main_slots']
        
        print(f"\n📊 スロット分析:")
        for slot_name, candidates in main_slots.items():
            print(f"  {slot_name}:")
            for candidate in candidates:
                label = candidate.get('label', 'unlabeled')
                text = candidate.get('value', candidate.get('text', ''))
                is_phrase_flag = candidate.get('is_phrase', False)
                print(f"    - '{text}' [{label}] (is_phrase: {is_phrase_flag})")

if __name__ == "__main__":
    test_infinitive_detection()
