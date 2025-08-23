from dynamic_grammar_mapper import DynamicGrammarMapper

sentence = 'The man whose car is red lives here.'
mapper = DynamicGrammarMapper()

doc = mapper.nlp(sentence)
tokens = mapper._extract_tokens(doc)

print('全トークンと品詞:')
for i, token in enumerate(tokens):
    print(f"{i}: {token['text']} (POS: {token['pos']}, TAG: {token['tag']})")

print()
main_verb_idx = mapper._find_main_verb(tokens)
print('メイン動詞インデックス:', main_verb_idx)
if main_verb_idx is not None:
    print('メイン動詞:', tokens[main_verb_idx]['text'])

print()
print('先行詞インデックス: 1 (man)')
print('動詞インデックス:', main_verb_idx)
if main_verb_idx and 1 < main_verb_idx:
    print('位置関係: 先行詞 < 動詞 → 主語')
