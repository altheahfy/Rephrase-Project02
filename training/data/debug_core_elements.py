from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
logging.basicConfig(level=logging.DEBUG)

mapper = DynamicGrammarMapper()
sentence = 'The student who studies diligently always succeeds academically.'

print('=== トークン情報 ===')
doc = mapper.nlp(sentence)
tokens = mapper._extract_tokens(doc)
for i, token in enumerate(tokens):
    print(f"{i}: '{token['text']}' (pos={token['pos']}, corrected={token.get('corrected_pos', 'None')})")

print('\n=== 関係節情報 ===')
relative_clause_info = mapper._detect_relative_clause(tokens, sentence)
print('relative_clause_info:', relative_clause_info)

print('\n=== 除外インデックス ===')
excluded_indices = mapper._identify_relative_clause_elements(tokens, relative_clause_info)
print('excluded_indices:', excluded_indices)

print('\n=== フィルター後トークン ===')
filtered_tokens = [token for i, token in enumerate(tokens) if i not in excluded_indices]
for i, token in enumerate(filtered_tokens):
    print(f"{i}: '{token['text']}' (pos={token['pos']}, original_idx={tokens.index(token)})")

print('\n=== コア要素検出 ===')
core_elements = mapper._identify_core_elements(filtered_tokens)
print('core_elements:', core_elements)
