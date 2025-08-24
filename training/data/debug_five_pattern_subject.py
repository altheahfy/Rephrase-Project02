#!/usr/bin/env python3
"""
5文型ハンドラーの主語検出デバッグ
=====================================

問題: "She quickly runs to school." で主語 'She' がO1として誤認識される
原因調査: 5文型ハンドラーの _find_subject と _assign_grammar_roles を詳細検証

期待: S='She', M1='quickly', V='runs', M2='to school'
実際: O1='She', M1='quickly', V='runs', M2='to school'
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_grammar_mapper import DynamicGrammarMapper
import spacy

def debug_five_pattern_subject():
    """5文型ハンドラーの主語検出を段階的にデバッグ"""
    
    print("=== 5文型ハンドラー主語検出デバッグ ===")
    
    # テスト文
    sentence = "She quickly runs to school."
    print(f"対象文: {sentence}")
    
    # DynamicGrammarMapperを初期化
    mapper = DynamicGrammarMapper()
    
    # spaCy解析
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    print("\n--- spaCy解析結果 ---")
    for token in doc:
        print(f"Token: '{token.text}' | POS: {token.pos_} | Tag: {token.tag_} | Dep: {token.dep_} | Head: {token.head.text}")
    
    # トークンリスト変換
    tokens = [
        {
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'head': token.head.text if token.head != token else 'ROOT'
        }
        for token in doc
    ]
    
    print("\n--- トークンリスト ---")
    for i, token in enumerate(tokens):
        print(f"[{i}] {token}")
    
    # Step 1: _identify_core_elements での主語検出
    print("\n--- Step 1: _identify_core_elements ---")
    core_elements = mapper._identify_core_elements(tokens)
    
    print(f"Subject: {core_elements.get('subject')}")
    print(f"Subject indices: {core_elements.get('subject_indices')}")
    print(f"Verb: {core_elements.get('verb')}")
    print(f"Verb indices: {core_elements.get('verb_indices')}")
    
    # Step 2: _find_subject を直接テスト
    print("\n--- Step 2: _find_subject 直接テスト ---")
    verb_idx = core_elements.get('verb_indices', [0])[0] if core_elements.get('verb_indices') else 2  # 'runs'のインデックス
    subject_indices = mapper._find_subject(tokens, verb_idx)
    
    print(f"動詞インデックス: {verb_idx} ('{tokens[verb_idx]['text']}')")
    print(f"検出された主語インデックス: {subject_indices}")
    if subject_indices:
        subject_text = ' '.join([tokens[i]['text'] for i in subject_indices])
        print(f"主語テキスト: '{subject_text}'")
    
    # Step 3: 文型判定
    print("\n--- Step 3: 文型判定 ---")
    pattern = mapper._determine_sentence_pattern(core_elements, tokens)
    print(f"判定された文型: {pattern}")
    
    # Step 4: _assign_grammar_roles での最終配置
    print("\n--- Step 4: _assign_grammar_roles ---")
    elements = mapper._assign_grammar_roles(tokens, pattern, core_elements)
    
    print("最終的な文法要素:")
    for element in elements:
        print(f"  Role: {element.role} | Text: '{element.text}' | Indices: {element.start_idx}-{element.end_idx}")
    
    # Step 5: 最終結果の確認
    print("\n--- Step 5: 最終結果変換 ---")
    result = mapper._convert_to_rephrase_format(elements, pattern)
    main_slots = result.get('main_slots', {})
    
    print("メインスロット:")
    for slot, text in main_slots.items():
        print(f"  {slot}: '{text}'")
    
    # 期待値との比較
    expected = {'S': 'She', 'M1': 'quickly', 'V': 'runs', 'M2': 'to school'}
    print(f"\n--- 期待値との比較 ---")
    print(f"期待: {expected}")
    print(f"実際: {main_slots}")
    
    # 問題箇所の特定
    issues = []
    if main_slots.get('S') != expected.get('S'):
        issues.append(f"主語不一致: 実際='{main_slots.get('S')}', 期待='{expected.get('S')}'")
    if 'O1' in main_slots and main_slots['O1'] == 'She':
        issues.append("主語'She'が目的語O1として誤分類")
    
    if issues:
        print("🔥 検出された問題:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ 正常に動作しています")

if __name__ == "__main__":
    debug_five_pattern_subject()
