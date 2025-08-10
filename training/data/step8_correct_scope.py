#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 8: 正しいサブスロットスコープ版
===================================
aux, vはサブスロット不要。複雑構造を持つ要素のみサブスロット化
"""

import spacy

class CorrectScopeSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_subslots_for_slot_phrase(self, slot_phrase, phrase_type, slot_type=None):
        """
        スロットタイプに応じた適切なサブスロット生成
        
        Args:
            slot_phrase (str): スロット内の語句
            phrase_type (str): "word", "phrase", "clause"
            slot_type (str): "S", "Aux", "V", "O1", "O2", "C1", "C2", "M1", "M2", "M3"
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'slot_type': slot_type,
            'subslots': {},
            'needs_subslots': False,
            'reasoning': ''
        }
        
        # wordタイプは常にサブスロット不要
        if phrase_type == "word":
            result['reasoning'] = "wordタイプ：サブスロット分解不要"
            return result
        
        # スロットタイプによる判定
        if slot_type in ["Aux", "V"]:
            result['reasoning'] = f"{slot_type}スロット：構造的に単純なためサブスロット不要"
            return result
        
        # 複雑構造を持つスロットのみサブスロット化
        if slot_type in ["S", "O1", "O2", "C1", "C2", "M1", "M2", "M3"]:
            result['needs_subslots'] = True
            result['reasoning'] = f"{slot_type}スロット：複雑構造の可能性ありサブスロット生成"
            
            if phrase_type == "phrase":
                result['subslots'] = self._extract_phrase_subslots(slot_phrase, slot_type)
            elif phrase_type == "clause":
                result['subslots'] = self._extract_clause_subslots(slot_phrase, slot_type)
        
        # 全単語カバレッジ検証
        if result['needs_subslots']:
            result['word_coverage_check'] = self._check_complete_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_clause_subslots(self, text, slot_type):
        """Clause: スロットタイプ別サブスロット抽出"""
        doc = self.nlp(text)
        subslots = {}
        
        if slot_type == "S":
            # 主語スロットの場合：関係節等の複雑構造を分解
            subslots = self._extract_subject_clause_subslots(doc)
        elif slot_type in ["O1", "O2"]:
            # 目的語スロットの場合：名詞句内の複雑構造を分解
            subslots = self._extract_object_clause_subslots(doc)
        elif slot_type in ["C1", "C2"]:
            # 補語スロットの場合：補語句内の複雑構造を分解
            subslots = self._extract_complement_clause_subslots(doc)
        elif slot_type in ["M1", "M2", "M3"]:
            # 修飾語スロットの場合：修飾句内の複雑構造を分解
            subslots = self._extract_modifier_clause_subslots(doc)
        
        return subslots
    
    def _extract_subject_clause_subslots(self, doc):
        """主語スロット内のClause構造分解"""
        subslots = {}
        
        # 関係節動詞を特定
        relcl_verb = None
        for token in doc:
            if token.dep_ == "relcl":
                relcl_verb = token
                break
        
        if not relcl_verb:
            return subslots
        
        tokens = list(doc)
        
        # sub-s: 主語部分（関係代名詞より前 + 関係代名詞）
        head_noun = relcl_verb.head
        if head_noun:
            # 主語名詞句の範囲を特定
            noun_phrase_start = head_noun.i
            for child in head_noun.children:
                if child.dep_ == "det" and child.i < head_noun.i:
                    noun_phrase_start = child.i
            
            # 関係代名詞を探す
            rel_pronoun = None
            for child in relcl_verb.children:
                if child.dep_ in ["nsubj", "dobj"] and child.pos_ in ["PRON"]:
                    rel_pronoun = child
                    break
            
            if rel_pronoun:
                sub_s_tokens = tokens[noun_phrase_start:head_noun.i+1] + [rel_pronoun]
                sub_s_tokens = sorted(sub_s_tokens, key=lambda x: x.i)
                
                subslots['sub-s'] = {
                    'text': ' '.join([t.text for t in sub_s_tokens]),
                    'tokens': [t.text for t in sub_s_tokens],
                    'token_indices': [t.i for t in sub_s_tokens]
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
        
        # sub-o1: 目的語
        obj_tokens = []
        for child in relcl_verb.children:
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
        mod_tokens = [child for child in relcl_verb.children if child.dep_ in ["advmod", "npadvmod"]]
        if mod_tokens:
            subslots['sub-m1'] = {
                'text': ' '.join([t.text for t in mod_tokens]),
                'tokens': [t.text for t in mod_tokens],
                'token_indices': [t.i for t in mod_tokens]
            }
        
        # 関係節内の独立した主語処理
        inner_subjects = [child for child in relcl_verb.children 
                         if child.dep_ == "nsubj" and child.pos_ in ["PRON"] and child.text != "who"]
        if inner_subjects:
            existing_sub_s_tokens = subslots.get('sub-s', {}).get('tokens', [])
            inner_subj = inner_subjects[0]
            
            if inner_subj.text not in existing_sub_s_tokens:
                subslots['sub-s2'] = {
                    'text': inner_subj.text,
                    'tokens': [inner_subj.text],
                    'token_indices': [inner_subj.i]
                }
        
        return subslots
    
    def _extract_object_clause_subslots(self, doc):
        """目的語スロット内のClause構造分解"""
        # 目的語内の関係節等を処理
        return self._extract_subject_clause_subslots(doc)  # 同じロジックを再利用
    
    def _extract_complement_clause_subslots(self, doc):
        """補語スロット内のClause構造分解"""
        subslots = {}
        # 補語内の複雑構造を処理（実装省略、必要に応じて拡張）
        return subslots
    
    def _extract_modifier_clause_subslots(self, doc):
        """修飾語スロット内のClause構造分解"""
        subslots = {}
        # 修飾語内の複雑構造を処理（実装省略、必要に応じて拡張）
        return subslots
    
    def _extract_phrase_subslots(self, text, slot_type):
        """Phrase: スロットタイプ別サブスロット抽出"""
        doc = self.nlp(text)
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

def test_correct_scope_generator():
    """正しいサブスロットスコープのテスト"""
    generator = CorrectScopeSubslotGenerator()
    
    test_cases = [
        # 助動詞・動詞スロット（サブスロット不要）
        ("had", "word", "Aux"),
        ("worked", "word", "V"),
        ("has been working", "phrase", "V"),  # 複合動詞でもVスロット内なら不要
        
        # 主語スロット（サブスロット必要）
        ("the manager who had recently taken charge of the project", "clause", "S"),
        
        # 目的語スロット（サブスロット必要）
        ("a pencil that I bought yesterday", "clause", "O1"),
        
        # 修飾語スロット
        ("deliver the final proposal flawlessly", "phrase", "M1")
    ]
    
    print("=== 正しいサブスロットスコープ テスト ===")
    
    for slot_phrase, phrase_type, slot_type in test_cases:
        print(f"\n{'='*60}")
        print(f"SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type} | SlotType: {slot_type}")
        print(f"{'='*60}")
        
        result = generator.generate_subslots_for_slot_phrase(slot_phrase, phrase_type, slot_type)
        
        print(f"判定: {result['reasoning']}")
        
        if result['needs_subslots'] and result['subslots']:
            print(f"\n【生成されたサブスロット】({len(result['subslots'])}個)")
            for subslot_id, subslot_data in result['subslots'].items():
                print(f"  {subslot_id}: '{subslot_data['text']}'")
            
            if 'word_coverage_check' in result:
                coverage = result['word_coverage_check']
                print(f"\n【カバレッジ】{coverage['coverage_rate']:.1%} ({coverage['covered_tokens']}/{coverage['total_tokens']})")
                if not coverage['is_complete']:
                    print(f"  ⚠️ 未配置: {coverage['missing_tokens']}")
                else:
                    print(f"  ✅ 完全カバレッジ")
        else:
            print("サブスロット生成なし")

if __name__ == "__main__":
    test_correct_scope_generator()
