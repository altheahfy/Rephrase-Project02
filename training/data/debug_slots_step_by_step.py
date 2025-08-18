#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()

    # Case 43の結果を段階的に確認
    sentence = 'Products are made very carefully by skilled workers.'
    print(f'=== Test: {sentence} ===')
    result = mapper.process(sentence)
    
    print('Raw result keys:', list(result.keys()))
    
    # 各要素を個別に確認
    for key in result.keys():
        print(f'\n--- {key} ---')
        try:
            if key == 'meta':
                # metaは安全に表示
                print(f"Type: {type(result[key])}")
                if isinstance(result[key], dict):
                    for meta_key, meta_value in result[key].items():
                        print(f"  {meta_key}: {meta_value}")
            elif key in ['slots', 'sub_slots']:
                # slotsを詳細確認
                slots = result[key]
                print(f"Type: {type(slots)}")
                if isinstance(slots, dict):
                    for slot_key, slot_value in slots.items():
                        print(f"  {slot_key}: '{slot_value}'")
                else:
                    print(f"Content: {slots}")
            else:
                print(f"Type: {type(result[key])}")
                if hasattr(result[key], '__len__'):
                    print(f"Length: {len(result[key])}")
        except Exception as e:
            print(f"Error processing {key}: {e}")

if __name__ == "__main__":
    main()
