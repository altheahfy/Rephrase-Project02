#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Case 32 複文Stanza解析詳細確認
関係節がどのようにsentenceとして解析されているかチェック
"""

import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログ設定
logging.basicConfig(level=logging.DEBUG)

def debug_stanza_sentences():
    print("Case 32 Stanza文分割解析")
    print("=" * 50)
    
    # マッパー初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 32 文章
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    
    # Stanza解析
    doc = mapper._analyze_with_stanza(sentence)
    
    print(f"文章: {sentence}")
    print(f"Stanza sentences数: {len(doc.sentences)}")
    print()
    
    # 各sentenceの詳細
    for i, sent in enumerate(doc.sentences):
        print(f"📍 Sentence {i+1}:")
        print(f"  Text: '{sent.text}'")
        print(f"  Words: {len(sent.words)}")
        print("  Word details:")
        
        for word in sent.words:
            print(f"    {word.id:2}: {word.text:12} | {word.upos:8} | {word.deprel:15} | head={word.head}")
        print()
    
    # 副詞検出
    print("🔍 副詞検出:")
    for i, sent in enumerate(doc.sentences):
        adverbs = []
        for word in sent.words:
            if word.upos == 'ADV':
                adverbs.append(f"{word.text}({word.deprel})")
        
        if adverbs:
            print(f"  Sentence {i+1}: {', '.join(adverbs)}")
        else:
            print(f"  Sentence {i+1}: 副詞なし")

if __name__ == "__main__":
    debug_stanza_sentences()
