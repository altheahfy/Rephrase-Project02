#!/usr/bin/env python3
"""
詳細デバッグ: 関係節ハンドラーの戻り値確認
"""

import sys
import os
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_handler_return():
    print("🔍 関係節ハンドラー戻り値デバッグ")
    print("=" * 60)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # 関係節ハンドラーを手動テスト
    sentence = "The car which was stolen is expensive"
    print(f"例文: '{sentence}'")
    print("-" * 50)
    
    # 文解析を手動実行
    doc = mapper.nlp(sentence)
    base_result = {
        'sentence': sentence,
        'slots': {},
        'sub_slots': {},
        'positional_sub_slots': {},
        'grammar_info': {
            'detected_patterns': [],
            'handler_contributions': {}
        }
    }
    
    # 関係節ハンドラーを直接呼び出し
    handler_result = mapper._handle_relative_clause(doc.sentences[0], base_result)
    
    print("\n📊 ハンドラー戻り値:")
    if handler_result:
        print(f"全体: {handler_result}")
        print(f"スロット: {handler_result.get('slots', {})}")
        print(f"サブスロット: {handler_result.get('sub_slots', {})}")
        print(f"位置別サブスロット: {handler_result.get('positional_sub_slots', {})}")
        print(f"戻り値のkeys: {list(handler_result.keys())}")
        
        # 位置別サブスロット詳細
        pos_sub_slots = handler_result.get('positional_sub_slots', {})
        if pos_sub_slots:
            print("\n🎯 位置別サブスロット詳細:")
            for position, sub_slots in pos_sub_slots.items():
                print(f"  [{position}]:")
                for sub_key, sub_info in sub_slots.items():
                    if isinstance(sub_info, dict):
                        print(f"    {sub_key}: {sub_info}")
                    else:
                        print(f"    {sub_key}: '{sub_info}' (レガシー)")
        else:
            print("\n❌ 位置別サブスロットが空です")
    else:
        print("❌ ハンドラー結果がNone")

if __name__ == "__main__":
    debug_handler_return()
