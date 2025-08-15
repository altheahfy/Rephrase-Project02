#!/usr/bin/env python3
"""Test23 詳細デバッグ - C1スロット問題"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_23_debug():
    print("Test23 C1スロット詳細デバッグ")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The person standing there is my friend."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("\n=== COMPLETE RESULT ===")
    print("Main slots:")
    for k, v in result['slots'].items():
        print(f"  {k}: '{v}' ({'NOT EMPTY' if v else 'EMPTY'})")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\n=== EXPECTED FOR TEST23 ===")
    print("S: '' (empty due to sub-o1)")
    print("V: 'is' (preserved)")  
    print("C1: 'my friend' (NOT empty - no sub-c1)")
    print("M2: '' (empty due to sub-m2)")
    print("sub-o1: 'The person [omitted]'")
    print("sub-v: 'standing'") 
    print("sub-m2: 'there'")

if __name__ == "__main__":
    test_23_debug()
