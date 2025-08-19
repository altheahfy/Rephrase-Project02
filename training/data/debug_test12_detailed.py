#!/usr/bin/env python3
"""
Test 12のRephrase複文ルール適用の詳細デバッグ
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_test12_detailed():
    print("🔍 Test 12 詳細分析 - Rephrase複文ルール追跡")
    print("文: The man whose car is red lives here.")
    print()
    
    # 期待値確認
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test_12 = test_data['data']['12']
    expected = test_12['expected']['main_slots']
    print(f"期待値: {expected}")
    print()
    
    # 結果生成と分析
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process("The man whose car is red lives here.")
    
    slots = result['slots']
    sub_slots = result['sub_slots']
    
    print(f"現在の結果:")
    print(f"  slots: {slots}")
    print(f"  sub_slots: {sub_slots}")
    print()
    
    print("🔍 問題分析:")
    print(f"1. V: 期待値='{expected.get('V', '')}', 実際='{slots.get('V', '')}', sub-v='{sub_slots.get('sub-v', '')}'")
    print(f"2. M2: 期待値='{expected.get('M2', '')}', 実際='{slots.get('M2', '')}', sub-m2='{sub_slots.get('sub-m2', '')}'")
    print()
    
    # main_to_sub_mappingの該当ケースを確認
    main_to_sub_mapping = {
        'V': 'sub-v',
        'Aux': 'sub-aux',
        'C1': 'sub-c1',
        'O1': 'sub-o1',
        'O2': 'sub-o2', 
        'C2': 'sub-c2', 
        'M1': 'sub-m1',
        'M2': 'sub-m2',
        'M3': 'sub-m3'
    }
    
    print("🔍 main_to_sub_mapping 分析:")
    for main_slot, sub_slot in main_to_sub_mapping.items():
        if sub_slot in sub_slots and sub_slots[sub_slot]:
            main_value = slots.get(main_slot, '')
            sub_value = sub_slots[sub_slot]
            print(f"  {main_slot} → {sub_slot}: main='{main_value}', sub='{sub_value}'")
            
            # 期待される処理
            if main_slot in expected and expected[main_slot]:
                print(f"    ❌ 期待: {main_slot}='{expected[main_slot]}' だが実際は '{main_value}'")
            else:
                print(f"    ✅ {main_slot}は期待通り空文字")

if __name__ == "__main__":
    debug_test12_detailed()
