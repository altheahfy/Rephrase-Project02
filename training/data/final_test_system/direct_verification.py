#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接検証用スクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import codecs

def direct_verification():
    """直接検証実行"""
    print("🔍 直接検証開始")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')  # INFOに変更
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause') 
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    print("✅ システム準備完了")
    
    # テスト例文
    test_cases = [
        "The car is red.",
        "I love you.", 
        "The man who runs fast is strong.",
        "The letter was written by John.",
        "The student writes essays carefully for better grades."
    ]
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n🧪 テスト {i}: {sentence}")
        print("-" * 50)
        
        result = mapper.process(sentence)
        if result and 'slots' in result:
            print("システム出力:")
            for slot, value in result['slots'].items():
                print(f"  {slot}: '{value}'")
        else:
            print("❌ システム処理失敗")

if __name__ == "__main__":
    direct_verification()
