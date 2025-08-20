#!/usr/bin/env python3
"""
Case 53単体テスト: whose構文の補語処理確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_case_53():
    """Case 53のwhose構文補語処理をテスト"""
    
    sentence = "The artist whose paintings were exhibited internationally became famous rapidly."
    
    # 期待値
    expected = {
        "main_slots": {
            "S": "",
            "V": "became",
            "C1": "famous",
            "M2": "rapidly"
        },
        "sub_slots": {
            "sub-s": "The artist whose paintings",
            "sub-aux": "were",
            "sub-v": "exhibited",
            "sub-m2": "internationally"
        }
    }
    
    print(f"🧪 Case 53テスト: {sentence}")
    print("=" * 80)
    
    # テスト実行
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)
    
    # 結果表示
    print("📊 実際の結果:")
    print(f"  Main slots: {json.dumps(result.get('slots', {}), indent=4, ensure_ascii=False)}")
    print(f"  Sub slots: {json.dumps(result.get('sub_slots', {}), indent=4, ensure_ascii=False)}")
    
    print("\n📋 期待値:")
    print(f"  Main slots: {json.dumps(expected['main_slots'], indent=4, ensure_ascii=False)}")
    print(f"  Sub slots: {json.dumps(expected['sub_slots'], indent=4, ensure_ascii=False)}")
    
    # 比較
    actual_main = result.get('slots', {})
    actual_sub = result.get('sub_slots', {})
    
    main_match = actual_main == expected['main_slots']
    sub_match = actual_sub == expected['sub_slots']
    
    print("\n🔍 比較結果:")
    print(f"  Main slots一致: {main_match}")
    print(f"  Sub slots一致: {sub_match}")
    
    if not main_match:
        print("  Main slots差異:")
        for key in set(expected['main_slots'].keys()) | set(actual_main.keys()):
            exp_val = expected['main_slots'].get(key, "欠落")
            act_val = actual_main.get(key, "欠落")
            if exp_val != act_val:
                print(f"    {key}: '{exp_val}' → '{act_val}'")
    
    if not sub_match:
        print("  Sub slots差異:")
        for key in set(expected['sub_slots'].keys()) | set(actual_sub.keys()):
            exp_val = expected['sub_slots'].get(key, "欠落")
            act_val = actual_sub.get(key, "欠落")
            if exp_val != act_val:
                print(f"    {key}: '{exp_val}' → '{act_val}'")
    
    # 精度計算
    total_slots = len(expected['main_slots']) + len(expected['sub_slots'])
    correct_slots = 0
    
    for key, exp_val in expected['main_slots'].items():
        if actual_main.get(key) == exp_val:
            correct_slots += 1
    
    for key, exp_val in expected['sub_slots'].items():
        if actual_sub.get(key) == exp_val:
            correct_slots += 1
    
    accuracy = (correct_slots / total_slots) * 100
    print(f"\n📊 精度: {accuracy:.1f}% ({correct_slots}/{total_slots})")
    
    # 結果判定
    if main_match and sub_match:
        print("✅ Case 53: 修正成功！100%精度達成")
        return True
    else:
        print("🔶 Case 53: まだ課題があります")
        return False

if __name__ == "__main__":
    test_case_53()
