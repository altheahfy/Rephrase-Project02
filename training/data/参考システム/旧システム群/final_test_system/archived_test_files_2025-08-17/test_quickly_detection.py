#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_quickly_detection():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    print(f"分析文: {sentence}")
    print()
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # Stanza解析結果を直接確認
    doc = mapper.nlp(sentence)
    
    print("=== Stanza解析詳細 ===")
    for sent in doc.sentences:
        for word in sent.words:
            if 'quick' in word.text.lower():
                print(f"quickly検出:")
                print(f"  text: {word.text}")
                print(f"  deprel: {word.deprel}")
                print(f"  upos: {word.upos}")
                print(f"  head: {word.head}")
                
                # head tokenを確認
                if word.head > 0:
                    head_word = sent.words[word.head - 1]  # 1-indexed
                    print(f"  head_text: {head_word.text}")
                    print(f"  head_deprel: {head_word.deprel}")
                print()
    
    # 副詞検出条件をテスト
    for sent in doc.sentences:
        for word in sent.words:
            if 'quick' in word.text.lower():
                is_adverb = (
                    word.deprel in ['advmod', 'obl', 'obl:tmod', 'obl:npmod', 'obl:agent', 'obl:unmarked', 'nmod:tmod'] or
                    word.upos == 'ADV'
                )
                print(f"quickly副詞判定: {is_adverb}")
                print(f"  deprel in advmod系: {word.deprel in ['advmod', 'obl', 'obl:tmod', 'obl:npmod', 'obl:agent', 'obl:unmarked', 'nmod:tmod']}")
                print(f"  upos == ADV: {word.upos == 'ADV'}")
                print()
    
    # システム処理結果
    print("=== システム処理結果 ===")
    result = mapper.process(sentence)
    sub_slots = result.get('sub_slots', {})
    print(f"従属節スロット: {sub_slots}")
    
    # quicklyがsub_slotsに含まれているかチェック
    quickly_found = False
    for slot_key, slot_value in sub_slots.items():
        if slot_value and 'quickly' in slot_value.lower():
            quickly_found = True
            print(f"quickly発見: {slot_key} = '{slot_value}'")
    
    if not quickly_found:
        print("❌ quicklyが従属節スロットに見つかりません")

if __name__ == "__main__":
    test_quickly_detection()
