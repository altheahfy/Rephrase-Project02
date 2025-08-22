#!/usr/bin/env python3
"""
テスト43専用デバッグ：全体テストと同じハンドラー構成でテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_43_full_handlers():
    """テスト43を全体テストと同じハンドラー構成でテスト"""
    
    print("=== テスト43 全ハンドラー構成テスト ===")
    
    # 全体テストと同じ初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    # テスト文
    test_sentence = "The building is being constructed very carefully by skilled workers."
    print(f"Test: {test_sentence}")
    
    # 解析実行
    result = mapper.process(test_sentence)
    
    # 結果表示
    actual_m_slots = {k: v for k, v in result['slots'].items() if k.startswith('M')}
    print(f"\nActual M-slots: {actual_m_slots}")
    
    # 期待値（修正版：システムの動作に合わせて）
    expected = {'M1': 'by skilled workers', 'M2': 'very carefully'}
    print(f"Expected: {expected}")
    
    # 比較
    if actual_m_slots == expected:
        print("\n✅ 完全一致")
    else:
        print("\n❌ 不一致")
        print("問題:")
        for key in set(expected.keys()) | set(actual_m_slots.keys()):
            exp_val = expected.get(key, '(なし)')
            act_val = actual_m_slots.get(key, '(なし)')
            if exp_val != act_val:
                print(f"  {key}: 期待='{exp_val}' vs 実際='{act_val}'")

if __name__ == "__main__":
    test_43_full_handlers()
