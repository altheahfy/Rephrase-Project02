from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

mapper = DynamicGrammarMapper()
sentence = 'The student who studies diligently always succeeds academically.'

print('=== 詳細分析 ===')
result = mapper.analyze_sentence(sentence)
print('sub_slots:', result.get('sub_slots', {}))
print()
print('=== サブスロットのキー分析 ===')
for key, value in result.get('sub_slots', {}).items():
    print(f"キー: '{key}' → 上位スロット: '{key[4:].upper()}' 値: '{value}'")
print()
print('=== 最終的なmain_slots ===')
print('main_slots:', result.get('main_slots', {}))
