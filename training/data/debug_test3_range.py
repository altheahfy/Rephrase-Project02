from dynamic_grammar_mapper import DynamicGrammarMapper

sentence = 'The man who runs fast is strong.'
mapper = DynamicGrammarMapper()

doc = mapper.nlp(sentence)
tokens = mapper._extract_tokens(doc)
relative_clause_info = mapper._detect_relative_clause(tokens, sentence)

print('Test 3の関係節範囲:')
print('関係代名詞位置:', relative_clause_info.get('clause_start_idx'))
print('関係節終了位置:', relative_clause_info.get('clause_end_idx'))
print('先行詞位置:', relative_clause_info.get('antecedent_idx'))
print()

for i, token in enumerate(tokens):
    print(f'{i}: {token["text"]} ({token["pos"]})')

print()
excluded_indices = mapper._identify_relative_clause_elements(tokens, relative_clause_info)
print('除外インデックス:', excluded_indices)

filtered_tokens = [token for i, token in enumerate(tokens) if i not in excluded_indices]
print('フィルタ後:', [t['text'] for t in filtered_tokens])
