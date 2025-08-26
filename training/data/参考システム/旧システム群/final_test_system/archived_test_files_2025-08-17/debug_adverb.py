#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_single_sentence():
    """単一例文でのデバッグテスト"""
    
    # ログレベルをDEBUGに設定
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # テスト例文
    sentence = "The students study hard for exams."
    print(f"Test: {sentence}")
    
    result = mapper.process(sentence)
    print(f"Result: {result}")

if __name__ == "__main__":
    test_single_sentence()
