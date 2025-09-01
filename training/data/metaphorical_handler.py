#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MetaphoricalHandler: 比喩表現ハンドラー
as if / as though 構文の専門分解
Rephrase的スロット分解の100%達成のため
"""

import re
import spacy
from typing import Dict, Any, List, Tuple, Optional

class MetaphoricalHandler:
    """比喻表現ハンドラー（as if / as though専用）"""
    
    def __init__(self, nlp_model=None, collaborators=None):
        """
        初期化
        
        Args:
            nlp_model: spaCyモデル（オプション）
            collaborators: 協力者ハンドラー辞書
        """
        self.name = "MetaphoricalHandler"
        self.version = "v1.0"
        self.nlp = nlp_model if nlp_model is not None else spacy.load('en_core_web_sm')
        
        # 協力者ハンドラーたち
        self.collaborators = collaborators or {}
        
        # 比喩表現パターン
        self.metaphorical_patterns = [
            r'\bas\s+if\b',
            r'\bas\s+though\b'
        ]
    
    def can_handle(self, text: str) -> bool:
        """
        比喩表現が処理可能かチェック
        
        Args:
            text: 処理対象文
            
        Returns:
            bool: 処理可能性
        """
        for pattern in self.metaphorical_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def handle(self, text: str) -> Dict[str, Any]:
        """
        比喩表現の処理メイン
        
        Args:
            text: 処理対象文
            
        Returns:
            Dict: 処理結果
        """
        print(f"🎭 MetaphoricalHandler処理開始: '{text}'")
        
        try:
            doc = self.nlp(text)
            
            # as if / as though パターン検出
            if ' as if ' in text.lower():
                return self._process_as_if_structure(doc, text)
            elif ' as though ' in text.lower():
                return self._process_as_though_structure(doc, text)
            else:
                return self._create_failure_result(text, "比喩表現パターンが見つかりません")
        
        except Exception as e:
            print(f"❌ MetaphoricalHandler error: {e}")
            return self._create_failure_result(text, f"比喩表現処理エラー: {e}")
    
    def _process_as_if_structure(self, doc, text: str) -> Dict[str, Any]:
        """
        as if 構文の処理
        
        Args:
            doc: spaCy解析結果
            text: 処理対象文
            
        Returns:
            Dict: 処理結果
        """
        print(f"🎭 as if構文処理: '{text}'")
        
        # 文を "main" + "as if + clause" に分離
        match = re.search(r'^(.+?)\s+as\s+if\s+(.+)$', text, re.IGNORECASE)
        if not match:
            return self._create_failure_result(text, "as if構造の分離に失敗")
        
        main_part = match.group(1).strip()
        metaphor_part = f"as if {match.group(2).strip()}"
        
        print(f"   主節: '{main_part}'")
        print(f"   比喩節: '{metaphor_part}'")
        
        # 主節の基本分解
        main_result = self._analyze_main_clause(main_part)
        
        # 比喩節の分解
        metaphor_result = self._analyze_metaphor_clause(metaphor_part, text)
        
        # スロット統合
        main_slots = main_result['main_slots']
        main_slots['M2'] = ''  # 比喩節はM2位置に配置
        
        sub_slots = metaphor_result['sub_slots']
        sub_slots['_parent_slot'] = 'M2'
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['metaphorical', 'basic_five_pattern'],
            'primary_handler': 'metaphorical',
            'metadata': {
                'handler': 'metaphorical_as_if',
                'main_clause': main_part,
                'metaphor_clause': metaphor_part,
                'confidence': 0.95
            }
        }
    
    def _process_as_though_structure(self, doc, text: str) -> Dict[str, Any]:
        """
        as though 構文の処理
        
        Args:
            doc: spaCy解析結果
            text: 処理対象文
            
        Returns:
            Dict: 処理結果
        """
        print(f"🎭 as though構文処理: '{text}'")
        
        # 文を "main" + "as though + clause" に分離
        match = re.search(r'^(.+?)\s+as\s+though\s+(.+)$', text, re.IGNORECASE)
        if not match:
            return self._create_failure_result(text, "as though構造の分離に失敗")
        
        main_part = match.group(1).strip()
        metaphor_part = f"as though {match.group(2).strip()}"
        
        print(f"   主節: '{main_part}'")
        print(f"   比喩節: '{metaphor_part}'")
        
        # 主節の基本分解
        main_result = self._analyze_main_clause(main_part)
        
        # 比喩節の分解
        metaphor_result = self._analyze_metaphor_clause(metaphor_part, text)
        
        # スロット統合
        main_slots = main_result['main_slots']
        main_slots['M2'] = ''  # 比喩節はM2位置に配置
        
        sub_slots = metaphor_result['sub_slots']
        sub_slots['_parent_slot'] = 'M2'
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['metaphorical', 'basic_five_pattern'],
            'primary_handler': 'metaphorical',
            'metadata': {
                'handler': 'metaphorical_as_though',
                'main_clause': main_part,
                'metaphor_clause': metaphor_part,
                'confidence': 0.95
            }
        }
    
    def _analyze_main_clause(self, main_text: str) -> Dict[str, Any]:
        """
        主節の分析
        
        Args:
            main_text: 主節テキスト
            
        Returns:
            Dict: 分析結果
        """
        print(f"🔍 主節分析: '{main_text}'")
        
        try:
            # BasicFivePatternHandlerがあれば使用
            if 'basic_five_pattern' in self.collaborators:
                result = self.collaborators['basic_five_pattern'].handle(main_text)
                if result.get('success'):
                    print(f"   ✅ 基本5文型分解成功: {result['main_slots']}")
                    return result
            
            # フォールバック: シンプルな分解
            doc = self.nlp(main_text)
            main_slots = {}
            
            for token in doc:
                if token.dep_ == 'nsubj':
                    main_slots['S'] = token.text
                elif token.dep_ == 'ROOT':
                    main_slots['V'] = token.text
                elif token.dep_ == 'dobj':
                    main_slots['O1'] = token.text
                elif token.dep_ in ['acomp', 'attr']:
                    main_slots['C1'] = token.text
            
            print(f"   ✅ フォールバック分解: {main_slots}")
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': {}
            }
            
        except Exception as e:
            print(f"   ❌ 主節分析エラー: {e}")
            return {
                'success': False,
                'main_slots': {'V': main_text},
                'sub_slots': {}
            }
    
    def _analyze_metaphor_clause(self, metaphor_text: str, original_text: str) -> Dict[str, Any]:
        """
        比喩節の分析
        
        Args:
            metaphor_text: 比喻節テキスト
            original_text: 元の文全体
            
        Returns:
            Dict: 分析結果
        """
        print(f"🔍 比喩節分析: '{metaphor_text}'")
        
        sub_slots = {}
        
        try:
            doc = self.nlp(original_text)
            
            # "as if" / "as though" 以降の部分を分析
            if ' as if ' in metaphor_text.lower():
                pattern = r'as\s+if\s+(.+)'
                connector = 'as if'
            else:
                pattern = r'as\s+though\s+(.+)'
                connector = 'as though'
            
            match = re.search(pattern, metaphor_text, re.IGNORECASE)
            if not match:
                return {'sub_slots': {}}
            
            clause_content = match.group(1).strip()
            print(f"   節内容: '{clause_content}'")
            
            # spaCy解析で比喩節内の要素を特定
            for token in doc:
                if token.text.lower() in ['as', 'if', 'though']:
                    continue
                
                # 比喩節内の主語検出
                if token.dep_ == 'nsubj' and token.i > self._find_as_if_position(doc):
                    if 'sub-s' not in sub_slots:
                        sub_slots['sub-s'] = f"{connector} {token.text}"
                        print(f"      比喩節主語検出: '{connector} {token.text}'")
                
                # 比喩節内の動詞検出
                elif token.dep_ in ['advcl', 'ccomp'] and token.i > self._find_as_if_position(doc):
                    sub_slots['sub-v'] = token.text
                    print(f"      比喩節動詞検出: '{token.text}'")
                    
                    # この動詞の助動詞を検出
                    for child in token.children:
                        if child.dep_ == 'aux':
                            sub_slots['sub-aux'] = child.text
                            print(f"      比喩節助動詞検出: '{child.text}'")
                    
                    # この動詞の補語・目的語を検出
                    for child in token.children:
                        if child.dep_ in ['attr', 'acomp']:
                            # 完全なフレーズを抽出
                            phrase = self._extract_full_phrase(child, doc)
                            sub_slots['sub-c1'] = phrase
                            print(f"      比喩節補語検出: '{phrase}'")
                        elif child.dep_ == 'dobj':
                            phrase = self._extract_full_phrase(child, doc)
                            sub_slots['sub-o1'] = phrase
                            print(f"      比喩節目的語検出: '{phrase}'")
            
            print(f"   ✅ 比喩節分解完了: {sub_slots}")
            return {'sub_slots': sub_slots}
            
        except Exception as e:
            print(f"   ❌ 比喩節分析エラー: {e}")
            return {'sub_slots': {}}
    
    def _find_as_if_position(self, doc) -> int:
        """
        'as if' / 'as though' の位置を特定
        
        Args:
            doc: spaCy解析結果
            
        Returns:
            int: 位置インデックス
        """
        for i, token in enumerate(doc):
            if token.text.lower() == 'as' and i + 1 < len(doc):
                next_token = doc[i + 1]
                if next_token.text.lower() in ['if', 'though']:
                    return i + 1
        return 0
    
    def _extract_full_phrase(self, token, doc) -> str:
        """
        完全なフレーズを抽出（修飾語含む）
        
        Args:
            token: 中心となるトークン
            doc: spaCy解析結果
            
        Returns:
            str: 完全なフレーズ
        """
        # 簡単な実装: トークンとその子要素
        phrase_tokens = [token.text]
        
        for child in token.children:
            if child.dep_ in ['det', 'amod', 'compound']:
                if child.i < token.i:
                    phrase_tokens.insert(0, child.text)
                else:
                    phrase_tokens.append(child.text)
        
        return ' '.join(phrase_tokens)
    
    def _create_failure_result(self, text: str, reason: str) -> Dict[str, Any]:
        """
        失敗結果を作成
        
        Args:
            text: 処理対象文
            reason: 失敗理由
            
        Returns:
            Dict: 失敗結果
        """
        return {
            'success': False,
            'error': reason,
            'text': text,
            'main_slots': {},
            'sub_slots': {},
            'primary_handler': 'metaphorical'
        }
