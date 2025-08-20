#!/usr/bin/env python3
"""Test 42のC1重複修正確認用スクリプト"""

import sys
import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_42_verification():
    """Test 42のC1重複が修正されたか確認"""
    
    # Test 42の文章
    test_sentence = "The time when everything changed dramatically was unexpected."
    
    # 期待値
    expected = {
        "V": "unexpected",
        "C1": ""  # 空であるべき（重複防止）
    }
    
    print(f"Test 42 verification: {test_sentence}")
    print("-" * 60)
    
    try:
        # マッパー初期化
        mapper = UnifiedStanzaRephraseMapper()
        
        # 処理実行
        result = mapper.process(test_sentence)
        
        # 結果確認
        actual_v = result.get("slots", {}).get("V", "")
        actual_c1 = result.get("slots", {}).get("C1", "")
        
        print(f"Expected: V='{expected['V']}', C1='{expected['C1']}'")
        print(f"Actual:   V='{actual_v}', C1='{actual_c1}'")
        print()
        
        # 検証
        success = (actual_v == expected["V"] and actual_c1 == expected["C1"])
        
        if success:
            print("✅ TEST 42 PASSED: C1 duplication fixed!")
        else:
            print("❌ TEST 42 FAILED: C1 duplication still exists")
            
        print(f"Full result: {result}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_42_verification()
    sys.exit(0 if success else 1)
