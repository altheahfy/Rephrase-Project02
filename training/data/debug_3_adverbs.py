#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cases 43,44の副詞処理デバッグ - 3個副詞の問題
"""

import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログ設定
logging.basicConfig(level=logging.DEBUG)

def debug_3_adverb_cases():
    print("Cases 43,44: 3個副詞処理デバッグ")
    print("=" * 50)
    
    # マッパー初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    test_cases = [
        {
            "id": 43,
            "sentence": "The building is being constructed very carefully by skilled workers.",
            "expected": {
                "M1": "by skilled workers",
                "M2": "very", 
                "M3": "carefully"
            }
        },
        {
            "id": 44,
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "expected": {
                "M1": "daily",
                "M2": "clearly",
                "M3": "to confused students"
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n🧪 Case {case['id']}: {case['sentence']}")
        print("-" * 60)
        
        result = mapper.process(case['sentence'])
        
        actual_slots = result.get('slots', {})
        expected = case['expected']
        
        print("実際の結果:")
        for slot in ['M1', 'M2', 'M3']:
            actual_value = actual_slots.get(slot, '')
            expected_value = expected.get(slot, '')
            status = "✅" if actual_value == expected_value else "❌"
            print(f"  {slot}: '{actual_value}' {status} (期待: '{expected_value}')")
        
        # Stanza解析結果も確認
        print("\nStanza解析:")
        doc = mapper._analyze_with_stanza(case['sentence'])
        for word in doc.sentences[0].words:
            if word.upos in ['ADV', 'ADP']:  # 副詞と前置詞
                print(f"  {word.text} ({word.upos}, {word.deprel})")

if __name__ == "__main__":
    debug_3_adverb_cases()
