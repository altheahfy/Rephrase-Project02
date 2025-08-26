#!/usr/bin/env pdef debug_case_42():
    """Case 42の副詞処理をデバッグ"""
    mapper = UnifiedStanzaRephraseMapper()
    
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    result = mapper.process_sentence(sentence)
    
    print(f"\n=== 結果 ===")
    print(f"S: '{result.get('slots', {}).get('S')}'")
    print(f"V: '{result.get('slots', {}).get('V')}'")
    print(f"Aux: '{result.get('slots', {}).get('Aux')}'")
    print(f"M2: '{result.get('slots', {}).get('M2')}'")
    
    sub_slots = result.get('sub_slots', {})
    print(f"\nsub-s: '{sub_slots.get('sub-s')}'")
    print(f"sub-v: '{sub_slots.get('sub-v')}'")
    print(f"sub-m2: '{sub_slots.get('sub-m2')}'")
    print(f"sub-m1: '{sub_slots.get('sub-m1')}'")副詞処理詳細デバッグ"""

import logging
import sys
import os

# パスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# ログレベルを DEBUG に設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_case_42():
    """Case 42の副詞処理をデバッグ"""
    mapper = UnifiedStanzaRephraseMapper(spacy_model='en_core_web_sm')
    
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    result = mapper.process_sentence(sentence)
    
    print(f"\n=== 結果 ===")
    print(f"S: '{result.get('slots', {}).get('S')}'")
    print(f"V: '{result.get('slots', {}).get('V')}'")
    print(f"Aux: '{result.get('slots', {}).get('Aux')}'")
    print(f"M2: '{result.get('slots', {}).get('M2')}'")
    
    sub_slots = result.get('sub_slots', {})
    print(f"\nsub-s: '{sub_slots.get('sub-s')}'")
    print(f"sub-v: '{sub_slots.get('sub-v')}'")
    print(f"sub-m2: '{sub_slots.get('sub-m2')}'")

if __name__ == "__main__":
    debug_case_42()
