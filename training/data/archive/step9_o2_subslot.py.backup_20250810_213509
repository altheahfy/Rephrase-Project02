#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 9: O2サブスロットタイプの実装
===============================
第4文型（SVOO）での間接目的語のサブスロット分解
"""

import spacy

class O2SubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_o2_subslots(self, slot_phrase, phrase_type):
        """
        O2（間接目的語）スロットのサブスロット生成
        
        例: "the student who studies hard" → sub-s, sub-v, sub-m1
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'slot_type': 'O2',
            'subslots': {},
            'word_coverage_check': {}
        }
        
        if phrase_type == "word":
            result['message'] = "wordタイプ：サブスロット分解不要"
            return result
        
        # O2スロットの複雑構造を分解
        if phrase_type in ["phrase", "clause"]:
            result['subslots'] = self._extract_o2_subslots(slot_phrase, phrase_type)
            result['word_coverage_check'] = self._check_complete_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_o2_subslots(self, text, phrase_type):
        """O2スロット内の構造分解"""
        doc = self.nlp(text)
        subslots = {}
        
        if phrase_type == "clause":
            # Clause: 関係節等の複雑構造
            subslots = self._extract_o2_clause_subslots(doc)
        elif phrase_type == "phrase":
            # Phrase: 動詞句等
            subslots = self._extract_o2_phrase_subslots(doc)
        
        return subslots
    
    def _extract_o2_clause_subslots(self, doc):
        """O2 Clauseサブスロット抽出"""
        subslots = {}
        tokens = list(doc)
        
        # 関係節動詞を特定
        relcl_verb = None
        for token in doc:
            if token.dep_ == "relcl":
                relcl_verb = token
                break
        
        if not relcl_verb:
            return subslots
        
        # 関係節の主語名詞（head noun）を取得
        head_noun = relcl_verb.head
        
        # 関係代名詞の役割を判定
        rel_pronoun = None
        rel_pronoun_role = None
        for child in relcl_verb.children:
            if child.pos_ in ["PRON"] and child.text.lower() in ["who", "that", "which"]:
                rel_pronoun = child
                rel_pronoun_role = child.dep_  # nsubj, dobj等
                break
        
        if rel_pronoun and head_noun:
            # 主語名詞句の範囲を特定
            noun_phrase_start = head_noun.i
            for child in head_noun.children:
                if child.dep_ == "det" and child.i < head_noun.i:
                    noun_phrase_start = child.i
            
            base_noun_phrase = tokens[noun_phrase_start:head_noun.i+1]
            
            if rel_pronoun_role == "nsubj":
                # 関係代名詞が主語の場合: "the person who" → sub-s
                sub_s_tokens = base_noun_phrase + [rel_pronoun]
                sub_s_tokens = sorted(sub_s_tokens, key=lambda x: x.i)
                
                subslots['sub-s'] = {
                    'text': ' '.join([t.text for t in sub_s_tokens]),
                    'tokens': [t.text for t in sub_s_tokens],
                    'token_indices': [t.i for t in sub_s_tokens]
                }
                
            elif rel_pronoun_role == "dobj":
                # 関係代名詞が目的語の場合: "the person that" → sub-o1
                obj_tokens = base_noun_phrase + [rel_pronoun]
                obj_tokens = sorted(obj_tokens, key=lambda x: x.i)
                
                subslots['sub-o1'] = {
                    'text': ' '.join([t.text for t in obj_tokens]),
                    'tokens': [t.text for t in obj_tokens],
                    'token_indices': [t.i for t in obj_tokens]
                }
                
                # 関係節内の独立した主語を sub-s として処理
                inner_subjects = [child for child in relcl_verb.children if child.dep_ == "nsubj"]
                if inner_subjects:
                    inner_subj = inner_subjects[0]
                    subslots['sub-s'] = {
                        'text': inner_subj.text,
                        'tokens': [inner_subj.text],
                        'token_indices': [inner_subj.i]
                    }
        
        # sub-aux: 助動詞
        aux_tokens = [child for child in relcl_verb.children if child.dep_ in ["aux", "auxpass"]]
        if aux_tokens:
            subslots['sub-aux'] = {
                'text': ' '.join([t.text for t in aux_tokens]),
                'tokens': [t.text for t in aux_tokens],
                'token_indices': [t.i for t in aux_tokens]
            }
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': relcl_verb.text,
            'tokens': [relcl_verb.text],
            'token_indices': [relcl_verb.i]
        }
        
        # sub-o1: 直接目的語（不定詞句も含める）
        # 関係代名詞が目的語でない場合のみ処理
        if not (rel_pronoun and rel_pronoun_role == "dobj"):
            obj_tokens = []
            for child in relcl_verb.children:
                if child.dep_ in ["dobj", "xcomp"]:  # xcomp: 不定詞補語
                    obj_subtree = list(child.subtree)
                    obj_tokens.extend(obj_subtree)
            
            if obj_tokens:
                obj_tokens = sorted(obj_tokens, key=lambda x: x.i)
                subslots['sub-o1'] = {
                    'text': ' '.join([t.text for t in obj_tokens]),
                    'tokens': [t.text for t in obj_tokens],
                    'token_indices': [t.i for t in obj_tokens]
                }
        
        # sub-m1: 修飾語
        mod_tokens = [child for child in relcl_verb.children if child.dep_ in ["advmod", "npadvmod"]]
        if mod_tokens:
            subslots['sub-m1'] = {
                'text': ' '.join([t.text for t in mod_tokens]),
                'tokens': [t.text for t in mod_tokens],
                'token_indices': [t.i for t in mod_tokens]
            }
        
        return subslots
    
    def _extract_o2_phrase_subslots(self, doc):
        """O2 Phraseサブスロット抽出"""
        subslots = {}
        
        # メイン動詞を特定
        main_verb = None
        for token in doc:
            if token.pos_ == "VERB":
                main_verb = token
                break
        
        if not main_verb:
            return subslots
        
        # sub-v: 動詞
        subslots['sub-v'] = {
            'text': main_verb.text,
            'tokens': [main_verb.text],
            'token_indices': [main_verb.i]
        }
        
        # sub-o1: 目的語
        obj_tokens = []
        for child in main_verb.children:
            if child.dep_ == "dobj":
                obj_subtree = list(child.subtree)
                obj_tokens.extend(obj_subtree)
        
        if obj_tokens:
            obj_tokens = sorted(obj_tokens, key=lambda x: x.i)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in obj_tokens]),
                'tokens': [t.text for t in obj_tokens],
                'token_indices': [t.i for t in obj_tokens]
            }
        
        # sub-m1: 修飾語
        mod_tokens = [child for child in main_verb.children if child.dep_ in ["advmod"]]
        if mod_tokens:
            subslots['sub-m1'] = {
                'text': mod_tokens[0].text,
                'tokens': [mod_tokens[0].text],
                'token_indices': [mod_tokens[0].i]
            }
        
        return subslots
    
    def _check_complete_coverage(self, original_text, subslots):
        """全単語カバレッジ検証"""
        doc = self.nlp(original_text)
        all_tokens = [(token.text, token.i) for token in doc]
        
        covered_indices = set()
        for subslot_data in subslots.values():
            if 'token_indices' in subslot_data:
                covered_indices.update(subslot_data['token_indices'])
        
        missing_tokens = [(text, idx) for text, idx in all_tokens if idx not in covered_indices]
        
        return {
            'total_tokens': len(all_tokens),
            'covered_tokens': len(covered_indices),
            'missing_tokens': missing_tokens,
            'coverage_rate': len(covered_indices) / len(all_tokens) if all_tokens else 0,
            'is_complete': len(missing_tokens) == 0
        }

