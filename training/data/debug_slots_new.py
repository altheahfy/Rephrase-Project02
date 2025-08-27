#!/usr/bin/env python3
"""
副詞ハンドラーのスロット配置デバッグ
"""

from adverb_handler import AdverbHandler
import spacy

def debug_slot_assignment():
    handler = AdverbHandler()
    nlp = spacy.load('en_core_web_sm')
    
    test_sentence = "The students study hard for exams."
    print(f"テスト文: {test_sentence}")
    
    # spaCy解析を直接確認
    doc = nlp(test_sentence)
    print(f"\nspaCy解析:")
    for i, token in enumerate(doc):
        print(f"  {i}: '{token.text}' - {token.pos_} ({token.tag_})")
    
    # 動詞の位置を確認
    verb_positions = []
    for i, token in enumerate(doc):
        if token.pos_ in ['VERB', 'AUX']:
            verb_positions.append(i)
            print(f"  動詞発見: '{token.text}' at position {i}")
    
    # 副詞ハンドラーの結果
    result = handler.process(test_sentence)
    
    print(f"\n副詞ハンドラー結果:")
    print(f"Success: {result['success']}")
    print(f"Separated text: '{result['separated_text']}'")
    print(f"Modifiers: {result['modifiers']}")
    print(f"Modifier slots: {result.get('modifier_slots', {})}")
    
    # 修飾語の位置確認
    modifiers = result['modifiers']
    for verb_idx, modifier_list in modifiers.items():
        print(f"\n動詞{verb_idx}の修飾語:")
        for mod in modifier_list:
            idx = mod.get('idx', 'unknown')
            print(f"  '{mod['text']}' at index {idx} ({mod['type']})")
            
    # 動詞位置との比較
    if verb_positions and modifiers:
        main_verb_pos = verb_positions[0]  # 'study' at position 2
        print(f"\n位置関係分析:")
        print(f"  主動詞位置: {main_verb_pos}")
        
        for verb_idx, modifier_list in modifiers.items():
            for mod in modifier_list:
                mod_pos = mod.get('idx', -1)
                if mod_pos < main_verb_pos:
                    print(f"  '{mod['text']}' (pos {mod_pos}) → 動詞より前")
                else:
                    print(f"  '{mod['text']}' (pos {mod_pos}) → 動詞より後")

if __name__ == "__main__":
    debug_slot_assignment()
