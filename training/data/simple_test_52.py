#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# 簡単なテスト
mapper = UnifiedStanzaRephraseMapper()
sentence = "The documents being reviewed thoroughly will be approved soon."
result = mapper.process(sentence)

print("=" * 50)
print(f"sub-aux: '{result['sub_slots'].get('sub-aux', 'NONE')}'")
print(f"期待値: 'The documents being'")
print(f"一致: {result['sub_slots'].get('sub-aux') == 'The documents being'}")
print("=" * 50)
