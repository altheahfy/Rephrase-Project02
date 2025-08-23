from dynamic_grammar_mapper import DynamicGrammarMapper
import json

# Test 3と12を比較
test_cases = [
    ('Test 3', 'The man who runs fast is strong.'),
    ('Test 12', 'The man whose car is red lives here.')
]

mapper = DynamicGrammarMapper()

for test_name, sentence in test_cases:
    print(f'{test_name}: {sentence}')
    result = mapper.analyze_sentence(sentence)
    print(f'  メインスロット: {json.dumps(result.get("main_slots", {}), ensure_ascii=False)}')
    print(f'  サブスロット: {json.dumps(result.get("sub_slots", {}), ensure_ascii=False)}')
    print()
