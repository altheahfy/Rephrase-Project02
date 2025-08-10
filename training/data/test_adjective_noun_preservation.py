#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
チェック7: 形容詞付き名詞の保持テスト

形容詞が名詞を修飾している場合、「形容詞+名詞」の組み合わせが
適切にスロットに保持されるかをテストします。

例:
- "a beautiful flower" → O1: "a beautiful flower" (形容詞付きで保持)
- "the old man" → S: "the old man" (形容詞付きで保持) 
- "big red car" → O1: "big red car" (複数形容詞付きで保持)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import spacy

def test_adjective_noun_combinations():
    """形容詞+名詞の組み合わせパターンをテスト"""
    
    print("✅ spaCy語彙認識エンジン初期化完了")
    
    test_sentences = [
        "I bought a beautiful flower.",
        "The old man walked slowly.",
        "She drives a big red car.",
        "He found an interesting book.",
        "They live in a small house.",
        "The young teacher explained clearly.",
        "We saw many tall buildings.",
        "She wore a long blue dress."
    ]
    
    print("=== 形容詞+名詞のspaCy依存関係分析 ===\n")
    
    # spaCy解析による形容詞修飾の確認
    nlp = spacy.load("en_core_web_sm")
    
    for sentence in test_sentences:
        doc = nlp(sentence)
        print(f"📝 例文: '{sentence}'")
        
        # 形容詞修飾パターンを検出
        adjective_noun_pairs = []
        for token in doc:
            if token.pos_ == 'NOUN':
                # この名詞を修飾する形容詞を探す
                modifying_adjs = []
                for child in token.children:
                    if child.pos_ == 'ADJ' and child.dep_ == 'amod':
                        modifying_adjs.append(child.text)
                
                if modifying_adjs:
                    # 決定詞も含める
                    det = ""
                    for child in token.children:
                        if child.pos_ == 'DET' and child.dep_ == 'det':
                            det = child.text + " "
                    
                    adj_phrase = det + " ".join(modifying_adjs) + " " + token.text
                    adjective_noun_pairs.append((adj_phrase.strip(), token.dep_))
                    print(f"  🔍 形容詞句: '{adj_phrase.strip()}' (文法役割: {token.dep_})")
        
        if not adjective_noun_pairs:
            print("  ❌ 形容詞修飾なし")
        
        print(f"  📊 全tokens: {[(token.text, token.pos_, token.dep_) for token in doc]}")
        print()

def test_adjective_noun_parsing():
    """CompleteRephraseParsingEngineでの形容詞+名詞解析テスト"""
    
    engine = CompleteRephraseParsingEngine()
    
    test_sentences = [
        "I bought a beautiful flower.",
        "The old man walked slowly.", 
        "She drives a big red car.",
        "He found an interesting book.",
        "They live in a small house.",
        "The young teacher explained clearly.",
        "We saw many tall buildings.",
        "She wore a long blue dress."
    ]
    
    print("=== チェック7: 形容詞+名詞保持テスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 例文{i:02d}: '{sentence}'")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # main_slotsからスロット内容を確認
            main_slots = result.get('main_slots', {})
            adjective_preservation_check = False
            
            for slot_name in ['S', 'O1', 'O2', 'C1']:
                if slot_name in main_slots and main_slots[slot_name]:
                    slot_values = main_slots[slot_name] if isinstance(main_slots[slot_name], list) else [main_slots[slot_name]]
                    
                    for value_item in slot_values:
                        # valueフィールドから実際の値を取得
                        if isinstance(value_item, dict) and 'value' in value_item:
                            value_str = value_item['value']
                        else:
                            value_str = str(value_item)
                        
                        # 形容詞を含むかチェック（簡易版）
                        adjective_indicators = [
                            'beautiful', 'old', 'big', 'red', 'interesting', 
                            'small', 'young', 'tall', 'long', 'blue'
                        ]
                        
                        if any(adj in value_str.lower() for adj in adjective_indicators):
                            adjective_preservation_check = True
                            print(f"  🔍 {slot_name}スロット: '{value_str}' ← 形容詞付き保持")
            
            # 結果表示
            if adjective_preservation_check:
                print("  ✅ 形容詞付き名詞が適切にスロットに保持されています")
            else:
                print("  ❌ 形容詞付き名詞の保持に問題があります")
                print(f"  📊 結果: {main_slots}")
                
        except Exception as e:
            print(f"  ❌ 解析エラー: {str(e)}")
        
        print()

if __name__ == "__main__":
    # spaCy依存関係分析
    test_adjective_noun_combinations()
    
    # CompleteRephraseParsingEngine解析
    test_adjective_noun_parsing()
