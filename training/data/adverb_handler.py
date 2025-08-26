#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdverbHandler: 副詞・修飾語処理ハンドラー
spaCy品詞分析ベース（ハードコーディング禁止）
責任分担原則に基づく専門ハンドラー
"""

import spacy
from typing import Dict, Any, List, Tuple

class AdverbHandler:
    """副詞・修飾語処理ハンドラー（spaCy POS判定ベース）"""
    
    def __init__(self):
        """初期化"""
        self.name = "AdverbHandler"
        self.version = "spaCy_v1.0"
        self.nlp = spacy.load('en_core_web_sm')  # spaCy品詞判定用
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        副詞・修飾語処理メイン
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果
        """
        try:
            # 文全体をspaCyで解析
            doc = self.nlp(text)
            
            # 動詞と修飾語のペアを特定
            verb_modifier_pairs = self._identify_verb_modifier_pairs(doc)
            
            if not verb_modifier_pairs:
                return {'success': False, 'error': '修飾語が見つかりませんでした'}
            
            # 修飾語を分離したテキストと修飾語情報を返す
            result = self._separate_modifiers(doc, verb_modifier_pairs)
            
            return {
                'success': True,
                'separated_text': result['separated_text'],
                'modifiers': result['modifiers'],
                'verb_positions': result['verb_positions']
            }
            
        except Exception as e:
            return {'success': False, 'error': f'処理エラー: {str(e)}'}
    
    def _identify_verb_modifier_pairs(self, doc) -> List[Dict]:
        """動詞と修飾語のペアを特定"""
        pairs = []
        
        for i, token in enumerate(doc):
            # 動詞を見つける
            if token.pos_ in ['VERB', 'AUX']:
                verb_info = {
                    'verb_idx': i,
                    'verb_text': token.text,
                    'verb_lemma': token.lemma_,
                    'modifiers': []
                }
                
                # 動詞の後続修飾語を収集
                modifiers = self._collect_verb_modifiers(doc, i)
                if modifiers:
                    verb_info['modifiers'] = modifiers
                    pairs.append(verb_info)
        
        return pairs
    
    def _collect_verb_modifiers(self, doc, verb_idx: int) -> List[Dict]:
        """動詞の修飾語を収集"""
        modifiers = []
        
        # 動詞の直後から文末まで（または次の主要要素まで）を検索
        for i in range(verb_idx + 1, len(doc)):
            token = doc[i]
            
            # 句読点で停止
            if token.pos_ == 'PUNCT':
                break
            
            # 次の動詞で停止（主節の動詞など）
            if token.pos_ in ['VERB', 'AUX'] and self._is_main_clause_verb(doc, i):
                break
            
            # 修飾語として識別
            if self._is_modifier(token):
                modifier_info = {
                    'text': token.text,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'idx': i,
                    'type': self._classify_modifier_type(token)
                }
                modifiers.append(modifier_info)
        
        return modifiers
    
    def _is_modifier(self, token) -> bool:
        """トークンが修飾語かどうか判定"""
        # 副詞
        if token.pos_ == 'ADV':
            return True
        
        # 前置詞句（前置詞で始まる）
        if token.pos_ == 'ADP':
            return True
        
        # 場所・時間を表す名詞
        if token.pos_ in ['NOUN', 'PROPN'] and self._is_adverbial_noun(token):
            return True
        
        return False
    
    def _is_adverbial_noun(self, token) -> bool:
        """副詞的な名詞かどうか判定（場所・時間など）"""
        # 場所・時間を表す一般的な語
        adverbial_patterns = [
            'here', 'there', 'everywhere', 'somewhere',
            'today', 'yesterday', 'tomorrow', 'now',
            'home', 'abroad', 'upstairs', 'downtown'
        ]
        
        return token.text.lower() in adverbial_patterns
    
    def _classify_modifier_type(self, token) -> str:
        """修飾語の種類を分類"""
        if token.pos_ == 'ADV':
            return 'adverb'
        elif token.pos_ == 'ADP':
            return 'prepositional'
        elif self._is_adverbial_noun(token):
            return 'adverbial_noun'
        else:
            return 'other'
    
    def _is_main_clause_verb(self, doc, verb_idx: int) -> bool:
        """主節の動詞かどうか判定（関係節内の動詞と区別）"""
        # 簡易判定：関係代名詞より後にある動詞は関係節、
        # それより前または関係代名詞がない場合は主節
        relative_pronouns = ['who', 'which', 'that', 'whom', 'whose']
        
        # 関係代名詞の位置を特定
        rel_pronoun_idx = None
        for i, token in enumerate(doc):
            if token.text.lower() in relative_pronouns:
                rel_pronoun_idx = i
                break
        
        # 関係代名詞がない場合、主節の動詞
        if rel_pronoun_idx is None:
            return True
        
        # 関係代名詞より後の最初の動詞は関係節、その後は主節
        if verb_idx > rel_pronoun_idx:
            # 関係節内の最初の動詞をチェック
            first_rel_verb_idx = None
            for i in range(rel_pronoun_idx + 1, len(doc)):
                if doc[i].pos_ in ['VERB', 'AUX']:
                    first_rel_verb_idx = i
                    break
            
            # 関係節内の最初の動詞ではない場合、主節の動詞
            return verb_idx != first_rel_verb_idx
        
        return True
    
    def _separate_modifiers(self, doc, verb_modifier_pairs: List[Dict]) -> Dict:
        """修飾語を分離したテキストと修飾語情報を生成"""
        separated_tokens = []
        modifiers_info = {}
        verb_positions = {}
        
        modifier_indices = set()
        
        # 修飾語のインデックスを収集
        for pair in verb_modifier_pairs:
            verb_idx = pair['verb_idx']
            verb_text = pair['verb_text']
            
            # 動詞位置を記録
            verb_positions[verb_idx] = {
                'original_text': verb_text,
                'modifiers': []
            }
            
            for modifier in pair['modifiers']:
                modifier_idx = modifier['idx']
                modifier_indices.add(modifier_idx)
                
                # 修飾語情報を記録
                if verb_idx not in modifiers_info:
                    modifiers_info[verb_idx] = []
                
                modifiers_info[verb_idx].append({
                    'text': modifier['text'],
                    'type': modifier['type'],
                    'pos': modifier['pos']
                })
                
                verb_positions[verb_idx]['modifiers'].append(modifier['text'])
        
        # 修飾語を除いたテキストを構築
        for i, token in enumerate(doc):
            if i not in modifier_indices:
                separated_tokens.append(token.text)
        
        separated_text = ' '.join(separated_tokens)
        
        return {
            'separated_text': separated_text,
            'modifiers': modifiers_info,
            'verb_positions': verb_positions
        }
