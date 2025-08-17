#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_adverbs_detailed():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    print(f"分析文: {sentence}")
    print()
    
    # システムの実行（ログ出力を抑制）
    import logging
    
    # デバッグ用にログレベルを調整
    logger = logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper')
    logger.setLevel(logging.DEBUG)
    
    # ハンドラー追加
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    print("=== システム処理結果（詳細ログ付き） ===")
    result = mapper.process(sentence)
    
    print(f"\n=== 最終結果 ===")
    print(f"主節slots: {result.get('slots', {})}")
    print(f"従属節slots: {result.get('sub_slots', {})}")

if __name__ == "__main__":
    debug_adverbs_detailed()
