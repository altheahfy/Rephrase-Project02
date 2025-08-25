#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dynamic_grammar_mapper import DynamicGrammarMapper
import spacy

# spaCyモデルのロード
nlp = spacy.load('en_core_web_sm')

# テスト文
sentence = 'The doctor who works carefully saves lives successfully'
print(f'🧪 テスト文: {sentence}')

# DynamicGrammarMapper経由でのテスト
mapper = DynamicGrammarMapper()

# Phase A3モードで実行
result = mapper.analyze_sentence(sentence)

print(f'🔍 Dynamic Grammar Mapper結果:')
print(f'  success: {result.get("success", False)}')
print(f'  analysis_method: {result.get("analysis_method", "")}')
print(f'  pattern_detected: {result.get("pattern_detected", "")}')
print(f'  confidence: {result.get("confidence", 0)}')

print(f'\n🔍 スロット結果:')
print(f'  main_slots: {result.get("main_slots", {})}')
print(f'  slots: {result.get("slots", {})}')

if 'sub_slots' in result:
    print(f'  sub_slots: {result.get("sub_slots", {})}')

# Phase情報
if hasattr(mapper, 'current_phase'):
    print(f'\n🔍 現在のフェーズ: {mapper.current_phase}')

# BasicFivePatternHandlerが直接呼ばれているかチェック
print(f'\n🔍 BasicFivePatternHandlerの詳細結果:')
if hasattr(mapper, 'basic_five_pattern_handler'):
    handler = mapper.basic_five_pattern_handler
    # spaCy解析
    doc = mapper.nlp(sentence)
    tokens = []
    for token in doc:
        tokens.append({
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'head': token.head.text,
            'idx': token.i
        })
    
    # 直接ハンドラーを呼び出し
    direct_result = handler.analyze_basic_pattern(tokens, {})
    print(f'  handler_success: {direct_result.get("handler_success", False)}')
    if direct_result.get("grammar_elements"):
        print(f'  grammar_elements:')
        for elem in direct_result["grammar_elements"]:
            print(f'    role={elem.role}, text="{elem.text}"')
