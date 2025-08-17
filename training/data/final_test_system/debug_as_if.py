#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_as_if():
    sentence = "She acts as if she knows everything."
    print(f"分析文: {sentence}")
    print()
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # Stanza解析の詳細を確認
    print("=== Stanza解析結果 ===")
    doc = mapper.nlp(sentence)
    
    for sent in doc.sentences:
        print("Token依存関係:")
        for token in sent.words:
            print(f"  {token.text} -> head:{token.head} deprel:{token.deprel} upos:{token.upos}")
    
    print("\n=== as if関連トークン検索 ===")
    for sent in doc.sentences:
        for token in sent.words:
            if token.text.lower() in ['as', 'if']:
                print(f"Found: {token.text} -> head:{token.head} deprel:{token.deprel} upos:{token.upos}")
                # head tokenを確認
                if token.head > 0:
                    head_token = sent.words[token.head - 1]  # 1-indexed
                    print(f"  Head token: {head_token.text} -> deprel:{head_token.deprel}")

if __name__ == "__main__":
    debug_as_if()
