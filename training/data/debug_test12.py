#!/usr/bin/env python3
"""
Test 12の詳細デバッグ
The man whose car is red lives here.

94.3%時: 成功
現在: M2: '' ≠ 'here' で失敗
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_test12():
    print("🔍 Test 12 詳細分析")
    print("文: The man whose car is red lives here.")
    print()
    
    # 期待値確認
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test_12 = test_data['data']['12']
    print(f"期待値: {test_12['expected']['main_slots']}")
    print()
    
    # 現在の結果
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process("The man whose car is red lives here.")
    print(f"現在の結果: {result}")
    print()
    
    # 差分確認
    expected = test_12['expected']['main_slots']
    actual = result
    
    print("🔍 スロット別比較:")
    for slot in ['S', 'V', 'C1', 'O1', 'M1', 'M2', 'M3', 'Aux']:
        exp_val = expected.get(slot, '')
        act_val = actual.get(slot, '')
        if exp_val != act_val:
            print(f"❌ {slot}: '{act_val}' ≠ '{exp_val}'")
        else:
            print(f"✅ {slot}: '{act_val}'")

if __name__ == "__main__":
    debug_test12()
