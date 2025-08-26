#!/usr/bin/env python3
"""副詞コンテキスト判定をデバッグ"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_adverb_context():
    """副詞コンテキスト判定をデバッグ"""
    mapper = UnifiedStanzaRephraseMapper()
    
    sentence = "The time when everything changed dramatically was unexpected."
    print(f"テスト: {sentence}")
    
    # Stanza解析結果を直接確認
    doc = mapper.nlp(sentence)
    
    print("\n=== Stanza解析結果 ===")
    for word in doc.sentences[0].words:
        print(f"{word.id}: {word.text} (POS={word.upos}, deprel={word.deprel}, head={word.head})")
    
    # 主動詞と従属節動詞を特定
    main_verb_id = mapper._find_main_verb(doc.sentences[0])
    subordinate_verbs = mapper._find_subordinate_verbs(doc.sentences[0], main_verb_id)
    
    print(f"\n主動詞ID: {main_verb_id}")
    print(f"従属節動詞IDs: {subordinate_verbs}")
    
    # dramatically の解析
    dramatically_word = None
    for word in doc.sentences[0].words:
        if word.text == "dramatically":
            dramatically_word = word
            break
    
    if dramatically_word:
        print(f"\ndramatically: id={dramatically_word.id}, head={dramatically_word.head}, deprel={dramatically_word.deprel}")
        
        # コンテキスト判定
        context = mapper._determine_adverb_context(dramatically_word, main_verb_id, subordinate_verbs, doc.sentences[0])
        print(f"コンテキスト判定: {context}")

if __name__ == "__main__":
    debug_adverb_context()
