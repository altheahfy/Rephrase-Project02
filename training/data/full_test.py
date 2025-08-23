from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
logging.basicConfig(level=logging.DEBUG)

mapper = DynamicGrammarMapper()
sentence = 'The student who studies diligently always succeeds academically.'

print('=== 完全な分析結果 ===')
result = mapper.analyze_sentence(sentence)

print('main_slots:', result.get('main_slots', {}))
print('sub_slots:', result.get('sub_slots', {}))
print()

print('=== 期待される結果 ===')
expected = {
    'S': '',                    # 関係節があるため空
    'V': 'succeeds',           # メイン動詞
    'M2': 'always',            # メイン副詞1個目
    'M3': 'academically'       # メイン副詞2個目
}
print('expected main_slots:', expected)
print()

print('=== 比較 ===')
for slot, expected_value in expected.items():
    actual_value = result.get('main_slots', {}).get(slot, '(なし)')
    status = '✅' if actual_value == expected_value else '❌'
    print(f'{status} {slot}: 期待="{expected_value}" 実際="{actual_value}"')
