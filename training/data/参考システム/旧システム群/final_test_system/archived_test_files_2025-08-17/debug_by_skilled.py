#!/usr/bin/env python3
"""
by skilled workers前置詞句検出の詳細デバッグ
"""

import stanza

def main():
    print("=== by skilled workers前置詞句デバッグ ===")
    
    # Stanza初期化
    stanza.download('en', verbose=False)
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', use_gpu=False, verbose=False)
    
    # テスト文
    test_sentence = "The building is being constructed very carefully by skilled workers."
    print(f"Test: {test_sentence}")
    
    # Stanza解析の詳細を確認
    doc = nlp(test_sentence)
    sentence = doc.sentences[0]
    
    print("\n=== Stanza解析詳細 ===")
    for word in sentence.words:
        print(f"ID:{word.id} Text:'{word.text}' POS:{word.pos} DepRel:{word.deprel} Head:{word.head}")
    
    print("\n=== 前置詞句候補検索 ===")
    prepositional_candidates = []
    for word in sentence.words:
        if word.deprel in ['obl', 'obl:agent', 'nmod:agent', 'nmod', 'obl:unmarked', 'nmod:unmarked', 'obl:tmod', 'nmod:tmod']:
            prepositional_candidates.append(word)
            print(f"前置詞句候補: {word.text} ({word.deprel}) - Head:{word.head}")
    
    print("\n=== by検索 ===")
    by_word = None
    for word in sentence.words:
        if word.text.lower() == 'by':
            by_word = word
            print(f"by発見: ID:{word.id} DepRel:{word.deprel} Head:{word.head}")
            
            # byに修飾される語を検索
            by_modifiers = []
            for mod_word in sentence.words:
                if mod_word.head == word.id:
                    by_modifiers.append(mod_word)
                    print(f"  by修飾語: {mod_word.text} ({mod_word.deprel})")
            
            # byが修飾する語（head）を確認
            head_word = next((w for w in sentence.words if w.id == word.head), None)
            if head_word:
                print(f"  byの修飾先: {head_word.text} ({head_word.deprel})")
    
    print("\n=== workers検索 ===")
    for word in sentence.words:
        if word.text.lower() == 'workers':
            print(f"workers発見: ID:{word.id} DepRel:{word.deprel} Head:{word.head}")
            
            # workersに修飾される語を検索
            workers_modifiers = []
            for mod_word in sentence.words:
                if mod_word.head == word.id:
                    workers_modifiers.append(mod_word)
                    print(f"  workers修飾語: {mod_word.text} ({mod_word.deprel})")

if __name__ == "__main__":
    main()
