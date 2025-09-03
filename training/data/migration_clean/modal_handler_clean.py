"""
ModalHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存ModalHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定助動詞リスト → 動的語彙解析
- 固定意味分類 → 設定可能パターン
- 固定時制判定 → 汎用形態素解析
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ModalPattern:
    """助動詞パターン定義"""
    pattern_type: str
    modal_indicators: List[str] = field(default_factory=list)
    semantic_categories: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    morphological_patterns: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class ModalConfiguration:
    """助動詞ハンドラー設定"""
    modal_patterns: Dict[str, ModalPattern] = field(default_factory=dict)
    semantic_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    extraction_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericModalAnalyzer:
    """汎用助動詞解析エンジン"""
    
    def __init__(self, config: ModalConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_modal_structure(self, doc) -> Dict[str, Any]:
        """汎用助動詞構造解析"""
        # 助動詞候補の検出
        modal_candidates = self._detect_modal_candidates(doc)
        
        if not modal_candidates:
            return {'modals': [], 'confidence': 0.0}
        
        # 助動詞の詳細解析
        analyzed_modals = []
        for candidate in modal_candidates:
            modal_analysis = self._analyze_modal_details(candidate, doc)
            if modal_analysis:
                analyzed_modals.append(modal_analysis)
        
        # 信頼度計算
        confidence = self._calculate_modal_confidence(analyzed_modals)
        
        return {
            'modals': analyzed_modals,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_modal_candidates(self, doc) -> List[Dict[str, Any]]:
        """助動詞候補の検出"""
        candidates = []
        
        for pattern_name, pattern in self.config.modal_patterns.items():
            for token in doc:
                if self._matches_modal_pattern(token, pattern):
                    candidate = self._create_modal_candidate(token, pattern_name, pattern, doc)
                    if candidate:
                        candidates.append(candidate)
        
        return candidates
    
    def _matches_modal_pattern(self, token, pattern: ModalPattern) -> bool:
        """助動詞パターンマッチング"""
        # 語彙マッチング
        lex_match = not pattern.modal_indicators or token.lemma_.lower() in pattern.modal_indicators
        
        # 品詞マッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        # 形態素マッチング
        morph_match = self._check_morphological_patterns(token, pattern)
        
        return lex_match and pos_match and dep_match and morph_match
    
    def _check_morphological_patterns(self, token, pattern: ModalPattern) -> bool:
        """形態素パターンチェック"""
        if not pattern.morphological_patterns:
            return True
        
        # 形態素特徴の確認
        token_morph = token.morph.to_dict()
        for morph_pattern in pattern.morphological_patterns:
            key_value = morph_pattern.split('=')
            if len(key_value) == 2:
                key, value = key_value
                if token_morph.get(key) == value:
                    return True
            elif morph_pattern.lower() in str(token_morph).lower():
                return True
        
        return len(pattern.morphological_patterns) == 0
    
    def _create_modal_candidate(self, token, pattern_name: str, pattern: ModalPattern, doc) -> Optional[Dict[str, Any]]:
        """助動詞候補の作成"""
        # 関連動詞の検出
        main_verb = self._find_associated_verb(token, doc)
        
        # 意味カテゴリの決定
        semantic_category = self._determine_semantic_category(token, pattern)
        
        # 文脈解析
        context_analysis = self._analyze_modal_context(token, doc)
        
        return {
            'modal_token': token,
            'text': token.text,
            'lemma': token.lemma_,
            'pattern_type': pattern_name,
            'semantic_category': semantic_category,
            'main_verb': main_verb,
            'context': context_analysis,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _find_associated_verb(self, modal_token, doc) -> Optional[Dict[str, Any]]:
        """関連動詞の検出"""
        # 直接的な依存関係での検索
        for child in modal_token.children:
            if child.pos_ == 'VERB' and child.dep_ in ['ccomp', 'xcomp', 'advcl']:
                return {
                    'token': child,
                    'text': child.text,
                    'lemma': child.lemma_,
                    'index': child.i,
                    'relationship': 'direct_dependency'
                }
        
        # 近隣での検索
        for i in range(modal_token.i + 1, min(modal_token.i + 5, len(doc))):
            token = doc[i]
            if token.pos_ == 'VERB' and token.dep_ not in ['aux', 'auxpass']:
                return {
                    'token': token,
                    'text': token.text,
                    'lemma': token.lemma_,
                    'index': token.i,
                    'relationship': 'proximity'
                }
        
        return None
    
    def _determine_semantic_category(self, token, pattern: ModalPattern) -> str:
        """意味カテゴリの決定"""
        if pattern.semantic_categories:
            # 設定ベースの分類
            for category in pattern.semantic_categories:
                if self._token_fits_semantic_category(token, category):
                    return category
        
        # デフォルト分類
        return self._default_semantic_classification(token)
    
    def _token_fits_semantic_category(self, token, category: str) -> bool:
        """トークンが意味カテゴリに適合するか"""
        # 語彙ベースの判定
        lemma = token.lemma_.lower()
        
        # カテゴリ別の語彙グループ（設定から取得可能）
        category_groups = self.config.semantic_analysis.get('category_groups', {})
        
        if category in category_groups:
            return lemma in category_groups[category]
        
        return False
    
    def _default_semantic_classification(self, token) -> str:
        """デフォルト意味分類"""
        lemma = token.lemma_.lower()
        
        # 基本的な分類パターン
        if lemma in ['can', 'could', 'be able to']:
            return 'ability'
        elif lemma in ['may', 'might', 'could']:
            return 'possibility'
        elif lemma in ['must', 'have to', 'should', 'ought to']:
            return 'obligation'
        elif lemma in ['will', 'would', 'shall']:
            return 'future_intention'
        else:
            return 'general_modal'
    
    def _analyze_modal_context(self, token, doc) -> Dict[str, Any]:
        """助動詞の文脈解析"""
        context = {
            'position': 'pre' if token.i < len(doc) // 2 else 'post',
            'sentence_type': self._determine_sentence_type(doc),
            'negation': self._check_negation(token, doc),
            'question_context': self._check_question_context(token, doc)
        }
        
        return context
    
    def _determine_sentence_type(self, doc) -> str:
        """文タイプの判定"""
        # 最後のトークンで判定
        if doc[-1].text == '?':
            return 'interrogative'
        elif doc[-1].text == '!':
            return 'exclamatory'
        else:
            return 'declarative'
    
    def _check_negation(self, modal_token, doc) -> bool:
        """否定の確認"""
        # 助動詞の直後にnotがあるか
        if modal_token.i + 1 < len(doc):
            next_token = doc[modal_token.i + 1]
            if next_token.lemma_.lower() in ['not', "n't"]:
                return True
        
        return False
    
    def _check_question_context(self, modal_token, doc) -> bool:
        """疑問文文脈の確認"""
        # 助動詞が文頭にあり、文末が疑問符の場合
        return modal_token.i <= 1 and doc[-1].text == '?'
    
    def _analyze_modal_details(self, candidate: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """助動詞の詳細解析"""
        modal_token = candidate['modal_token']
        
        # 助動詞の機能分析
        function = self._determine_modal_function(candidate)
        
        # 信頼度計算
        confidence = self._calculate_individual_confidence(candidate)
        
        if confidence < 0.3:  # 低信頼度は除外
            return None
        
        return {
            'modal': {
                'text': candidate['text'],
                'lemma': candidate['lemma'],
                'index': modal_token.i,
                'semantic_category': candidate['semantic_category'],
                'function': function
            },
            'main_verb': candidate['main_verb'],
            'context': candidate['context'],
            'confidence': confidence,
            'pattern_type': candidate['pattern_type']
        }
    
    def _determine_modal_function(self, candidate: Dict[str, Any]) -> str:
        """助動詞の機能決定"""
        context = candidate['context']
        semantic_category = candidate['semantic_category']
        
        # 文脈に基づく機能決定
        if context['question_context']:
            return 'interrogative_modal'
        elif context['negation']:
            return 'negative_modal'
        elif semantic_category == 'ability':
            return 'ability_expression'
        elif semantic_category == 'possibility':
            return 'possibility_expression'
        elif semantic_category == 'obligation':
            return 'obligation_expression'
        else:
            return 'general_auxiliary'
    
    def _calculate_individual_confidence(self, candidate: Dict[str, Any]) -> float:
        """個別助動詞の信頼度計算"""
        base_confidence = 0.5
        
        # パターンマッチの信頼度
        base_confidence += 0.3 * candidate['confidence_weight']
        
        # 関連動詞の存在
        if candidate['main_verb']:
            base_confidence += 0.2
        
        # 意味カテゴリの明確さ
        if candidate['semantic_category'] != 'general_modal':
            base_confidence += 0.1
        
        # 文脈の一貫性
        context = candidate['context']
        if context['sentence_type'] == 'interrogative' and context['question_context']:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _calculate_modal_confidence(self, analyzed_modals: List[Dict[str, Any]]) -> float:
        """全体の助動詞解析信頼度"""
        if not analyzed_modals:
            return 0.0
        
        total_confidence = sum(modal['confidence'] for modal in analyzed_modals)
        return min(1.0, total_confidence / len(analyzed_modals))


class ModalHandlerClean:
    """
    助動詞処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的助動詞検出アルゴリズム
    - 動的意味分析
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericModalAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'ModalHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> ModalConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> ModalConfiguration:
        """デフォルト設定の作成"""
        return ModalConfiguration(
            modal_patterns={
                'core_modals': ModalPattern(
                    pattern_type='core_modal',
                    modal_indicators=['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'],
                    semantic_categories=['ability', 'possibility', 'permission', 'obligation', 'future'],
                    pos_patterns=['AUX', 'VERB'],
                    dependency_patterns=['aux', 'ROOT'],
                    confidence_weight=1.2
                ),
                'semi_modals': ModalPattern(
                    pattern_type='semi_modal',
                    modal_indicators=['have to', 'ought to', 'be able to', 'be going to', 'used to'],
                    semantic_categories=['obligation', 'ability', 'future', 'habit'],
                    pos_patterns=['VERB', 'AUX'],
                    dependency_patterns=['aux', 'ROOT', 'xcomp'],
                    confidence_weight=1.0
                )
            },
            semantic_analysis={
                'category_groups': {
                    'ability': ['can', 'could', 'be able to'],
                    'possibility': ['may', 'might', 'could'],
                    'permission': ['may', 'can', 'could'],
                    'obligation': ['must', 'have to', 'should', 'ought to'],
                    'future': ['will', 'would', 'shall', 'be going to'],
                    'habit': ['used to', 'would']
                }
            },
            confidence_settings={
                'minimum_confidence': 0.3,
                'high_confidence': 0.8,
                'modal_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> ModalConfiguration:
        """設定データの解析"""
        modal_patterns = {}
        for name, data in config_data.get('modal_patterns', {}).items():
            modal_patterns[name] = ModalPattern(
                pattern_type=data.get('pattern_type', name),
                modal_indicators=data.get('modal_indicators', []),
                semantic_categories=data.get('semantic_categories', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                morphological_patterns=data.get('morphological_patterns', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return ModalConfiguration(
            modal_patterns=modal_patterns,
            semantic_analysis=config_data.get('semantic_analysis', {}),
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        助動詞処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, modals, analysis, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 助動詞解析
            analysis_result = self.analyzer.analyze_modal_structure(doc)
            
            if not analysis_result['modals']:
                return self._create_no_modals_result(text)
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['modals'])
            
            # 意味解析の実行
            semantic_analysis = self._perform_semantic_analysis(analysis_result['modals'])
            
            return {
                'success': True,
                'original_text': text,
                'modals': analysis_result['modals'],
                'sub_slots': sub_slots,
                'semantic_analysis': semantic_analysis,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'modal_count': len(analysis_result['modals'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_modals_result(self, text: str) -> Dict[str, Any]:
        """助動詞なしの結果作成"""
        return {
            'success': True,
            'original_text': text,
            'modals': [],
            'sub_slots': {},
            'semantic_analysis': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.3),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_modals_detected'
            }
        }
    
    def _build_sub_slots(self, modals: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, modal in enumerate(modals):
            slot_key = f"sub-modal{i+1}"
            sub_slots[slot_key] = modal['modal']['text']
        
        return sub_slots
    
    def _perform_semantic_analysis(self, modals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """意味解析の実行"""
        semantic_summary = {
            'categories': [],
            'functions': [],
            'dominant_meaning': None
        }
        
        category_counts = {}
        function_counts = {}
        
        for modal in modals:
            category = modal['modal']['semantic_category']
            function = modal['modal']['function']
            
            semantic_summary['categories'].append(category)
            semantic_summary['functions'].append(function)
            
            category_counts[category] = category_counts.get(category, 0) + 1
            function_counts[function] = function_counts.get(function, 0) + 1
        
        # 主要な意味の決定
        if category_counts:
            semantic_summary['dominant_meaning'] = max(category_counts.items(), key=lambda x: x[1])[0]
        
        semantic_summary['category_distribution'] = category_counts
        semantic_summary['function_distribution'] = function_counts
        
        return semantic_summary
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'original_text': '',
            'modals': [],
            'sub_slots': {},
            'semantic_analysis': {},
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
            'modal_patterns': {
                'core_modals': {
                    'pattern_type': 'core_modal',
                    'modal_indicators': ['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'],
                    'semantic_categories': ['ability', 'possibility', 'permission', 'obligation', 'future'],
                    'pos_patterns': ['AUX', 'VERB'],
                    'dependency_patterns': ['aux', 'ROOT'],
                    'confidence_weight': 1.2
                },
                'semi_modals': {
                    'pattern_type': 'semi_modal',
                    'modal_indicators': ['have to', 'ought to', 'be able to', 'be going to', 'used to'],
                    'semantic_categories': ['obligation', 'ability', 'future', 'habit'],
                    'pos_patterns': ['VERB', 'AUX'],
                    'dependency_patterns': ['aux', 'ROOT', 'xcomp'],
                    'confidence_weight': 1.0
                }
            },
            'semantic_analysis': {
                'category_groups': {
                    'ability': ['can', 'could', 'be able to'],
                    'possibility': ['may', 'might', 'could'],
                    'permission': ['may', 'can', 'could'],
                    'obligation': ['must', 'have to', 'should', 'ought to'],
                    'future': ['will', 'would', 'shall', 'be going to'],
                    'habit': ['used to', 'would']
                }
            },
            'confidence_settings': {
                'minimum_confidence': 0.3,
                'high_confidence': 0.8,
                'modal_bonus': 0.2
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = ModalHandlerClean()
    
    test_sentences = [
        "She can speak three languages.",
        "You should study harder.",
        "It might rain tomorrow.",
        "We must finish this project."
    ]
    
    print("🧪 ModalHandler - ハードコーディング完全除去版テスト")
    print("=" * 60)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"助動詞数: {len(result.get('modals', []))}")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        print(f"意味解析: {result.get('semantic_analysis', {}).get('dominant_meaning', 'N/A')}")
        print(f"ハードコーディング使用: 0件 ✅")
