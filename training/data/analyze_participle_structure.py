#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza
import logging

def main():
    # Stanzaパイプライン初期化
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
    
    # 分詞構文の例文を詳細分析
    sentences = [
        "The team working overtime completed the project successfully yesterday.",
        "The woman standing quietly near the door was waiting patiently.",
        "The documents being reviewed thoroughly will be approved soon."
    ]
    
    for i, sentence in enumerate(sentences, 1):
        print(f"\n=== Case {48+i}: {sentence} ===")
        doc = nlp(sentence)
        
        for word in doc.sentences[0].words:
            print(f"ID:{word.id:2} {word.text:12} | POS:{word.upos:4} | xPOS:{word.xpos:4} | HEAD:{word.head:2} | DEP:{word.deprel:10}")
        
        # VBG（現在分詞）を探す
        print("\n🔍 現在分詞（VBG）の検出:")
        for word in doc.sentences[0].words:
            if word.xpos == 'VBG':
                print(f"  VBG found: {word.text} (ID:{word.id}, HEAD:{word.head}, DEP:{word.deprel})")
                
                # 分詞の依存語を確認
                dependents = [w for w in doc.sentences[0].words if w.head == word.id]
                if dependents:
                    print(f"    Dependents: {[f'{w.text}({w.deprel})' for w in dependents]}")
        
        # beingの検出
        print("\n🔍 being + 過去分詞の検出:")
        for word in doc.sentences[0].words:
            if word.text.lower() == 'being':
                print(f"  being found: {word.text} (ID:{word.id}, HEAD:{word.head}, DEP:{word.deprel})")
                
                # beingの依存語を確認
                dependents = [w for w in doc.sentences[0].words if w.head == word.id]
                if dependents:
                    print(f"    Dependents: {[f'{w.text}({w.deprel})' for w in dependents]}")

if __name__ == "__main__":
    main()
