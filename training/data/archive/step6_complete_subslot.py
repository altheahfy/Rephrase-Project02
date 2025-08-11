#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 6: 全単語保全Subslot Generator
================================
例文の100%の単語をスロットに配置する
"""

import spacy

class CompleteSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_subslots_for_slot_phrase(self, slot_phrase, phrase_type):
        """
        全単語保全を保証するサブスロット生成
        
        Args:
            slot_phrase (str): スロット内の語句
            phrase_type (str): "word", "phrase", "clause"
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'subslots': {},
            'needs_subslots': False,
            'word_coverage': []  # 各単語がどのサブスロットに入ったか追跡
        }
        
        if phrase_type == "word":
            result['message'] = "wordタイプ：サブスロット分解不要"
            # 全単語を"未分解"として記録
            result['word_coverage'] = [{'word': word, 'assigned_to': 'main_slot'} 
                                     for word in slot_phrase.split()]
            return result
        
        elif phrase_type == "phrase":
            result['needs_subslots'] = True
            result['subslots'] = self._extract_phrase_subslots_complete(slot_phrase)
            
        elif phrase_type == "clause":
            result['needs_subslots'] = True
            result['subslots'] = self._extract_clause_subslots_complete(slot_phrase)
        
        # 単語カバレッジの検証
        result['word_coverage'] = self._verify_word_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_clause_subslots_complete(self, text):
        """Clause用：全単語保全サブスロット抽出"""
        doc = self.nlp(text)
        subslots = {}
        
        # 関係節動詞を見つける
        relcl_verb = None
        for token in doc:
            if token.dep_ == "relcl" and token.pos_ in ["VERB", "AUX"]:
                relcl_verb = token
                break
        
        if not relcl_verb:
            return subslots
        
        # sub-s: 主語（関係代名詞より前の名詞句 + 関係代名詞）
        # "the manager who" のように関係代名詞まで含める
        subject_tokens = []
        
        # 関係代名詞を探す
        rel_pronoun = None
        for child in relcl_verb.children:
            if child.dep_ == "nsubj" and child.pos_ == "PRON":  # who, that, which
                rel_pronoun = child
                break
        
        if rel_pronoun:
            # 関係代名詞の前にある名詞句（主語部分）を含める
            head_noun = relcl_verb.head  # "manager"
            if head_noun:
                # 名詞句全体を収集（"the manager"）
                noun_phrase_tokens = self._collect_subtree(head_noun)
                # 関係代名詞も追加
                subject_tokens = noun_phrase_tokens + [rel_pronoun]
                
                subslots['sub-s'] = {
                    'text': ' '.join([t.text for t in subject_tokens]),
                    'tokens': [t.text for t in subject_tokens],
                    'composition': f"noun_phrase + relative_pronoun"
                }
        
        # sub-aux: 助動詞
        aux_tokens = [child for child in relcl_verb.children if child.dep_ in ["aux", "auxpass"]]
        if aux_tokens:
            subslots['sub-aux'] = {
                'text': ' '.join([t.text for t in aux_tokens]),
                'tokens': [t.text for t in aux_tokens]
            }
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': relcl_verb.text,
            'tokens': [relcl_verb.text],
            'root_token': relcl_verb.text
        }
        
        # sub-o1: 直接目的語（前置詞句も含める）
        objects = [child for child in relcl_verb.children if child.dep_ == "dobj"]
        if objects:
            obj = objects[0]
            obj_tokens = self._collect_subtree(obj)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in obj_tokens]),
                'tokens': [t.text for t in obj_tokens],
                'root_token': obj.text
            }
        
        # sub-m1: 修飾語
        modifiers = [child for child in relcl_verb.children if child.dep_ in ["advmod"]]
        if modifiers:
            mod = modifiers[0]
            subslots['sub-m1'] = {
                'text': mod.text,
                'tokens': [mod.text],
                'root_token': mod.text
            }
        
        return subslots
    
    def _extract_phrase_subslots_complete(self, text):
        """Phrase用：全単語保全サブスロット抽出"""
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
            'tokens': [main_verb.text]
        }
        
        # sub-o1: 目的語（完全な名詞句）
        objects = [child for child in main_verb.children if child.dep_ == "dobj"]
        if objects:
            obj = objects[0]
            obj_tokens = self._collect_subtree(obj)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in obj_tokens]),
                'tokens': [t.text for t in obj_tokens]
            }
        
        # sub-m1: 修飾語
        modifiers = [child for child in main_verb.children if child.dep_ in ["advmod"]]
        if modifiers:
            mod = modifiers[0]
            subslots['sub-m1'] = {
                'text': mod.text,
                'tokens': [mod.text]
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
    
    def _verify_word_coverage(self, original_text, subslots):
        """全単語がサブスロットに配置されているか検証"""
        original_words = original_text.split()
        covered_words = []
        
        for subslot_id, subslot_data in subslots.items():
            if 'tokens' in subslot_data:
                for token in subslot_data['tokens']:
                    covered_words.append({'word': token, 'assigned_to': subslot_id})
        
        # カバレッジ分析
        coverage = []
        for word in original_words:
            found = False
            for covered in covered_words:
                if covered['word'].lower() == word.lower():
                    coverage.append(covered)
                    found = True
                    break
            if not found:
                coverage.append({'word': word, 'assigned_to': 'MISSING'})
        
        return coverage

def test_complete_coverage():
    """完全カバレッジテスト"""
    generator = CompleteSubslotGenerator()
    
    test_cases = [
        # 問題のあった例
        ("the manager who had recently taken charge of the project", "clause"),
        ("a pencil that I bought yesterday", "clause"),
        ("deliver the final proposal flawlessly", "phrase")
    ]
    
    print("=== 全単語保全 Subslot Generator テスト ===")
    for slot_phrase, phrase_type in test_cases:
        print(f"\n--- SlotPhrase: '{slot_phrase}' (PhraseType: {phrase_type}) ---")
        
        result = generator.generate_subslots_for_slot_phrase(slot_phrase, phrase_type)
        
        if result['subslots']:
            print(f"サブスロット生成: {len(result['subslots'])}個")
            for subslot_id, subslot_data in result['subslots'].items():
                print(f"  {subslot_id}: '{subslot_data['text']}'")
        
        # カバレッジ検証
        print("\n【単語カバレッジ検証】")
        missing_words = []
        for coverage in result['word_coverage']:
            if coverage['assigned_to'] == 'MISSING':
                missing_words.append(coverage['word'])
            print(f"  '{coverage['word']}' → {coverage['assigned_to']}")
        
        if missing_words:
            print(f"⚠️ 未配置単語: {missing_words}")
        else:
            print("✅ 全単語配置済み")

if __name__ == "__main__":
    test_complete_coverage()
