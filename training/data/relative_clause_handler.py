#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RelativeClauseHandler: Phase 2 関係節処理ハンドラー
spaCy品詞判定ベース（ハードコーディング禁止）
Legacy パターンを参考にした正規表現 + spaCy POS判定
"""

import re
import spacy
from typing import Dict, Any, Tuple

class RelativeClauseHandler:
    """関係節処理ハンドラー（spaCy POS判定ベース）"""
    
    def __init__(self):
        """初期化"""
        self.name = "RelativeClauseHandler"
        self.version = "spaCy_v1.0"
        self.nlp = spacy.load('en_core_web_sm')  # spaCy品詞判定用
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        関係節処理メイン
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果
        """
        try:
            # 基本的な関係代名詞検出（優先順位順）
            if ' whose ' in text.lower():
                return self._process_whose(text)
            elif ' whom ' in text.lower():
                return self._process_whom(text)
            elif ' who ' in text.lower():
                return self._process_who(text)
            elif ' which ' in text.lower():
                return self._process_which(text)
            elif ' that ' in text.lower():
                return self._process_that(text)
            else:
                return {'success': False, 'error': '関係節が見つかりませんでした'}
                
        except Exception as e:
            return {'success': False, 'error': f'処理エラー: {str(e)}'}
    
    def _process_who(self, text: str) -> Dict[str, Any]:
        """who関係節処理（spaCy文脈解析ベース）"""
        
        # spaCy文脈解析で関係節を分析
        analysis = self._analyze_relative_clause(text, 'who')
        if not analysis['success']:
            return analysis
        
        doc = analysis['doc']
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        main_clause_start = analysis['main_clause_start']
        
        # 関係節の修飾語を特定（動詞の後続要素）
        rel_verb_idx = None
        for i, token in enumerate(doc):
            if token.text == rel_verb:
                rel_verb_idx = i
                break
        
        # 関係節部分の完全な動詞句を構築
        rel_verb_phrase = rel_verb
        rel_modifiers = []  # 修飾語を別途記録
        
        if rel_verb_idx is not None:
            # 動詞の後続修飾語を収集
            for i in range(rel_verb_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':  # 主節に達したら停止
                    break
                # 動詞に依存する要素を追加
                if doc[i].head.i == rel_verb_idx:
                    rel_modifiers.append(doc[i].text)
        
        # 修飾語がある場合はsub-m2に設定
        sub_m2 = " ".join(rel_modifiers) if rel_modifiers else ""
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        # サブスロット構築
        sub_slots = {
            'sub-s': f"{antecedent} who",
            'sub-v': rel_verb,  # 動詞のみ
            '_parent_slot': 'S'  # 必須フィールド
        }
        
        # 修飾語がある場合は追加
        if sub_m2:
            sub_slots['sub-m2'] = sub_m2
        
        return {
            'success': True,
            'main_slots': {'S': ''},  # 設計仕様書準拠: 主語スロット空文字列
            'sub_slots': sub_slots,
            'pattern_type': 'who_subject',
            'relative_pronoun': 'who',
            'antecedent': antecedent,
            'main_continuation': main_clause.strip(),
            'spacy_analysis': {
                'relative_verb_pos': analysis['relative_verb_pos'],
                'relative_verb_lemma': analysis['relative_verb_lemma']
            }
        }
    
    def _analyze_relative_clause(self, text: str, relative_pronoun: str) -> Dict[str, Any]:
        """spaCy文脈解析による関係節分析"""
        try:
            # 文全体をspaCyで解析
            doc = self.nlp(text)
            
            # 関係代名詞の位置を特定
            rel_pronoun_idx = None
            for i, token in enumerate(doc):
                if token.text.lower() == relative_pronoun.lower():
                    rel_pronoun_idx = i
                    break
            
            if rel_pronoun_idx is None:
                return {'success': False, 'error': f'{relative_pronoun}が見つかりません'}
            
            # 関係節内の動詞を特定
            rel_verb_token = None
            for i in range(rel_pronoun_idx + 1, len(doc)):
                token = doc[i]
                if token.pos_ in ['VERB', 'AUX']:
                    rel_verb_token = token
                    break
                # 主節の動詞に達したら停止
                if token.dep_ == 'ROOT':
                    break
            
            if rel_verb_token is None:
                return {'success': False, 'error': '関係節内に動詞が見つかりません'}
            
            # 先行詞を特定
            antecedent_tokens = []
            for i in range(rel_pronoun_idx):
                antecedent_tokens.append(doc[i])
            
            # 主節部分を特定
            main_clause_start = None
            for i in range(rel_pronoun_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':
                    main_clause_start = i
                    break
            
            result = {
                'success': True,
                'antecedent': ' '.join([t.text for t in antecedent_tokens]).strip(),
                'relative_verb': rel_verb_token.text,
                'relative_verb_pos': rel_verb_token.pos_,
                'relative_verb_lemma': rel_verb_token.lemma_,
                'main_clause_start': main_clause_start,
                'doc': doc  # 後続処理用
            }
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': f'spaCy解析エラー: {str(e)}'}
    
    def _process_which(self, text: str) -> Dict[str, Any]:
        """which関係節処理（spaCy文脈解析ベース）"""
        
        # spaCy文脈解析で関係節を分析
        analysis = self._analyze_relative_clause(text, 'which')
        if not analysis['success']:
            return analysis
        
        doc = analysis['doc']
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        main_clause_start = analysis['main_clause_start']
        
        # 関係節の修飾語を特定
        rel_verb_idx = None
        for i, token in enumerate(doc):
            if token.text == rel_verb:
                rel_verb_idx = i
                break
        
        # 関係節部分の完全な動詞句を構築
        rel_verb_phrase = rel_verb
        if rel_verb_idx is not None:
            for i in range(rel_verb_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':
                    break
                if doc[i].head.i == rel_verb_idx:
                    rel_verb_phrase += " " + doc[i].text
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': {
                'sub-o1': f"{antecedent} which",  # whichは通常目的格
                'sub-v': rel_verb_phrase.strip()
            },
            'pattern_type': 'which_object',
            'relative_pronoun': 'which',
            'antecedent': antecedent,
            'main_continuation': main_clause.strip(),
            'spacy_analysis': {
                'relative_verb_pos': analysis['relative_verb_pos'],
                'relative_verb_lemma': analysis['relative_verb_lemma']
            }
        }
    
    def _process_that(self, text: str) -> Dict[str, Any]:
        """that関係節処理（spaCy文脈解析ベース）"""
        
        # spaCy文脈解析で関係節を分析
        analysis = self._analyze_relative_clause(text, 'that')
        if not analysis['success']:
            return analysis
        
        doc = analysis['doc']
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        main_clause_start = analysis['main_clause_start']
        
        # 関係節の修飾語を特定
        rel_verb_idx = None
        for i, token in enumerate(doc):
            if token.text == rel_verb:
                rel_verb_idx = i
                break
        
        # 関係節部分の完全な動詞句を構築
        rel_verb_phrase = rel_verb
        if rel_verb_idx is not None:
            for i in range(rel_verb_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':
                    break
                if doc[i].head.i == rel_verb_idx:
                    rel_verb_phrase += " " + doc[i].text
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        # thatは主格・目的格両方の可能性があるため文脈で判断
        # 簡略化：主格として扱う
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': {
                'sub-s': f"{antecedent} that",
                'sub-v': rel_verb_phrase.strip()
            },
            'pattern_type': 'that_subject',
            'relative_pronoun': 'that',
            'antecedent': antecedent,
            'main_continuation': main_clause.strip(),
            'spacy_analysis': {
                'relative_verb_pos': analysis['relative_verb_pos'],
                'relative_verb_lemma': analysis['relative_verb_lemma']
            }
        }

    def _process_whom(self, text: str) -> Dict[str, Any]:
        """whom関係節処理（spaCy文脈解析ベース）"""
        
        # spaCy文脈解析で関係節を分析
        analysis = self._analyze_relative_clause(text, 'whom')
        if not analysis['success']:
            return analysis
        
        doc = analysis['doc']
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        main_clause_start = analysis['main_clause_start']
        
        # whomは目的格なので、関係節内に主語が必要
        # "The man whom I met" -> I が主語、met が動詞
        rel_verb_idx = None
        for i, token in enumerate(doc):
            if token.text == rel_verb:
                rel_verb_idx = i
                break
        
        # 関係節内の主語を特定
        rel_subject = ""
        if rel_verb_idx is not None:
            for i in range(rel_verb_idx):
                if doc[i].text.lower() == 'whom':
                    # whomの後の最初の名詞/代名詞が主語
                    for j in range(i + 1, rel_verb_idx):
                        if doc[j].pos_ in ['PRON', 'NOUN', 'PROPN']:
                            rel_subject = doc[j].text
                            break
                    break
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': {
                'sub-o1': f"{antecedent} whom",  # whomは目的格
                'sub-s': rel_subject,
                'sub-v': rel_verb
            },
            'pattern_type': 'whom_object',
            'relative_pronoun': 'whom',
            'antecedent': antecedent,
            'main_continuation': main_clause.strip(),
            'spacy_analysis': {
                'relative_verb_pos': analysis['relative_verb_pos'],
                'relative_verb_lemma': analysis['relative_verb_lemma']
            }
        }

    def _process_whose(self, text: str) -> Dict[str, Any]:
        """whose関係節処理（spaCy文脈解析ベース）"""
        
        # spaCy文脈解析で関係節を分析
        analysis = self._analyze_relative_clause(text, 'whose')
        if not analysis['success']:
            return analysis
        
        doc = analysis['doc']
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        main_clause_start = analysis['main_clause_start']
        
        # whoseは所有格なので、whose + 名詞の構造
        # "The man whose car is red" -> car が主語、is が動詞
        whose_noun = ""
        whose_idx = None
        for i, token in enumerate(doc):
            if token.text.lower() == 'whose':
                whose_idx = i
                # whoseの直後の名詞を取得
                if i + 1 < len(doc):
                    whose_noun = doc[i + 1].text
                break
        
        # 関係節内の主語は "whose + noun"
        rel_subject = f"whose {whose_noun}" if whose_noun else "whose"
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': {
                'sub-s': rel_subject,
                'sub-v': rel_verb
            },
            'pattern_type': 'whose_possessive',
            'relative_pronoun': 'whose',
            'antecedent': antecedent,
            'main_continuation': main_clause.strip(),
            'spacy_analysis': {
                'relative_verb_pos': analysis['relative_verb_pos'],
                'relative_verb_lemma': analysis['relative_verb_lemma']
            }
        }
