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
    
    # 期待値を確認（設計仕様書準拠）
    expected = {
        'S': 'The teacher',  # 実装では上位S設定
        'Aux': 'is',         # 受動態のAux
        'V': 'respected',    # 受動態のV（過去分詞）
        'M2': 'greatly'      # 副詞修飾語
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
