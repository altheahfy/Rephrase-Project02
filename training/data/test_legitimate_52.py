#!/usr/bin/env python3
"""
正当なTest 52テストスクリプト
unified_stanza_rephrase_mapper.pyを直接使用して正確な結果を検証
"""

import sys
import os
import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_legitimate_52():
    """Test 52の正当なテスト実行"""
    
    print("=" * 60)
    print("Test 52 正当なテスト開始")
    print("=" * 60)
    
    # 初期化
    print("🔄 初期化中...")
    mapper = UnifiedStanzaRephraseMapper()
    
    # Test 52文章
    sentence = "The documents being reviewed thoroughly will be approved soon."
    
    print(f"📝 対象文: {sentence}")
    print()
    
    # 処理実行
    print("🔥 処理開始...")
    result = mapper.process(sentence)
    
    print()
    print("=" * 60)
    print("📊 正当なテスト結果")
    print("=" * 60)
    
    print(f"文: {sentence}")
    print()
    print("スロット結果:")
    for slot, value in result['slots'].items():
        print(f"  {slot}: '{value}'")
    
    print()
    print("サブスロット結果:")
    for sub_slot, value in result['sub_slots'].items():
        print(f"  {sub_slot}: '{value}'")
    
    print()
    print("期待値との比較:")
    expected_sub_aux = "The documents being"
    actual_sub_aux = result['sub_slots'].get('sub-aux', '')
    
    print(f"  期待sub-aux: '{expected_sub_aux}'")
    print(f"  実際sub-aux: '{actual_sub_aux}'")
    
    if actual_sub_aux == expected_sub_aux:
        print("  ✅ Test 52 PASS")
        return True
    else:
        print("  ❌ Test 52 FAIL")
        return False

if __name__ == "__main__":
    success = test_legitimate_52()
    sys.exit(0 if success else 1)
