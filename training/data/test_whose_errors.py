from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

mapper = UnifiedStanzaRephraseMapper()

# Case 13をテスト
test_sentence = 'The student whose book I borrowed is smart.'
print('=== Case 13分析 ===')
print('文:', test_sentence)
result = mapper.process(test_sentence)
print('実際メイン:', result['slots'])
print('実際サブ:', result['sub_slots'])
print('期待メイン: {"S": "", "V": "is", "C1": "smart"}')
print()

# Case 14をテスト  
test_sentence = 'The woman whose dog barks is my neighbor.'
print('=== Case 14分析 ===')
print('文:', test_sentence)
result = mapper.process(test_sentence)
print('実際メイン:', result['slots'])
print('実際サブ:', result['sub_slots'])
print('期待メイン: {"S": "", "V": "is", "C1": "my neighbor"}')
