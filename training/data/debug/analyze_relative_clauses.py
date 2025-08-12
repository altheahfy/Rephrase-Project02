#!/usr/bin/env python3
"""
関係代名詞節のStanza依存関係分析
"The book that he bought"の構造を詳細調査
"""

import stanza

def analyze_relative_clause_structure():
    """関係代名詞節のStanza出力構造分析"""
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_sentences = [
        "The book that he bought is expensive.",
        "The man who runs fast won the race.",
        "The house which I visited was old.",
        "The girl whose book I borrowed is smart.",
    ]
    
    print("🔍 関係代名詞節のStanza依存関係分析")
    print("="*60)
    
    for sentence in test_sentences:
        print(f"\n📝 テスト文: {sentence}")
        print("-" * 40)
        
        doc = nlp(sentence)
        sent = doc.sentences[0]
        
        # 依存関係を詳細表示
        print("依存関係構造:")
        for word in sent.words:
            marker = ""
            if word.text.lower() in ['that', 'which', 'who', 'whom', 'whose']:
                marker = " 🎯 [関係代名詞]"
            elif word.deprel in ['acl:relcl', 'acl']:
                marker = " 📎 [関係節]"
            elif word.deprel == 'nsubj' and any(w.text.lower() in ['that', 'which', 'who'] for w in sent.words if w.head == word.head):
                marker = " 👤 [関係節内主語]"
            
            print(f"  {word.id:2d} {word.text:12} | {word.deprel:15} | head:{word.head:2d} | {word.pos}{marker}")
        
        # 関係代名詞とその節の特定
        relative_info = identify_relative_structure(sent)
        if relative_info:
            print(f"\n🎯 関係構造分析:")
            for info in relative_info:
                print(f"  {info}")

def identify_relative_structure(sent):
    """関係代名詞構造の特定"""
    relative_info = []
    
    # 関係代名詞の検出
    relative_pronouns = []
    for word in sent.words:
        if word.text.lower() in ['that', 'which', 'who', 'whom', 'whose']:
            relative_pronouns.append(word)
    
    # 関係節の検出
    relative_clauses = []
    for word in sent.words:
        if word.deprel in ['acl:relcl', 'acl']:
            relative_clauses.append(word)
    
    # 関係節内の要素特定
    for rel_pronoun in relative_pronouns:
        relative_info.append(f"関係代名詞: '{rel_pronoun.text}' (id: {rel_pronoun.id}, deprel: {rel_pronoun.deprel})")
        
        # この関係代名詞に関連する節の要素を探す
        related_words = []
        for word in sent.words:
            # 関係代名詞を中心とした依存関係の範囲を特定
            if word.head == rel_pronoun.id or (word.deprel == 'nsubj' and any(w.id == word.head for w in relative_clauses)):
                related_words.append(word)
        
        if related_words:
            related_texts = [f"'{w.text}'({w.deprel})" for w in related_words]
            relative_info.append(f"  関連語: {', '.join(related_texts)}")
    
    return relative_info

if __name__ == "__main__":
    analyze_relative_clause_structure()
