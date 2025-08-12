#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""受動態構文のStanza構造解析"""

import stanza

def analyze_passive_structures():
    """受動態のStanza構造を分析"""
    print("🔍 受動態構文のStanza解析")
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_sentences = [
        "The book was read.",                           # 単純受動態
        "The book was read by him.",                    # by句付き受動態
        "The house is being built.",                    # 進行受動態
        "The work has been completed by the team.",     # 完了受動態
        "The door was opened by the wind."              # 動作主付き受動態
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 文: {sentence}")
        doc = nlp(sentence)
        sent = doc.sentences[0]
        
        print("  構造解析:")
        for word in sent.words:
            print(f"    {word.text:12} | {word.upos:6} | {word.deprel:12} | head: {word.head:2} | lemma: {word.lemma}")
        
        # 受動態の特徴を検出
        passive_features = analyze_passive_features(sent)
        if passive_features:
            print(f"  🎯 受動態検出: {passive_features}")
        else:
            print("  ❌ 受動態なし")

def analyze_passive_features(sent):
    """受動態の特徴を検出"""
    features = {
        'auxiliary': None,    # be動詞
        'main_verb': None,    # 過去分詞
        'subject': None,      # 主語
        'agent': None,        # by句
        'type': None          # 受動態の種類
    }
    
    # be動詞 + 過去分詞の組み合わせを探す
    for word in sent.words:
        # be動詞検出
        if word.lemma in ['be'] and word.upos == 'AUX':
            features['auxiliary'] = word
            
        # 過去分詞検出（be動詞に依存）
        elif word.upos == 'VERB' and word.deprel == 'root' and features['auxiliary']:
            # be動詞の後に来る動詞をチェック
            if word.id > features['auxiliary'].id:
                features['main_verb'] = word
                
        # 主語検出
        elif word.deprel == 'nsubj:pass':
            features['subject'] = word
            
        # by句検出
        elif word.text.lower() == 'by' and word.upos == 'ADP':
            # byに依存する語を探す
            for w in sent.words:
                if w.head == word.id and w.deprel == 'obl:agent':
                    features['agent'] = w
                    break
    
    # 受動態判定
    if features['auxiliary'] and features['main_verb'] and features['subject']:
        if features['agent']:
            features['type'] = 'agent_passive'
        else:
            features['type'] = 'simple_passive'
        return features
    
    return None

if __name__ == "__main__":
    analyze_passive_structures()
