#!/usr/bin/env python3
"""Case 32の複文副詞処理詳細デバッグ"""

import sys
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

print('Case 32 詳細デバッグ: 複文での副詞処理')
print('=' * 50)

mapper = UnifiedStanzaRephraseMapper()
sentence = 'The car that was quickly repaired yesterday runs smoothly.'

result = mapper.process(sentence)
print(f'文章: {sentence}')
print(f'実際の結果:')
print(f'  Main slots: {result.get("slots", {})}')
print(f'  Sub slots: {result.get("sub_slots", {})}')

print(f'\n期待値:')
print(f'  Main M2: "smoothly"')
print(f'  Sub sub-m2: "quickly"')  
print(f'  Sub sub-m3: "yesterday"')
