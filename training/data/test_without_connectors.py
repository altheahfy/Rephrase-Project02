#!/usr/bin/env python3
"""
"even though"を除いてテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pure_stanza_engine_v2 import PureStanzaEngine

def test_without_even_though():
    """even thoughを除いた文でテスト"""
    engine = PureStanzaEngine()
    
    test_sentences = [
        "he was under intense pressure",  # even though 除去
        "the outcome would reflect their full potential",  # so 除去
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"🎯 テスト文: {sentence}")
        print(f"{'='*80}")
        
        result = engine.decompose(sentence)
        if result:
            print(f"\n✅ 分解成功: {len(result)}個のスロット検出")
            for slot_name, slot_data in result.items():
                if isinstance(slot_data, dict) and 'main' in slot_data:
                    print(f"  📋 {slot_name}: '{slot_data['main']}'")
        else:
            print("\n❌ 分解失敗")

if __name__ == "__main__":
    test_without_even_though()
