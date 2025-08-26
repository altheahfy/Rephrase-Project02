#!/usr/bin/env python3
"""
V slot extraction debugging
"""

import stanza

def debug_v_extraction():
    """V抽出のデバッグ"""
    
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
    text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    doc = nlp(text)
    sent = doc.sentences[0]
    
    # ROOT動詞を特定
    root_verb = None
    for word in sent.words:
        if word.deprel == 'root':
            root_verb = word
            break
    
    print(f"🎯 ROOT動詞: '{root_verb.text}' (POS: {root_verb.upos})")
    
    # 全ての動詞とその依存関係を表示
    print(f"\n📋 全動詞とその依存関係:")
    for word in sent.words:
        if word.upos == 'VERB':
            print(f"  {word.text:12} | head: {sent.words[word.head-1].text if word.head != 0 else 'ROOT':12} | deprel: {word.deprel:12}")
    
    # xcomp関係を確認
    print(f"\n🔍 xcomp構造分析:")
    for word in sent.words:
        if word.deprel == 'xcomp':
            head_word = sent.words[word.head-1] if word.head != 0 else None
            print(f"  {word.text:12} ← xcomp ← {head_word.text if head_word else 'ROOT'}")
    
    # 正解の'make'を探す
    print(f"\n🎯 'make'動詞分析:")
    for word in sent.words:
        if word.text == 'make':
            head_word = sent.words[word.head-1] if word.head != 0 else None
            print(f"  make: head={head_word.text if head_word else 'ROOT'}, deprel={word.deprel}")

if __name__ == "__main__":
    debug_v_extraction()
