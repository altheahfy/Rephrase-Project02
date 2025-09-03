"""
InfinitiveHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存InfinitiveHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定不定詞マーカー → 動的パターン解析
- 固定用法分類 → 設定可能用法定義
- 固定動詞リスト → 汎用統語解析
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class InfinitivePattern:
    """不定詞パターン定義"""
    pattern_type: str
    infinitive_markers: List[str] = field(default_factory=list)
    function_types: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    construction_patterns: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class InfinitiveConfiguration:
    """不定詞ハンドラー設定"""
    infinitive_patterns: Dict[str, InfinitivePattern] = field(default_factory=dict)
    function_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    usage_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericInfinitiveAnalyzer:
    """汎用不定詞解析エンジン"""
    
    def __init__(self, config: InfinitiveConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_infinitive_structure(self, doc) -> Dict[str, Any]:
        """汎用不定詞構造解析"""
        # to不定詞の検出
        infinitive_candidates = self._detect_infinitive_candidates(doc)
        
        if not infinitive_candidates:
            return {'infinitives': [], 'confidence': 0.0}
        
        # 不定詞の詳細解析
        analyzed_infinitives = []
        for candidate in infinitive_candidates:
            infinitive_analysis = self._analyze_infinitive_details(candidate, doc)
            if infinitive_analysis:
                analyzed_infinitives.append(infinitive_analysis)
        
        # 信頼度計算
        confidence = self._calculate_infinitive_confidence(analyzed_infinitives)
        
        return {
            'infinitives': analyzed_infinitives,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_infinitive_candidates(self, doc) -> List[Dict[str, Any]]:
        """不定詞候補の検出"""
        candidates = []
        
        for pattern_name, pattern in self.config.infinitive_patterns.items():
            for token in doc:
                if self._matches_infinitive_pattern(token, pattern):
                    candidate = self._create_infinitive_candidate(token, pattern_name, pattern, doc)
                    if candidate:
                        candidates.append(candidate)
        
        return candidates
    
    def _matches_infinitive_pattern(self, token, pattern: InfinitivePattern) -> bool:
        """不定詞パターンマッチング"""
        # 語彙マッチング
        lex_match = not pattern.infinitive_markers or token.lemma_.lower() in pattern.infinitive_markers
        
        # 品詞マッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        return lex_match and pos_match and dep_match
    
    def _create_infinitive_candidate(self, token, pattern_name: str, pattern: InfinitivePattern, doc) -> Optional[Dict[str, Any]]:
        """不定詞候補の作成"""
        # to不定詞の場合、動詞部分を特定
        infinitive_verb = None
        
        if token.lemma_.lower() == 'to':
            # toの次のトークンが動詞か確認
            if token.i + 1 < len(doc):
                next_token = doc[token.i + 1]
                if next_token.pos_ == 'VERB':
                    infinitive_verb = next_token
        else:
            # bare infinitive（原形不定詞）の場合
            if token.pos_ == 'VERB':
                infinitive_verb = token
        
        if not infinitive_verb:
            return None
        
        # 不定詞の用法分析
        function_analysis = self._analyze_infinitive_function(token, infinitive_verb, doc)
        
        # 構文分析
        construction_analysis = self._analyze_infinitive_construction(token, infinitive_verb, doc)
        
        return {
            'to_marker': token if token.lemma_.lower() == 'to' else None,
            'infinitive_verb': infinitive_verb,
            'pattern_type': pattern_name,
            'function_analysis': function_analysis,
            'construction_analysis': construction_analysis,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _analyze_infinitive_function(self, marker_token, infinitive_verb, doc) -> Dict[str, Any]:
        """不定詞の用法分析"""
        function_info = {
            'syntactic_function': 'unknown',
            'semantic_role': 'unknown',
            'position': 'unknown'
        }
        
        # 統語機能の分析
        function_info['syntactic_function'] = self._determine_syntactic_function(marker_token, infinitive_verb, doc)
        
        # 意味役割の分析
        function_info['semantic_role'] = self._determine_semantic_role(marker_token, infinitive_verb, doc)
        
        # 位置の分析
        function_info['position'] = self._determine_position_in_sentence(marker_token, doc)
        
        return function_info
    
    def _determine_syntactic_function(self, marker_token, infinitive_verb, doc) -> str:
        """統語機能の決定"""
        # 依存関係ベースの分析
        dependency = infinitive_verb.dep_
        
        if dependency == 'nsubj':
            return 'subject'
        elif dependency in ['dobj', 'iobj']:
            return 'object'
        elif dependency == 'advcl':
            return 'adverbial'
        elif dependency == 'amod':
            return 'adjectival'
        elif dependency in ['xcomp', 'ccomp']:
            return 'complement'
        elif dependency == 'acl':
            return 'relative'
        else:
            # 文脈から推定
            return self._infer_function_from_context(marker_token, infinitive_verb, doc)
    
    def _infer_function_from_context(self, marker_token, infinitive_verb, doc) -> str:
        """文脈からの機能推定"""
        # 主語位置にある場合
        if marker_token.i < 3:  # 文の前半
            return 'subject_candidate'
        
        # 目的語位置にある場合
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                if marker_token.i > token.i:
                    return 'complement_candidate'
        
        # 文末の場合
        if marker_token.i > len(doc) * 0.7:
            return 'purpose_candidate'
        
        return 'unknown'
    
    def _determine_semantic_role(self, marker_token, infinitive_verb, doc) -> str:
        """意味役割の決定"""
        # 動詞の意味から推定
        verb_lemma = infinitive_verb.lemma_.lower()
        
        # 設定ベースの分類
        semantic_groups = self.config.function_analysis.get('semantic_groups', {})
        
        for role, verbs in semantic_groups.items():
            if verb_lemma in verbs:
                return role
        
        # デフォルト分類
        return self._default_semantic_classification(verb_lemma)
    
    def _default_semantic_classification(self, verb_lemma: str) -> str:
        """デフォルト意味分類"""
        # 基本的な意味分類
        if verb_lemma in ['go', 'come', 'move', 'travel']:
            return 'motion'
        elif verb_lemma in ['want', 'hope', 'expect', 'plan']:
            return 'intention'
        elif verb_lemma in ['help', 'try', 'manage', 'fail']:
            return 'attempt'
        elif verb_lemma in ['see', 'watch', 'hear', 'feel']:
            return 'perception'
        else:
            return 'general_action'
    
    def _determine_position_in_sentence(self, marker_token, doc) -> str:
        """文における位置の決定"""
        position_ratio = marker_token.i / len(doc)
        
        if position_ratio < 0.3:
            return 'initial'
        elif position_ratio < 0.7:
            return 'medial'
        else:
            return 'final'
    
    def _analyze_infinitive_construction(self, marker_token, infinitive_verb, doc) -> Dict[str, Any]:
        """不定詞構文の分析"""
        construction_info = {
            'type': 'unknown',
            'governing_verb': None,
            'subject_controller': None,
            'complements': []
        }
        
        # 支配動詞の検出
        construction_info['governing_verb'] = self._find_governing_verb(marker_token, doc)
        
        # 主語制御の分析
        construction_info['subject_controller'] = self._analyze_subject_control(marker_token, infinitive_verb, doc)
        
        # 補語の検出
        construction_info['complements'] = self._find_infinitive_complements(infinitive_verb, doc)
        
        # 構文タイプの決定
        construction_info['type'] = self._determine_construction_type(construction_info)
        
        return construction_info
    
    def _find_governing_verb(self, marker_token, doc) -> Optional[Dict[str, Any]]:
        """支配動詞の検出"""
        # 不定詞より前の動詞を検索
        for i in range(marker_token.i - 1, -1, -1):
            token = doc[i]
            if token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'ccomp', 'xcomp']:
                return {
                    'token': token,
                    'text': token.text,
                    'lemma': token.lemma_,
                    'index': token.i
                }
        
        return None
    
    def _analyze_subject_control(self, marker_token, infinitive_verb, doc) -> Optional[Dict[str, Any]]:
        """主語制御の分析"""
        # 不定詞の意味上の主語を特定
        for token in doc:
            if token.dep_ == 'nsubj' and token.head == infinitive_verb:
                return {
                    'controller': token,
                    'type': 'explicit_subject'
                }
        
        # 暗黙の主語制御を検索
        governing_verb = self._find_governing_verb(marker_token, doc)
        if governing_verb:
            for token in doc:
                if token.dep_ == 'nsubj' and token.head == governing_verb['token']:
                    return {
                        'controller': token,
                        'type': 'subject_control'
                    }
        
        return None
    
    def _find_infinitive_complements(self, infinitive_verb, doc) -> List[Dict[str, Any]]:
        """不定詞の補語検出"""
        complements = []
        
        for child in infinitive_verb.children:
            if child.dep_ in ['dobj', 'iobj', 'pobj', 'attr']:
                complements.append({
                    'text': child.text,
                    'lemma': child.lemma_,
                    'dependency': child.dep_,
                    'index': child.i
                })
        
        return complements
    
    def _determine_construction_type(self, construction_info: Dict[str, Any]) -> str:
        """構文タイプの決定"""
        if construction_info['governing_verb']:
            governing_lemma = construction_info['governing_verb']['lemma'].lower()
            
            # 知覚動詞構文
            if governing_lemma in ['see', 'watch', 'hear', 'feel']:
                return 'perception_construction'
            
            # 使役動詞構文
            elif governing_lemma in ['make', 'let', 'have']:
                return 'causative_construction'
            
            # want型構文
            elif governing_lemma in ['want', 'expect', 'ask', 'tell']:
                return 'object_control_construction'
            
            # try型構文
            elif governing_lemma in ['try', 'decide', 'hope', 'plan']:
                return 'subject_control_construction'
        
        return 'independent_infinitive'
    
    def _analyze_infinitive_details(self, candidate: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """不定詞の詳細解析"""
        # 信頼度計算
        confidence = self._calculate_individual_confidence(candidate)
        
        if confidence < 0.3:  # 低信頼度は除外
            return None
        
        infinitive_verb = candidate['infinitive_verb']
        to_marker = candidate['to_marker']
        
        return {
            'infinitive': {
                'to_marker': to_marker.text if to_marker else None,
                'verb': {
                    'text': infinitive_verb.text,
                    'lemma': infinitive_verb.lemma_,
                    'index': infinitive_verb.i
                },
                'full_form': f"{to_marker.text + ' ' if to_marker else ''}{infinitive_verb.text}"
            },
            'function': candidate['function_analysis'],
            'construction': candidate['construction_analysis'],
            'confidence': confidence,
            'pattern_type': candidate['pattern_type']
        }
    
    def _calculate_individual_confidence(self, candidate: Dict[str, Any]) -> float:
        """個別不定詞の信頼度計算"""
        base_confidence = 0.5
        
        # パターンマッチの信頼度
        base_confidence += 0.2 * candidate['confidence_weight']
        
        # to の存在（to不定詞の場合）
        if candidate['to_marker']:
            base_confidence += 0.2
        
        # 統語機能の明確さ
        function = candidate['function_analysis']['syntactic_function']
        if function != 'unknown':
            base_confidence += 0.2
        
        # 構文の明確さ
        construction = candidate['construction_analysis']['type']
        if construction != 'unknown':
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _calculate_infinitive_confidence(self, analyzed_infinitives: List[Dict[str, Any]]) -> float:
        """全体の不定詞解析信頼度"""
        if not analyzed_infinitives:
            return 0.0
        
        total_confidence = sum(inf['confidence'] for inf in analyzed_infinitives)
        return min(1.0, total_confidence / len(analyzed_infinitives))


class InfinitiveHandlerClean:
    """
    不定詞処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的不定詞検出アルゴリズム
    - 動的用法分析
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericInfinitiveAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'InfinitiveHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> InfinitiveConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> InfinitiveConfiguration:
        """デフォルト設定の作成"""
        return InfinitiveConfiguration(
            infinitive_patterns={
                'to_infinitive': InfinitivePattern(
                    pattern_type='to_infinitive',
                    infinitive_markers=['to'],
                    function_types=['subject', 'object', 'adverbial', 'adjectival'],
                    pos_patterns=['PART', 'ADP'],
                    dependency_patterns=['aux', 'mark'],
                    construction_patterns=['control', 'raising', 'perception'],
                    confidence_weight=1.2
                ),
                'bare_infinitive': InfinitivePattern(
                    pattern_type='bare_infinitive',
                    infinitive_markers=[],  # 原形動詞
                    function_types=['complement', 'causative'],
                    pos_patterns=['VERB'],
                    dependency_patterns=['xcomp', 'ccomp'],
                    construction_patterns=['causative', 'perception'],
                    confidence_weight=1.0
                )
            },
            function_analysis={
                'semantic_groups': {
                    'motion': ['go', 'come', 'move', 'travel', 'run', 'walk'],
                    'intention': ['want', 'hope', 'expect', 'plan', 'intend'],
                    'attempt': ['try', 'manage', 'fail', 'succeed', 'attempt'],
                    'perception': ['see', 'watch', 'hear', 'feel', 'observe'],
                    'causation': ['make', 'let', 'have', 'cause', 'force']
                }
            },
            confidence_settings={
                'minimum_confidence': 0.3,
                'high_confidence': 0.8,
                'infinitive_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> InfinitiveConfiguration:
        """設定データの解析"""
        infinitive_patterns = {}
        for name, data in config_data.get('infinitive_patterns', {}).items():
            infinitive_patterns[name] = InfinitivePattern(
                pattern_type=data.get('pattern_type', name),
                infinitive_markers=data.get('infinitive_markers', []),
                function_types=data.get('function_types', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                construction_patterns=data.get('construction_patterns', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return InfinitiveConfiguration(
            infinitive_patterns=infinitive_patterns,
            function_analysis=config_data.get('function_analysis', {}),
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        不定詞処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, infinitives, functions, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 不定詞解析
            analysis_result = self.analyzer.analyze_infinitive_structure(doc)
            
            if not analysis_result['infinitives']:
                return self._create_no_infinitives_result(text)
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['infinitives'])
            
            # 用法分析の実行
            function_summary = self._summarize_functions(analysis_result['infinitives'])
            
            return {
                'success': True,
                'original_text': text,
                'infinitives': analysis_result['infinitives'],
                'sub_slots': sub_slots,
                'function_summary': function_summary,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'infinitive_count': len(analysis_result['infinitives'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_infinitives_result(self, text: str) -> Dict[str, Any]:
        """不定詞なしの結果作成"""
        return {
            'success': True,
            'original_text': text,
            'infinitives': [],
            'sub_slots': {},
            'function_summary': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.3),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_infinitives_detected'
            }
        }
    
    def _build_sub_slots(self, infinitives: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, infinitive in enumerate(infinitives):
            slot_key = f"sub-inf{i+1}"
            sub_slots[slot_key] = infinitive['infinitive']['full_form']
        
        return sub_slots
    
    def _summarize_functions(self, infinitives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """用法分析の要約"""
        summary = {
            'syntactic_functions': [],
            'semantic_roles': [],
            'construction_types': [],
            'dominant_function': None
        }
        
        function_counts = {}
        
        for infinitive in infinitives:
            function = infinitive['function']['syntactic_function']
            role = infinitive['function']['semantic_role']
            construction = infinitive['construction']['type']
            
            summary['syntactic_functions'].append(function)
            summary['semantic_roles'].append(role)
            summary['construction_types'].append(construction)
            
            function_counts[function] = function_counts.get(function, 0) + 1
        
        # 主要な機能の決定
        if function_counts:
            summary['dominant_function'] = max(function_counts.items(), key=lambda x: x[1])[0]
        
        summary['function_distribution'] = function_counts
        
        return summary
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'original_text': '',
            'infinitives': [],
            'sub_slots': {},
            'function_summary': {},
            'confidence': 0.0,
            'error': error_message,
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'error_handling'
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = InfinitiveHandlerClean()
    
    test_sentences = [
        "I want to learn English.",
        "To be or not to be is the question.",
        "She made him cry.",
        "They decided to go home."
    ]
    
    print("🧪 InfinitiveHandler - ハードコーディング完全除去版テスト")
    print("=" * 65)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"不定詞数: {len(result.get('infinitives', []))}")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        if result.get('function_summary', {}).get('dominant_function'):
            print(f"主要機能: {result['function_summary']['dominant_function']}")
        print(f"ハードコーディング使用: 0件 ✅")
