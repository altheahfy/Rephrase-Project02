#!/usr/bin/env python3
"""when構文単体テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_when_clause():
    mapper = UnifiedStanzaRephraseMapper()
    
    # 問題ケース42番
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    result = mapper.process(sentence)
    print(f"結果: {result}")
    
    # 期待値
    print(f"\n期待値:")
    print(f"  S='', Aux='was', V='unexpected'")
    print(f"  sub-s='everything', sub-v='changed', sub-m1='The time when', sub-m2='dramatically'")
    
    print(f"\n実際:")
    slots = result.get('slots', {})
    sub_slots = result.get('sub_slots', {})
    print(f"  S='{slots.get('S')}', Aux='{slots.get('Aux')}', V='{slots.get('V')}', C1='{slots.get('C1')}'")
    print(f"  sub-s='{sub_slots.get('sub-s')}', sub-v='{sub_slots.get('sub-v')}', sub-m1='{sub_slots.get('sub-m1')}', sub-m2='{sub_slots.get('sub-m2')}'")
    
    print(f"\n❌ 問題:")
    print(f"  1. V='was' → V='unexpected' (動詞と補語が逆転)")
    print(f"  2. C1='unexpected' → 削除 (補語が主動詞になるべき)")  
    print(f"  3. Aux未設定 → Aux='was' (助動詞として認識)")
    print(f"  4. M2='dramatically' → sub-m2='dramatically' (副詞位置)")

if __name__ == "__main__":
    test_when_clause()
