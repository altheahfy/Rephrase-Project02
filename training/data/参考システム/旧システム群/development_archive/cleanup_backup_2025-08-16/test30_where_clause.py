#!/usr/bin/env python3
"""Test30 関係副詞where節テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_30():
    print("Test30: The house where I was born is in Tokyo.")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The house where I was born is in Tokyo."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("\n=== CURRENT RESULT ===")
    print("Main slots:")
    for k, v in result['slots'].items():
        print(f"  {k}: '{v}'")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\n=== EXPECTED RESULT ===")
    print("S: '' (empty due to relative clause)")
    print("V: 'is'")  
    print("C2: 'in Tokyo'")
    print("sub-m3: 'The house where'")
    print("sub-s: 'I'")
    print("sub-aux: 'was'")
    print("sub-v: 'born'")

if __name__ == "__main__":
    test_30()
