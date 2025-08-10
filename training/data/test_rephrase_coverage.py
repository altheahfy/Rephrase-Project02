#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephrase 100%取りこぼしなしルール テスト
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_rephrase_complete_coverage():
    """Rephraseの100%取りこぼしなしルールをテスト"""
    
    engine = CompleteRephraseParsingEngine()
    
    # テスト1: that I bought yesterday (関係代名詞目的語)
    print("🔍 テスト1: 関係代名詞目的語 - that I bought yesterday")
    print("=" * 60)
    sentence1 = "The book that I bought yesterday is interesting."
    result1 = engine.analyze_sentence(sentence1)
    
    print(f"文: {sentence1}")
    print("期待値: the book that_sub-o1, I_sub-s, bought_sub-v, yesterday_sub-m3")
    print("\n📋 実際のサブスロット:")
    for sub in result1.get('sub_structures', []):
        if sub['type'] == 'relative':
            for slot, content in sub['sub_slots'].items():
                if content:
                    print(f"  {slot}: {content}")
    
    # テスト2: When I arrived (副詞節)
    print("\n\n🔍 テスト2: 副詞節 - When I arrived")
    print("=" * 60)
    sentence2 = "When I arrived, the meeting started."
    result2 = engine.analyze_sentence(sentence2)
    
    print(f"文: {sentence2}")
    print("期待値: When_sub-m3, I_sub-s, arrived_sub-v")
    print("\n📋 実際のサブスロット:")
    for sub in result2.get('sub_structures', []):
        if sub['type'] == 'adverbial':
            for slot, content in sub['sub_slots'].items():
                if content:
                    print(f"  {slot}: {content}")
    
    # テスト3: who plays soccer (関係代名詞主語)
    print("\n\n🔍 テスト3: 関係代名詞主語 - who plays soccer")
    print("=" * 60)
    sentence3 = "The boy who plays soccer is my friend."
    result3 = engine.analyze_sentence(sentence3)
    
    print(f"文: {sentence3}")
    print("期待値: the boy who_sub-s, plays_sub-v, soccer_sub-o1")
    print("\n📋 実際のサブスロット:")
    for sub in result3.get('sub_structures', []):
        if sub['type'] == 'relative':
            for slot, content in sub['sub_slots'].items():
                if content:
                    print(f"  {slot}: {content}")
    
    # テスト4: 複合パターン
    print("\n\n🔍 テスト4: 複合パターン")
    print("=" * 60)
    sentence4 = "When the student who studies hard arrived, the teacher smiled."
    result4 = engine.analyze_sentence(sentence4)
    
    print(f"文: {sentence4}")
    print("\n📋 全サブ構造:")
    for i, sub in enumerate(result4.get('sub_structures', []), 1):
        print(f"  サブ構造{i} ({sub['type']}, 動詞: {sub['verb']}):")
        for slot, content in sub['sub_slots'].items():
            if content:
                print(f"    {slot}: {content}")

if __name__ == "__main__":
    test_rephrase_complete_coverage()
