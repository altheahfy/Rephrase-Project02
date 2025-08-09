#!/usr/bin/env python3
"""
Complete Rephrase Parsing Engine - デバッグ専用テスト
1つの例文のみで詳細なデバッグ情報を取得
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_debug_single():
    engine = CompleteRephraseParsingEngine()
    
    print("🧪 デバッグテスト: 単一例文の詳細解析\n")
    
    # テスト: 基本SVO文
    sentence = "I love you."
    print(f"=== 例文: {sentence} ===")
    
    result = engine.analyze_sentence(sentence)
    
    print(f"📊 解析結果:")
    for slot_type, values in result['main_slots'].items():
        if values:
            for value_info in values:
                print(f"  {slot_type}: '{value_info['value']}' ({value_info.get('rule_id', 'unknown')})")
    
    print(f"  文型: {result.get('sentence_type', 'unknown')}")
    print(f"  適用ルール数: {result.get('metadata', {}).get('rules_applied', 0)}")

if __name__ == "__main__":
    test_debug_single()
