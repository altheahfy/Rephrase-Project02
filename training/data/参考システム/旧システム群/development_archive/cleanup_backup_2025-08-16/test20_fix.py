#!/usr/bin/env python3
"""Test20 修正確認"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_20():
    print("Test20 last night修正確認")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The movie we watched last night was amazing."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("Current result:")
    print("Main slots:")
    for k, v in result['slots'].items():
        if v:
            print(f"  {k}: '{v}'")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\nExpected:")
    print("  sub-m2: 'last night' (not just 'night')")
    
    actual_sub_m2 = result['sub_slots'].get('sub-m2', 'なし')
    print(f"Result: sub-m2 = '{actual_sub_m2}'")
    
    if actual_sub_m2 == 'last night':
        print("✅ Success: 'last night' correctly preserved")
    else:
        print(f"❌ Failed: Expected 'last night', got '{actual_sub_m2}'")

if __name__ == "__main__":
    test_20()
