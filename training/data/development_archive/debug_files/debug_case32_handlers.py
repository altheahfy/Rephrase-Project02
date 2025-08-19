#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Case 32 ハンドラー実行順序詳細確認
副詞ハンドラーと助動詞ハンドラーの競合をチェック
"""

import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルをDEBUGに変更
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')

def debug_handler_execution():
    print("Case 32 ハンドラー実行順序デバッグ")
    print("=" * 60)
    
    # マッパー初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 32 文章
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    
    print(f"📝 文章: {sentence}")
    print(f"🔧 アクティブハンドラー: {mapper.active_handlers}")
    print()
    
    # 処理実行（DEBUGログで詳細確認）
    result = mapper.process(sentence)
    
    print("\n" + "="*60)
    print("📊 最終結果:")
    print(f"  Main slots: {result.get('slots', {})}")
    print(f"  Sub slots: {result.get('sub_slots', {})}")
    
    # ハンドラー貢献詳細
    print("\n🔍 ハンドラー貢献:")
    contributions = result.get('grammar_info', {}).get('handler_contributions', {})
    for handler, info in contributions.items():
        print(f"  {handler}: {info}")

if __name__ == "__main__":
    debug_handler_execution()
