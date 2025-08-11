#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

def debug_stanza_structure():
    """Stanzaの依存関係構造をデバッグ"""
    print("🔍 Stanza依存関係構造デバッグ開始")
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    doc = nlp(sentence)
    
    for sent in doc.sentences:
        print(f"\n📋 全体構造:")
        print(f"文: {sent.text}")
        
        print(f"\n📋 全単語の依存関係:")
        for word in sent.words:
            head_text = sent.words[word.head-1].text if word.head > 0 else "ROOT"
            print(f"{word.id:2d}: {word.text:15} ({word.deprel:12}) -> {word.head:2d}:{head_text}")
        
        # ROOT動詞を特定
        root_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                root_verb = word
                break
        
        if root_verb:
            print(f"\n🎯 ROOT動詞: {root_verb.text} (ID: {root_verb.id})")
            
            # 'make'動詞（xcomp）を特定
            make_verb = None
            for word in sent.words:
                if word.head == root_verb.id and word.deprel == 'xcomp':
                    make_verb = word
                    print(f"🎯 MAKE動詞: {make_verb.text} (ID: {make_verb.id})")
                    break
            
            if make_verb:
                print(f"\n📋 MAKE動詞の子要素:")
                for word in sent.words:
                    if word.head == make_verb.id:
                        print(f"  {word.text:20} ({word.deprel:12}) -> {make_verb.text}")
                
                # 'deliver'動詞（C2候補）を探索
                deliver_verb = None
                for word in sent.words:
                    if word.head == make_verb.id and word.text == 'deliver':
                        deliver_verb = word
                        print(f"🎯 DELIVER動詞: {deliver_verb.text} (ID: {deliver_verb.id}, deprel: {deliver_verb.deprel})")
                        break
                
                if deliver_verb:
                    print(f"\n📋 DELIVER動詞の子要素:")
                    for word in sent.words:
                        if word.head == deliver_verb.id:
                            print(f"  {word.text:20} ({word.deprel:12}) -> {deliver_verb.text}")

if __name__ == '__main__':
    debug_stanza_structure()
