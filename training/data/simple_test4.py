from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# シンプルテスト4
mapper = UnifiedStanzaRephraseMapper()
mapper.add_handler('basic_five_pattern')
mapper.add_handler('relative_clause')

print('Test 4 fix verification:')
result = mapper.process('The book which lies there is mine.')

slots = result.get('slots', {})
sub_slots = result.get('sub_slots', {})

print('Main slots:')
for key, value in slots.items():
    print(f'  {key}: {value}')

print('Sub slots:')  
for key, value in sub_slots.items():
    print(f'  {key}: {value}')

# Success check
expected = {'V': 'is', 'C1': 'mine'}
success = all(slots.get(k) == v for k, v in expected.items())
print(f'Fix Status: {"SUCCESS" if success else "FAILED"}')
