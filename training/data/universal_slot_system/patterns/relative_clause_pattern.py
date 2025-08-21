#!/usr/bin/env python3
"""
RelativeClausePattern - 関係節構文の統一パターン実装
=====================================================

Phase 2の一環として関係節処理を統一システムに移行
- who/which/that/whom/whose関係代名詞の包括的処理
- sub-slots展開による複雑構造の正確な分解
- 統一confidence計算システム

統合対象:
- relative_clause handler の全機能
- sub-slots生成ロジック
- 関係代名詞別の特化処理
"""

import re
import logging
from typing import Dict, List, Tuple, Any, Optional
from ..base_patterns import GrammarPattern

class RelativeClausePattern(GrammarPattern):
    """関係節構文の統一パターン実装"""
    
    def __init__(self):
        super().__init__("relative_clause", confidence_threshold=0.85)
        self.logger = logging.getLogger('RelativeClausePattern')
        
        # 関係代名詞パターン定義
        self.relative_pronouns = {
            'who': {'type': 'subject', 'human': True},
            'whom': {'type': 'object', 'human': True}, 
            'whose': {'type': 'possessive', 'human': True},
            'which': {'type': 'subject_object', 'human': False},
            'that': {'type': 'universal', 'human': 'both'}
        }
        
        # 関係節検出パターン
        self.relative_patterns = [
            # 主格関係代名詞 (who/which/that + verb)
            r'\b(.*?)\s+(who|which|that)\s+(\w+(?:\s+\w+)*?)\s+(.*)',
            # 目的格関係代名詞 (whom/which/that + subject + verb)  
            r'\b(.*?)\s+(whom|which|that)\s+(\w+)\s+(\w+(?:\s+\w+)*?)\s+(.*)',
            # 所有格関係代名詞 (whose + noun + verb)
            r'\b(.*?)\s+whose\s+(\w+(?:\s+\w+)*?)\s+(\w+(?:\s+\w+)*?)\s+(.*)'
        ]
        
    def detect(self, words: List, sentence: str) -> Dict[str, Any]:
        """関係節パターン検出"""
        detection_result = {
            'found': False,
            'pattern_type': None,
            'relative_pronoun': None,
            'main_clause': None,
            'relative_clause': None,
            'sub_slots': {},
            'confidence_factors': []
        }
        
        try:
            # 各関係代名詞パターンをチェック
            for rel_pronoun, info in self.relative_pronouns.items():
                result = self._detect_specific_relative(sentence, rel_pronoun, info)
                if result['found']:
                    detection_result.update(result)
                    detection_result['confidence_factors'].append(f"relative_{rel_pronoun}_detected")
                    break
                    
            if detection_result['found']:
                self.logger.debug(f"🔍 関係節検出: {detection_result['relative_pronoun']} - {detection_result['pattern_type']}")
                
        except Exception as e:
            self.logger.error(f"❌ 関係節検出エラー: {e}")
            
        return detection_result
        
    def _detect_specific_relative(self, sentence: str, pronoun: str, info: Dict) -> Dict[str, Any]:
        """特定の関係代名詞パターン検出"""
        result = {'found': False}
        
        if pronoun == 'who':
            return self._detect_who_pattern(sentence)
        elif pronoun == 'which':
            return self._detect_which_pattern(sentence)
        elif pronoun == 'that':
            return self._detect_that_pattern(sentence)
        elif pronoun == 'whom':
            return self._detect_whom_pattern(sentence)
        elif pronoun == 'whose':
            return self._detect_whose_pattern(sentence)
            
        return result
        
    def _detect_who_pattern(self, sentence: str) -> Dict[str, Any]:
        """who構文検出 (主格関係代名詞)"""
        pattern = r'(.+?)\s+who\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match = re.match(pattern, sentence, re.IGNORECASE)
        
        if match:
            antecedent = match.group(1).strip()
            rel_verb = match.group(2).strip() 
            rest = match.group(3).strip()
            
            return {
                'found': True,
                'pattern_type': 'who_subject',
                'relative_pronoun': 'who',
                'antecedent': antecedent,
                'relative_verb': rel_verb,
                'main_continuation': rest,
                'sub_slots': {
                    'sub-s': f"{antecedent} who",
                    'sub-v': rel_verb
                }
            }
            
        return {'found': False}
        
    def _detect_which_pattern(self, sentence: str) -> Dict[str, Any]:
        """which構文検出 (主格・目的格両対応)"""
        # 主格which (which + verb)
        pattern_subj = r'(.+?)\s+which\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match_subj = re.match(pattern_subj, sentence, re.IGNORECASE)
        
        if match_subj:
            antecedent = match_subj.group(1).strip()
            rel_verb = match_subj.group(2).strip()
            rest = match_subj.group(3).strip()
            
            # 動詞かどうか確認 (簡易チェック)
            if self._is_likely_verb(rel_verb.split()[0]):
                return {
                    'found': True,
                    'pattern_type': 'which_subject',
                    'relative_pronoun': 'which',
                    'antecedent': antecedent,
                    'relative_verb': rel_verb,
                    'main_continuation': rest,
                    'sub_slots': {
                        'sub-s': f"{antecedent} which",
                        'sub-v': rel_verb
                    }
                }
        
        # 目的格which (which + subject + verb)  
        pattern_obj = r'(.+?)\s+which\s+(\w+)\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match_obj = re.match(pattern_obj, sentence, re.IGNORECASE)
        
        if match_obj:
            antecedent = match_obj.group(1).strip()
            rel_subj = match_obj.group(2).strip()
            rel_verb = match_obj.group(3).strip()
            rest = match_obj.group(4).strip()
            
            return {
                'found': True,
                'pattern_type': 'which_object',
                'relative_pronoun': 'which',
                'antecedent': antecedent,
                'relative_subject': rel_subj,
                'relative_verb': rel_verb,
                'main_continuation': rest,
                'sub_slots': {
                    'sub-o1': f"{antecedent} which",
                    'sub-s': rel_subj,
                    'sub-v': rel_verb
                }
            }
            
        return {'found': False}
        
    def _detect_that_pattern(self, sentence: str) -> Dict[str, Any]:
        """that構文検出 (汎用関係代名詞)"""
        # 主格that (that + verb)
        pattern_subj = r'(.+?)\s+that\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match_subj = re.match(pattern_subj, sentence, re.IGNORECASE)
        
        if match_subj:
            antecedent = match_subj.group(1).strip()
            rel_verb = match_subj.group(2).strip()
            rest = match_subj.group(3).strip()
            
            if self._is_likely_verb(rel_verb.split()[0]):
                return {
                    'found': True,
                    'pattern_type': 'that_subject',
                    'relative_pronoun': 'that',
                    'antecedent': antecedent,
                    'relative_verb': rel_verb,
                    'main_continuation': rest,
                    'sub_slots': {
                        'sub-s': f"{antecedent} that",
                        'sub-v': rel_verb
                    }
                }
                
        return {'found': False}
        
    def _detect_whom_pattern(self, sentence: str) -> Dict[str, Any]:
        """whom構文検出 (目的格関係代名詞)"""
        pattern = r'(.+?)\s+whom\s+(\w+)\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match = re.match(pattern, sentence, re.IGNORECASE)
        
        if match:
            antecedent = match.group(1).strip()
            rel_subj = match.group(2).strip()
            rel_verb = match.group(3).strip()
            rest = match.group(4).strip()
            
            return {
                'found': True,
                'pattern_type': 'whom_object',
                'relative_pronoun': 'whom',
                'antecedent': antecedent,
                'relative_subject': rel_subj,
                'relative_verb': rel_verb,
                'main_continuation': rest,
                'sub_slots': {
                    'sub-o1': f"{antecedent} whom",
                    'sub-s': rel_subj,
                    'sub-v': rel_verb
                }
            }
            
        return {'found': False}
        
    def _detect_whose_pattern(self, sentence: str) -> Dict[str, Any]:
        """whose構文検出 (所有格関係代名詞)"""
        pattern = r'(.+?)\s+whose\s+(\w+(?:\s+\w+)*?)\s+(\w+(?:\s+\w+)*?)\s+(.+)'
        match = re.match(pattern, sentence, re.IGNORECASE)
        
        if match:
            antecedent = match.group(1).strip()
            possessed = match.group(2).strip()
            rel_verb = match.group(3).strip()
            rest = match.group(4).strip()
            
            return {
                'found': True,
                'pattern_type': 'whose_possessive',
                'relative_pronoun': 'whose',
                'antecedent': antecedent,
                'possessed_noun': possessed,
                'relative_verb': rel_verb,
                'main_continuation': rest,
                'sub_slots': {
                    'sub-s': f"{antecedent} whose {possessed}",
                    'sub-v': rel_verb
                }
            }
            
        return {'found': False}
        
    def _is_likely_verb(self, word: str) -> bool:
        """動詞らしさの簡易判定"""
        # 基本動詞リスト (簡易版)
        common_verbs = {
            'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did',
            'can', 'could', 'will', 'would', 'shall', 'should',
            'may', 'might', 'must',
            'run', 'runs', 'ran', 'running',
            'work', 'works', 'worked', 'working',
            'live', 'lives', 'lived', 'living',
            'go', 'goes', 'went', 'going',
            'come', 'comes', 'came', 'coming',
            'see', 'sees', 'saw', 'seeing',
            'get', 'gets', 'got', 'getting',
            'make', 'makes', 'made', 'making',
            'know', 'knows', 'knew', 'knowing',
            'think', 'thinks', 'thought', 'thinking'
        }
        
        return word.lower() in common_verbs
        
    def correct(self, doc: Any, detection_result: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """関係節修正処理"""
        corrections = {'applied': [], 'slots_modified': [], 'sub_slots_created': []}
        
        if not detection_result.get('found', False):
            return doc, corrections
            
        try:
            # 関係節タイプに応じた修正処理
            pattern_type = detection_result['pattern_type']
            
            if pattern_type in ['who_subject', 'which_subject', 'that_subject']:
                corrections = self._correct_subject_relative(doc, detection_result)
            elif pattern_type in ['which_object', 'whom_object']:
                corrections = self._correct_object_relative(doc, detection_result)
            elif pattern_type == 'whose_possessive':
                corrections = self._correct_possessive_relative(doc, detection_result)
                
            self.logger.debug(f"✅ 関係節修正適用: {pattern_type}")
            
        except Exception as e:
            self.logger.error(f"❌ 関係節修正エラー: {e}")
            
        return doc, corrections
        
    def _correct_subject_relative(self, doc: Any, detection: Dict) -> Dict[str, Any]:
        """主格関係代名詞修正"""
        corrections = {
            'applied': ['subject_relative_clause'],
            'slots_modified': ['S'],
            'sub_slots_created': ['sub-s', 'sub-v'],
            'main_clause_restructure': {
                'S': '',  # 主スロットを空に
                'continuing_clause': detection['main_continuation']
            },
            'sub_slots': detection['sub_slots']
        }
        
        return corrections
        
    def _correct_object_relative(self, doc: Any, detection: Dict) -> Dict[str, Any]:
        """目的格関係代名詞修正"""
        corrections = {
            'applied': ['object_relative_clause'],
            'slots_modified': ['O1'],  
            'sub_slots_created': ['sub-o1', 'sub-s', 'sub-v'],
            'main_clause_restructure': {
                'continuing_clause': detection['main_continuation']
            },
            'sub_slots': detection['sub_slots']
        }
        
        return corrections
        
    def _correct_possessive_relative(self, doc: Any, detection: Dict) -> Dict[str, Any]:
        """所有格関係代名詞修正"""
        corrections = {
            'applied': ['possessive_relative_clause'],
            'slots_modified': ['S'],
            'sub_slots_created': ['sub-s', 'sub-v'],
            'main_clause_restructure': {
                'S': '',  # 主スロットを空に
                'continuing_clause': detection['main_continuation']
            },
            'sub_slots': detection['sub_slots']
        }
        
        return corrections
        
    def calculate_confidence(self, detection_result: Dict[str, Any]) -> float:
        """関係節パターンconfidence計算"""
        if not detection_result.get('found', False):
            return 0.0
            
        base_confidence = 0.85  # 関係節検出基本confidence
        
        # パターン特異性によるbonus
        pattern_bonuses = {
            'whose_possessive': 0.10,  # whoseは明確
            'whom_object': 0.08,       # whomも明確
            'who_subject': 0.06,       # whoも信頼性高い
            'which_subject': 0.04,     # whichは汎用的
            'which_object': 0.04,
            'that_subject': 0.02       # thatは最も汎用的
        }
        
        pattern_type = detection_result.get('pattern_type', '')
        bonus = pattern_bonuses.get(pattern_type, 0.0)
        
        # 検出された関係代名詞の信頼性
        pronoun_confidence = {
            'whose': 0.95,
            'whom': 0.92,
            'who': 0.88,
            'which': 0.82,
            'that': 0.75
        }
        
        pronoun = detection_result.get('relative_pronoun', '')
        pronoun_factor = pronoun_confidence.get(pronoun, 0.7)
        
        final_confidence = min(0.98, base_confidence + bonus) * pronoun_factor
        
        self.logger.debug(f"📊 Confidence計算: base={base_confidence}, bonus={bonus}, pronoun_factor={pronoun_factor}, final={final_confidence:.3f}")
        
        return round(final_confidence, 3)
        
    def get_pattern_priority(self) -> int:
        """パターン優先度 (関係節は高優先度)"""
        return 88  # whose(90), passive(85)の間
        
    def get_pattern_description(self) -> str:
        """パターン説明"""
        return "関係節構文 (who/which/that/whom/whose)"
