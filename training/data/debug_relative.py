#!/usr/bin/env python3
"""
デバッグ用: 関係節検出確認
"""

import sys
import os
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_relative_clause():
    print("🔍 関係節検出デバッグ")
    print("=" * 60)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # 関係節ハンドラーのみ追加
    mapper.add_handler('relative_clause')
    
    sentence = "The car which was stolen is expensive"
    print(f"例文: '{sentence}'")
    print("-" * 50)
    
    result = mapper.process(sentence)
    print("\n📊 結果:")
    print(f"スロット: {result.get('slots', {})}")
    print(f"サブスロット: {result.get('sub_slots', {})}")
    print(f"位置別サブスロット: {result.get('positional_sub_slots', {})}")

if __name__ == "__main__":
    debug_relative_clause()
