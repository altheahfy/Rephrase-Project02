#!/usr/bin/env python3
"""
Stanza本体の直接テスト - エンジンを通さずに
"""

import stanza

def test_stanza_raw():
    """Stanza本体で直接解析"""
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_sentences = [
        "he was under intense pressure",
        "I like you",
        "deliver the final proposal flawlessly"
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"🎯 文: {sentence}")
        print(f"{'='*60}")
        
        doc = nlp(sentence)
        sent = doc.sentences[0]
        
        # 全ての単語とその依存関係を表示
        print("📋 全単語の依存関係:")
        for word in sent.words:
            print(f"  {word.id:2}: {word.text:15} | POS: {word.upos:8} | HEAD: {word.head:2} | DEPREL: {word.deprel:15}")
        
        # ROOT探索
        root_word = None
        for word in sent.words:
            if word.deprel == 'root':
                root_word = word
                break
        
        if root_word:
            print(f"\n📌 ROOT: '{root_word.text}' (POS: {root_word.upos}, DEPREL: {root_word.deprel})")
        else:
            print("\n❌ ROOT が見つかりません")

if __name__ == "__main__":
    test_stanza_raw()
