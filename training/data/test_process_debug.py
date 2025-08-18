#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 49を実際のprocess メソッドで実行
    sentence = "The team working overtime completed the project successfully yesterday."
    print(f"🧪 Process実行テスト: {sentence}")
    
    # デバッグモード有効化
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    result = mapper.process(sentence)
    
    print(f"\n📊 実行結果:")
    print(f"Main slots: {result.get('slots', {})}")
    print(f"Sub slots: {result.get('sub_slots', {})}")
    print(f"Detected patterns: {result.get('grammar_info', {}).get('detected_patterns', [])}")

if __name__ == "__main__":
    main()
