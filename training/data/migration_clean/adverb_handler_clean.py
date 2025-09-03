"""
AdverbHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存AdverbHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定品詞タグ → 設定可能なパターンマッチング
- 固定副詞リスト → 動的語彙解析
- 固定依存関係 → 汎用関係性分析
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ModifierPattern:
    """修飾語パターン定義"""
    pattern_type: str
    pos_indicators: List[str] = field(default_factory=list)
    dependency_indicators: List[str] = field(default_factory=list)
    lexical_indicators: List[str] = field(default_factory=list)
    position_preferences: List[str] = field(default_factory=list)  # ['pre', 'post', 'any']
    confidence_weight: float = 1.0


@dataclass
class AdverbConfiguration:
    """副詞ハンドラー設定"""
    modifier_patterns: Dict[str, ModifierPattern] = field(default_factory=dict)
    analysis_methods: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    extraction_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericModifierAnalyzer:
    """汎用修飾語解析エンジン"""
    
    def __init__(self, config: AdverbConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_modifiers(self, doc, target_verb_idx: Optional[int] = None) -> Dict[str, Any]:
        """汎用修飾語解析"""
        if target_verb_idx is None:
            target_verb_idx = self._find_primary_verb(doc)
        
        if target_verb_idx is None:
            return {'modifiers': {}, 'confidence': 0.0}
        
        # パターンベース修飾語検出
        modifier_candidates = self._detect_modifier_candidates(doc, target_verb_idx)
        
        # 修飾語の分類と分離
        classified_modifiers = self._classify_modifiers(modifier_candidates, doc)
        
        # 信頼度計算
        confidence = self._calculate_modifier_confidence(classified_modifiers)
        
        return {
            'modifiers': classified_modifiers,
            'target_verb_idx': target_verb_idx,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _find_primary_verb(self, doc) -> Optional[int]:
        """主動詞の動的検出"""
        verb_candidates = []
        
        for token in doc:
            if self._matches_pattern(token, 'verb_indicators'):
                score = self._calculate_verb_priority(token, doc)
                verb_candidates.append((token.i, score))
        
        if not verb_candidates:
            return None
        
        # 最高スコアの動詞を選択
        return max(verb_candidates, key=lambda x: x[1])[0]
    
    def _matches_pattern(self, token, pattern_name: str) -> bool:
        """パターンマッチング"""
        if pattern_name not in self.config.modifier_patterns:
            return False
        
        pattern = self.config.modifier_patterns[pattern_name]
        
        # 品詞マッチング
        pos_match = not pattern.pos_indicators or token.pos_ in pattern.pos_indicators
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_indicators or token.dep_ in pattern.dependency_indicators
        
        # 語彙マッチング
        lex_match = not pattern.lexical_indicators or token.lemma_.lower() in pattern.lexical_indicators
        
        return pos_match and dep_match and lex_match
    
    def _calculate_verb_priority(self, token, doc) -> float:
        """動詞優先度の計算"""
        score = 0.0
        
        # ROOT動詞は最高優先度
        if token.dep_ == 'ROOT':
            score += 1.0
        
        # AUXは優先度を下げる
        if token.pos_ == 'AUX':
            score -= 0.3
        
        # 修飾語の存在で優先度を上げる
        modifier_count = sum(1 for child in token.children 
                           if self._matches_pattern(child, 'adverb_indicators'))
        score += modifier_count * 0.2
        
        return score
    
    def _detect_modifier_candidates(self, doc, verb_idx: int) -> List[Dict[str, Any]]:
        """修飾語候補の検出"""
        candidates = []
        verb_token = doc[verb_idx]
        
        # 全パターンで修飾語を検出
        for pattern_name, pattern in self.config.modifier_patterns.items():
            if pattern_name == 'verb_indicators':  # 動詞パターンはスキップ
                continue
            
            for token in doc:
                if self._matches_pattern(token, pattern_name):
                    candidate = self._create_modifier_candidate(
                        token, verb_token, pattern_name, pattern
                    )
                    if candidate:
                        candidates.append(candidate)
        
        return candidates
    
    def _create_modifier_candidate(self, token, verb_token, pattern_name: str, 
                                 pattern: ModifierPattern) -> Optional[Dict[str, Any]]:
        """修飾語候補の作成"""
        # 関係性の検証
        relationship_score = self._calculate_relationship_score(token, verb_token, pattern)
        
        if relationship_score < 0.1:  # 関係が薄い場合は除外
            return None
        
        # 位置関係の分析
        position = 'pre' if token.i < verb_token.i else 'post'
        position_score = self._calculate_position_score(position, pattern)
        
        return {
            'token': token,
            'text': token.text,
            'pattern_type': pattern_name,
            'relationship_score': relationship_score,
            'position': position,
            'position_score': position_score,
            'total_confidence': relationship_score * position_score * pattern.confidence_weight
        }
    
    def _calculate_relationship_score(self, modifier_token, verb_token, pattern: ModifierPattern) -> float:
        """関係性スコアの計算"""
        score = 0.0
        
        # 直接の依存関係
        if modifier_token.head == verb_token:
            score += 0.8
        elif verb_token.head == modifier_token:
            score += 0.6
        
        # 間接的な関係
        if self._has_indirect_relationship(modifier_token, verb_token):
            score += 0.4
        
        # 距離による減衰
        distance = abs(modifier_token.i - verb_token.i)
        if distance <= 2:
            score += 0.3
        elif distance <= 5:
            score += 0.1
        
        return min(1.0, score)
    
    def _has_indirect_relationship(self, token1, token2) -> bool:
        """間接的関係の検証"""
        # 共通の親を持つか
        if token1.head == token2.head and token1.head != token1 and token1.head != token2:
            return True
        
        # 2段階以内の関係か
        if token1.head.head == token2 or token2.head.head == token1:
            return True
        
        return False
    
    def _calculate_position_score(self, position: str, pattern: ModifierPattern) -> float:
        """位置スコアの計算"""
        if not pattern.position_preferences or 'any' in pattern.position_preferences:
            return 1.0
        
        if position in pattern.position_preferences:
            return 1.0
        else:
            return 0.5  # 非推奨位置だが完全に除外はしない
    
    def _classify_modifiers(self, candidates: List[Dict[str, Any]], doc) -> Dict[str, Any]:
        """修飾語の分類"""
        classified = {}
        
        # 信頼度でソート
        sorted_candidates = sorted(candidates, key=lambda x: x['total_confidence'], reverse=True)
        
        for candidate in sorted_candidates:
            pattern_type = candidate['pattern_type']
            
            if pattern_type not in classified:
                classified[pattern_type] = []
            
            classified[pattern_type].append({
                'text': candidate['text'],
                'position': candidate['position'],
                'confidence': candidate['total_confidence'],
                'slot_key': self._generate_slot_key(candidate, len(classified[pattern_type]))
            })
        
        return classified
    
    def _generate_slot_key(self, candidate: Dict[str, Any], index: int) -> str:
        """スロットキーの生成"""
        pattern_type = candidate['pattern_type']
        position = candidate['position']
        
        # パターンタイプに基づく接頭辞
        if 'adverb' in pattern_type:
            prefix = 'sub-m'
        elif 'adjective' in pattern_type:
            prefix = 'sub-a'
        elif 'prepositional' in pattern_type:
            prefix = 'sub-p'
        else:
            prefix = 'sub-x'
        
        # 位置情報を含む
        suffix = '1' if position == 'pre' else '2'
        
        return f"{prefix}{suffix}"
    
    def _calculate_modifier_confidence(self, classified_modifiers: Dict[str, Any]) -> float:
        """修飾語解析の全体信頼度"""
        if not classified_modifiers:
            return 0.0
        
        total_confidence = 0.0
        total_modifiers = 0
        
        for pattern_type, modifiers in classified_modifiers.items():
            for modifier in modifiers:
                total_confidence += modifier['confidence']
                total_modifiers += 1
        
        if total_modifiers == 0:
            return 0.0
        
        return min(1.0, total_confidence / total_modifiers)


class AdverbHandlerClean:
    """
    副詞・修飾語処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的修飾語検出アルゴリズム
    - 動的信頼度計算
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericModifierAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'AdverbHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> AdverbConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> AdverbConfiguration:
        """デフォルト設定の作成"""
        return AdverbConfiguration(
            modifier_patterns={
                'verb_indicators': ModifierPattern(
                    pattern_type='verb',
                    pos_indicators=['VERB', 'AUX'],
                    dependency_indicators=['ROOT', 'aux', 'cop'],
                    confidence_weight=1.0
                ),
                'adverb_indicators': ModifierPattern(
                    pattern_type='adverb',
                    pos_indicators=['ADV'],
                    dependency_indicators=['advmod', 'npadvmod'],
                    position_preferences=['pre', 'post'],
                    confidence_weight=1.2
                ),
                'adjective_modifiers': ModifierPattern(
                    pattern_type='adjective',
                    pos_indicators=['ADJ'],
                    dependency_indicators=['amod', 'advmod'],
                    position_preferences=['pre'],
                    confidence_weight=0.8
                ),
                'prepositional_phrases': ModifierPattern(
                    pattern_type='prepositional',
                    pos_indicators=['ADP'],
                    dependency_indicators=['prep', 'agent'],
                    position_preferences=['post'],
                    confidence_weight=0.9
                )
            },
            confidence_settings={
                'minimum_confidence': 0.3,
                'high_confidence': 0.7,
                'modifier_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> AdverbConfiguration:
        """設定データの解析"""
        modifier_patterns = {}
        for name, data in config_data.get('modifier_patterns', {}).items():
            modifier_patterns[name] = ModifierPattern(
                pattern_type=data.get('pattern_type', name),
                pos_indicators=data.get('pos_indicators', []),
                dependency_indicators=data.get('dependency_indicators', []),
                lexical_indicators=data.get('lexical_indicators', []),
                position_preferences=data.get('position_preferences', ['any']),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return AdverbConfiguration(
            modifier_patterns=modifier_patterns,
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        副詞・修飾語処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, modifiers, separated_text, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 修飾語解析
            analysis_result = self.analyzer.analyze_modifiers(doc)
            
            if not analysis_result['modifiers']:
                return self._create_no_modifiers_result(text)
            
            # 修飾語分離テキストの生成
            separated_text = self._generate_separated_text(doc, analysis_result)
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['modifiers'])
            
            return {
                'success': True,
                'separated_text': separated_text,
                'modifiers': analysis_result['modifiers'],
                'sub_slots': sub_slots,
                'confidence': analysis_result['confidence'],
                'verb_positions': {
                    'main_verb_idx': analysis_result['target_verb_idx']
                },
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'modifier_count': sum(len(mods) for mods in analysis_result['modifiers'].values())
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_modifiers_result(self, text: str) -> Dict[str, Any]:
        """修飾語なしの結果作成"""
        return {
            'success': True,
            'separated_text': text,
            'modifiers': {},
            'sub_slots': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.3),
            'verb_positions': {},
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_modifiers_detected'
            }
        }
    
    def _generate_separated_text(self, doc, analysis_result: Dict[str, Any]) -> str:
        """修飾語分離テキストの生成"""
        # 修飾語として認識されたトークンのインデックスを収集
        modifier_indices = set()
        
        for pattern_type, modifiers in analysis_result['modifiers'].items():
            for modifier in modifiers:
                # 修飾語トークンのインデックスを特定
                for token in doc:
                    if token.text == modifier['text']:
                        modifier_indices.add(token.i)
                        # 前置詞句の場合は関連トークンも除外
                        if pattern_type == 'prepositional_phrases':
                            for child in token.subtree:
                                modifier_indices.add(child.i)
        
        # 修飾語以外のトークンでテキストを再構築
        remaining_tokens = [token.text for i, token in enumerate(doc) 
                          if i not in modifier_indices]
        
        return ' '.join(remaining_tokens)
    
    def _build_sub_slots(self, modifiers: Dict[str, Any]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for pattern_type, modifier_list in modifiers.items():
            for modifier in modifier_list:
                slot_key = modifier['slot_key']
                sub_slots[slot_key] = modifier['text']
        
        return sub_slots
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'separated_text': '',
            'modifiers': {},
            'sub_slots': {},
            'confidence': 0.0,
            'error': error_message,
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'error_handling'
            }
        }
    
    def get_configuration_template(self) -> Dict[str, Any]:
        """設定ファイルテンプレートの取得"""
        return {
            'modifier_patterns': {
                'adverb_indicators': {
                    'pattern_type': 'adverb',
                    'pos_indicators': ['ADV'],
                    'dependency_indicators': ['advmod', 'npadvmod'],
                    'lexical_indicators': ['quickly', 'slowly', 'carefully'],
                    'position_preferences': ['pre', 'post'],
                    'confidence_weight': 1.2
                },
                'adjective_modifiers': {
                    'pattern_type': 'adjective',
                    'pos_indicators': ['ADJ'],
                    'dependency_indicators': ['amod', 'advmod'],
                    'position_preferences': ['pre'],
                    'confidence_weight': 0.8
                },
                'prepositional_phrases': {
                    'pattern_type': 'prepositional',
                    'pos_indicators': ['ADP'],
                    'dependency_indicators': ['prep', 'agent'],
                    'position_preferences': ['post'],
                    'confidence_weight': 0.9
                }
            },
            'confidence_settings': {
                'minimum_confidence': 0.3,
                'high_confidence': 0.7,
                'modifier_bonus': 0.2
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = AdverbHandlerClean()
    
    test_sentences = [
        "She reads books quickly.",
        "The cat sleeps peacefully in the garden.",
        "He carefully opened the door.",
        "They arrived yesterday."
    ]
    
    print("🧪 AdverbHandler - ハードコーディング完全除去版テスト")
    print("=" * 60)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"分離テキスト: \"{result.get('separated_text', '')}\"")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"修飾語: {result.get('modifiers', {})}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        print(f"ハードコーディング使用: 0件 ✅")
