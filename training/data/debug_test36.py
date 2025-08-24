#!/usr/bin/env python3
"""
テスト36の品詞判定詳細調査
"""

import spacy
from dynamic_grammar_mapper import DynamicGrammarMapper

# spaCyの基本解析
nlp = spacy.load('en_core_web_sm')
sentence = 'The doctor who works carefully saves lives successfully.'
doc = nlp(sentence)

print('=== spaCy基本解析 ===')
for i, token in enumerate(doc):
    print(f'{i}: {token.text:<12} | POS: {token.pos_:<6} | TAG: {token.tag_:<6} | DEP: {token.dep_:<10} | HEAD: {token.head.text}')

print('\n=== DynamicGrammarMapperのトークン抽出 ===')
mapper = DynamicGrammarMapper()
tokens = mapper._extract_tokens(doc)
for i, token in enumerate(tokens):
    text = token["text"]
    pos = token["pos"]
    tag = token["tag"]
    dep = token["dep"]
    head = token["head"]
    print(f'{i}: {text:<12} | POS: {pos:<6} | TAG: {tag:<6} | DEP: {dep:<10} | HEAD: {head}')

print('\n=== 曖昧語解決結果 ===')
for i, token in enumerate(tokens):
    original_pos = token["pos"]
    resolved_pos = mapper._resolve_ambiguous_word(token, tokens, i, sentence)
    text = token["text"]
    if original_pos != resolved_pos:
        print(f'{i}: {text:<12} | ORIGINAL: {original_pos:<6} | RESOLVED: {resolved_pos:<6} | 変更あり')
    else:
        print(f'{i}: {text:<12} | POS: {original_pos:<6} | (変更なし)')
