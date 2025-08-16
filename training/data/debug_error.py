#!/usr/bin/env python3
"""
エラー詳細確認
"""

import sys
import os
import traceback
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_error():
    print("🔍 エラー詳細確認")
    print("=" * 60)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # ハンドラー追加
    mapper.add_handler('relative_clause')
    mapper.add_handler('basic_five_pattern')
    
    sentence = "The car which was stolen is expensive"
    print(f"例文: '{sentence}'")
    print("-" * 50)
    
    try:
        result = mapper.process(sentence)
        print("✅ 成功")
        print(f"結果: {result}")
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("\n📊 詳細トレースバック:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_error()
