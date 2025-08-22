#!/usr/bin/env python3
"""
副詞ハンドラー有無での比較テスト
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_with_without_adverb_handler():
    """副詞ハンドラー有無での影響確認"""
    
    test_sentences = [
        "The car is red.",
        "I love you.", 
        "The book which I bought is expensive.",
        "He has finished his homework.",
        "The letter was written by John."
    ]
    
    print("🔍 副詞ハンドラー有無での比較テスト")
    print("=" * 60)
    
    for sentence in test_sentences:
        print(f"\n📝 テスト文: {sentence}")
        print("-" * 50)
        
        # 副詞ハンドラー無し
        mapper1 = UnifiedStanzaRephraseMapper()
        mapper1.add_handler('basic_five_pattern')
        mapper1.add_handler('relative_clause')
        mapper1.add_handler('passive_voice') 
        mapper1.add_handler('auxiliary_complex')
        
        result1 = mapper1.process(sentence)
        slots1 = {k: v for k, v in result1.get('slots', {}).items() if v}
        sub_slots1 = {k: v for k, v in result1.get('sub_slots', {}).items() if v}
        
        print("副詞ハンドラー無し:")
        print(f"  slots: {slots1}")
        print(f"  sub_slots: {sub_slots1}")
        
        # 副詞ハンドラー有り
        mapper2 = UnifiedStanzaRephraseMapper()
        mapper2.add_handler('basic_five_pattern')
        mapper2.add_handler('relative_clause')
        mapper2.add_handler('passive_voice')
        mapper2.add_handler('adverbial_modifier')  # 追加
        mapper2.add_handler('auxiliary_complex')
        
        result2 = mapper2.process(sentence)
        slots2 = {k: v for k, v in result2.get('slots', {}).items() if v}
        sub_slots2 = {k: v for k, v in result2.get('sub_slots', {}).items() if v}
        
        print("副詞ハンドラー有り:")
        print(f"  slots: {slots2}")
        print(f"  sub_slots: {sub_slots2}")
        
        # 差分チェック
        if slots1 != slots2 or sub_slots1 != sub_slots2:
            print("⚠️  副詞ハンドラーによる変化検出!")

if __name__ == "__main__":
    test_with_without_adverb_handler()
