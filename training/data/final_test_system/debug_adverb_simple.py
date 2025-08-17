#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_adverb_handler():
    """副詞ハンドラーの動作確認"""
    
    print("=== 副詞ハンドラーデバッグテスト ===")
    
    # システム初期化（DEBUGレベル）
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # ハンドラー有効化
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('adverbial_modifier')
    
    # アクティブハンドラー確認
    print(f"Active handlers: {mapper.list_active_handlers()}")
    
    # テスト例文
    sentence = "The students study hard for exams."
    print(f"Test sentence: {sentence}")
    
    # 処理実行
    result = mapper.process(sentence)
    print(f"Result: {result}")

if __name__ == "__main__":
    test_adverb_handler()
