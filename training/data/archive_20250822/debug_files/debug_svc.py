#!/usr/bin/env python3
"""
SVC文型デバッグスクリプト
"The car is red."の詳細分析
"""

from spacy_human_grammar_mapper import SpacyHumanGrammarMapper

def debug_svc_recognition():
    """SVC認識のデバッグ"""
    mapper = SpacyHumanGrammarMapper()
    sentence = "The car is red."
    
    print(f"=== SVC文型デバッグ: '{sentence}' ===")
    
    # 語彙解析
    lexical_info = mapper._extract_lexical_knowledge(sentence)
    tokens = lexical_info['tokens']
    
    print(f"\n📋 トークン化結果 ({len(tokens)}語):")
    for i, token in enumerate(tokens):
        print(f"  [{i}] '{token['text']}' - POS:{token['pos']} TAG:{token['tag']}")
    
    # 各トークンの判定結果
    print(f"\n🔍 各トークンの品詞判定:")
    for i, token in enumerate(tokens):
        text = token['text']
        print(f"  [{i}] '{text}':")
        print(f"      determiner: {mapper._is_determiner_human(token)}")
        print(f"      noun: {mapper._is_noun_human(token)}")
        print(f"      linking_verb: {mapper._is_linking_verb_human(token)}")
        print(f"      complement: {mapper._is_complement_human(token)}")
    
    # SVC認識テスト
    print(f"\n🎯 SVC認識テスト:")
    svc_result = mapper._detect_svc_pattern_human(tokens)
    print(f"  結果: {svc_result}")
    
    # 全体的な文型認識
    print(f"\n📊 全体の文型認識:")
    full_result = mapper.analyze_sentence(sentence)
    print(f"  結果: {full_result}")

if __name__ == '__main__':
    debug_svc_recognition()
