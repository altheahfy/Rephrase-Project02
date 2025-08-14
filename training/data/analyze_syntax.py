#!/usr/bin/env python3
"""Stanza/spaCyの構文解析機能を調査"""

import stanza
import spacy
from advanced_grammar_detector import AdvancedGrammarDetector

def analyze_syntactic_structures():
    """Stanza/spaCyの構文解析結果を詳細調査"""
    
    # 基盤システム初期化
    detector = AdvancedGrammarDetector()
    
    test_sentences = [
        "I think that he is smart.",           # that節
        "Being a teacher, she knows well.",    # 分詞構文  
        "The book that I read was good.",      # 関係代名詞
        "If I were rich, I would travel.",     # 仮定法
        "Having finished work, he went home.", # 完了分詞構文
        "To succeed, you must work hard.",     # 不定詞句
    ]
    
    print("🔍 Stanza/spaCy 構文解析詳細調査")
    print("=" * 60)
    
    for sentence in test_sentences:
        print(f"\n📝 分析文: \"{sentence}\"")
        print("-" * 50)
        
        try:
            # Stanza解析
            stanza_doc = detector.nlp_stanza(sentence)
            
            print("🔵 Stanza依存構造:")
            for sent in stanza_doc.sentences:
                for word in sent.words:
                    if word.head != 0:  # rootでない場合
                        head_word = sent.words[word.head-1].text
                        print(f"  {word.text} --{word.deprel}--> {head_word}")
                    else:
                        print(f"  {word.text} [ROOT]")
            
            print("\n🔵 句構造 (Constituency):")
            for sent in stanza_doc.sentences:
                if hasattr(sent, 'constituency'):
                    print(f"  {sent.constituency}")
                
            # spaCy解析
            spacy_doc = detector.nlp_spacy(sentence)
            
            print("\n🟢 spaCy名詞句・動詞句:")
            for chunk in spacy_doc.noun_chunks:
                print(f"  NP: '{chunk.text}' (root: {chunk.root.text}, dep: {chunk.root.dep_})")
                
            print("\n🟢 spaCy依存構造 (主要):")
            for token in spacy_doc:
                if token.dep_ in ['nsubj', 'dobj', 'ccomp', 'xcomp', 'advcl', 'acl', 'relcl']:
                    print(f"  {token.text} --{token.dep_}--> {token.head.text}")
                    
        except Exception as e:
            print(f"❌ 解析エラー: {e}")

if __name__ == "__main__":
    analyze_syntactic_structures()
