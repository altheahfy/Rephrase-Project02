#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_handler_execution():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    print(f"分析文: {sentence}")
    print()
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # ハンドラー実行順序をトレース
    original_merge = mapper._merge_handler_results
    
    def trace_merge(base_result, handler_result, handler_name):
        print(f"\n=== {handler_name} ハンドラー結果 ===")
        print(f"ベース: {base_result}")
        print(f"ハンドラー: {handler_result}")
        
        merged = original_merge(base_result, handler_result, handler_name)
        print(f"マージ後: {merged}")
        return merged
    
    mapper._merge_handler_results = trace_merge
    
    print("=== ハンドラー実行トレース ===")
    result = mapper.process(sentence)
    
    print(f"\n=== 最終結果 ===")
    print(f"主節: {result.get('slots', {})}")
    print(f"従属節: {result.get('sub_slots', {})}")

if __name__ == "__main__":
    debug_handler_execution()
