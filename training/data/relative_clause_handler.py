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
    """関係節処理ハンドラー（協力アプローチ版）"""
    
    def __init__(self, collaborators=None):
        """
        初期化
        
        Args:
            collaborators: 協力者ハンドラー辞書
                - 'adverb': AdverbHandler（修飾語分離）
                - 'five_pattern': BasicFivePatternHandler（5文型分析）
                - 'passive': PassiveVoiceHandler（受動態理解）
        """
        self.name = "RelativeClauseHandler"
        self.version = "cooperation_v1.0"
        self.nlp = spacy.load('en_core_web_sm')  # spaCy品詞判定用
        
        # 協力者ハンドラーたち（Dependency Injection）
        if collaborators:
            self.adverb_handler = collaborators.get('adverb') or collaborators.get('AdverbHandler')
            self.five_pattern_handler = collaborators.get('five_pattern') or collaborators.get('FivePatternHandler')
            self.passive_handler = collaborators.get('passive') or collaborators.get('PassiveHandler')
        else:
            self.adverb_handler = None
            self.five_pattern_handler = None
            self.passive_handler = None
    
    def process(self, text: str, original_text: str = None) -> Dict[str, Any]:
        """
        関係節処理メイン（協力アプローチ版）
        
        Args:
            text: 処理対象の英語文（修飾語分離済み可能性あり）
            original_text: オリジナルテキスト（修飾語情報保持用）
            
        Returns:
            Dict: 処理結果
        """
        # オリジナルテキストの決定
        self.original_text = original_text if original_text else text
        
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
        """who関係節処理（協力アプローチ版）"""
        
        # spaCy文脈解析で関係節を分析（協力者情報を含む）
        analysis = self._analyze_relative_clause(text, 'who')
        if not analysis['success']:
            return analysis
        
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        
        # 修飾語情報（協力者 AdverbHandler の結果を活用）
        modifiers_info = analysis.get('modifiers', {})
        sub_m2 = ""
        
        # 協力者から修飾語情報を取得
        if modifiers_info and 'M2' in modifiers_info:
            sub_m2 = modifiers_info['M2']
        
        # 主節を構築
        main_clause_start = analysis.get('main_clause_start')
        main_clause = ""
        if main_clause_start is not None:
            doc = analysis['doc']
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
    
    def _extract_relative_clause_text_original(self, text: str, relative_pronoun: str) -> str:
        """オリジナルテキストから関係節部分のテキストを抽出（修飾語込み）"""
        try:
            doc = self.nlp(text)
            
            rel_start = None
            rel_end = len(doc)
            
            # Step 1: 関係代名詞の位置を特定
            for i, token in enumerate(doc):
                if token.text.lower() == relative_pronoun.lower():
                    rel_start = i
                    break
            
            if rel_start is None:
                return text
            
            # Step 2: 文全体のメイン動詞（真のROOT）を特定
            main_root_idx = None
            for i, token in enumerate(doc):
                if token.dep_ == 'ROOT':
                    main_root_idx = i
                    break
            
            # Step 3: 関係節の終了位置を決定
            # - 関係代名詞以降で主節動詞より前まで
            if main_root_idx is not None and main_root_idx > rel_start:
                rel_end = main_root_idx
            else:
                # フォールバック: 品詞パターンで判定
                for i in range(rel_start + 1, len(doc)):
                    token = doc[i]
                    # 主語的語句（名詞＋動詞）に遭遇したら関係節終了
                    if (token.pos_ in ['NOUN', 'PROPN'] and 
                        i + 1 < len(doc) and 
                        doc[i + 1].pos_ in ['VERB', 'AUX']):
                        rel_end = i
                        break
            
            # Step 4: 関係節テキストを抽出
            if rel_start is not None:
                clause_tokens = doc[rel_start:rel_end]
                extracted = ' '.join([t.text for t in clause_tokens])
                return extracted
            
            return text
            
        except Exception as e:
            return text

    def _extract_relative_clause_text(self, text: str, relative_pronoun: str) -> str:
        """関係節部分のテキストを抽出（修飾語込み）"""
        try:
            doc = self.nlp(text)
            
            rel_start = None
            rel_end = len(doc)
            
            # Step 1: 関係代名詞の位置を特定
            for i, token in enumerate(doc):
                if token.text.lower() == relative_pronoun.lower():
                    rel_start = i
                    break
            
            if rel_start is None:
                return text
            
            # Step 2: 文全体のメイン動詞（真のROOT）を特定
            main_root_idx = None
            for i, token in enumerate(doc):
                if token.dep_ == 'ROOT':
                    main_root_idx = i
                    break
            
            # Step 3: 関係節の終了位置を決定
            # - 関係代名詞以降で主節動詞より前まで
            if main_root_idx is not None and main_root_idx > rel_start:
                rel_end = main_root_idx
            else:
                # フォールバック: 品詞パターンで判定
                for i in range(rel_start + 1, len(doc)):
                    token = doc[i]
                    # 主語的語句（名詞＋動詞）に遭遇したら関係節終了
                    if (token.pos_ in ['NOUN', 'PROPN'] and 
                        i + 1 < len(doc) and 
                        doc[i + 1].pos_ in ['VERB', 'AUX']):
                        rel_end = i
                        break
            
            # Step 4: 関係節テキストを抽出
            if rel_start is not None:
                clause_tokens = doc[rel_start:rel_end]
                extracted = ' '.join([t.text for t in clause_tokens])
                print(f"[DEBUG] 関係節抽出: '{text}' → '{extracted}'")
                return extracted
            
            return text
            
        except Exception as e:
            print(f"[DEBUG] 関係節抽出エラー: {str(e)}")
            return text
            return text

    def _analyze_relative_clause(self, text: str, relative_pronoun: str) -> Dict[str, Any]:
        """spaCy文脈解析による関係節分析（協力アプローチ版）"""
        try:
            # Step 1: オリジナルテキストから関係節部分を抽出（修飾語込み）
            original_clause_text = self._extract_relative_clause_text_original(
                getattr(self, 'original_text', text), relative_pronoun
            )
            
            # Step 2: 協力者（副詞ハンドラー）と連携：修飾語分離
            cleaned_clause = original_clause_text
            modifiers = {}
            
            if self.adverb_handler and original_clause_text:
                adverb_result = self.adverb_handler.process(original_clause_text)
                
                if adverb_result.get('success'):
                    cleaned_clause = adverb_result.get('separated_text', original_clause_text)
                    
                    # AdverbHandlerの結果を5文型システム形式に変換
                    raw_modifiers = adverb_result.get('modifiers', {})
                    
                    if raw_modifiers:
                        # 位置インデックスキーから修飾語テキストを抽出してM2に統合
                        modifier_texts = []
                        for pos_idx, modifier_list in raw_modifiers.items():
                            if isinstance(modifier_list, list):
                                for modifier_info in modifier_list:
                                    if isinstance(modifier_info, dict) and 'text' in modifier_info:
                                        modifier_texts.append(modifier_info['text'])
                        
                        # M2キーとして統合
                        if modifier_texts:
                            modifiers['M2'] = ' '.join(modifier_texts)
            
            # Step 3: 協力者（5文型ハンドラー）と連携：構造分析
            structure_analysis = None
            if self.five_pattern_handler and cleaned_clause:
                structure_result = self.five_pattern_handler.process(cleaned_clause)
                if structure_result.get('success'):
                    structure_analysis = structure_result
            
            # Step 4: 文全体をspaCyで解析（フォールバック・詳細情報用）
            doc = self.nlp(text)
            
            # Step 5: 関係代名詞の位置を特定
            rel_pronoun_idx = None
            for i, token in enumerate(doc):
                if token.text.lower() == relative_pronoun.lower():
                    rel_pronoun_idx = i
                    break
            
            if rel_pronoun_idx is None:
                return {'success': False, 'error': f'{relative_pronoun}が見つかりません'}
            
            # Step 6: 関係節内の動詞を特定（協力者の結果を優先、フォールバック有り）
            rel_verb_token = None
            if structure_analysis and structure_analysis.get('slots', {}).get('V'):
                # 協力者からの5文型分析結果を使用
                rel_verb = structure_analysis['slots']['V']
            else:
                # フォールバック: spaCy直接分析
                for i in range(rel_pronoun_idx + 1, len(doc)):
                    token = doc[i]
                    if token.pos_ in ['VERB', 'AUX']:
                        rel_verb_token = token
                        rel_verb = token.text
                        break
                    # 主節の動詞に達したら停止
                    if token.dep_ == 'ROOT':
                        break
            
            if not rel_verb_token and not rel_verb:
                return {'success': False, 'error': '関係節内に動詞が見つかりません'}
            
            # Step 7: 先行詞を特定
            antecedent_tokens = []
            for i in range(rel_pronoun_idx):
                antecedent_tokens.append(doc[i])
            
            # Step 8: 主節部分を特定
            main_clause_start = None
            for i in range(rel_pronoun_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':
                    main_clause_start = i
                    break
            
            result = {
                'success': True,
                'antecedent': ' '.join([t.text for t in antecedent_tokens]).strip(),
                'relative_verb': rel_verb,
                'relative_verb_pos': rel_verb_token.pos_ if rel_verb_token else 'VERB',
                'relative_verb_lemma': rel_verb_token.lemma_ if rel_verb_token else rel_verb,
                'main_clause_start': main_clause_start,
                'doc': doc,
                'modifiers': modifiers,  # 協力者からの修飾語情報
                'structure_analysis': structure_analysis  # 協力者からの5文型分析
            }
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': f'spaCy解析エラー: {str(e)}'}
    
    def _process_which(self, text: str) -> Dict[str, Any]:
        """which関係節処理（協力アプローチ版）"""
        
        # spaCy文脈解析で関係節を分析（協力者情報を含む）
        analysis = self._analyze_relative_clause(text, 'which')
        if not analysis['success']:
            return analysis
        
        antecedent = analysis['antecedent']
        rel_verb = analysis['relative_verb']
        
        # 修飾語情報（協力者 AdverbHandler の結果を活用）
        modifiers_info = analysis.get('modifiers', {})
        sub_m2 = ""
        
        # 協力者から修飾語情報を取得
        if modifiers_info and 'M2' in modifiers_info:
            sub_m2 = modifiers_info['M2']
        
        # whichは主語・目的語を文脈で判定
        doc = analysis['doc']  # _analyze_relative_clauseから取得
        which_idx = None
        for i, token in enumerate(doc):
            if token.text.lower() == 'which':
                which_idx = i
                break
        
        is_subject = True
        if which_idx is not None and which_idx + 1 < len(doc):
            next_token = doc[which_idx + 1]
            if next_token.pos_ in ['PRON', 'NOUN', 'PROPN']:
                is_subject = False  # which + 名詞 = 目的格
        
        # サブスロット構築
        if is_subject:
            sub_slots = {
                'sub-s': f"{antecedent} which",
                'sub-v': rel_verb,
                '_parent_slot': 'S'
            }
        else:
            # 目的格whichの場合、関係節内の主語を特定
            rel_subject = ""
            if which_idx is not None:
                for i in range(which_idx + 1, len(doc)):
                    if doc[i].pos_ in ['PRON', 'NOUN', 'PROPN'] and doc[i].text != rel_verb:
                        rel_subject = doc[i].text
                        break
            
            sub_slots = {
                'sub-o1': f"{antecedent} which",
                'sub-s': rel_subject,
                'sub-v': rel_verb,
                '_parent_slot': 'S'
            }
        
        # 修飾語がある場合は追加
        if sub_m2:
            sub_slots['sub-m2'] = sub_m2
        
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': sub_slots,
            'pattern_type': 'which_object' if not is_subject else 'which_subject',
            'relative_pronoun': 'which',
            'antecedent': antecedent,
            'main_continuation': analysis.get('main_clause', ''),
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
        rel_modifiers = []  # 修飾語を別途記録
        
        if rel_verb_idx is not None:
            for i in range(rel_verb_idx + 1, len(doc)):
                if doc[i].dep_ == 'ROOT':
                    break
                if doc[i].head.i == rel_verb_idx:
                    rel_modifiers.append(doc[i].text)
        
        # 修飾語がある場合はsub-m2に設定
        sub_m2 = " ".join(rel_modifiers) if rel_modifiers else ""
        
        # 主節を構築
        main_clause = ""
        if main_clause_start is not None:
            main_tokens = [token.text for token in doc[main_clause_start:]]
            main_clause = " ".join(main_tokens)
        
        # thatは主語・目的語を文脈で判定
        # 簡略判定：that直後に動詞があれば主語、名詞があれば目的語
        is_subject = True
        that_idx = None
        for i, token in enumerate(doc):
            if token.text.lower() == 'that':
                that_idx = i
                break
        
        if that_idx is not None and that_idx + 1 < len(doc):
            next_token = doc[that_idx + 1]
            if next_token.pos_ in ['PRON', 'NOUN', 'PROPN']:
                is_subject = False  # that + 名詞 = 目的格
        
        # サブスロット構築
        if is_subject:
            sub_slots = {
                'sub-s': f"{antecedent} that",
                'sub-v': rel_verb,
                '_parent_slot': 'S'
            }
        else:
            # 目的格thatの場合、関係節内の主語を特定
            rel_subject = ""
            if that_idx is not None:
                for i in range(that_idx + 1, len(doc)):
                    if doc[i].pos_ in ['PRON', 'NOUN', 'PROPN'] and doc[i].text != rel_verb:
                        rel_subject = doc[i].text
                        break
            
            sub_slots = {
                'sub-o1': f"{antecedent} that",
                'sub-s': rel_subject,
                'sub-v': rel_verb,
                '_parent_slot': 'S'
            }
        
        # 修飾語がある場合は追加
        if sub_m2:
            sub_slots['sub-m2'] = sub_m2
        
        return {
            'success': True,
            'main_slots': {'S': ''},
            'sub_slots': sub_slots,
            'pattern_type': 'that_subject' if is_subject else 'that_object',
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
                'sub-v': rel_verb,
                '_parent_slot': 'S'
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
                'sub-v': rel_verb,
                '_parent_slot': 'S'
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
