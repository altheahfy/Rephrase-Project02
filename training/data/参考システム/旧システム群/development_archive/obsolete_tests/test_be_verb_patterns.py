#!/usr/bin/env python3
"""
be動詞構文のStanza解析テスト
"""

import stanza

def test_be_verb_constructions():
    """be動詞構文のパターン分析"""
    nlp = stanza.Pipeline('en', verbose=False)
    
    # 名詞が補語になるパターン
    noun_complement_sentences = [
        "He is a teacher",
        "She was a student", 
        "They are engineers",
        "I am the manager",
        "It was a mistake"
    ]
    
    # 形容詞が補語になるパターン
    adj_complement_sentences = [
        "He is happy",
        "She was tired",
        "They are intelligent", 
        "I am ready",
        "It was difficult"
    ]
    
    # 前置詞句が補語になるパターン
    prep_complement_sentences = [
        "He is under pressure",
        "She was in trouble",
        "They are at home",
        "I am on vacation",
        "It was over there"
    ]
    
    all_tests = [
        ("名詞補語パターン", noun_complement_sentences),
        ("形容詞補語パターン", adj_complement_sentences),
        ("前置詞句補語パターン", prep_complement_sentences)
    ]
    
    for pattern_name, sentences in all_tests:
        print(f"\n{'='*80}")
        print(f"🎯 {pattern_name}")
        print(f"{'='*80}")
        
        for sentence in sentences:
            print(f"\n📝 文: {sentence}")
            print("-" * 60)
            
            doc = nlp(sentence)
            sent = doc.sentences[0]
            
            # ROOT探索
            root_word = None
            copula_word = None
            subject_word = None
            
            for word in sent.words:
                if word.deprel == 'root':
                    root_word = word
                elif word.deprel == 'cop':
                    copula_word = word
                elif word.deprel == 'nsubj':
                    subject_word = word
            
            # 結果表示
            if root_word:
                print(f"📌 ROOT: '{root_word.text}' (POS: {root_word.upos})")
            if copula_word:
                print(f"🔗 COPULA: '{copula_word.text}' (POS: {copula_word.upos})")
            if subject_word:
                print(f"👤 SUBJECT: '{subject_word.text}' (POS: {subject_word.upos})")
            
            # 全依存関係表示
            print("📋 全依存関係:")
            for word in sent.words:
                print(f"  {word.id:2}: {word.text:12} | POS: {word.upos:8} | HEAD: {word.head:2} | DEPREL: {word.deprel}")

if __name__ == "__main__":
    test_be_verb_constructions()
