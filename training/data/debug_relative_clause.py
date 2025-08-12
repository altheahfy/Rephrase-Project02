#!/usr/bin/env python3
"""
関係節構造のデバッグツール
StanzaとspaCyでの構造解析を詳細に確認
"""

import stanza
import spacy

def debug_relative_clause():
    """関係節の依存構造を詳細分析"""
    
    # NLP パイプライン初期化
    stanza_nlp = stanza.Pipeline('en', verbose=False)
    spacy_nlp = spacy.load("en_core_web_sm")
    
    text = "The book that he bought"
    
    print("="*60)
    print(f"🔍 関係節構造解析: '{text}'")
    print("="*60)
    
    # === Stanza解析 ===
    print("\n📊 Stanza解析結果:")
    print("-" * 30)
    stanza_doc = stanza_nlp(text)
    sent = stanza_doc.sentences[0]
    
    for word in sent.words:
        print(f"  {word.id:2d}. '{word.text:8s}' | {word.pos:6s} | {word.deprel:12s} | head={word.head} ({sent.words[word.head-1].text if word.head > 0 else 'ROOT'})")
    
    # ROOT語特定
    root_word = next((w for w in sent.words if w.head == 0), None)
    print(f"\n🎯 ROOT語: '{root_word.text}' ({root_word.pos})")
    
    # 関係節検出
    rel_clauses = [w for w in sent.words if w.deprel == 'acl:relcl']
    print(f"🔗 関係節: {len(rel_clauses)}個")
    for rel in rel_clauses:
        print(f"  - '{rel.text}' (head={sent.words[rel.head-1].text})")
    
    # === spaCy解析 ===
    print("\n📊 spaCy解析結果:")
    print("-" * 30)
    spacy_doc = spacy_nlp(text)
    
    for token in spacy_doc:
        print(f"  {token.i:2d}. '{token.text:8s}' | {token.pos_:6s} | {token.dep_:12s} | head={token.head.text}")
    
    # 関係節検出
    rel_clauses_spacy = [t for t in spacy_doc if t.dep_ == 'relcl']
    print(f"🔗 spaCy関係節: {len(rel_clauses_spacy)}個")
    for rel in rel_clauses_spacy:
        print(f"  - '{rel.text}' (head={rel.head.text})")

if __name__ == "__main__":
    debug_relative_clause()
