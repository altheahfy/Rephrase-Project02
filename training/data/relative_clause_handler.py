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
            # 基本的な関係代名詞検出
            if ' who ' in text.lower():
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
        """who関係節処理（Legacy正規表現パターン）"""
        # Legacy パターン: (.+?)\s+who\s+(\w+(?:\s+\w+)*?)\s+(.+)
        pattern = r'(.+?)\s+who\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match = re.match(pattern, text, re.IGNORECASE)
        
        if match:
            antecedent = match.group(1).strip()
            rel_verb = match.group(2).strip() 
            rest = match.group(3).strip()
            
            # 動詞確認（Legacy方式）
            if self._is_likely_verb(rel_verb.split()[0]):
                return {
                    'success': True,
                    'main_slots': {'S': ''},  # Legacy戦略: 主語スロット空文字列
                    'sub_slots': {
                        'sub-s': f"{antecedent} who",
                        'sub-v': rel_verb
                    },
                    'pattern_type': 'who_subject',
                    'relative_pronoun': 'who',
                    'antecedent': antecedent,
                    'main_continuation': rest
                }
        
        return {'success': False, 'error': 'whoパターンマッチ失敗'}
    
    def _is_likely_verb(self, word: str) -> bool:
        """spaCy品詞判定による動詞判定（ハードコーディング禁止）"""
        try:
            # spaCyで品詞判定
            doc = self.nlp(word)
            if len(doc) > 0:
                token = doc[0]
                # VERB または AUX (助動詞) を動詞として判定
                return token.pos_ in ['VERB', 'AUX']
            return False
        except Exception:
            # spaCy処理エラー時はFalseを返す
            return False
    
    def _process_which(self, text: str) -> Dict[str, Any]:
        """which関係節処理"""
        return {'success': False, 'error': 'which処理は未実装'}
    
    def _process_that(self, text: str) -> Dict[str, Any]:
        """that関係節処理（Legacy正規表現パターン）"""
        
        # パターン1: 主格that (that + verb) - (.+?)\s+that\s+(\w+(?:\s+\w+)*?)\s+(.+)
        pattern_subj = r'(.+?)\s+that\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match_subj = re.match(pattern_subj, text, re.IGNORECASE)
        
        if match_subj:
            antecedent = match_subj.group(1).strip()
            rel_verb = match_subj.group(2).strip()
            rest = match_subj.group(3).strip()
            
            # 動詞確認（Legacy方式）
            if self._is_likely_verb(rel_verb.split()[0]):
                return {
                    'success': True,
                    'main_slots': {'S': ''},  # Legacy戦略: 主語スロット空文字列
                    'sub_slots': {
                        'sub-s': f"{antecedent} that",
                        'sub-v': rel_verb
                    },
                    'pattern_type': 'that_subject',
                    'relative_pronoun': 'that',
                    'antecedent': antecedent,
                    'main_continuation': rest
                }
        
        # パターン2: 目的格that (that + subject + verb) - (.+?)\s+that\s+(\w+)\s+(\w+(?:\s+\w+)*?)\s+(.+)
        pattern_obj = r'(.+?)\s+that\s+(\w+)\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match_obj = re.match(pattern_obj, text, re.IGNORECASE)
        
        if match_obj:
            antecedent = match_obj.group(1).strip()
            rel_subj = match_obj.group(2).strip()
            rel_verb = match_obj.group(3).strip()
            rest = match_obj.group(4).strip()
            
            # 動詞確認
            if self._is_likely_verb(rel_verb.split()[0]):
                return {
                    'success': True,
                    'main_slots': {'S': ''},  # Legacy戦略
                    'sub_slots': {
                        'sub-o1': f"{antecedent} that",  # 目的格として
                        'sub-s': rel_subj,
                        'sub-v': rel_verb
                    },
                    'pattern_type': 'that_object',
                    'relative_pronoun': 'that',
                    'antecedent': antecedent,
                    'main_continuation': rest
                }
        
        return {'success': False, 'error': 'thatパターンマッチ失敗'}
