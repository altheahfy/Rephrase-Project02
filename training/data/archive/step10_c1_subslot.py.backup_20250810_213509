#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 10: C1サブスロット実装
========================
第2文型（SVC）・第5文型（SVOC）の補語サブスロット分解
"""

import spacy

class C1SubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_c1_subslots(self, slot_phrase, phrase_type):
        """
        C1（補語1）スロットのサブスロット生成
        
        例: "the leader who is very experienced" → sub-s, sub-aux, sub-v, sub-m1
        例: "to be successful in business" → sub-v, sub-c1, sub-m1
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'slot_type': 'C1',
            'subslots': {},
            'word_coverage_check': {}
        }
        
        if phrase_type == "word":
            result['message'] = "wordタイプ：サブスロット分解不要"
            return result
        
        # C1スロットの複雑構造を分解
        if phrase_type in ["phrase", "clause"]:
            result['subslots'] = self._extract_c1_subslots(slot_phrase, phrase_type)
            result['word_coverage_check'] = self._check_complete_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_c1_subslots(self, text, phrase_type):
        """C1スロット内の構造分解"""
        doc = self.nlp(text)
        subslots = {}
        
        if phrase_type == "clause":
            # Clause: 関係節等の複雑構造
            subslots = self._extract_c1_clause_subslots(doc)
        elif phrase_type == "phrase":
            # Phrase: 動詞句等（to be successful等）
            subslots = self._extract_c1_phrase_subslots(doc)
        
        return subslots
    
    def _extract_c1_clause_subslots(self, doc):
        """C1 Clauseサブスロット抽出"""
        subslots = {}
        tokens = list(doc)
        
        # what節の特殊処理
        what_token = None
        for token in doc:
            if token.text.lower() == "what" and token.pos_ == "PRON":
                what_token = token
                break
        
        if what_token:
            # "what I want to become" の特殊処理
            return self._extract_what_clause_subslots(doc, what_token)
        
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
                # 関係代名詞が主語の場合: "the leader who" → sub-s
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
        
        # sub-aux: 助動詞（受動態のbe含む）
        aux_tokens = []
        for child in relcl_verb.children:
            if child.dep_ in ["aux", "auxpass"]:
                aux_tokens.append(child)
        
        # 受動態判定：be + 過去分詞 の場合、beを助動詞として扱う
        if relcl_verb.text.lower() in ["be", "is", "was", "were", "been", "being"] and relcl_verb.pos_ == "AUX":
            aux_tokens.append(relcl_verb)
            # 過去分詞を実質動詞として特定
            participle_verb = None
            for child in relcl_verb.children:
                if child.dep_ in ["acomp"] and child.pos_ in ["VERB", "ADJ"]:  # 過去分詞は形容詞扱いの場合もある
                    participle_verb = child
                    break
            
            if participle_verb:
                # sub-aux: be動詞
                subslots['sub-aux'] = {
                    'text': relcl_verb.text,
                    'tokens': [relcl_verb.text],
                    'token_indices': [relcl_verb.i]
                }
                
                # sub-v: 過去分詞（実質動詞）
                subslots['sub-v'] = {
                    'text': participle_verb.text,
                    'tokens': [participle_verb.text],
                    'token_indices': [participle_verb.i]
                }
                
                # sub-m2: 副詞修飾語（very等）
                adv_tokens = [child for child in participle_verb.children if child.dep_ == "advmod"]
                if adv_tokens:
                    subslots['sub-m2'] = {
                        'text': ' '.join([t.text for t in adv_tokens]),
                        'tokens': [t.text for t in adv_tokens],
                        'token_indices': [t.i for t in adv_tokens]
                    }
                
                return subslots
        
        # 通常の助動詞処理
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
        
        # sub-c1: 補語（形容詞・名詞補語）
        comp_tokens = []
        for child in relcl_verb.children:
            if child.dep_ in ["acomp", "attr"]:  # 形容詞補語・名詞補語
                comp_subtree = list(child.subtree)
                comp_tokens.extend(comp_subtree)
        
        if comp_tokens:
            comp_tokens = sorted(comp_tokens, key=lambda x: x.i)
            subslots['sub-c1'] = {
                'text': ' '.join([t.text for t in comp_tokens]),
                'tokens': [t.text for t in comp_tokens],
                'token_indices': [t.i for t in comp_tokens]
            }
        
        # sub-o1: 直接目的語（関係代名詞が目的語でない場合のみ）
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
    
    def _extract_what_clause_subslots(self, doc, what_token):
        """what節の特殊処理: "what I want to become" """
        subslots = {}
        
        # sub-o2: what (本来はbecomeの目的語だが便宜的にo2)
        subslots['sub-o2'] = {
            'text': what_token.text,
            'tokens': [what_token.text],
            'token_indices': [what_token.i]
        }
        
        # メイン動詞を特定（want）
        main_verb = None
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                main_verb = token
                break
        
        if not main_verb:
            return subslots
        
        # sub-s: 主語 (I)
        subjects = [child for child in main_verb.children if child.dep_ == "nsubj"]
        if subjects:
            subslots['sub-s'] = {
                'text': subjects[0].text,
                'tokens': [subjects[0].text],
                'token_indices': [subjects[0].i]
            }
        
        # sub-v: 動詞 (want)
        subslots['sub-v'] = {
            'text': main_verb.text,
            'tokens': [main_verb.text],
            'token_indices': [main_verb.i]
        }
        
        # sub-o1: 不定詞句 (to become) - 便宜的にo1
        infinitive_tokens = []
        for child in main_verb.children:
            if child.dep_ == "xcomp":  # 不定詞補語
                # toも含めて抽出（ただしwhatは除外）
                to_token = None
                for token in doc:
                    if token.text.lower() == "to" and token.head == child:
                        to_token = token
                        break
                
                inf_tokens = [child]  # メイン動詞（become）
                if to_token:
                    inf_tokens = [to_token, child]  # to + become
                
                infinitive_tokens.extend(inf_tokens)
        
        if infinitive_tokens:
            infinitive_tokens = sorted(infinitive_tokens, key=lambda x: x.i)
            subslots['sub-o1'] = {
                'text': ' '.join([t.text for t in infinitive_tokens]),
                'tokens': [t.text for t in infinitive_tokens],
                'token_indices': [t.i for t in infinitive_tokens]
            }
        
        return subslots
    
    def _extract_c1_phrase_subslots(self, doc):
        """C1 Phraseサブスロット抽出（不定詞句等）"""
        subslots = {}
        tokens = list(doc)
        
        # 不定詞のtoを処理
        to_token = None
        if tokens and tokens[0].text.lower() == "to":
            to_token = tokens[0]
        
        # メイン動詞を特定（不定詞のto be等）
        main_verb = None
        for token in doc:
            if token.pos_ == "VERB" or (token.pos_ == "AUX" and token.text.lower() in ["be", "been", "being"]):
                main_verb = token
                break
        
        # 動詞が見つからない場合は形容詞句として処理
        if not main_verb:
            # "very experienced" のような形容詞句
            adj_tokens = [token for token in doc if token.pos_ == "ADJ"]
            if adj_tokens:
                main_adj = adj_tokens[0]  # メイン形容詞
                
                # sub-v: 形容詞をメイン動詞として扱う
                subslots['sub-v'] = {
                    'text': main_adj.text,
                    'tokens': [main_adj.text],
                    'token_indices': [main_adj.i]
                }
                
                # sub-m2: 副詞修飾語
                adv_tokens = [child for child in main_adj.children if child.dep_ == "advmod"]
                if adv_tokens:
                    subslots['sub-m2'] = {
                        'text': ' '.join([t.text for t in adv_tokens]),
                        'tokens': [t.text for t in adv_tokens],
                        'token_indices': [t.i for t in adv_tokens]
                    }
            
            return subslots
        
        # sub-v: 不定詞の場合は "to + 動詞" として統合
        if to_token:
            verb_phrase = f"{to_token.text} {main_verb.text}"
            subslots['sub-v'] = {
                'text': verb_phrase,
                'tokens': [to_token.text, main_verb.text],
                'token_indices': [to_token.i, main_verb.i]
            }
        else:
            # 通常の動詞
            subslots['sub-v'] = {
                'text': main_verb.text,
                'tokens': [main_verb.text],
                'token_indices': [main_verb.i]
            }
        
        # sub-c1: 補語（形容詞・名詞）- 前置詞句は分離してsub-m3に
        comp_tokens = []
        prep_mod_tokens = []
        
        for child in main_verb.children:
            if child.dep_ in ["acomp", "attr"]:  # 形容詞補語・名詞補語
                # 補語の核だけを取得（前置詞句の子要素は除外）
                comp_tokens.append(child)
                
                # 補語に付く修飾語（副詞）も含める
                for grandchild in child.children:
                    if grandchild.dep_ == "advmod":
                        comp_tokens.append(grandchild)
                    elif grandchild.dep_ == "prep":  # 前置詞句は別途sub-m3として処理
                        prep_subtree = list(grandchild.subtree)
                        prep_mod_tokens.extend(prep_subtree)
        
        if comp_tokens:
            comp_tokens = sorted(comp_tokens, key=lambda x: x.i)
            subslots['sub-c1'] = {
                'text': ' '.join([t.text for t in comp_tokens]),
                'tokens': [t.text for t in comp_tokens],
                'token_indices': [t.i for t in comp_tokens]
            }
        
        # sub-m3: 前置詞句修飾語（in business等）
        if prep_mod_tokens:
            prep_mod_tokens = sorted(prep_mod_tokens, key=lambda x: x.i)
            subslots['sub-m3'] = {
                'text': ' '.join([t.text for t in prep_mod_tokens]),
                'tokens': [t.text for t in prep_mod_tokens],
                'token_indices': [t.i for t in prep_mod_tokens]
            }
        
        # sub-m1: その他の修飾語（副詞等、前置詞句以外）
        other_mod_tokens = []
        for child in main_verb.children:
            if child.dep_ in ["advmod"] and child not in comp_tokens:
                other_mod_tokens.append(child)
        
        if other_mod_tokens:
            subslots['sub-m1'] = {
                'text': ' '.join([t.text for t in other_mod_tokens]),
                'tokens': [t.text for t in other_mod_tokens],
                'token_indices': [t.i for t in other_mod_tokens]
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

def test_c1_subslot_generator():
    """C1サブスロット生成テスト"""
    generator = C1SubslotGenerator()
    
    # 第2文型（SVC）・第5文型（SVOC）でのC1の例
    test_cases = [
        # Word examples (サブスロット不要)
        ("happy", "word"),
        ("successful", "word"),
        ("a leader", "word"),
        
        # Phrase examples (不定詞句等)
        ("to be successful", "phrase"),
        ("to be successful in business", "phrase"),
        ("very experienced", "phrase"),
        
        # Clause examples (関係節を含む補語)
        ("the leader who is very experienced", "clause"),
        ("someone that everyone respects", "clause"),
        ("what I want to become", "clause")
    ]
    
    print("=== C1サブスロット生成テスト ===")
    
    for slot_phrase, phrase_type in test_cases:
        print(f"\n{'='*50}")
        print(f"C1 SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type}")
        print(f"{'='*50}")
        
        result = generator.generate_c1_subslots(slot_phrase, phrase_type)
        
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
    test_c1_subslot_generator()
