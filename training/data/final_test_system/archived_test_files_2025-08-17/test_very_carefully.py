#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_very_carefully():
    """very carefully問題の具体的テスト"""
    
    print("=== Very Carefully問題テスト ===")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    # 問題の例文
    sentence = "The building is being constructed very carefully by skilled workers."
    print(f"Test: {sentence}")
    print()
    
    # 期待値
    expected = {
        "M1": "very carefully",
        "M2": "by skilled workers"
    }
    print(f"Expected: {expected}")
    print()
    
    # 実際の処理
    result = mapper.process(sentence)
    
    # 結果表示
    actual_m_slots = {k: v for k, v in result['slots'].items() if k.startswith('M')}
    print(f"Actual M-slots: {actual_m_slots}")
    print()
    
    # 比較
    if actual_m_slots == expected:
        print("✅ 完全一致")
    else:
        print("❌ 不一致")
        print("問題:")
        for key, exp_value in expected.items():
            actual_value = actual_m_slots.get(key, '(なし)')
            if actual_value != exp_value:
                print(f"  {key}: 期待='{exp_value}' vs 実際='{actual_value}'")

if __name__ == "__main__":
    test_very_carefully()
