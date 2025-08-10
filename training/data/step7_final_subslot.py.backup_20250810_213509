#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 7: 完全単語保全Subslot Generator - 構造解析版
=============================================
全単語を適切なサブスロットに配置する
"""

import spacy

class FinalSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_subslots_for_slot_phrase(self, slot_phrase, phrase_type):
        """完全な単語保全を保証するサブスロット生成"""
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'subslots': {},
            'needs_subslots': False,
            'word_coverage_check': {}
        }
        
        if phrase_type == "word":
            result['message'] = "wordタイプ：サブスロット分解不要"
            return result
        
        elif phrase_type == "phrase":
            result['needs_subslots'] = True
            result['subslots'] = self._extract_phrase_subslots_complete(slot_phrase)
            
        elif phrase_type == "clause":
            result['needs_subslots'] = True
            result['subslots'] = self._extract_clause_subslots_complete(slot_phrase)
        
        # 全単語カバレッジ検証
        result['word_coverage_check'] = self._check_complete_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_clause_subslots_complete(self, text):
        """Clause: 全単語を適切なサブスロットに配置"""
        doc = self.nlp(text)
        subslots = {}
        
        # 関係節動詞を特定
        relcl_verb = None
        for token in doc:
            if token.dep_ == "relcl":
                relcl_verb = token
                break
        
        if not relcl_verb:
            return subslots
        
        # Token indexベースで範囲を特定
        tokens = list(doc)
        
        # sub-s: 関係代名詞の主語 + 関係代名詞
        # パターン1: "the manager who" (主語名詞句 + 関係代名詞)
        head_noun = relcl_verb.head
        if head_noun:
            # 主語名詞句の範囲を特定
            noun_phrase_start = None
            noun_phrase_end = head_noun.i
            
            # 冠詞や修飾語を含める
            for child in head_noun.children:
                if child.dep_ == "det" and child.i < head_noun.i:
                    noun_phrase_start = child.i
            
            if noun_phrase_start is None:
                noun_phrase_start = head_noun.i
            
            # 関係代名詞を探す
            rel_pronoun = None
            for child in relcl_verb.children:
                if child.dep_ in ["nsubj", "dobj"] and child.pos_ in ["PRON"]:  # who, that, which
                    rel_pronoun = child
                    break
            
            if rel_pronoun:
                # "the manager who" または "a pencil that"
                sub_s_tokens = tokens[noun_phrase_start:noun_phrase_end+1] + [rel_pronoun]
                sub_s_tokens = sorted(sub_s_tokens, key=lambda x: x.i)  # インデックス順
                
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
        
        # sub-o1: 目的語（前置詞句含む）
        obj_tokens = []
        for child in relcl_verb.children:
            if child.dep_ == "dobj":
                obj_subtree = list(child.subtree)  # 前置詞句も含む
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
        
        # パターン2処理: "a pencil that I bought" の "I" 処理
        # 関係節内に独立した主語がある場合の追加処理
        inner_subjects = [child for child in relcl_verb.children 
                         if child.dep_ == "nsubj" and child.pos_ in ["PRON"] and child.text != "who"]
        if inner_subjects:
            # 既存のsub-sのトークンリストを取得
            existing_sub_s_tokens = subslots.get('sub-s', {}).get('tokens', [])
            inner_subj = inner_subjects[0]
            
            if inner_subj.text not in existing_sub_s_tokens:
                # 関係節内の主語を sub-s2 として作成
                subslots['sub-s2'] = {
                    'text': inner_subj.text,
                    'tokens': [inner_subj.text],
                    'token_indices': [inner_subj.i]
                }
        
        # sub-o1の重複チェック：関係代名詞が目的語として重複している場合の修正
        if 'sub-o1' in subslots and 'sub-s' in subslots:
            # sub-sに含まれるトークンをsub-o1から除外
            sub_s_indices = set(subslots['sub-s']['token_indices'])
            if 'token_indices' in subslots['sub-o1']:
                original_o1_indices = subslots['sub-o1']['token_indices']
                filtered_o1_indices = [idx for idx in original_o1_indices if idx not in sub_s_indices]
                
                if len(filtered_o1_indices) != len(original_o1_indices):
                    # 重複があった場合、フィルタリングされたトークンで再構築
                    if filtered_o1_indices:
                        filtered_tokens = [tokens[idx] for idx in filtered_o1_indices]
                        subslots['sub-o1'] = {
                            'text': ' '.join([t.text for t in filtered_tokens]),
                            'tokens': [t.text for t in filtered_tokens],
                            'token_indices': filtered_o1_indices
                        }
                    else:
                        # sub-o1が空になった場合は削除
                        del subslots['sub-o1']
        
        return subslots
    
    def _extract_phrase_subslots_complete(self, text):
        """Phrase: 全単語を適切なサブスロットに配置"""
        doc = self.nlp(text)
        subslots = {}
        
        tokens = list(doc)
        
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
        """全単語がサブスロットに配置されているか詳細検証"""
        doc = self.nlp(original_text)
        all_tokens = [(token.text, token.i) for token in doc]
        
        covered_indices = set()
        coverage_details = {}
        
        # 各サブスロットがカバーするトークンインデックスを収集
        for subslot_id, subslot_data in subslots.items():
            if 'token_indices' in subslot_data:
                for idx in subslot_data['token_indices']:
                    covered_indices.add(idx)
                    coverage_details[idx] = subslot_id
        
        # 未カバーのトークンを特定
        missing_tokens = []
        for token_text, token_idx in all_tokens:
            if token_idx not in covered_indices:
                missing_tokens.append((token_text, token_idx))
        
        return {
            'total_tokens': len(all_tokens),
            'covered_tokens': len(covered_indices),
            'missing_tokens': missing_tokens,
            'coverage_rate': len(covered_indices) / len(all_tokens) if all_tokens else 0,
            'is_complete': len(missing_tokens) == 0,
            'token_assignment': coverage_details
        }

def test_final_complete_generator():
    """最終版完全カバレッジテスト"""
    generator = FinalSubslotGenerator()
    
    test_cases = [
        ("the manager who had recently taken charge of the project", "clause"),
        ("a pencil that I bought yesterday", "clause"),
        ("deliver the final proposal flawlessly", "phrase")
    ]
    
    print("=== 最終版：完全単語保全 Subslot Generator ===")
    
    for slot_phrase, phrase_type in test_cases:
        print(f"\n{'='*60}")
        print(f"SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type}")
        print(f"{'='*60}")
        
        result = generator.generate_subslots_for_slot_phrase(slot_phrase, phrase_type)
        
        if result['subslots']:
            print(f"\n【生成されたサブスロット】")
            for subslot_id, subslot_data in result['subslots'].items():
                print(f"  {subslot_id}: '{subslot_data['text']}'")
                if 'token_indices' in subslot_data:
                    print(f"    └─ indices: {subslot_data['token_indices']}")
        
        # カバレッジ結果
        coverage = result['word_coverage_check']
        print(f"\n【単語カバレッジ検証】")
        print(f"  総トークン数: {coverage['total_tokens']}")
        print(f"  カバー済み: {coverage['covered_tokens']}")
        print(f"  カバー率: {coverage['coverage_rate']:.1%}")
        
        if coverage['is_complete']:
            print(f"  ✅ 完全カバレッジ達成")
        else:
            print(f"  ⚠️ 未配置トークン: {coverage['missing_tokens']}")

if __name__ == "__main__":
    test_final_complete_generator()
