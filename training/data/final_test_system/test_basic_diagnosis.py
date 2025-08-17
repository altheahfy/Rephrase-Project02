#!/usr/bin/env python3
"""
Test1 - 基本文法要素空問題の診断
極シンプルなケースでシステムがなぜ基本要素を空にするかを確認
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_basic_simple():
    """最もシンプルなテストケース"""
    print("🔧 基本要素空問題診断テスト開始...")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    
    # 最もシンプルなケース
    sentence = "The car is red."
    result = mapper.process(sentence)
    
    print(f"\n📖 テスト文: '{sentence}'")
    print(f"期待値: S='The car', V='is', C1='red'")
    print(f"システム結果:")
    print(f"  slots: {result.get('slots', {})}")
    print(f"  sub_slots: {result.get('sub_slots', {})}")
    print(f"  grammar_info: {result.get('grammar_info', {})}")
    
    slots = result.get('slots', {})
    problems = []
    
    if not slots.get('S'):
        problems.append("S (主語) が空")
    if not slots.get('V'):
        problems.append("V (動詞) が空")
    if not slots.get('C1'):
        problems.append("C1 (補語) が空")
    
    if problems:
        print(f"\n❌ 問題発見:")
        for p in problems:
            print(f"  - {p}")
    else:
        print(f"\n✅ 基本要素正常")

if __name__ == "__main__":
    test_basic_simple()
