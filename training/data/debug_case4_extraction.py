#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 4 直接デバッグ
"""

import sys
sys.path.append('.')
from relative_clause_handler import RelativeClauseHandler

handler = RelativeClauseHandler()
sentence = 'The book which lies there is mine.'

print(f"元文: {sentence}")

# 直接テスト
result = handler._extract_relative_clause_text(sentence, 'which')
print(f'関係節抽出結果: "{result}"')

# spaCy分析
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(sentence)

print('\nspaCy分析:')
for i, token in enumerate(doc):
    print(f'{i}: {token.text} | POS:{token.pos_} | DEP:{token.dep_}')

print('\n期待: which lies there を抽出')
print('実際: 上記の結果を確認')
