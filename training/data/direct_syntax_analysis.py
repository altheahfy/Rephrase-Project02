#!/usr/bin/env python3
"""直接Stanza/spaCyを使用した構文解析調査"""

import stanza
import spacy

def direct_syntactic_analysis():
    """StanzaとspaCyを直接使用した構文解析"""
    
    print("🔍 Direct Stanza/spaCy 構文解析調査")
    print("=" * 60)
    
    # 初期化
    try:
        print("🚀 NLPパイプライン初期化中...")
        nlp_stanza = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
        nlp_spacy = spacy.load("en_core_web_sm")
        print("✅ 初期化完了")
    except Exception as e:
        print(f"❌ 初期化失敗: {e}")
        return
    
    test_sentences = [
        "I think that he is smart.",           # that節
        "Being a teacher, she knows well.",    # 分詞構文  
        "The book that I read was good.",      # 関係代名詞
        "If I were rich, I would travel.",     # 仮定法
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 分析文: \"{sentence}\"")
        print("-" * 50)
        
        try:
            # Stanza解析
            stanza_doc = nlp_stanza(sentence)
            
            print("🔵 Stanza依存構造:")
            for sent in stanza_doc.sentences:
                for word in sent.words:
                    if word.head != 0:  # rootでない場合
                        head_word = sent.words[word.head-1].text
                        print(f"  {word.text}({word.upos}) --{word.deprel}--> {head_word}")
                    else:
                        print(f"  {word.text}({word.upos}) [ROOT]")
            
            # spaCy解析
            spacy_doc = nlp_spacy(sentence)
            
            print("\n🟢 spaCy名詞句・句構造:")
            for chunk in spacy_doc.noun_chunks:
                print(f"  NP: '{chunk.text}' (root: {chunk.root.text})")
                
            print("\n🟢 spaCy重要依存関係:")
            for token in spacy_doc:
                if token.dep_ in ['nsubj', 'dobj', 'ccomp', 'xcomp', 'advcl', 'acl', 'relcl', 'mark']:
                    print(f"  {token.text}({token.pos_}) --{token.dep_}--> {token.head.text}")
                    
            # 節構造検出
            print("\n🎯 検出可能な節構造:")
            clauses = []
            for token in spacy_doc:
                if token.dep_ in ['ccomp', 'xcomp', 'advcl', 'acl', 'relcl']:
                    clause_tokens = [t for t in token.subtree]
                    clause_text = ' '.join([t.text for t in clause_tokens])
                    clauses.append({
                        'type': token.dep_,
                        'text': clause_text,
                        'root': token.text,
                        'has_subject': any(t.dep_ == 'nsubj' for t in clause_tokens),
                        'has_verb': any(t.pos_ == 'VERB' for t in clause_tokens)
                    })
            
            for clause in clauses:
                sv_status = "SV" if clause['has_subject'] and clause['has_verb'] else "phrase"
                print(f"  {clause['type']}: '{clause['text']}' ({sv_status})")
                    
        except Exception as e:
            print(f"❌ 解析エラー: {e}")

if __name__ == "__main__":
    direct_syntactic_analysis()
