#!/usr/bin/env python3
"""
サブスロットで使われている文を上位スロットでテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pure_stanza_engine_v2 import PureStanzaEngine

def test_subslot_sentences_as_main():
    """サブスロットで使われている文を上位スロットとしてテスト"""
    engine = PureStanzaEngine()
    
    # サブスロット分解で問題になっている文たち
    test_sentences = [
        "even though he was under intense pressure",
        "deliver the final proposal flawlessly", 
        "so the outcome would reflect their full potential",
        "the manager who had recently taken charge of the project"
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
    test_subslot_sentences_as_main()
