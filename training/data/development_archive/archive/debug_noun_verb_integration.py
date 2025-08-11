#!/usr/bin/env python3
import spacy
import sys
import os

# 現在のディレクトリをパスに追加
sys.path.append(os.path.dirname(__file__))

from step13_o1_subslot_new import O1SubslotGenerator

def debug_test():
    generator = O1SubslotGenerator()
    text = "students studying abroad this year"
    
    print(f"=== Debug test for: '{text}' ===")
    
    # Step by step debugging
    doc = generator.nlp(text)
    subslots = {}
    
    # 1. noun-verb統合チェック
    root_tokens = [token for token in doc if token.dep_ == "ROOT" and token.pos_ in ["NOUN", "PROPN"]]
    print(f"ROOT tokens: {[t.text for t in root_tokens]}")
    
    if root_tokens:
        root_token = root_tokens[0]
        verb_children = [child for child in root_token.children if child.pos_ == "VERB" and child.dep_ in ["acl", "relcl"]]
        print(f"Verb children of '{root_token.text}': {[v.text for v in verb_children]}")
        
        if verb_children:
            verb_token = verb_children[0]
            combined_text = f"{root_token.text} {verb_token.text}"
            subslots['sub-v'] = {
                'text': combined_text,
                'tokens': [root_token.text, verb_token.text],
                'token_indices': [root_token.i, verb_token.i]
            }
            print(f"✅ Manual noun-verb integration: {combined_text}")
            print(f"subslots after noun-verb integration: {subslots}")
    
    # 2. Complete generator test
    result = generator.generate_o1_subslots(text, 'phrase')
    print(f"Final generator result: {result}")
    
    # 3. Comparison
    if 'sub-v' in subslots and 'sub-v' in result:
        manual_subv = subslots['sub-v']['text']
        generator_subv = result['sub-v']['text']
        print(f"\nComparison:")
        print(f"Manual integration: '{manual_subv}'")
        print(f"Generator result:  '{generator_subv}'")
        print(f"Match: {manual_subv == generator_subv}")

if __name__ == "__main__":
    debug_test()
