#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()

    # Case 43と44の生の結果構造を確認
    test_cases = {
        '43': 'Products are made very carefully by skilled workers.',
        '44': 'The teacher explains grammar clearly to confused students daily.'
    }

    for case_id, sentence in test_cases.items():
        print(f'=== Case {case_id}: {sentence} ===')
        result = mapper.process(sentence)
        
        print('Raw result keys:', list(result.keys()))
        print('Result structure:')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print('\n' + '='*50 + '\n')

if __name__ == "__main__":
    main()
