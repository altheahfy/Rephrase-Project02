#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    # 簡潔テスト
    mapper = UnifiedStanzaRephraseMapper()

    # Case 43と44のみテスト
    test_cases = {
        '43': 'Products are made very carefully by skilled workers.',
        '44': 'The teacher explains grammar clearly to confused students daily.'
    }

    for case_id, sentence in test_cases.items():
        print(f'Case {case_id}: {sentence}')
        result = mapper.process(sentence)
        main_slots = result.get('main_slots', {})
        print(f'  M1={main_slots.get("M1", "None")}')
        print(f'  M2={main_slots.get("M2", "None")}')
        print(f'  M3={main_slots.get("M3", "None")}')
        print()

if __name__ == "__main__":
    main()
