#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def analyze_test19():
    # Test19データを取得
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test19 = test_data['data']['19']
    sentence = test19['sentence']
    expected = test19['expected']
    
    print(f"=== Test19分析 ===")
    print(f"文: {sentence}")
    print(f"期待値: {expected}")
    print()
    
    # システム実行
    mapper = UnifiedStanzaRephraseMapper()
    result = mapper.process(sentence)
    
    print(f"システム結果: {result}")
    print()
    
    # Stanza解析結果を確認
    doc = mapper.nlp(sentence)
    print("=== Stanza解析詳細 ===")
    for sent in doc.sentences:
        print("Token依存関係:")
        for token in sent.words:
            print(f"  {token.text} -> head:{token.head} deprel:{token.deprel} upos:{token.upos}")
    print()
    
    # 問題分析
    main_expected = expected['main_slots']
    sub_expected = expected['sub_slots']
    main_result = result.get('slots', {})
    sub_result = result.get('sub_slots', {})
    
    print("=== 問題分析 ===")
    print("主節比較:")
    print(f"  期待値: {main_expected}")
    print(f"  システム: {main_result}")
    
    print("従属節比較:")
    print(f"  期待値: {sub_expected}")
    print(f"  システム: {sub_result}")
    
    # 具体的な不一致を特定
    print("\n=== 不一致の詳細 ===")
    
    # 主節の不一致
    print("主節の不一致:")
    for key in set(list(main_expected.keys()) + list(main_result.keys())):
        exp_val = main_expected.get(key, "MISSING")
        sys_val = main_result.get(key, "MISSING")
        if exp_val != sys_val:
            print(f"  {key}: 期待値='{exp_val}' システム='{sys_val}' ❌")
    
    # 従属節の不一致
    print("従属節の不一致:")
    for key in set(list(sub_expected.keys()) + list(sub_result.keys())):
        exp_val = sub_expected.get(key, "MISSING")
        sys_val = sub_result.get(key, "MISSING")
        if exp_val != sys_val:
            print(f"  {key}: 期待値='{exp_val}' システム='{sys_val}' ❌")

if __name__ == "__main__":
    analyze_test19()
