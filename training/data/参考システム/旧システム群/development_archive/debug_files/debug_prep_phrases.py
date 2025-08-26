#!/usr/bin/env python3
"""前置詞句抽出問題をデバッグ"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_prepositional_phrases():
    """前置詞句の抽出問題をデバッグ"""
    mapper = UnifiedStanzaRephraseMapper()
    
    test_cases = [
        "The cake is being baked by my mother.",  # Case 24
        "The window was gently opened by the morning breeze.",  # Case 37
        "The problem was quickly solved by the expert team."  # Case 39
    ]
    
    for i, sentence in enumerate(test_cases, 24):
        print(f"\n🧪 Case {i}: {sentence}")
        
        # Stanza解析結果を確認
        doc = mapper.nlp(sentence)
        
        print("=== Stanza解析結果 ===")
        for word in doc.sentences[0].words:
            print(f"{word.id}: {word.text} (POS={word.upos}, deprel={word.deprel}, head={word.head})")
        
        # 処理結果を確認
        result = mapper.process(sentence)
        slots = result.get('slots', {})
        
        print(f"\n結果: M1='{slots.get('M1')}', M2='{slots.get('M2')}', M3='{slots.get('M3')}'")

if __name__ == "__main__":
    debug_prepositional_phrases()
