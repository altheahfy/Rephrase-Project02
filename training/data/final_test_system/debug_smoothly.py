#!/usr/bin/env python3
"""
smoothly副詞の検出デバッグ
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_smoothly():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    mapper = UnifiedStanzaRephraseMapper()
    
    print(f"📝 デバッグ文: {sentence}")
    print("=" * 70)
    
    # 一時的にデバッグ用の副詞ハンドラーを追加
    mapper.add_handler('adverbial_modifier')
    
    # 処理実行
    result = mapper.process(sentence)
    
    print("🔍 システム結果:")
    slots = result.get('slots', {})
    sub_slots = result.get('sub_slots', {})
    
    all_slots = {**slots, **sub_slots}
    for k, v in all_slots.items():
        if v:
            print(f"  {k}: {v}")
    
    print("\n📊 期待される副詞:")
    print("  M1: smoothly (主節)")
    print("  sub-m1: quickly (従属節)")
    print("  sub-m2: yesterday (従属節)")

if __name__ == "__main__":
    debug_smoothly()
