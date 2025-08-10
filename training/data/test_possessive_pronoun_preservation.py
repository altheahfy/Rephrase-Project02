#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
チェック8: 所有格代名詞保持テスト

所有格代名詞（his, her, their, my, your, our, its）を含む名詞句が
適切にスロットに保持されるかをテストします。

問題例:
- "He resembles his mother." → O1: "mother" (❌ "his"が欠落)
- 正しくは → O1: "his mother"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import spacy

def test_possessive_pronoun_analysis():
    """所有格代名詞+名詞のspaCy依存関係分析"""
    
    print("✅ spaCy語彙認識エンジン初期化完了")
    
    test_sentences = [
        "He resembles his mother.",
        "She resembles her father.",
        "Tom resembles his uncle.",
        "They resemble their parents.",
        "I love my car.",
        "You forgot your keys.",
        "We sold our house.",
        "The dog wagged its tail."
    ]
    
    print("=== 所有格代名詞+名詞のspaCy依存関係分析 ===\n")
    
    nlp = spacy.load("en_core_web_sm")
    
    for sentence in test_sentences:
        doc = nlp(sentence)
        print(f"📝 例文: '{sentence}'")
        
        # 所有格代名詞を含む名詞句を検出
        possessive_noun_phrases = []
        for token in doc:
            if token.pos_ == 'NOUN':
                # この名詞を修飾する所有格代名詞を探す
                possessive_modifiers = []
                for child in token.children:
                    if child.pos_ == 'PRON' and child.dep_ == 'poss':
                        possessive_modifiers.append(child.text)
                
                if possessive_modifiers:
                    # 決定詞や形容詞も含める
                    full_phrase_tokens = []
                    for child in token.children:
                        if child.dep_ in ['det', 'amod', 'poss']:
                            full_phrase_tokens.append((child.text, child.i))
                    
                    # トークンを位置順でソート
                    full_phrase_tokens.sort(key=lambda x: x[1])
                    modifier_text = " ".join([t[0] for t in full_phrase_tokens])
                    
                    full_phrase = f"{modifier_text} {token.text}".strip()
                    possessive_noun_phrases.append((full_phrase, token.dep_))
                    print(f"  🔍 所有格句: '{full_phrase}' (文法役割: {token.dep_})")
        
        if not possessive_noun_phrases:
            print("  ❌ 所有格代名詞修飾なし")
        
        print(f"  📊 全tokens: {[(token.text, token.pos_, token.dep_) for token in doc]}")
        print()

def test_possessive_pronoun_parsing():
    """CompleteRephraseParsingEngineでの所有格代名詞保持テスト"""
    
    engine = CompleteRephraseParsingEngine()
    
    test_sentences = [
        "He resembles his mother.",
        "She resembles her father.", 
        "Tom resembles his uncle.",
        "They resemble their parents.",
        "I love my car.",
        "You forgot your keys.",
        "We sold our house.",
        "The dog wagged its tail."
    ]
    
    print("=== チェック8: 所有格代名詞保持テスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 例文{i:02d}: '{sentence}'")
        
        try:
            result = engine.analyze_sentence(sentence)
            main_slots = result.get('main_slots', {})
            
            # 所有格代名詞の保持チェック
            possessive_preservation_check = False
            missing_possessives = []
            
            # 期待される所有格代名詞
            expected_possessives = {
                "He resembles his mother.": "his",
                "She resembles her father.": "her",
                "Tom resembles his uncle.": "his", 
                "They resemble their parents.": "their",
                "I love my car.": "my",
                "You forgot your keys.": "your",
                "We sold our house.": "our",
                "The dog wagged its tail.": "its"
            }
            
            expected_poss = expected_possessives.get(sentence, "")
            
            for slot_name in ['S', 'O1', 'O2', 'C1']:
                if slot_name in main_slots and main_slots[slot_name]:
                    slot_values = main_slots[slot_name] if isinstance(main_slots[slot_name], list) else [main_slots[slot_name]]
                    
                    for value_item in slot_values:
                        if isinstance(value_item, dict) and 'value' in value_item:
                            value_str = value_item['value']
                        else:
                            value_str = str(value_item)
                        
                        # 所有格代名詞が含まれているかチェック
                        if expected_poss and expected_poss in value_str.lower():
                            possessive_preservation_check = True
                            print(f"  🔍 {slot_name}スロット: '{value_str}' ← 所有格代名詞保持")
                        elif expected_poss and expected_poss not in value_str.lower():
                            # 名詞のみで所有格が欠落している可能性
                            possessive_words = ['mother', 'father', 'uncle', 'parents', 'car', 'keys', 'house', 'tail']
                            if any(word in value_str.lower() for word in possessive_words):
                                missing_possessives.append((slot_name, value_str, expected_poss))
            
            # 結果表示
            if possessive_preservation_check:
                print("  ✅ 所有格代名詞が適切にスロットに保持されています")
            elif missing_possessives:
                print("  ❌ 所有格代名詞の保持に問題があります")
                for slot_name, value, expected in missing_possessives:
                    print(f"      {slot_name}: '{value}' → 期待値: '{expected} {value.split()[-1]}'")
                print(f"  📊 結果: {main_slots}")
            else:
                print("  ❓ 所有格代名詞含有の確認ができませんでした")
                print(f"  📊 結果: {main_slots}")
                
        except Exception as e:
            print(f"  ❌ 解析エラー: {str(e)}")
        
        print()

if __name__ == "__main__":
    # spaCy依存関係分析
    test_possessive_pronoun_analysis()
    
    # CompleteRephraseParsingEngine解析
    test_possessive_pronoun_parsing()
