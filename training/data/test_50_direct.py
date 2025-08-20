#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedMapper

def test_sentence_50():
    sentence = "The woman standing quietly near the door was waiting patiently."
    
    print(f"🧪 Test 50 分析開始: {sentence}")
    
    # システム初期化
    mapper = UnifiedMapper()
    
    # 文を処理
    result = mapper.process_sentence(sentence)
    
    print(f"📊 現在の結果:")
    print(f"  メインスロット: {result.get('main_slots', {})}")
    print(f"  サブスロット: {result.get('sub_slots', {})}")
    
    return result

if __name__ == "__main__":
    test_sentence_50()
