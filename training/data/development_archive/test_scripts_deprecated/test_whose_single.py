#!/usr/bin/env python3
"""whose構文単体テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_whose_clause():
    mapper = UnifiedStanzaRephraseMapper()
    
    # 問題ケース35番
    sentence = "The teacher whose class runs efficiently is respected greatly."
    print(f"テスト: {sentence}")
    
    result = mapper.process(sentence)
    print(f"結果: {result}")
    
    # 期待値
    expected = {
        "S": "",
        "Aux": "is", 
        "V": "respected",
        "M2": "greatly"
    }
    
    print(f"期待: S='', V='respected', Aux='is', M2='greatly'")
    print(f"実際: S='{result.get('slots', {}).get('S')}', V='{result.get('slots', {}).get('V')}', Aux='{result.get('slots', {}).get('Aux')}', M2='{result.get('slots', {}).get('M2')}'")

if __name__ == "__main__":
    test_whose_clause()
