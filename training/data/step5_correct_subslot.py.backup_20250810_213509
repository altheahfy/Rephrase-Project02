#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 5: 正しいSubslot Generator - 5文型フルセット準拠版
====================================================
上位スロット内のPhraseType（word/phrase/clause）に応じたsubslot生成
"""

import spacy
import json

class CorrectSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_subslots_for_slot_phrase(self, slot_phrase, phrase_type):
        """
        上位スロット内のSlotPhraseに対してサブスロット生成
        
        Args:
            slot_phrase (str): スロット内の語句 (例: "the manager who works here")
            phrase_type (str): "word", "phrase", "clause"のいずれか
            
        Returns:
            dict: サブスロット情報
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'subslots': {},
            'needs_subslots': False
        }
        
        if phrase_type == "word":
            # Word: サブスロット不使用
            result['message'] = "wordタイプ：サブスロット分解不要"
            return result
        
        elif phrase_type == "phrase":
            # Phrase: V以降のみサブスロット化
            result['needs_subslots'] = True
            result['subslots'] = self._extract_phrase_subslots(slot_phrase)
            
        elif phrase_type == "clause":
            # Clause: 完全サブスロット化
            result['needs_subslots'] = True
            result['subslots'] = self._extract_clause_subslots(slot_phrase)
        
        return result
    
    def _extract_clause_subslots(self, text):
        """Clause用：完全サブスロット抽出（sub-s, sub-v, sub-o1等）"""
        doc = self.nlp(text)
        subslots = {}
        
        # 動詞を見つける（ROOT動詞か関係節動詞）
        main_verb = None
        
        # まずROOT動詞を探す
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                main_verb = token
                break
        
        # ROOT動詞がない場合は関係節動詞を探す
        if not main_verb:
            for token in doc:
                if token.dep_ == "relcl" and token.pos_ in ["VERB", "AUX"]:
                    main_verb = token
                    break
        
        if not main_verb:
            return subslots
        
        # sub-s: 主語
        subjects = [child for child in main_verb.children if child.dep_ in ["nsubj", "nsubjpass"]]
        if subjects:
            subject = subjects[0]
            sub_s_tokens = self._collect_subtree(subject)
            subslots['sub-s'] = {
                'text': ' '.join([t.text for t in sub_s_tokens]),
                'root_token': subject.text,
                'dependency': subject.dep_,
                'tokens': [t.text for t in sub_s_tokens]
            }
        
        # sub-aux: 助動詞
        aux_tokens = [child for child in main_verb.children if child.dep_ in ["aux", "auxpass"]]
        if aux_tokens:
            subslots['sub-aux'] = {
                'text': ' '.join([t.text for t in aux_tokens]),
                'tokens': [t.text for t in aux_tokens],
                'dependencies': [t.dep_ for t in aux_tokens]
            }
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': main_verb.text,
            'root_token': main_verb.text,
            'pos': main_verb.pos_,
            'tag': main_verb.tag_,
            'dependency': main_verb.dep_
        }
        
        # sub-o1: 直接目的語
        objects = [child for child in main_verb.children if child.dep_ == "dobj"]
        if objects:
            obj = objects[0]
            obj_tokens = self._collect_subtree(obj)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in obj_tokens]),
                'root_token': obj.text,
                'dependency': obj.dep_,
                'tokens': [t.text for t in obj_tokens]
            }
        
        # sub-c1: 補語
        complements = [child for child in main_verb.children if child.dep_ in ["attr", "acomp"]]
        if complements:
            comp = complements[0]
            comp_tokens = self._collect_subtree(comp)
            subslots['sub-c1'] = {
                'text': ' '.join([t.text for t in comp_tokens]),
                'root_token': comp.text,
                'dependency': comp.dep_,
                'tokens': [t.text for t in comp_tokens]
            }
        
        # sub-m1, sub-m2, sub-m3: 修飾語
        modifiers = [child for child in main_verb.children if child.dep_ in ["advmod", "prep", "npadvmod"]]
        for i, mod in enumerate(modifiers[:3], 1):  # 最大3つまで
            mod_tokens = self._collect_subtree(mod)
            subslots[f'sub-m{i}'] = {
                'text': ' '.join([t.text for t in mod_tokens]),
                'root_token': mod.text,
                'dependency': mod.dep_,
                'tokens': [t.text for t in mod_tokens]
            }
        
        return subslots
    
    def _extract_phrase_subslots(self, text):
        """Phrase用：V以降のみサブスロット抽出"""
        doc = self.nlp(text)
        subslots = {}
        
        # メイン動詞を探す
        main_verbs = [token for token in doc if token.pos_ == "VERB"]
        if not main_verbs:
            return subslots
        
        main_verb = main_verbs[0]
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': main_verb.text,
            'root_token': main_verb.text,
            'pos': main_verb.pos_,
            'tag': main_verb.tag_
        }
        
        # sub-o1: 目的語（もしあれば）
        objects = [child for child in main_verb.children if child.dep_ == "dobj"]
        if objects:
            obj = objects[0]
            obj_tokens = self._collect_subtree(obj)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in obj_tokens]),
                'root_token': obj.text,
                'tokens': [t.text for t in obj_tokens]
            }
        
        # sub-m1: 修飾語
        modifiers = [child for child in main_verb.children if child.dep_ in ["advmod", "prep"]]
        if modifiers:
            mod = modifiers[0]
            mod_tokens = self._collect_subtree(mod)
            subslots['sub-m1'] = {
                'text': ' '.join([t.text for t in mod_tokens]),
                'root_token': mod.text,
                'tokens': [t.text for t in mod_tokens]
            }
        
        return subslots
    
    def _collect_subtree(self, token):
        """トークンとその子を語順通りに収集"""
        subtree = []
        
        def collect_children(t):
            subtree.append(t)
            for child in sorted(t.children, key=lambda x: x.i):
                collect_children(child)
        
        collect_children(token)
        return sorted(subtree, key=lambda x: x.i)

def test_with_actual_examples():
    """5文型フルセットの実例でテスト"""
    generator = CorrectSubslotGenerator()
    
    test_cases = [
        # Word examples
        ("he", "word"),
        ("gave", "word"), 
        ("yesterday", "word"),
        ("a message", "word"),
        
        # Phrase example
        ("deliver the final proposal flawlessly", "phrase"),
        
        # Clause example  
        ("the manager who had recently taken charge of the project", "clause")
    ]
    
    print("=== 5文型フルセット準拠 Subslot Generator テスト ===")
    for slot_phrase, phrase_type in test_cases:
        print(f"\n--- SlotPhrase: '{slot_phrase}' (PhraseType: {phrase_type}) ---")
        
        result = generator.generate_subslots_for_slot_phrase(slot_phrase, phrase_type)
        
        if not result['needs_subslots']:
            print(f"  {result.get('message', 'サブスロット不要')}")
        else:
            print(f"  サブスロット生成: {len(result['subslots'])}個")
            for subslot_id, subslot_data in result['subslots'].items():
                print(f"    {subslot_id}: '{subslot_data['text']}'")

if __name__ == "__main__":
    test_with_actual_examples()
