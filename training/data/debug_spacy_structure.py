#!/usr/bin/env python3
"""
spaCyの詳細解析結果を確認
"""

import spacy

def analyze_spacy_structure():
    nlp = spacy.load('en_core_web_sm')
    
    test_sentence = "The students study hard for exams."
    doc = nlp(test_sentence)
    
    print(f"文: {test_sentence}")
    print(f"=" * 50)
    
    print(f"\n📊 トークン解析:")
    for i, token in enumerate(doc):
        print(f"{i:2d}. '{token.text}' - POS: {token.pos_} | TAG: {token.tag_} | DEP: {token.dep_} | HEAD: '{token.head.text}'")
    
    print(f"\n🔍 依存関係ツリー:")
    for token in doc:
        children = [child.text for child in token.children]
        print(f"'{token.text}' ({token.dep_}) <- HEAD: '{token.head.text}' | CHILDREN: {children}")
    
    print(f"\n🎯 副詞と前置詞句の特定:")
    for token in doc:
        if token.pos_ == 'ADV':
            print(f"副詞: '{token.text}' - 修飾対象: '{token.head.text}' ({token.head.pos_})")
        elif token.pos_ == 'ADP':
            # 前置詞句全体を取得
            prep_phrase = [token.text]
            for child in token.children:
                prep_phrase.append(child.text)
                # 前置詞の目的語の修飾語も含める
                for grandchild in child.children:
                    prep_phrase.append(grandchild.text)
            print(f"前置詞句: '{' '.join(prep_phrase)}' - 修飾対象: '{token.head.text}' ({token.head.pos_})")

if __name__ == "__main__":
    analyze_spacy_structure()
