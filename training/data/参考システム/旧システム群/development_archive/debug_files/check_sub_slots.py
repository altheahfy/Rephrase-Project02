#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()

    # Case 43と44の詳細結果を確認
    test_cases = {
        '43': 'Products are made very carefully by skilled workers.',
        '44': 'The teacher explains grammar clearly to confused students daily.'
    }

    for case_id, sentence in test_cases.items():
        print(f'=== Case {case_id}: {sentence} ===')
        result = mapper.process(sentence)
        
        print('Main slots:')
        for slot, value in result.get('main_slots', {}).items():
            print(f'  {slot}: "{value}"')
        
        print('Sub slots:')
        for slot, value in result.get('sub_slots', {}).items():
            print(f'  {slot}: "{value}"')
        print()

if __name__ == "__main__":
    main()
