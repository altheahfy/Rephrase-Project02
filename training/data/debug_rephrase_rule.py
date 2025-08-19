#!/usr/bin/env python3
"""
Rephrase複文ルール処理の詳細デバッグ
特に副詞特別処理の動作を追跡
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_rephrase_rule():
    print("🔍 Rephrase複文ルール処理 詳細デバッグ")
    print("文: The man whose car is red lives here.")
    print()
    
    # unified_stanza_rephrase_mapper.pyに一時的なデバッグログを追加する必要がある
    # しかし、直接修正は危険なので、処理の流れを分析する
    
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process("The man whose car is red lives here.")
    
    slots = result['slots']
    sub_slots = result['sub_slots']
    
    print("🔍 最終結果分析:")
    print(f"  slots: {slots}")
    print(f"  sub_slots: {sub_slots}")
    print()
    
    # main_to_sub_mappingのシミュレーション
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
    
    print("🔍 Rephrase複文ルール分析:")
    for main_slot, sub_slot in main_to_sub_mapping.items():
        if sub_slot in sub_slots and sub_slots[sub_slot]:
            main_value = slots.get(main_slot, '')
            sub_value = sub_slots[sub_slot]
            
            print(f"  {main_slot} → {sub_slot}:")
            print(f"    sub_slot存在: '{sub_value}'")
            print(f"    main_slot現在値: '{main_value}'")
            
            # 副詞特別処理の条件チェック
            if main_slot.startswith('M'):
                print(f"    副詞スロット検出: {main_slot}")
                if main_value:  # original_valueに相当
                    print(f"    副詞特別処理適用されるべき: main_value='{main_value}' があるため")
                    print(f"    ❌ しかし実際は空文字 → 副詞特別処理が失敗している")
                else:
                    print(f"    副詞特別処理適用されない: main_value='{main_value}' が空のため")
                    print(f"    ✅ 期待通り空文字化")
            else:
                if main_value == '':
                    print(f"    ✅ 正常な空文字化")
                else:
                    print(f"    ❌ 予期しない値残存: '{main_value}'")
    
    print()
    print("🔍 処理順序の推測:")
    print("1. 副詞ハンドラー: M2='here', sub-m2='here' を設定")
    print("2. 関係節ハンドラー: sub-s, sub-v, sub-c1 を設定")  
    print("3. Rephrase複文ルール: sub-m2が存在するため M2='' に空文字化")
    print("   → 副詞特別処理が何らかの理由で動作していない")

if __name__ == "__main__":
    debug_rephrase_rule()
