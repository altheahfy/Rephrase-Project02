#!/usr/bin/env python3
"""
whose構文の詳細デバッグ
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import logging

def debug_whose_structure():
    """whose構文の依存関係を詳細に確認"""
    
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')
    
    mapper = DynamicGrammarMapper()
    
    # 問題のある文で詳細分析
    sentence = "The woman whose car is blue works here."
    
    print(f"🔍 デバッグ対象: '{sentence}'")
    print("=" * 60)
    
    # spaCy解析
    doc = mapper.nlp(sentence)
    tokens = mapper._extract_tokens(doc)
    
    print("📊 トークン詳細:")
    for i, token in enumerate(tokens):
        print(f"  {i}: '{token['text']}' (POS:{token['pos']}, DEP:{token['dep']}, HEAD:{token['head']} [idx:{token['head_idx']}])")
    
    print("\n🔍 whose構文解析:")
    
    # whose の位置を特定
    whose_idx = None
    for i, token in enumerate(tokens):
        if token['text'].lower() == 'whose':
            whose_idx = i
            break
    
    if whose_idx is not None:
        print(f"whose位置: {whose_idx}")
        
        # 関係節動詞(relcl)を探す
        relcl_verbs = []
        for i, token in enumerate(tokens):
            if token['dep'] == 'relcl':
                relcl_verbs.append((i, token))
        
        print(f"関係節動詞(relcl): {relcl_verbs}")
        
        # ROOT動詞を探す
        root_verbs = []
        for i, token in enumerate(tokens):
            if token['dep'] == 'ROOT':
                root_verbs.append((i, token))
        
        print(f"ROOT動詞: {root_verbs}")
        
        # 依存関係分析
        if relcl_verbs:
            relcl_idx, relcl_token = relcl_verbs[0]
            print(f"\n関係節動詞 '{relcl_token['text']}' の依存要素:")
            
            dependents = []
            for i, token in enumerate(tokens):
                if token['head_idx'] == relcl_idx:
                    dependents.append((i, token))
                    print(f"  {i}: '{token['text']}' (DEP:{token['dep']})")
            
            print(f"依存要素数: {len(dependents)}")
    
    # 実際の処理結果
    print(f"\n🧠 実際の関係節検出結果:")
    relative_info = mapper._detect_relative_clause(tokens, sentence)
    print(f"結果: {relative_info}")

if __name__ == "__main__":
    debug_whose_structure()
