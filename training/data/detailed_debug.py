#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
句動詞コンポーネント抽出の詳細デバッグ
"""

from Rephrase_Parsing_Engine import RephraseParsingEngine
import spacy

def detailed_debug():
    print("=== 句動詞コンポーネント抽出の詳細デバッグ ===")
    
    parser = RephraseParsingEngine()
    sentence = "Could you write it down"
    
    # Step 1: 句動詞検出
    phrasal_verbs = parser.detect_phrasal_verbs_with_spacy(sentence)
    print(f"句動詞検出結果: {phrasal_verbs}")
    
    if phrasal_verbs:
        # Step 2: 成分抽出の詳細
        doc = parser.nlp(sentence)
        print(f"\nspaCy doc: {[token.text for token in doc]}")
        
        for verb, pv_info in phrasal_verbs.items():
            verb_token = pv_info['verb_token']
            particle_token = pv_info['particle_token']
            
            print(f"\n動詞: {verb_token.text} (index: {verb_token.i})")
            print(f"パーティクル: {particle_token.text} (index: {particle_token.i})")
            
            print("\n依存関係チェック:")
            for token in doc:
                if token.head == verb_token:
                    print(f"  {token.text} ({token.dep_}) -> {verb_token.text}")
        
        # Step 3: パーサー結果
        result = parser.extract_phrasal_verb_components(sentence, phrasal_verbs)
        print(f"\n抽出結果: {result}")
    
    # Step 4: 最終パーサー結果  
    final_result = parser.analyze_sentence(sentence)
    print(f"\n最終結果: {final_result}")

if __name__ == "__main__":
    detailed_debug()
