import logging
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_case_42():
    mapper = UnifiedStanzaRephraseMapper()
    
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    result = mapper.process(sentence)
    
    print(f"\n=== 結果 ===")
    slots = result.get('slots', {})
    print(f"S: '{slots.get('S')}'")
    print(f"V: '{slots.get('V')}'")
    print(f"Aux: '{slots.get('Aux')}'")
    print(f"M2: '{slots.get('M2')}'")
    
    sub_slots = result.get('sub_slots', {})
    print(f"\nsub-s: '{sub_slots.get('sub-s')}'")
    print(f"sub-v: '{sub_slots.get('sub-v')}'")
    print(f"sub-m2: '{sub_slots.get('sub-m2')}'")
    print(f"sub-m1: '{sub_slots.get('sub-m1')}'")

if __name__ == "__main__":
    debug_case_42()
