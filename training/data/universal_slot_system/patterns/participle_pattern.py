#!/usr/bin/env python3
"""
ParticiplePattern - Phase 2 分詞構文処理システム
===============================================

分詞の形容詞的・副詞的用法の統一的処理

Phase 2 Component: 予想効果 +7%
対象パターン:
- working overtime (現在分詞)
- standing quietly (現在分詞 + 副詞)
- being reviewed thoroughly (受動分詞構文)
- written carefully (過去分詞)
"""

import re
import logging
from typing import Dict, List, Tuple, Any, Optional
from ..base_patterns import GrammarPattern
from ..universal_manager import UniversalSlotPositionManager


class ParticiplePattern(GrammarPattern):
    def __init__(self):
        super().__init__(pattern_name="participle_clause")
        self.participle_markers = {
            'present': ['working', 'standing', 'running', 'sitting', 'walking', 'talking', 'being'],
            'past': ['written', 'spoken', 'broken', 'given', 'taken', 'made', 'done', 'seen'],
            'compound': ['being written', 'being reviewed', 'being done', 'being made']
        }
        
    def detect(self, analysis_doc, sentence):
        """分詞構文パターンの検出"""
        
        # Stanza解析結果の検証
        if not hasattr(analysis_doc, 'sentences') or not analysis_doc.sentences:
            print(f"DEBUG: analysis_doc検証失敗: {type(analysis_doc)}")
            return False
            
        tokens = analysis_doc.sentences[0].words
        print(f"DEBUG: Participle検出開始 - tokens数: {len(tokens)}")
        
        # 分詞パターンの検出
        participle_detected = False
        participle_positions = []
        
        for i, token in enumerate(tokens):
            print(f"DEBUG: Token {i}: '{token.text}' upos={token.upos} feats={token.feats}")
            
            # 現在分詞検出 (VBG) - Stanza では 'Tense=Pres|VerbForm=Part' または 'VerbForm=Ger'
            if token.upos == 'VERB' and token.feats:
                feats_str = str(token.feats)
                if 'VerbForm=Ger' in feats_str or ('VerbForm=Part' in feats_str and 'Tense=Pres' in feats_str):
                    print(f"DEBUG: 現在分詞検出: {token.text} ({feats_str})")
                    participle_detected = True
                    participle_positions.append(i)
                
                # 過去分詞検出 (VBN) - Stanza では 'Tense=Past|VerbForm=Part'
                elif 'VerbForm=Part' in feats_str and 'Tense=Past' in feats_str:
                    print(f"DEBUG: 過去分詞検出: {token.text} ({feats_str})")
                    participle_detected = True
                    participle_positions.append(i)
                    
            # 複合分詞 (being + 過去分詞)
            elif token.text.lower() == 'being' and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.upos == 'VERB' and next_token.feats:
                    next_feats = str(next_token.feats)
                    if 'VerbForm=Part' in next_feats:
                        print(f"DEBUG: 複合分詞検出: {token.text} + {next_token.text}")
                        participle_detected = True
                        participle_positions.extend([i, i + 1])
        
        print(f"DEBUG: 分詞検出結果: {participle_detected}, positions: {participle_positions}")
        return participle_detected and len(participle_positions) > 0
    
    def correct(self, analysis_doc, sentence):
        """分詞構文の統一処理"""
        
        if not self.detect(analysis_doc, sentence):
            return None
            
        # UniversalSlotPositionManagerによる基本処理
        manager = UniversalSlotPositionManager()
        base_result = manager.process_all_patterns(analysis_doc, sentence)
        
        if not isinstance(base_result, tuple) or len(base_result) != 2:
            return None
            
        unified_result, confidence = base_result
        
        # JSONシリアライズ可能な形式に変換
        clean_result = self._make_json_safe(unified_result)
        
        # 分詞構文の特殊処理
        enhanced_result = self._enhance_participle_slots(analysis_doc, clean_result, sentence)
        enhanced_confidence = self.calculate_confidence(analysis_doc, sentence)
        
        return enhanced_result, enhanced_confidence
    
    def _make_json_safe(self, data):
        """Document objectsをJSONシリアライズ可能な形式に変換"""
        if hasattr(data, 'copy'):
            # dict-like object
            result = {}
            for key, value in data.items():
                if hasattr(value, '__dict__'):
                    # Document object など
                    result[key] = str(value)
                else:
                    result[key] = value
            return result
        else:
            return data
    
    def _enhance_participle_slots(self, analysis_doc, base_result, sentence):
        """分詞構文に特化したスロット拡張"""
        
        tokens = analysis_doc.sentences[0].words
        enhanced_result = base_result.copy()
        
        # 分詞構文のサブスロット生成
        participle_info = self._extract_participle_info(tokens)
        
        if participle_info:
            # 分詞構文用のサブスロットを生成
            enhanced_result['sub_slots'] = enhanced_result.get('sub_slots', {})
            enhanced_result['sub_slots']['participle_clause'] = {
                'type': participle_info['type'],
                'main_participle': participle_info['main_verb'],
                'modifiers': participle_info['modifiers'],
                'semantic_role': participle_info['role']
            }
            
            # 分詞の役割に応じてメインスロットを調整
            if participle_info['role'] == 'adjectival':
                # 形容詞的用法: 名詞修飾
                if 'ADJ' in enhanced_result:
                    enhanced_result['ADJ'] += f" [{participle_info['main_verb']}]"
                else:
                    enhanced_result['ADJ'] = f"[{participle_info['main_verb']}]"
                    
            elif participle_info['role'] == 'adverbial':
                # 副詞的用法: 動作・状況の説明
                if 'ADV' in enhanced_result:
                    enhanced_result['ADV'] += f" [{participle_info['main_verb']}]"
                else:
                    enhanced_result['ADV'] = f"[{participle_info['main_verb']}]"
        
        return enhanced_result
    
    def _extract_participle_info(self, tokens):
        """分詞構文の詳細情報抽出"""
        
        participle_info = {
            'type': 'unknown',
            'main_verb': '',
            'modifiers': [],
            'role': 'adjectival'  # デフォルト: 形容詞的用法
        }
        
        for i, token in enumerate(tokens):
            # 現在分詞
            if token.upos == 'VERB' and token.feats and 'VerbForm=Ger' in str(token.feats):
                participle_info['type'] = 'present'
                participle_info['main_verb'] = token.text
                
                # 修飾語の収集
                modifiers = []
                # 前後の副詞を検索
                for j in range(max(0, i-2), min(len(tokens), i+3)):
                    if j != i and tokens[j].upos == 'ADV':
                        modifiers.append(tokens[j].text)
                        
                participle_info['modifiers'] = modifiers
                
                # 役割判定: 文脈から形容詞的か副詞的かを判断
                if self._is_adverbial_use(tokens, i):
                    participle_info['role'] = 'adverbial'
                break
                
            # 過去分詞
            elif token.upos == 'VERB' and token.feats and 'VerbForm=Part' in str(token.feats):
                participle_info['type'] = 'past'
                participle_info['main_verb'] = token.text
                
                # 複合分詞チェック
                if i > 0 and tokens[i-1].text.lower() == 'being':
                    participle_info['type'] = 'compound_passive'
                    participle_info['main_verb'] = f"being {token.text}"
                
                # 修飾語の収集
                modifiers = []
                for j in range(max(0, i-2), min(len(tokens), i+3)):
                    if j != i and tokens[j].upos == 'ADV':
                        modifiers.append(tokens[j].text)
                        
                participle_info['modifiers'] = modifiers
                break
        
        return participle_info if participle_info['main_verb'] else None
    
    def _is_adverbial_use(self, tokens, participle_index):
        """分詞の副詞的用法判定"""
        
        # 簡易的な判定ロジック
        # 1. 分詞の後に副詞が続く場合は副詞的用法の可能性が高い
        if participle_index + 1 < len(tokens):
            next_token = tokens[participle_index + 1]
            if next_token.upos == 'ADV':
                return True
                
        # 2. 分詞が文末近くにある場合は副詞的用法の可能性が高い
        if participle_index > len(tokens) * 0.7:
            return True
            
        # 3. 分詞の前に前置詞がある場合は副詞的用法
        if participle_index > 0:
            prev_token = tokens[participle_index - 1]
            if prev_token.upos == 'ADP':
                return True
        
        return False
    
    def calculate_confidence(self, analysis_doc, sentence):
        """信頼度計算"""
        
        if not self.detect(analysis_doc, sentence):
            return 0.0
            
        tokens = analysis_doc.sentences[0].words
        confidence_factors = []
        
        # 分詞パターンの明確性
        participle_count = 0
        for token in tokens:
            if (token.upos == 'VERB' and token.feats and 
                ('VerbForm=Ger' in str(token.feats) or 'VerbForm=Part' in str(token.feats))):
                participle_count += 1
                
        if participle_count == 1:
            confidence_factors.append(0.9)  # 単一の明確な分詞
        elif participle_count > 1:
            confidence_factors.append(0.7)  # 複数分詞（複雑）
            
        # 文構造の複雑さ
        sentence_length = len(tokens)
        if sentence_length <= 8:
            confidence_factors.append(0.9)  # 短文
        elif sentence_length <= 15:
            confidence_factors.append(0.8)  # 中文
        else:
            confidence_factors.append(0.6)  # 長文
            
        # 修飾関係の明確性
        adverb_count = sum(1 for token in tokens if token.upos == 'ADV')
        if adverb_count <= 2:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)
            
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5


# モジュール登録用のクラス参照
__all__ = ['ParticiplePattern']
