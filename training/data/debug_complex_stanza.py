#!/usr/bin/env python3
"""
複文のStanza解析構造をデバッグするスクリプト
"""

import stanza

def debug_stanza_structure(text):
    """Stanza解析構造の詳細表示"""
    print(f"\n{'='*80}")
    print(f"文: {text}")
    print('='*80)
    
    # Stanza初期化
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', download_method=None)
    doc = nlp(text)
    sent = doc.sentences[0]
    
    # 依存関係の詳細表示
    print("\n📊 単語別依存関係:")
    for word in sent.words:
        head_text = sent.words[word.head-1].text if word.head > 0 else "ROOT"
        print(f"  {word.id:2d}: {word.text:15s} -> {head_text:15s} ({word.deprel})")
    
    # 特別な関係の抽出
    print(f"\n🔍 検出された関係: {sorted(set([w.deprel for w in sent.words]))}")
    
    # ROOT発見
    root_words = [w for w in sent.words if w.deprel == 'root']
    print(f"\n📌 ROOT: {[w.text for w in root_words]}")
    
    # 従属節の検出
    subordinate_relations = ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'csubj']
    subordinate_clauses = []
    
    for word in sent.words:
        if word.deprel in subordinate_relations:
            subordinate_clauses.append((word, word.deprel))
            
    if subordinate_clauses:
        print(f"\n🔍 従属節:")
        for clause_verb, rel_type in subordinate_clauses:
            print(f"  - {clause_verb.text} ({rel_type})")
            
            # この従属節の構成要素を表示
            clause_components = []
            for w in sent.words:
                if w.head == clause_verb.id:
                    clause_components.append((w, w.deprel))
                    
            print(f"    構成要素:")
            for comp, rel in clause_components:
                print(f"      {comp.text} ({rel})")
    
    # mark関係の検出（従属接続詞）
    marks = [w for w in sent.words if w.deprel == 'mark']
    if marks:
        print(f"\n🔗 従属接続詞: {[w.text for w in marks]}")

def main():
    test_sentences = [
        "He succeeded even though he was under intense pressure.",
        "She passed the test because she is very intelligent.",
        "We waited while they are working.",
        "I will help you if you need it.",
        "The man who is tall walks quickly.",
        "I know that he is happy."
    ]
    
    for sentence in test_sentences:
        debug_stanza_structure(sentence)

if __name__ == "__main__":
    main()
