#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_quickly():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    print(f"分析文: {sentence}")
    print()
    
    # システムの実行（ログ出力を抑制）
    import logging
    logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # Stanza解析の詳細を確認
    print("=== Stanza解析結果 ===")
    doc = mapper.nlp(sentence)
    
    for sent in doc.sentences:
        print("Token依存関係:")
        for token in sent.words:
            print(f"  {token.text} -> head:{token.head} deprel:{token.deprel} upos:{token.upos}")
    
    print("\n=== システム処理結果 ===")
    result = mapper.process(sentence)
    
    # 従属節の修飾語を確認
    sub_slots = result.get('sub_slots', {})
    print(f"検出された従属節スロット: {sub_slots}")
    
    # quicklyが検出されない理由を調査
    print("\n=== quickly関連トークン検索 ===")
    for sent in doc.sentences:
        for token in sent.words:
            if 'quick' in token.text.lower():
                print(f"Found: {token.text} -> head:{token.head} deprel:{token.deprel} upos:{token.upos}")
                # head tokenを確認
                if token.head > 0:
                    head_token = sent.words[token.head - 1]  # 1-indexed
                    print(f"  Head token: {head_token.text} -> deprel:{head_token.deprel}")

if __name__ == "__main__":
    debug_quickly()
