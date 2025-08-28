#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ケース35の詳細デバッグ
"""

import sys
import json
from central_controller import CentralController

def debug_case_35():
    print("=== ケース35 詳細デバッグ ===")
    
    # テストケース35の情報
    input_text = "The teacher whose class runs efficiently is respected greatly."
    print(f"入力: {input_text}")
    
    # CentralControllerで処理
    controller = CentralController()
    result = controller.process_sentence(input_text)
    
    print(f"\n📊 実際の出力:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 期待値を確認（REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md準拠）
    expected = {
        'original_text': "The teacher whose class runs efficiently is respected greatly.",
        'success': True,
        'main_slots': {
            'S': '',              # 🎯 Rephrase準拠: サブスロットがあるため空
            'Aux': 'is',          # 🎯 受動態のAux
            'V': 'respected',     # 🎯 受動態のV（過去分詞）
            'M2': 'greatly'       # 🎯 主節の副詞修飾語
        },
        'slots': {
            'S': '',
            'Aux': 'is',
            'V': 'respected',
            'M2': 'greatly'
        },
        'sub_slots': {
            'sub-s': 'The teacher whose class',  # 🎯 先行詞+関係代名詞+関係節主語
            'sub-v': 'runs',                     # 🎯 関係節動詞
            'sub-m2': 'efficiently',             # 🎯 関係節内修飾語
            '_parent_slot': 'S'
        },
        'grammar_pattern': 'relative_clause + basic_five_pattern + passive_voice',
        'phase': 3
    }
    print(f"\n📋 期待値:")
    print(json.dumps(expected, ensure_ascii=False, indent=2))
    
    # 比較
    print(f"\n🔍 比較:")
    for key, expected_value in expected.items():
        actual_value = result.get(key, "未設定")
        status = "✅" if actual_value == expected_value else "❌"
        print(f"  {status} {key}: 期待='{expected_value}' 実際='{actual_value}'")

if __name__ == "__main__":
    debug_case_35()
