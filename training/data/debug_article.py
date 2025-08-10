#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冠詞問題のデバッグ
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def debug_article_issue():
    print("=== 冠詞問題のデバッグ ===\n")
    
    engine = CompleteRephraseParsingEngine()
    
    sentence = 'The boy who plays soccer is my friend.'
    print(f"テスト文: {sentence}")
    
    # spaCy解析
    doc = engine.nlp(sentence)
    
    print("\n=== spaCyトークン情報 ===")
    for token in doc:
        print(f"{token.i}: '{token.text}' (pos: {token.pos_}, dep: {token.dep_}, head: '{token.head.text}')")
    
    print("\n=== 主語トークンのテスト ===")
    for token in doc:
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            print(f"主語トークン: '{token.text}' (位置: {token.i})")
            complete_phrase = engine._get_complete_noun_phrase(token)
            print(f"_get_complete_noun_phrase結果: '{complete_phrase}'")
            
            print("\n冠詞の検索:")
            for child in token.children:
                print(f"  子要素: '{child.text}' (pos: {child.pos_}, dep: {child.dep_}, i: {child.i})")

if __name__ == "__main__":
    debug_article_issue()
