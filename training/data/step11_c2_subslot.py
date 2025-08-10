#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 11: C2サブスロット実装
========================
第5文型（SVOC）の補語2サブスロット分解
"""

import spacy

class C2SubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_c2_subslots(self, slot_phrase, phrase_type):
        """
        C2（補語2）スロットのサブスロット生成
        
        例: "very easy to understand" → sub-m2, sub-v, sub-o1
        例: "confident that he will succeed" → sub-v, sub-s, sub-aux, sub-v, sub-o1
        """
        result = {
            'slot_phrase': slot_phrase,
            'phrase_type': phrase_type,
            'slot_type': 'C2',
            'subslots': {},
            'word_coverage_check': {}
        }
        
        if phrase_type == "word":
            result['message'] = "wordタイプ：サブスロット分解不要"
            return result
        
        # C2スロットの複雑構造を分解
        if phrase_type in ["phrase", "clause"]:
            result['subslots'] = self._extract_c2_subslots(slot_phrase, phrase_type)
            result['word_coverage_check'] = self._check_complete_coverage(slot_phrase, result['subslots'])
        
        return result
    
    def _extract_c2_subslots(self, text, phrase_type):
        """C2スロット内の構造分解"""
        doc = self.nlp(text)
        subslots = {}
        
        if phrase_type == "clause":
            # Clause: that節や関係節等の複雑構造
            subslots = self._extract_c2_clause_subslots(doc)
        elif phrase_type == "phrase":
            # Phrase: 形容詞句や不定詞句等
            subslots = self._extract_c2_phrase_subslots(doc)
        
        return subslots
    
    def _extract_c2_clause_subslots(self, doc):
        """C2 Clauseサブスロット抽出"""
        subslots = {}
        
        # that節の特殊処理
        that_token = None
        for token in doc:
            if token.text.lower() == "that" and token.pos_ == "SCONJ":
                that_token = token
                break
        
        if that_token:
            # "confident that he will succeed" の処理
            return self._extract_that_clause_c2_subslots(doc)
        
        # 関係節や他の複雑構造の処理
        return self._extract_complex_c2_clause(doc)
    
    def _extract_that_clause_c2_subslots(self, doc):
        """
        C2文型のthat節を解析してRephrase subslotを抽出
        例: "I am confident that he will succeed"
        """
        subslots = {}
        
        # that節を見つける
        that_token = None
        for token in doc:
            if token.text.lower() == "that":
                that_token = token
                break
        
        if not that_token:
            return subslots
        
        # that節の前にある形容詞を特定（C2の補語）
        main_adj = None
        for token in doc:
            if token.i < that_token.i and token.pos_ == "ADJ":
                main_adj = token
        
        # that節内部の動詞を特定
        clause_verb = None
        for token in doc:
            if token.i > that_token.i and token.pos_ == "VERB":
                clause_verb = token
                break
        
        # sub-s: 形容詞 + that + 主語（Rephraseルール：全部まとめてsub-s）
        if clause_verb:
            subjects = [child for child in clause_verb.children if child.dep_ == "nsubj"]
            if subjects and main_adj:
                subslots['sub-s'] = {
                    'text': f"{main_adj.text} that {subjects[0].text}",
                    'tokens': [main_adj.text, that_token.text, subjects[0].text],
                    'token_indices': [main_adj.i, that_token.i, subjects[0].i]
                }
            
            # sub-aux: 助動詞
            aux_tokens = [child for child in clause_verb.children if child.dep_ in ["aux", "auxpass"]]
            if aux_tokens:
                subslots['sub-aux'] = {
                    'text': ' '.join([t.text for t in aux_tokens]),
                    'tokens': [t.text for t in aux_tokens],
                    'token_indices': [t.i for t in aux_tokens]
                }
            
            # sub-v: 節内動詞
            subslots['sub-v'] = {
                'text': clause_verb.text,
                'tokens': [clause_verb.text],
                'token_indices': [clause_verb.i]
            }
            
            # sub-o1: 目的語
            objects = [child for child in clause_verb.children if child.dep_ == "dobj"]
            if objects:
                subslots['sub-o1'] = {
                    'text': objects[0].text,
                    'tokens': [objects[0].text],
                    'token_indices': [objects[0].i]
                }
        
        return subslots
    
    def _extract_complex_c2_clause(self, doc):
        """複雑なC2節構造の処理"""
        subslots = {}
        # 複雑な関係節等の処理は必要に応じて実装
        return subslots
    
    def _extract_c2_phrase_subslots(self, doc):
        """C2 Phraseサブスロット抽出"""
        subslots = {}
        tokens = list(doc)
        
        # 不定詞のtoを処理
        to_token = None
        if tokens and tokens[0].text.lower() == "to":
            to_token = tokens[0]
        
        # メイン形容詞を特定
        main_adj = None
        for token in doc:
            if token.pos_ == "ADJ":
                main_adj = token
                break
        
        if main_adj:
            # sub-c1: 形容詞補語
            subslots['sub-c1'] = {
                'text': main_adj.text,
                'tokens': [main_adj.text],
                'token_indices': [main_adj.i]
            }
            
            # sub-m1: 副詞修飾語（too, very等）を分離
            adv_tokens = [child for child in main_adj.children if child.dep_ == "advmod"]
            if adv_tokens:
                subslots['sub-m1'] = {
                    'text': ' '.join([t.text for t in adv_tokens]),
                    'tokens': [t.text for t in adv_tokens],
                    'token_indices': [t.i for t in adv_tokens]
                }
            
            # 不定詞句の処理（to understand等）→ sub-m2
            infinitive_tokens = []
            for child in main_adj.children:
                if child.dep_ in ["xcomp", "ccomp"]:  # 不定詞補語
                    # to + 動詞を統合
                    if to_token and to_token.head == child:
                        infinitive_tokens.extend([to_token, child])
                    else:
                        # toが別の場所にある場合を探す
                        to_for_verb = None
                        for token in doc:
                            if token.text.lower() == "to" and token.head == child:
                                to_for_verb = token
                                break
                        
                        if to_for_verb:
                            infinitive_tokens.extend([to_for_verb, child])
                        else:
                            infinitive_tokens.append(child)
                    break
            
            if infinitive_tokens:
                infinitive_tokens = sorted(infinitive_tokens, key=lambda x: x.i)
                subslots['sub-m2'] = {
                    'text': ' '.join([t.text for t in infinitive_tokens]),
                    'tokens': [t.text for t in infinitive_tokens],
                    'token_indices': [t.i for t in infinitive_tokens]
                }
        
        # very easy のような副詞+形容詞の処理
        elif not subslots:
            adv_tokens = [token for token in doc if token.pos_ == "ADV"]
            adj_tokens = [token for token in doc if token.pos_ == "ADJ"]
            
            if adj_tokens:
                # sub-c1: 形容詞
                subslots['sub-c1'] = {
                    'text': adj_tokens[0].text,
                    'tokens': [adj_tokens[0].text],
                    'token_indices': [adj_tokens[0].i]
                }
            
            if adv_tokens:
                # sub-m2: 副詞修飾語（very等）
                subslots['sub-m2'] = {
                    'text': ' '.join([t.text for t in adv_tokens]),
                    'tokens': [t.text for t in adv_tokens],
                    'token_indices': [t.i for t in adv_tokens]
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

def test_c2_subslot_generator():
    """C2サブスロット生成テスト"""
    generator = C2SubslotGenerator()
    
    # 第5文型（SVOC）でのC2の例
    test_cases = [
        # Word examples (サブスロット不要)
        ("happy", "word"),
        ("difficult", "word"),
        ("important", "word"),
        
        # Phrase examples (形容詞句・不定詞句)
        ("very easy", "phrase"),
        ("easy to understand", "phrase"),
        ("too difficult to solve", "phrase"),
        
        # Clause examples (that節等)
        ("confident that he will succeed", "clause"),
        ("sure that it works", "clause"),
        ("happy that you came", "clause")
    ]
    
    print("=== C2サブスロット生成テスト ===")
    
    for slot_phrase, phrase_type in test_cases:
        print(f"\n{'='*50}")
        print(f"C2 SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type}")
        print(f"{'='*50}")
        
        result = generator.generate_c2_subslots(slot_phrase, phrase_type)
        
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
    test_c2_subslot_generator()
