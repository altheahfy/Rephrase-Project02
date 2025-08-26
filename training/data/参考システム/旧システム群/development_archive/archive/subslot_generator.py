#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サブスロット自動生成エンジン v1.0
==================================
Phase 1.2 実装: 9種類のサブスロット自動生成

【基盤データ】
- final_rephrase_analysis.py の分析結果
- 192個のサブスロット要素
- 9種類のサブスロット: sub-s, sub-aux, sub-v, sub-o1, sub-o2, sub-c1, sub-c2, sub-m1, sub-m2, sub-m3

【重要パターン】
S[clause]: "the manager who had recently taken charge of the project"
→ sub-s: "the manager who", sub-aux: "had", sub-m2: "recently", sub-v: "taken", sub-o1: "charge of the project"
"""

import spacy
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

@dataclass
class SubslotResult:
    """サブスロット生成結果"""
    subslot_type: str
    content: str
    confidence: float = 1.0
    source_tokens: List = None

class SubslotGenerator:
    """サブスロット自動生成エンジン"""
    
    def __init__(self, nlp_model="en_core_web_sm"):
        """初期化"""
        self.nlp = spacy.load(nlp_model)
        
        # 関係詞・接続詞パターン（5文型フルセット分析結果より）
        self.relative_pronouns = {"who", "that", "which", "whom", "whose"}
        self.conjunctions = {
            "time": {"when", "while", "as"},
            "reason": {"because", "since", "as"},
            "contrast": {"although", "even though", "though"},
            "result": {"so", "so that", "therefore"}
        }
        
        # 助動詞パターン
        self.auxiliary_verbs = {
            "modal": {"might", "could", "would", "should", "may", "can", "will", "must"},
            "perfect": {"had", "have", "has"},
            "progressive": {"was", "were", "is", "are", "am", "be"},
            "passive": {"was", "were", "is", "are", "been", "be"}
        }
    
    def generate_subslots(self, phrase: str, phrase_type: str, slot_type: str) -> Dict[str, SubslotResult]:
        """
        フレーズからサブスロットを自動生成
        
        Args:
            phrase: 分解対象フレーズ
            phrase_type: word/phrase/clause
            slot_type: S/V/O1/M1等
            
        Returns:
            Dict[subslot_name, SubslotResult]: 生成されたサブスロット
        """
        doc = self.nlp(phrase)
        
        if phrase_type == "clause":
            return self._generate_clause_subslots(doc, slot_type)
        elif phrase_type == "phrase":
            return self._generate_phrase_subslots(doc, slot_type)
        else:  # word
            return {}  # wordタイプはサブスロット生成なし
    
    def _generate_clause_subslots(self, doc, slot_type: str) -> Dict[str, SubslotResult]:
        """
        clause型フレーズのサブスロット生成
        
        【重要パターン】（final_rephrase_analysis.py より）
        S[clause]: "the manager who had recently taken charge of the project"
        M2[clause]: "even though he was under intense pressure"
        M3[clause]: "so the outcome would reflect their full potential"
        """
        subslots = {}
        
        # スロット種別に応じた処理
        if slot_type == "S":
            subslots.update(self._extract_subject_clause_subslots(doc))
        elif slot_type in ["M1", "M2", "M3"]:
            subslots.update(self._extract_modifier_clause_subslots(doc))
        elif slot_type in ["O1", "O2"]:
            subslots.update(self._extract_object_clause_subslots(doc))
        elif slot_type in ["C1", "C2"]:
            subslots.update(self._extract_complement_clause_subslots(doc))
        
        return subslots
    
    def _extract_subject_clause_subslots(self, doc) -> Dict[str, SubslotResult]:
        """
        S[clause]のサブスロット抽出
        
        パターン: "the manager who had recently taken charge of the project"
        → sub-s: "the manager who", sub-aux: "had", sub-m2: "recently", sub-v: "taken", sub-o1: "charge of the project"
        """
        subslots = {}
        tokens = list(doc)
        
        # 関係詞位置を検索
        relative_idx = self._find_relative_pronoun_index(tokens)
        
        if relative_idx >= 0:
            # sub-s: 関係詞までの部分
            sub_s_tokens = tokens[:relative_idx+1]
            subslots["sub-s"] = SubslotResult(
                "sub-s", 
                " ".join([t.text for t in sub_s_tokens]),
                1.0,
                sub_s_tokens
            )
            
            # 関係詞節内の構造解析
            relative_clause_tokens = tokens[relative_idx+1:]
            if relative_clause_tokens:
                subslots.update(self._analyze_relative_clause_structure(relative_clause_tokens))
        
        return subslots
    
    def _extract_modifier_clause_subslots(self, doc) -> Dict[str, SubslotResult]:
        """
        M1/M2/M3[clause]のサブスロット抽出
        
        パターン例:
        M2: "even though he was under intense pressure"
        → sub-m1: "even though", sub-s: "he", sub-v: "was", sub-m2: "under intense pressure"
        """
        subslots = {}
        tokens = list(doc)
        
        # 接続詞部分を特定
        conjunction_end = self._find_conjunction_boundary(tokens)
        
        if conjunction_end >= 0:
            # sub-m1: 接続詞部分
            conjunction_tokens = tokens[:conjunction_end+1]
            subslots["sub-m1"] = SubslotResult(
                "sub-m1",
                " ".join([t.text for t in conjunction_tokens]),
                1.0,
                conjunction_tokens
            )
            
            # 接続詞後の従属節構造解析
            clause_tokens = tokens[conjunction_end+1:]
            if clause_tokens:
                subslots.update(self._analyze_subordinate_clause_structure(clause_tokens))
        
        return subslots
    
    def _extract_object_clause_subslots(self, doc) -> Dict[str, SubslotResult]:
        """
        O1/O2[clause]のサブスロット抽出
        
        パターン例:
        O1: "that he had been trying to avoid Tom"
        → sub-s: "that he", sub-aux: "had", sub-v: "been trying", sub-o2: "to avoid Tom"
        """
        subslots = {}
        tokens = list(doc)
        
        # that節の処理
        if tokens and tokens[0].lemma_ == "that":
            # sub-s: "that + 主語"
            subject_end = self._find_subject_boundary(tokens[1:])
            if subject_end >= 0:
                sub_s_tokens = tokens[:subject_end+2]  # that + subject
                subslots["sub-s"] = SubslotResult(
                    "sub-s",
                    " ".join([t.text for t in sub_s_tokens]),
                    1.0,
                    sub_s_tokens
                )
                
                # 述語部分の解析
                predicate_tokens = tokens[subject_end+2:]
                if predicate_tokens:
                    subslots.update(self._analyze_predicate_structure(predicate_tokens))
        
        return subslots
    
    def _extract_complement_clause_subslots(self, doc) -> Dict[str, SubslotResult]:
        """
        C1/C2[clause]のサブスロット抽出
        
        パターン例:
        C1: "the dependable voice everyone had been waiting for"
        → sub-s: "everyone", sub-aux: "had been", sub-v: "waiting for", sub-o1: "the dependable voice"
        """
        subslots = {}
        # 補語節の複雑な構造解析
        # TODO: より詳細な実装が必要
        return subslots
    
    def _generate_phrase_subslots(self, doc, slot_type: str) -> Dict[str, SubslotResult]:
        """
        phrase型フレーズのサブスロット生成
        
        【重要パターン】
        C2[phrase]: "deliver the final proposal flawlessly"
        → sub-v: "deliver", sub-o1: "the final proposal", sub-m3: "flawlessly"
        """
        subslots = {}
        tokens = list(doc)
        
        if slot_type == "C2":
            # 動詞 + 目的語 + 修飾句のパターン
            verb_idx = self._find_main_verb_index(tokens)
            if verb_idx >= 0:
                # sub-v: 主動詞
                subslots["sub-v"] = SubslotResult(
                    "sub-v",
                    tokens[verb_idx].text,
                    1.0,
                    [tokens[verb_idx]]
                )
                
                # 目的語と修飾句を分離
                remaining_tokens = tokens[verb_idx+1:]
                if remaining_tokens:
                    subslots.update(self._separate_object_and_modifier(remaining_tokens))
        
        return subslots
    
    # =========================================================================
    # 補助メソッド群
    # =========================================================================
    
    def _find_relative_pronoun_index(self, tokens) -> int:
        """関係詞の位置を検索"""
        for i, token in enumerate(tokens):
            if token.lemma_.lower() in self.relative_pronouns:
                return i
        return -1
    
    def _find_conjunction_boundary(self, tokens) -> int:
        """接続詞境界を検索"""
        # "even though", "so that" などの複合接続詞対応
        text = " ".join([t.text.lower() for t in tokens])
        
        for conj_type, conj_set in self.conjunctions.items():
            for conj in conj_set:
                if text.startswith(conj):
                    return len(conj.split()) - 1
        return -1
    
    def _find_subject_boundary(self, tokens) -> int:
        """主語境界を検索（spaCy依存関係利用）"""
        for i, token in enumerate(tokens):
            if token.dep_ == "nsubj":
                return i
        return 0 if tokens else -1
    
    def _find_main_verb_index(self, tokens) -> int:
        """主動詞を検索"""
        for i, token in enumerate(tokens):
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "xcomp", "ccomp"]:
                return i
        return -1
    
    def _analyze_relative_clause_structure(self, tokens) -> Dict[str, SubslotResult]:
        """関係詞節内の構造解析 - 改善版"""
        subslots = {}
        
        # 助動詞検索
        aux_tokens = [t for t in tokens if t.lemma_.lower() in 
                     set().union(*self.auxiliary_verbs.values())]
        if aux_tokens:
            subslots["sub-aux"] = SubslotResult("sub-aux", aux_tokens[0].text, 0.9, aux_tokens[:1])
        
        # 主動詞検索
        main_verb = self._find_main_verb_in_tokens(tokens)
        if main_verb:
            subslots["sub-v"] = SubslotResult("sub-v", main_verb.text, 0.9, [main_verb])
        
        # 副詞（時間・頻度）検索 - recently, just, often等
        adverb_tokens = [t for t in tokens if t.pos_ == "ADV" and t.dep_ == "advmod"]
        if adverb_tokens:
            # 動詞の前にある副詞は通常sub-m2（頻度・時間）
            subslots["sub-m2"] = SubslotResult(
                "sub-m2", 
                adverb_tokens[0].text, 
                0.8, 
                adverb_tokens[:1]
            )
        
        # 目的語・補語検索 - 動詞の後にある要素
        if main_verb:
            verb_idx = tokens.index(main_verb)
            post_verb_tokens = tokens[verb_idx+1:]
            
            # 前置詞句や目的語を検出
            if post_verb_tokens:
                # sub-o1として残りの要素をまとめる
                remaining_text = " ".join([t.text for t in post_verb_tokens])
                subslots["sub-o1"] = SubslotResult("sub-o1", remaining_text, 0.7, post_verb_tokens)
        
        return subslots
    
    def _analyze_subordinate_clause_structure(self, tokens) -> Dict[str, SubslotResult]:
        """従属節構造の解析 - 改善版"""
        subslots = {}
        
        # 主語検索
        subject_token = self._find_subject_in_tokens(tokens)
        if subject_token:
            subslots["sub-s"] = SubslotResult("sub-s", subject_token.text, 0.9, [subject_token])
        
        # 動詞検索
        verb_token = self._find_main_verb_in_tokens(tokens)
        if verb_token:
            subslots["sub-v"] = SubslotResult("sub-v", verb_token.text, 0.9, [verb_token])
        
        # 修飾句検索 - "under intense pressure" などの前置詞句
        prep_phrases = []
        for i, token in enumerate(tokens):
            if token.pos_ == "ADP":  # 前置詞
                # 前置詞から文末まで、または次の重要語まで
                phrase_tokens = []
                for j in range(i, len(tokens)):
                    if tokens[j].dep_ in ["prep", "pobj", "det"]:
                        phrase_tokens.append(tokens[j])
                    else:
                        break
                if phrase_tokens:
                    prep_phrases.append(phrase_tokens)
        
        if prep_phrases:
            # 最初の前置詞句をsub-m2として使用
            phrase_text = " ".join([t.text for t in prep_phrases[0]])
            subslots["sub-m2"] = SubslotResult("sub-m2", phrase_text, 0.8, prep_phrases[0])
        
        return subslots
    
    def _analyze_predicate_structure(self, tokens) -> Dict[str, SubslotResult]:
        """述語構造の解析"""
        subslots = {}
        # TODO: 実装
        return subslots
    
    def _separate_object_and_modifier(self, tokens) -> Dict[str, SubslotResult]:
        """目的語と修飾句の分離 - 改善版"""
        subslots = {}
        
        # 動詞を探す
        verb_token = None
        for token in tokens:
            if token.pos_ in ["VERB", "AUX"] and not verb_token:
                verb_token = token
                subslots["sub-v"] = SubslotResult(
                    "sub-v",
                    token.text,
                    0.9,
                    [token]
                )
        
        # 前置詞句を探す（修飾句候補）
        prep_phrases = []
        current_phrase = []
        
        for token in tokens:
            if token == verb_token:
                continue
                
            if token.pos_ == "ADP":  # 前置詞
                if current_phrase:
                    prep_phrases.append(current_phrase)
                current_phrase = [token.text]
            elif current_phrase and token.pos_ in ["NOUN", "PROPN", "DET", "ADJ", "NUM"]:
                current_phrase.append(token.text)
            elif current_phrase:
                prep_phrases.append(current_phrase)
                current_phrase = []
                
        if current_phrase:
            prep_phrases.append(current_phrase)
        
        # 修飾句として登録
        for i, phrase in enumerate(prep_phrases):
            if i == 0:
                subslots["sub-m2"] = SubslotResult(
                    "sub-m2",
                    " ".join(phrase),
                    0.9,
                    phrase
                )
        
        # 副詞（様態修飾）を検索
        adverb_tokens = [t for t in tokens if t.pos_ == "ADV" and t != verb_token]
        if adverb_tokens:
            subslots["sub-m3"] = SubslotResult(
                "sub-m3", 
                adverb_tokens[-1].text,  # 最後の副詞を様態修飾とみなす
                0.8,
                adverb_tokens[-1:]
            )
        
        return subslots
    
    def _find_main_verb_in_tokens(self, tokens):
        """トークン列から主動詞を検索 - 改善版"""
        # be動詞、助動詞も含めて動詞として認識
        for token in tokens:
            if token.pos_ in ["VERB", "AUX"] and token.dep_ in ["ROOT", "xcomp", "ccomp", "cop", "aux"]:
                return token
        
        # より広い検索 - POSタグのみ
        for token in tokens:
            if token.pos_ in ["VERB", "AUX"]:
                return token
                
        return None
    
    def _find_subject_in_tokens(self, tokens):
        """トークン列から主語を検索"""
        for token in tokens:
            if token.dep_ == "nsubj":
                return token
        return None


# =========================================================================
# テスト・実証コード
# =========================================================================

def test_subslot_generation():
    """サブスロット生成のテスト"""
    generator = SubslotGenerator()
    
    # 5文型フルセット分析結果からの重要例
    test_cases = [
        {
            "phrase": "the manager who had recently taken charge of the project",
            "phrase_type": "clause",
            "slot_type": "S",
            "expected": ["sub-s", "sub-aux", "sub-m2", "sub-v", "sub-o1"]
        },
        {
            "phrase": "even though he was under intense pressure", 
            "phrase_type": "clause",
            "slot_type": "M2",
            "expected": ["sub-m1", "sub-s", "sub-v", "sub-m2"]
        },
        {
            "phrase": "deliver the final proposal flawlessly",
            "phrase_type": "phrase", 
            "slot_type": "C2",
            "expected": ["sub-v", "sub-o1", "sub-m3"]
        }
    ]
    
    print("=== サブスロット生成エンジン テスト ===")
    for i, case in enumerate(test_cases):
        print(f"\n【テスト{i+1}】")
        print(f"入力: {case['slot_type']}[{case['phrase_type']}] = \"{case['phrase']}\"")
        
        result = generator.generate_subslots(
            case["phrase"], 
            case["phrase_type"], 
            case["slot_type"]
        )
        
        print("生成結果:")
        for subslot_name, subslot_result in result.items():
            print(f"  {subslot_name}: \"{subslot_result.content}\" (confidence: {subslot_result.confidence:.2f})")
        
        print(f"期待値: {case['expected']}")
        generated_types = list(result.keys())
        coverage = len(set(generated_types) & set(case['expected'])) / len(case['expected'])
        print(f"カバレッジ: {coverage:.1%}")

if __name__ == "__main__":
    test_subslot_generation()
