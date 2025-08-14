"""
Stanza/spaCy境界検出分析スクリプト
テスト失敗の原因を詳しく調査
"""

import stanza
import spacy
from pprint import pprint

def analyze_boundary_detection():
    """境界検出の詳細分析"""
    
    # 初期化
    stanza_nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
    spacy_nlp = spacy.load('en_core_web_sm')
    
    # 問題のあった文を分析
    test_sentences = [
        "Having finished the project, the student submitted it confidently.",
        "Walking to school, she met her friend.",
        "The book that she bought was expensive.",
        "Students who study hard succeed in life.",
        "I know what you did yesterday.",
        "When the rain stopped, we went outside."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"🔍 Analyzing: {sentence}")
        print('='*60)
        
        # Stanza分析
        print("\n📊 STANZA ANALYSIS:")
        stanza_doc = stanza_nlp(sentence)
        
        for sent in stanza_doc.sentences:
            print(f"\nTokens with dependencies:")
            for word in sent.words:
                print(f"  {word.id:2d}: {word.text:<12} | POS: {word.upos:<8} | deprel: {word.deprel:<15} | head: {word.head}")
            
            # 動詞を特定
            print(f"\nVerbs found:")
            for word in sent.words:
                if word.upos in ['VERB', 'AUX']:
                    print(f"  {word.text} (pos: {word.id}, deprel: {word.deprel}, head: {word.head})")
        
        # spaCy分析
        print(f"\n📊 SPACY ANALYSIS:")
        spacy_doc = spacy_nlp(sentence)
        
        print(f"Dependencies:")
        for token in spacy_doc:
            if token.pos_ in ['VERB', 'AUX']:
                print(f"  VERB: {token.text} | dep: {token.dep_} | head: {token.head.text} | children: {[child.text for child in token.children]}")
        
        print(f"\nNoun chunks:")
        for chunk in spacy_doc.noun_chunks:
            print(f"  {chunk.text} | root: {chunk.root.text} | dep: {chunk.root.dep_}")
        
        print(f"\nClausal dependencies:")
        for token in spacy_doc:
            if token.dep_ in ['ccomp', 'xcomp', 'advcl', 'acl', 'relcl', 'csubj']:
                print(f"  {token.text} | dep: {token.dep_} | head: {token.head.text}")

if __name__ == "__main__":
    analyze_boundary_detection()
