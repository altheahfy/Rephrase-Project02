#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

def debug_svc_structures():
    """第2文型の依存関係構造をデバッグ"""
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_sentences = [
        "She is happy.",
        "He became a teacher.",
        "The book is interesting.",
        "They remained silent."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"🔍 文: {sentence}")
        print('='*60)
        
        doc = nlp(sentence)
        sent = doc.sentences[0]
        
        # ROOT動詞特定
        root_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                root_verb = word
                break
        
        print(f"📌 ROOT動詞: '{root_verb.text}' (pos={root_verb.upos})")
        
        print("\n🏗️ 依存関係構造:")
        for word in sent.words:
            head_text = "ROOT" if word.head == 0 else sent.words[word.head-1].text
            print(f"  {word.id:2d}: {word.text:12} ← {head_text:12} ({word.deprel:10}) [{word.upos}]")
        
        print("\n🎯 第2文型成分予測:")
        
        # S: nsubj
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'nsubj':
                print(f"  S候補:  '{word.text}' (nsubj)")
        
        # V: ROOT
        print(f"  V候補:  '{root_verb.text}' (ROOT)")
        
        # C1: acomp, nmod, attr, xcomp
        for word in sent.words:
            if word.head == root_verb.id and word.deprel in ['acomp', 'attr', 'nmod', 'xcomp']:
                print(f"  C1候補: '{word.text}' ({word.deprel})")

if __name__ == '__main__':
    debug_svc_structures()
