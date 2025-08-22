#!/usr/bin/env python3
"""
smoothly副詞の詳細解析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def analyze_smoothly_detailed():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    mapper = UnifiedStanzaRephraseMapper()
    
    print(f"SENTENCE: {sentence}")
    print("=" * 70)
    
    # 副詞ハンドラー単独実行
    mapper.add_handler('adverbial_modifier')
    
    # ログレベルをDEBUGに設定
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    result = mapper.process(sentence)
    
    print("\nRESULT:")
    slots = result.get('slots', {})
    sub_slots = result.get('sub_slots', {})
    
    print("SLOTS:", slots)
    print("SUB_SLOTS:", sub_slots)

if __name__ == "__main__":
    analyze_smoothly_detailed()
