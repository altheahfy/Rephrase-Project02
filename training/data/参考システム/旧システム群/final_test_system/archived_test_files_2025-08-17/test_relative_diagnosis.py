#!/usr/bin/env python3
"""
Test2 - 関係節文での基本要素空問題の診断
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_relative_clause_empty():
    """関係節文で基本要素が空になる問題を確認"""
    print("🔧 関係節文基本要素空問題診断テスト開始...")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # 関係節を含む文
    sentence = "The man who runs fast is strong."
    result = mapper.process(sentence)
    
    print(f"\n📖 テスト文: '{sentence}'")
    print(f"期待値: S=empty(sub-sへ移行), V='is', C1='strong'")
    print(f"システム結果:")
    print(f"  slots: {result.get('slots', {})}")
    print(f"  sub_slots: {result.get('sub_slots', {})}")
    print(f"  grammar_info: {result.get('grammar_info', {})}")
    
    slots = result.get('slots', {})
    problems = []
    
    if slots.get('V') != 'is':
        problems.append(f"V: '{slots.get('V')}' ≠ 'is'")
    if slots.get('C1') != 'strong':
        problems.append(f"C1: '{slots.get('C1')}' ≠ 'strong'")
    
    if problems:
        print(f"\n❌ 主節基本要素問題:")
        for p in problems:
            print(f"  - {p}")
        
        # Rephraseルール適用状況を確認
        grammar_info = result.get('grammar_info', {})
        print(f"\n🔍 Handler contributions:")
        for handler, info in grammar_info.get('handler_contributions', {}).items():
            print(f"  {handler}: {info}")
            
    else:
        print(f"\n✅ 主節基本要素正常")

if __name__ == "__main__":
    test_relative_clause_empty()
