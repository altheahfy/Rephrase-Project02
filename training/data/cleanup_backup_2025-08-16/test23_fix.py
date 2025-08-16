#!/usr/bin/env python3
"""Test23 修正確認"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_23():
    print("Test23 universal emptying rule test")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The person standing there is my friend."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("Current result:")
    print("Main slots:")
    for k, v in result['slots'].items():
        if v:
            print(f"  {k}: '{v}'")
        else:
            print(f"  {k}: (empty)")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\nBEFORE fix:")
    print("  S: 'The person' (WRONG - should be empty)")
    print("\nAFTER fix (Expected):")
    print("  S: (empty) - Universal rule applied")
    print("  V: 'is'")
    print("  C1: 'my friend'")
    
    # 検証
    s_slot = result['slots'].get('S', 'missing')
    if s_slot == "":
        print("✅ SUCCESS: S slot correctly emptied!")
    else:
        print(f"❌ FAILED: S slot should be empty, got '{s_slot}'")

if __name__ == "__main__":
    test_23()
