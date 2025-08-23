from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
logging.basicConfig(level=logging.DEBUG)

mapper = DynamicGrammarMapper()
sentence = 'The man who runs fast is strong.'

print('=== Test 3 デバッグ ===')
result = mapper.analyze_sentence(sentence)
print('main_slots:', result.get('main_slots', {}))
print('sub_slots:', result.get('sub_slots', {}))
print()
print('=== Sスロット確認 ===')
if 'S' in result.get('main_slots', {}):
    print('S スロット存在:', result['main_slots']['S'])
else:
    print('ERROR: S スロットが存在しません')
