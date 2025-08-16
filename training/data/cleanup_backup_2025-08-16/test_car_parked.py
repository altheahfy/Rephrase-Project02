#!/usr/bin/env python3
"""The car parked outside is mine テスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_car_parked():
    print("The car parked outside is mine テスト")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('adverbial_modifier')
    
    sentence = "The car parked outside is mine."
    print(f"Sentence: {sentence}")
    
    result = mapper.process(sentence)
    
    print("\n=== CURRENT RESULT ===")
    print("Main slots:")
    for k, v in result['slots'].items():
        if v:
            print(f"  {k}: '{v}'")
    
    print("Sub slots:")
    for k, v in result['sub_slots'].items():
        if v:
            print(f"  {k}: '{v}'")
    
    print("\n=== EXPECTED RESULT ===")
    print("S: '' (empty due to sub-slots)")
    print("V: 'is'")  
    print("C1: 'mine'")
    print("sub-v: 'the car parked'")
    print("sub-m2: 'outside'")

if __name__ == "__main__":
    test_car_parked()
