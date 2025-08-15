#!/usr/bin/env python3
"""Test19 詳細デバッグ"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_test19():
    print("Test19 detailed debug start")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The book I read yesterday was boring."
    print(f"Sentence: {sentence}")
    print("="*50)
    
    result = mapper.process(sentence)
    
    print("="*50)
    print("Final result:")
    print("Main slots:")
    for k, v in result['slots'].items():
        if v:
            print(f"  {k:3}: '{v}'")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        print(f"  {k}: '{v}'")
    
    print("\nExpected:")
    print("  S  : '' (empty)")
    print("  V  : 'was'")
    print("  C1 : 'boring'")
    print("  sub-s  : 'I'")
    print("  sub-v  : 'read'")
    print("  sub-o1 : 'The book [omitted]'")
    print("  sub-m2 : 'yesterday'")

if __name__ == "__main__":
    debug_test19()
