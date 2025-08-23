from dynamic_grammar_mapper import DynamicGrammarMapper

sentence = 'The man whose car is red lives here.'
mapper = DynamicGrammarMapper()

doc = mapper.nlp(sentence)
tokens = mapper._extract_tokens(doc)
relative_clause_info = mapper._detect_relative_clause(tokens, sentence)

antecedent_idx = relative_clause_info.get('antecedent_idx')
print(f'先行詞インデックス: {antecedent_idx}')
print(f'先行詞トークン: {tokens[antecedent_idx]["text"]}')
print(f'前のトークン: {tokens[antecedent_idx-1]["text"]}')
print()
print('全体の先行詞句を取得する必要がある')

# 先行詞句全体を取得
antecedent_phrase = ""
for i in range(max(0, antecedent_idx-2), antecedent_idx+1):
    token = tokens[i]
    if token['pos'] in ['DET', 'ADJ', 'NOUN', 'PROPN']:
        antecedent_phrase += token['text'] + " "

print(f'先行詞句: "{antecedent_phrase.strip()}"')
