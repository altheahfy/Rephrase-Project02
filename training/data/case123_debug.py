#!/usr/bin/env python3
"""
Case 123の詳細分析
"""

from central_controller import CentralController
import json

def analyze_case_123():
    sentence = "She doesn't know whether he will come."
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print("=== Case 123 詳細分析 ===")
    print(f"入力文: {sentence}")
    print(f"プライマリハンドラー: {result.get('metadata', {}).get('primary_handler')}")
    print(f"スロット構造:")
    print(json.dumps(result.get('ordered_slots', {}), ensure_ascii=False, indent=2))
    
    expected = {'1': 'She', '2': "doesn't", '3': 'know', '4': 'whether', '5': 'he', '6': 'will', '7': 'come'}
    print(f"期待値: {expected}")
    
    # 実際の結果と期待値の比較
    actual_subslots = result.get('ordered_slots', {})
    print("\n=== 比較結果 ===")
    for key in expected:
        expected_val = expected[key]
        actual_val = actual_subslots.get(key, '<不在>')
        status = "✅" if expected_val == actual_val else "❌"
        print(f"{status} スロット{key}: 期待値='{expected_val}' | 実際='{actual_val}'")

if __name__ == "__main__":
    analyze_case_123()
