#!/usr/bin/env python3
"""
Case 125の詳細分析: that主語節
"""

from central_controller import CentralController
import json

def analyze_case_125():
    sentence = "That you are here is wonderful."
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    # JSONファイルから正しい期待値を読み込む
    import json
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    expected = test_data['data']['125']['expected']
    
    print("=== Case 125 詳細分析 ===")
    print(f"入力文: {sentence}")
    print(f"プライマリハンドラー: {result.get('metadata', {}).get('primary_handler')}")
    
    print(f"\n=== 期待値 (JSONから) ===")
    print(f"main_slots: {expected['main_slots']}")
    print(f"sub_slots: {expected['sub_slots']}")
    
    print(f"\n=== 実際の結果 ===")
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"sub_slots: {result.get('sub_slots', {})}")
    
    # main_slots比較
    print("\n=== main_slots比較 ===")
    expected_main = expected['main_slots']
    actual_main = result.get('main_slots', {})
    for key in expected_main:
        expected_val = expected_main[key]
        actual_val = actual_main.get(key, '<不在>')
        status = "✅" if expected_val == actual_val else "❌"
        print(f"{status} {key}: 期待値='{expected_val}' | 実際='{actual_val}'")
    
    # sub_slots比較
    print("\n=== sub_slots比較 ===")
    expected_sub = expected['sub_slots']
    actual_sub = result.get('sub_slots', {})
    for key in expected_sub:
        expected_val = expected_sub[key]
        actual_val = actual_sub.get(key, '<不在>')
        status = "✅" if expected_val == actual_val else "❌"
        print(f"{status} {key}: 期待値='{expected_val}' | 実際='{actual_val}'")
    
    # 詳細なspaCy解析も表示
    print(f"\n=== 完全な結果構造 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    analyze_case_125()
