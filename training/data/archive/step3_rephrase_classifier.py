#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3: Rephrase定義に基づく分類システム
=========================================
Word/Phrase/Clause分類ロジックの実装
"""

import spacy

class RephraseClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def classify_text(self, text):
        """テキストをWord/Phrase/Clauseに分類"""
        doc = self.nlp(text)
        
        # 動詞の数を数える
        verbs = [token for token in doc if token.pos_ in ["VERB", "AUX"]]
        
        # 主語-動詞ペアを探す
        sv_pairs = []
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                subjects = [child for child in token.children if child.dep_ in ["nsubj", "nsubjpass"]]
                if subjects:
                    sv_pairs.append((subjects[0], token))
        
        # 分類ロジック
        classification = self._determine_type(doc, verbs, sv_pairs)
        
        return {
            'text': text,
            'type': classification,
            'verbs': [v.text for v in verbs],
            'sv_pairs': [(s.text, v.text) for s, v in sv_pairs],
            'analysis': self._get_analysis_details(doc)
        }
    
    def _determine_type(self, doc, verbs, sv_pairs):
        """Word/Phrase/Clause判定"""
        
        # Clause: SV構造がある
        if sv_pairs:
            return "CLAUSE"
        
        # Phrase: 動詞はあるがSV構造なし（不定詞、動名詞等）
        if verbs:
            # to play tennis, playing tennis等をチェック
            for verb in verbs:
                # 不定詞 (to + 動詞)
                if any(child.text.lower() == "to" and child.dep_ == "aux" for child in verb.children):
                    return "PHRASE"
                # 動名詞・分詞
                if verb.tag_ in ["VBG", "VBN"]:
                    return "PHRASE"
        
        # Word: 文構造の入れ子なし
        return "WORD"
    
    def _get_analysis_details(self, doc):
        """詳細分析情報"""
        details = []
        for token in doc:
            details.append({
                'text': token.text,
                'pos': token.pos_,
                'tag': token.tag_,
                'dep': token.dep_,
                'head': token.head.text
            })
        return details

def test_classification():
    """分類テスト"""
    classifier = RephraseClassifier()
    
    test_cases = [
        # Word examples
        "A new project",
        "The experienced manager", 
        "Efficiently",
        "Yesterday",
        
        # Phrase examples  
        "to play tennis",
        "playing tennis",
        "completed yesterday",
        
        # Clause examples
        "The manager works",
        "A new project was completed",
        "The manager who works here"
    ]
    
    print("=== Rephrase分類テスト ===")
    for text in test_cases:
        result = classifier.classify_text(text)
        print(f"\n'{text}' → {result['type']}")
        print(f"  動詞: {result['verbs']}")
        print(f"  SV構造: {result['sv_pairs']}")

if __name__ == "__main__":
    test_classification()
