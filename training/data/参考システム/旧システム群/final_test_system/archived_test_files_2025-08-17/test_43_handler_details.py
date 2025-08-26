#!/usr/bin/env python3
"""
テスト43ハンドラー詳細デバッグ：どのハンドラーが何を処理しているか
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_43_handler_details():
    """テスト43のハンドラー別処理詳細"""
    
    print("=== テスト43 ハンドラー詳細デバッグ ===")
    
    # 全体テストと同じ初期化（ログレベルをDEBUGに変更）
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    # テスト文
    test_sentence = "The building is being constructed very carefully by skilled workers."
    print(f"Test: {test_sentence}")
    print("\n" + "="*60)
    
    # 解析実行（詳細ログ付き）
    result = mapper.process(test_sentence)
    
    print("="*60)
    print("\n📊 最終結果:")
    print(f"All slots: {result['slots']}")
    
    actual_m_slots = {k: v for k, v in result['slots'].items() if k.startswith('M')}
    print(f"M-slots only: {actual_m_slots}")
    
    # ハンドラー貢献度の確認
    if 'grammar_info' in result and 'handler_contributions' in result['grammar_info']:
        print("\n🔧 ハンドラー貢献度:")
        for handler, contribution in result['grammar_info']['handler_contributions'].items():
            if 'slots' in contribution:
                handler_m_slots = {k: v for k, v in contribution['slots'].items() if k.startswith('M')}
                if handler_m_slots:
                    print(f"  {handler}: {handler_m_slots}")

if __name__ == "__main__":
    test_43_handler_details()
