from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
logging.basicConfig(level=logging.DEBUG)

mapper = DynamicGrammarMapper()
sentence = 'The student whose book I borrowed is smart.'

print('=== Test 13 問題調査 ===')
print(f'文章: {sentence}')
result = mapper.analyze_sentence(sentence)

print('\n=== 期待値 ===')
print('sub-o1: "The student whose book"')
print('sub-s: "I"') 
print('sub-v: "borrowed"')

print('\n=== 実際値 ===')
sub_slots = result.get('sub_slots', {})
for key, value in sub_slots.items():
    print(f'{key}: "{value}"')
    
print('\n=== 問題分析 ===')
if 'sub-o1' not in sub_slots:
    print('❌ sub-o1が欠落している')
else:
    print('✅ sub-o1が存在している')
