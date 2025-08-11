#!/usr/bin/env python3
"""
v4エンジンのデバッグスクリプト
"""

import stanza

def debug_word_extraction():
    """単語抽出の詳細デバッグ"""
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', download_method=None)
    
    text = "He succeeded even though he was under intense pressure."
    doc = nlp(text)
    sent = doc.sentences[0]
    
    print(f"文: {text}")
    print("\n🔍 全単語の依存関係:")
    for word in sent.words:
        head_text = sent.words[word.head-1].text if word.head > 0 else "ROOT"
        print(f"  {word.id:2d}: {word.text:15s} -> {head_text:15s} ({word.deprel})")
    
    # ROOT動詞
    root_verb = None
    for word in sent.words:
        if word.deprel == 'root':
            root_verb = word
            break
    
    print(f"\n📌 ROOT動詞: {root_verb.text}")
    
    # 従属節識別
    subordinate_relations = ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'csubj']
    subordinate_heads = [w for w in sent.words if w.deprel in subordinate_relations]
    
    print(f"\n🔍 従属節ヘッド: {[w.text for w in subordinate_heads]}")
    
    # 従属節の単語収集
    for sub_head in subordinate_heads:
        print(f"\n📋 従属節'{sub_head.text}'の構成要素:")
        subtree_ids = get_subtree_word_ids(sent, sub_head)
        clause_words = [w for w in sent.words if w.id in subtree_ids]
        
        for word in clause_words:
            print(f"  {word.text} ({word.deprel})")
        
        # 従属節内の依存関係
        clause_relations = [w.deprel for w in clause_words]
        print(f"  → 依存関係: {clause_relations}")
    
    # 主節の単語収集
    subordinate_word_ids = set()
    for sub_head in subordinate_heads:
        subordinate_word_ids.update(get_subtree_word_ids(sent, sub_head))
    
    main_words = [w for w in sent.words if w.id not in subordinate_word_ids]
    print(f"\n🏛️ 主節の単語: {[w.text for w in main_words]}")
    main_relations = [w.deprel for w in main_words]
    print(f"  → 依存関係: {main_relations}")

def get_subtree_word_ids(sent, head_word):
    """部分木の単語ID収集"""
    subtree_ids = {head_word.id}
    
    def add_children(word_id):
        for word in sent.words:
            if word.head == word_id and word.id not in subtree_ids:
                subtree_ids.add(word.id)
                add_children(word.id)
    
    add_children(head_word.id)
    return subtree_ids

def debug_second_sentence():
    """2番目の文のデバッグ"""
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', download_method=None)
    
    text = "She passed the test because she is very intelligent."
    doc = nlp(text)
    sent = doc.sentences[0]
    
    print(f"\n{'='*50}")
    print(f"文: {text}")
    print("\n🔍 全単語の依存関係:")
    for word in sent.words:
        head_text = sent.words[word.head-1].text if word.head > 0 else "ROOT"
        print(f"  {word.id:2d}: {word.text:15s} -> {head_text:15s} ({word.deprel})")
    
    # 従属節識別
    subordinate_relations = ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'csubj']
    subordinate_heads = [w for w in sent.words if w.deprel in subordinate_relations]
    subordinate_word_ids = set()
    for sub_head in subordinate_heads:
        subordinate_word_ids.update(get_subtree_word_ids(sent, sub_head))
    
    main_words = [w for w in sent.words if w.id not in subordinate_word_ids]
    print(f"\n🏛️ 主節の単語: {[w.text for w in main_words]}")
    main_relations = [w.deprel for w in main_words]
    print(f"  → 依存関係: {main_relations}")
    print(f"  → 'obj'が含まれる？: {'obj' in main_relations}")

if __name__ == "__main__":
    debug_word_extraction()
    debug_second_sentence()
