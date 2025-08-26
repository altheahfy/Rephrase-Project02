#!/usr/bin/env python3
"""ケース42番（when+受動態）単体テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_case_42():
    mapper = UnifiedStanzaRephraseMapper()
    
    # ケース42番
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    result = mapper.process(sentence)
    print(f"結果: {result}")
    
    # 期待値
    expected = {
        "S": "",
        "Aux": "was", 
        "V": "unexpected",
        "sub-s": "everything",
        "sub-v": "changed",
        "sub-m1": "The time when",
        "sub-m2": "dramatically"
    }
    
    print(f"期待: S='', Aux='was', V='unexpected'")
    print(f"実際: S='{result.get('slots', {}).get('S')}', Aux='{result.get('slots', {}).get('Aux')}', V='{result.get('slots', {}).get('V')}'")
    
    # サブスロットも確認
    sub_slots = result.get('sub_slots', {})
    print(f"期待サブ: sub-s='everything', sub-v='changed', sub-m2='dramatically'")
    print(f"実際サブ: sub-s='{sub_slots.get('sub-s')}', sub-v='{sub_slots.get('sub-v')}', sub-m2='{sub_slots.get('sub-m2')}'")

if __name__ == "__main__":
    test_case_42()
