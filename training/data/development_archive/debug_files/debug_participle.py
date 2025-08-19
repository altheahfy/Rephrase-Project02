#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# デバッグ用に詳細ログを有効化
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.DEBUG)

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 49をデバッグテスト
    sentence = 'The team working overtime completed the project successfully yesterday.'
    print(f"🔍 デバッグテスト: {sentence}")
    
    result = mapper.process(sentence)
    
    print("\n結果:")
    print(f"Main slots: {result.get('slots', {})}")
    print(f"Sub slots: {result.get('sub_slots', {})}")

if __name__ == "__main__":
    main()
