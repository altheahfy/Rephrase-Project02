#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 4: 正確なSubslot Generator - Rephrase定義準拠
===============================================
Word/Phrase/Clauseに基づく適切なsubslot生成
"""

import spacy

class AccurateSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_subslots(self, text):
        """テキストタイプに応じたsubslot生成"""
        doc = self.nlp(text)
        
        # まず分類
        text_type = self._classify_text(doc)
        
        result = {
            'text': text,
            'type': text_type,
            'subslots': {}
        }
        
        if text_type == "WORD":
            # Wordは上位スロットのみ、サブスロット不使用
            result['subslots'] = None
            result['message'] = "Wordタイプのため、サブスロット分解は行いません"
            
        elif text_type == "PHRASE":
            # PhraseはV以降のみサブスロット化
            result['subslots'] = self._extract_phrase_subslots(doc)
            
        elif text_type == "CLAUSE":
            # ClauseはSV構造で完全サブスロット化
            result['subslots'] = self._extract_clause_subslots(doc)
        
        return result
    
    def _classify_text(self, doc):
        """Word/Phrase/Clause分類"""
        # SV構造の検出
        sv_pairs = self._find_sv_pairs(doc)
        if sv_pairs:
            return "CLAUSE"
        
        # 動詞の存在チェック（不定詞、動名詞等）
        verbs = [token for token in doc if token.pos_ in ["VERB"] and token.dep_ != "relcl"]
        if verbs:
            return "PHRASE"
        
        return "WORD"
    
    def _find_sv_pairs(self, doc):
        """主語-動詞ペアを検出"""
        pairs = []
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                subjects = [child for child in token.children if child.dep_ in ["nsubj", "nsubjpass"]]
                for subject in subjects:
                    pairs.append((subject, token))
        return pairs
    
    def _extract_clause_subslots(self, doc):
        """Clause用サブスロット抽出"""
        subslots = {}
        
        # ROOT動詞を見つける
        root = None
        for token in doc:
            if token.dep_ == "ROOT":
                root = token
                break
        
        if not root:
            return subslots
        
        # sub-s: 主語
        subjects = [child for child in root.children if child.dep_ in ["nsubj", "nsubjpass"]]
        if subjects:
            subject = subjects[0]
            subslots['sub-s'] = {
                'text': ' '.join([t.text for t in self._collect_subtree(subject)]),
                'root_token': subject.text,
                'dependency': subject.dep_
            }
        
        # sub-aux: 助動詞
        aux_tokens = [child for child in root.children if child.dep_ in ["aux", "auxpass"]]
        if aux_tokens:
            subslots['sub-aux'] = {
                'text': ' '.join([t.text for t in aux_tokens]),
                'tokens': [t.text for t in aux_tokens]
            }
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': root.text,
            'root_token': root.text,
            'pos': root.pos_,
            'dependency': root.dep_
        }
        
        # sub-o1: 直接目的語
        objects = [child for child in root.children if child.dep_ == "dobj"]
        if objects:
            obj = objects[0]
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in self._collect_subtree(obj)]),
                'root_token': obj.text,
                'dependency': obj.dep_
            }
        
        return subslots
    
    def _extract_phrase_subslots(self, doc):
        """Phrase用サブスロット抽出（V以降のみ）"""
        subslots = {}
        
        # メイン動詞を探す
        main_verb = None
        for token in doc:
            if token.pos_ == "VERB":
                main_verb = token
                break
        
        if main_verb:
            # sub-v: 動詞
            subslots['sub-v'] = {
                'text': main_verb.text,
                'root_token': main_verb.text,
                'pos': main_verb.pos_
            }
            
            # sub-o1: 目的語（もしあれば）
            objects = [child for child in main_verb.children if child.dep_ == "dobj"]
            if objects:
                obj = objects[0]
                subslots['sub-o1'] = {
                    'text': ' '.join([t.text for t in self._collect_subtree(obj)]),
                    'root_token': obj.text
                }
        
        return subslots
    
    def _collect_subtree(self, token):
        """トークンとその子を収集"""
        subtree = []
        def collect_children(t):
            subtree.append(t)
            for child in sorted(t.children, key=lambda x: x.i):
                collect_children(child)
        collect_children(token)
        return sorted(subtree, key=lambda x: x.i)

def test_accurate_generator():
    """正確なSubslot Generatorテスト"""
    generator = AccurateSubslotGenerator()
    
    test_cases = [
        # Word cases
        "A new project",
        "The experienced manager",
        
        # Phrase cases  
        "to play tennis",
        "playing tennis efficiently",
        
        # Clause cases
        "The manager works",
        "The manager had completed the project",
        "A new project was completed yesterday"
    ]
    
    print("=== 正確なSubslot Generator テスト ===")
    for text in test_cases:
        result = generator.generate_subslots(text)
        print(f"\n'{text}' → {result['type']}")
        
        if result['subslots'] is None:
            print(f"  {result['message']}")
        elif result['subslots']:
            for slot_name, slot_data in result['subslots'].items():
                print(f"  {slot_name}: '{slot_data['text']}'")
        else:
            print("  サブスロット: なし")

if __name__ == "__main__":
    test_accurate_generator()
