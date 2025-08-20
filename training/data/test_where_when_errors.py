from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

mapper = UnifiedStanzaRephraseMapper()

# Case 41をテスト
test_sentence = 'The place where we met accidentally became our favorite spot.'
print('=== Case 41分析 ===')
print('文:', test_sentence)
result = mapper.process(test_sentence)
print('実際メイン:', result['slots'])
print('実際サブ:', result['sub_slots'])
print('期待メイン: {"S": "", "V": "became", "C1": "our favorite spot"}')
print('期待サブ: {"sub-s": "we", "sub-v": "met", "sub-m2": "The place where", "sub-m3": "accidentally"}')
print()

# Case 42をテスト  
test_sentence = 'The time when everything changed dramatically was unexpected.'
print('=== Case 42分析 ===')
print('文:', test_sentence)
result = mapper.process(test_sentence)
print('実際メイン:', result['slots'])
print('実際サブ:', result['sub_slots'])
print('期待メイン: {"S": "", "Aux": "was", "V": "unexpected"}')
print('期待サブ: {"sub-s": "everything", "sub-v": "changed", "sub-m2": "The time when", "sub-m3": "dramatically"}')
