#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""分詞構文ハンドラーのデバッグテスト"""

import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを詳細に設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_participle_handler_only():
    """分詞構文ハンドラーのみを単体テスト"""
    
    # マッパー初期化（分詞構文ハンドラーのみ有効化）
    mapper = UnifiedStanzaRephraseMapper()
    
    # 他のハンドラーを無効化
    mapper.active_handlers = {'participle_construction'}
    
    # Case 49テスト
    sentence = "The team working overtime completed the project successfully yesterday."
    
    print(f"\n=== 分詞構文ハンドラー単体テスト ===")
    print(f"入力: {sentence}")
    
    try:
        result = mapper.process(sentence)
        print(f"\n結果:")
        print(f"  Main slots: {result.get('slots', {})}")
        print(f"  Sub slots: {result.get('sub_slots', {})}")
        print(f"  Patterns: {result.get('grammar_info', {}).get('detected_patterns', [])}")
        print(f"  Control flags: {result.get('grammar_info', {}).get('control_flags', {})}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_participle_handler_only()
