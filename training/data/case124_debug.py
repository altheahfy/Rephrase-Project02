#!/usr/bin/env python3
"""
Case 124の詳細分析: where節
"""

from central_controller import CentralController
import json

def analyze_case_124():
    sentence = "I wonder where she lives."
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print("=== Case 124 詳細分析 ===")
    print(f"入力文: {sentence}")
    print(f"プライマリハンドラー: {result.get('metadata', {}).get('primary_handler')}")
    print(f"スロット構造:")
    print(json.dumps(result.get('ordered_slots', {}), ensure_ascii=False, indent=2))
    
    expected = {'1': 'I', '2': 'wonder', '3': 'where', '4': 'she', '5': 'lives'}
    print(f"期待値: {expected}")
    
    # 実際の結果と期待値の比較
    actual_subslots = result.get('ordered_slots', {})
    print("\n=== 比較結果 ===")
    for key in expected:
        expected_val = expected[key]
        actual_val = actual_subslots.get(key, '<不在>')
        status = "✅" if expected_val == actual_val else "❌"
        print(f"{status} スロット{key}: 期待値='{expected_val}' | 実際='{actual_val}'")
    
    # 詳細なspaCy解析も表示
    print(f"\n=== 完全な結果構造 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    analyze_case_124()
