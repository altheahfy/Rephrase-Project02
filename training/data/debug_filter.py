from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

logging.basicConfig(level=logging.DEBUG)

sentence = 'The man whose car is red lives here.'
mapper = DynamicGrammarMapper()

doc = mapper.nlp(sentence)
tokens = mapper._extract_tokens(doc)
relative_clause_info = mapper._detect_relative_clause(tokens, sentence)
excluded_indices = mapper._identify_relative_clause_elements(tokens, relative_clause_info)
filtered_tokens = [token for i, token in enumerate(tokens) if i not in excluded_indices]

print('元のトークン:')
for i, token in enumerate(tokens):
    excluded = "❌" if i in excluded_indices else "✅"
    print(f'{i}: {token["text"]} (品詞: {token["pos"]}) {excluded}')

print('\nフィルタ後のトークン:')
for i, token in enumerate(filtered_tokens):
    print(f'{i}: {token["text"]} (品詞: {token["pos"]})')

core_elements = mapper._identify_core_elements(filtered_tokens)
print('\n動詞要素:', core_elements.get('verb'))
print('動詞インデックス:', core_elements.get('verb_indices'))
print('主語要素:', core_elements.get('subject'))
print('主語インデックス:', core_elements.get('subject_indices'))