def test_o2_subslot_generator():
    """O2サブスロット生成テスト"""
    generator = O2SubslotGenerator()
    
    # 第4文型（SVOO）でのO2の例
    test_cases = [
        # Word examples (サブスロット不要)
        ("him", "word"),
        ("her", "word"),
        ("the student", "word"),
        
        # Phrase examples
        ("everyone in the class", "phrase"),
        
        # Clause examples
        ("the student who studies hard", "clause"),
        ("anyone who wants to learn", "clause"),
        ("the person that I met yesterday", "clause")
    ]
    
    print("=== O2サブスロット生成テスト ===")
    
    for slot_phrase, phrase_type in test_cases:
        print(f"\n{'='*50}")
        print(f"O2 SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type}")
        print(f"{'='*50}")
        
        result = generator.generate_o2_subslots(slot_phrase, phrase_type)
        
        if 'message' in result:
            print(f"判定: {result['message']}")
        elif result['subslots']:
            print(f"サブスロット生成: {len(result['subslots'])}個")
            for subslot_id, subslot_data in result['subslots'].items():
                print(f"  {subslot_id}: '{subslot_data['text']}'")
            
            # カバレッジ検証
            if 'word_coverage_check' in result:
                coverage = result['word_coverage_check']
                print(f"\nカバレッジ: {coverage['coverage_rate']:.1%} ({coverage['covered_tokens']}/{coverage['total_tokens']})")
                if not coverage['is_complete']:
                    print(f"⚠️ 未配置: {coverage['missing_tokens']}")
                else:
                    print("✅ 完全カバレッジ")
        else:
            print("サブスロット生成なし")

if __name__ == "__main__":
    test_o2_subslot_generator()
