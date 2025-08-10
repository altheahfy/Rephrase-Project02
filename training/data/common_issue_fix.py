#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全スロット共通課題修正パッチ
spaCy依存構造解析の改善

修正内容:
1. advmod も目的語として認識 (home問題の解決)
2. 疑問詞節の完全処理 (what you said問題の解決)
"""

def extract_enhanced_objects(verb_token, include_advmod=True):
    """拡張された目的語抽出"""
    objects = []
    
    # 直接目的語
    direct_objects = [child for child in verb_token.children if child.dep_ == "dobj"]
    objects.extend(direct_objects)
    
    # 副詞修飾語も含める（home問題対応）
    if include_advmod:
        adverbial_objects = [child for child in verb_token.children if child.dep_ == "advmod" and child.pos_ == "NOUN"]
        objects.extend(adverbial_objects)
    
    # 前置詞目的語
    prep_objects = [child for child in verb_token.children if child.dep_ == "pobj"]
    objects.extend(prep_objects)
    
    return objects

def is_wh_clause(doc):
    """疑問詞節の検出強化"""
    wh_words = {
        "what": "PRON",
        "where": "SCONJ", 
        "when": "SCONJ",
        "why": "SCONJ",
        "how": "SCONJ",
        "which": "PRON",
        "who": "PRON",
        "whom": "PRON"
    }
    
    for token in doc:
        if token.text.lower() in wh_words:
            expected_pos = wh_words[token.text.lower()]
            if token.pos_ in [expected_pos, "PRON", "SCONJ", "DET"]:  # 柔軟な判定
                return token
    
    return None

def extract_wh_clause_subslots(doc, wh_token):
    """疑問詞節の完全分解"""
    subslots = {}
    
    # 疑問詞そのものをsub-o1として設定
    subslots['sub-o1'] = {
        'text': wh_token.text,
        'tokens': [wh_token.text],
        'token_indices': [wh_token.i]
    }
    
    # ROOT動詞を探す
    root_verb = None
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            root_verb = token
            break
    
    if root_verb:
        # sub-v: ROOT動詞
        subslots['sub-v'] = {
            'text': root_verb.text,
            'tokens': [root_verb.text],
            'token_indices': [root_verb.i]
        }
        
        # sub-s: 主語
        subjects = [child for child in root_verb.children if child.dep_ == "nsubj"]
        if subjects:
            subslots['sub-s'] = {
                'text': subjects[0].text,
                'tokens': [subjects[0].text],
                'token_indices': [subjects[0].i]
            }
    
    return subslots

# テスト用のパッチ適用関数
def test_enhanced_parsing():
    """修正版の解析テスト"""
    import spacy
    
    nlp = spacy.load("en_core_web_sm")
    
    test_cases = [
        "to go home",           # advmod問題テスト
        "what you said",        # 疑問詞節テスト
        "where he went",        # 疑問詞節テスト
        "reading books"         # 正常ケース
    ]
    
    for text in test_cases:
        print(f"=== '{text}' 拡張解析 ===")
        doc = nlp(text)
        
        # 疑問詞節チェック
        wh_token = is_wh_clause(doc)
        if wh_token:
            print(f"疑問詞検出: {wh_token.text}")
            subslots = extract_wh_clause_subslots(doc, wh_token)
            for slot_type, data in subslots.items():
                print(f"  {slot_type}: '{data['text']}'")
        else:
            # 通常の処理
            for token in doc:
                if token.pos_ == "VERB" and token.dep_ == "ROOT":
                    print(f"動詞: {token.text}")
                    objects = extract_enhanced_objects(token)
                    if objects:
                        print(f"拡張目的語: {[obj.text for obj in objects]}")
                    break
        print()

if __name__ == "__main__":
    test_enhanced_parsing()
