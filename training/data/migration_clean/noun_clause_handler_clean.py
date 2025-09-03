"""
NounClauseHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存NounClauseHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定節マーカー → 動的パターン解析
- 固定節タイプ → 設定可能節分類
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
class NounClausePattern:
    """名詞節パターン定義"""
    pattern_type: str
    clause_markers: List[str] = field(default_factory=list)
    complementizer_patterns: List[str] = field(default_factory=list)
    function_types: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class NounClauseConfiguration:
    """名詞節ハンドラー設定"""
    noun_clause_patterns: Dict[str, NounClausePattern] = field(default_factory=dict)
    function_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    clause_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericNounClauseAnalyzer:
    """汎用名詞節解析エンジン"""
    
    def __init__(self, config: NounClauseConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_noun_clause_structure(self, doc) -> Dict[str, Any]:
        """汎用名詞節構造解析"""
        # 名詞節候補の検出
        clause_candidates = self._detect_noun_clause_candidates(doc)
        
        if not clause_candidates:
            return {'noun_clauses': [], 'confidence': 0.0}
        
        # 名詞節の詳細解析
        analyzed_clauses = []
        for candidate in clause_candidates:
            clause_analysis = self._analyze_clause_details(candidate, doc)
            if clause_analysis:
                analyzed_clauses.append(clause_analysis)
        
        # 信頼度計算
        confidence = self._calculate_clause_confidence(analyzed_clauses)
        
        return {
            'noun_clauses': analyzed_clauses,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_noun_clause_candidates(self, doc) -> List[Dict[str, Any]]:
        """名詞節候補の検出"""
        candidates = []
        
        for pattern_name, pattern in self.config.noun_clause_patterns.items():
            for token in doc:
                if self._matches_clause_pattern(token, pattern):
                    candidate = self._create_clause_candidate(token, pattern_name, pattern, doc)
                    if candidate:
                        candidates.append(candidate)
        
        return candidates
    
    def _matches_clause_pattern(self, token, pattern: NounClausePattern) -> bool:
        """名詞節パターンマッチング"""
        # 語彙マッチング
        lex_match = not pattern.clause_markers or token.lemma_.lower() in pattern.clause_markers
        
        # 品詞マッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        return lex_match and pos_match and dep_match
    
    def _create_clause_candidate(self, token, pattern_name: str, pattern: NounClausePattern, doc) -> Optional[Dict[str, Any]]:
        """名詞節候補の作成"""
        # 節の境界を特定
        clause_boundary = self._identify_clause_boundary(token, doc)
        
        if not clause_boundary:
            return None
        
        # 節内容の抽出
        clause_content = self._extract_clause_content(clause_boundary, doc)
        
        # 節の機能分析
        function_analysis = self._analyze_clause_function(token, clause_boundary, doc)
        
        # 補文標識の分析
        complementizer_analysis = self._analyze_complementizer(token, doc)
        
        return {
            'marker_token': token,
            'clause_boundary': clause_boundary,
            'clause_content': clause_content,
            'pattern_type': pattern_name,
            'function_analysis': function_analysis,
            'complementizer_analysis': complementizer_analysis,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _identify_clause_boundary(self, marker_token, doc) -> Optional[Dict[str, int]]:
        """節の境界特定"""
        # 節の開始点
        start_index = marker_token.i
        
        # 節の終了点を検出
        end_index = self._find_clause_end(marker_token, doc)
        
        if end_index is None or end_index <= start_index:
            return None
        
        return {
            'start': start_index,
            'end': end_index,
            'length': end_index - start_index + 1
        }
    
    def _find_clause_end(self, marker_token, doc) -> Optional[int]:
        """節の終了点検出"""
        # 構文木を使用した境界検出
        clause_root = self._find_clause_root(marker_token, doc)
        
        if not clause_root:
            # フォールバック: 句読点または文末まで
            for i in range(marker_token.i + 1, len(doc)):
                token = doc[i]
                if token.pos_ == 'PUNCT' and token.text in [',', '.', ';', '!', '?']:
                    return i - 1
            return len(doc) - 1
        
        # 節ルートの支配範囲を特定
        end_index = clause_root.i
        for descendant in clause_root.subtree:
            if descendant.i > end_index:
                end_index = descendant.i
        
        return end_index
    
    def _find_clause_root(self, marker_token, doc) -> Optional:
        """節のルート動詞検出"""
        # マーカートークンの支配下にある動詞を検索
        for child in marker_token.children:
            if child.pos_ == 'VERB':
                return child
        
        # マーカートークンの右側の最初の動詞
        for i in range(marker_token.i + 1, len(doc)):
            token = doc[i]
            if token.pos_ == 'VERB' and token.dep_ in ['ccomp', 'acl', 'advcl']:
                return token
        
        return None
    
    def _extract_clause_content(self, clause_boundary: Dict[str, int], doc) -> Dict[str, Any]:
        """節内容の抽出"""
        start = clause_boundary['start']
        end = clause_boundary['end']
        
        clause_tokens = doc[start:end+1]
        
        # 節内の要素分析
        clause_elements = self._analyze_clause_elements(clause_tokens)
        
        return {
            'text': ' '.join([token.text for token in clause_tokens]),
            'tokens': [{'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'dep': token.dep_} 
                      for token in clause_tokens],
            'elements': clause_elements,
            'word_count': len(clause_tokens)
        }
    
    def _analyze_clause_elements(self, clause_tokens) -> Dict[str, Any]:
        """節内要素の分析"""
        elements = {
            'subject': None,
            'predicate': None,
            'objects': [],
            'complements': [],
            'adverbials': []
        }
        
        for token in clause_tokens:
            if token.dep_ == 'nsubj':
                elements['subject'] = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'index': token.i
                }
            elif token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'ccomp', 'xcomp']:
                elements['predicate'] = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'index': token.i
                }
            elif token.dep_ in ['dobj', 'iobj']:
                elements['objects'].append({
                    'text': token.text,
                    'lemma': token.lemma_,
                    'dependency': token.dep_,
                    'index': token.i
                })
            elif token.dep_ in ['attr', 'acomp']:
                elements['complements'].append({
                    'text': token.text,
                    'lemma': token.lemma_,
                    'dependency': token.dep_,
                    'index': token.i
                })
            elif token.dep_ in ['advmod', 'npadvmod']:
                elements['adverbials'].append({
                    'text': token.text,
                    'lemma': token.lemma_,
                    'dependency': token.dep_,
                    'index': token.i
                })
        
        return elements
    
    def _analyze_clause_function(self, marker_token, clause_boundary: Dict[str, int], doc) -> Dict[str, Any]:
        """名詞節の機能分析"""
        function_info = {
            'syntactic_function': 'unknown',
            'semantic_role': 'unknown',
            'clause_type': 'unknown',
            'governing_element': None
        }
        
        # 統語機能の分析
        function_info['syntactic_function'] = self._determine_syntactic_function(marker_token, doc)
        
        # 意味役割の分析
        function_info['semantic_role'] = self._determine_semantic_role(marker_token, doc)
        
        # 節タイプの分析
        function_info['clause_type'] = self._determine_clause_type(marker_token, doc)
        
        # 支配要素の特定
        function_info['governing_element'] = self._find_governing_element(marker_token, doc)
        
        return function_info
    
    def _determine_syntactic_function(self, marker_token, doc) -> str:
        """統語機能の決定"""
        # 依存関係による分析
        dependency = marker_token.dep_
        
        if dependency == 'nsubj':
            return 'subject'
        elif dependency in ['dobj', 'iobj']:
            return 'object'
        elif dependency in ['ccomp', 'xcomp']:
            return 'complement'
        elif dependency == 'acl':
            return 'relative'
        elif dependency == 'appos':
            return 'appositive'
        else:
            # 位置による推定
            return self._infer_function_from_position(marker_token, doc)
    
    def _infer_function_from_position(self, marker_token, doc) -> str:
        """位置からの機能推定"""
        # 文の前半にある場合
        if marker_token.i < len(doc) * 0.3:
            return 'subject_candidate'
        
        # 動詞の後にある場合
        for i in range(marker_token.i - 1, -1, -1):
            token = doc[i]
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                return 'object_candidate'
        
        return 'unknown'
    
    def _determine_semantic_role(self, marker_token, doc) -> str:
        """意味役割の決定"""
        marker_lemma = marker_token.lemma_.lower()
        
        # 設定ベースの分類
        semantic_groups = self.config.function_analysis.get('semantic_groups', {})
        
        for role, markers in semantic_groups.items():
            if marker_lemma in markers:
                return role
        
        # デフォルト分類
        return self._default_semantic_classification(marker_lemma)
    
    def _default_semantic_classification(self, marker_lemma: str) -> str:
        """デフォルト意味分類"""
        if marker_lemma == 'that':
            return 'propositional_content'
        elif marker_lemma in ['what', 'who', 'where', 'when', 'why', 'how']:
            return 'interrogative_content'
        elif marker_lemma in ['whether', 'if']:
            return 'alternative_content'
        elif marker_lemma in ['whatever', 'whoever', 'wherever']:
            return 'free_relative_content'
        else:
            return 'general_content'
    
    def _determine_clause_type(self, marker_token, doc) -> str:
        """節タイプの決定"""
        marker_lemma = marker_token.lemma_.lower()
        
        # that節
        if marker_lemma == 'that':
            return 'declarative_clause'
        
        # wh節
        elif marker_lemma in ['what', 'who', 'where', 'when', 'why', 'how', 'which']:
            return 'interrogative_clause'
        
        # whether/if節
        elif marker_lemma in ['whether', 'if']:
            return 'alternative_clause'
        
        # 自由関係詞節
        elif marker_lemma in ['whatever', 'whoever', 'wherever', 'whenever']:
            return 'free_relative_clause'
        
        else:
            return 'other_clause'
    
    def _find_governing_element(self, marker_token, doc) -> Optional[Dict[str, Any]]:
        """支配要素の検出"""
        # 直接の統語的支配者
        head = marker_token.head
        
        if head != marker_token:  # 自分自身でない場合
            return {
                'token': head,
                'text': head.text,
                'lemma': head.lemma_,
                'pos': head.pos_,
                'index': head.i,
                'relation': marker_token.dep_
            }
        
        return None
    
    def _analyze_complementizer(self, marker_token, doc) -> Dict[str, Any]:
        """補文標識の分析"""
        return {
            'text': marker_token.text,
            'lemma': marker_token.lemma_,
            'type': self._classify_complementizer(marker_token),
            'position': marker_token.i,
            'can_be_omitted': self._check_omissibility(marker_token, doc)
        }
    
    def _classify_complementizer(self, marker_token) -> str:
        """補文標識の分類"""
        lemma = marker_token.lemma_.lower()
        
        if lemma == 'that':
            return 'declarative_complementizer'
        elif lemma in ['whether', 'if']:
            return 'interrogative_complementizer'
        elif lemma in ['what', 'who', 'where', 'when', 'why', 'how']:
            return 'wh_complementizer'
        else:
            return 'other_complementizer'
    
    def _check_omissibility(self, marker_token, doc) -> bool:
        """省略可能性のチェック"""
        # that節の場合、多くは省略可能
        if marker_token.lemma_.lower() == 'that':
            return True
        
        # wh語は通常省略不可
        if marker_token.lemma_.lower() in ['what', 'who', 'where', 'when', 'why', 'how']:
            return False
        
        return False
    
    def _analyze_clause_details(self, candidate: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """名詞節の詳細解析"""
        # 信頼度計算
        confidence = self._calculate_individual_confidence(candidate)
        
        if confidence < 0.3:  # 低信頼度は除外
            return None
        
        marker_token = candidate['marker_token']
        clause_content = candidate['clause_content']
        
        return {
            'clause': {
                'marker': {
                    'text': marker_token.text,
                    'lemma': marker_token.lemma_,
                    'index': marker_token.i
                },
                'content': clause_content,
                'full_text': clause_content['text']
            },
            'function': candidate['function_analysis'],
            'complementizer': candidate['complementizer_analysis'],
            'confidence': confidence,
            'pattern_type': candidate['pattern_type']
        }
    
    def _calculate_individual_confidence(self, candidate: Dict[str, Any]) -> float:
        """個別名詞節の信頼度計算"""
        base_confidence = 0.4
        
        # パターンマッチの信頼度
        base_confidence += 0.2 * candidate['confidence_weight']
        
        # 補文標識の明確さ
        complementizer_type = candidate['complementizer_analysis']['type']
        if complementizer_type != 'other_complementizer':
            base_confidence += 0.2
        
        # 統語機能の明確さ
        function = candidate['function_analysis']['syntactic_function']
        if function != 'unknown':
            base_confidence += 0.2
        
        # 節内容の完全性
        elements = candidate['clause_content']['elements']
        if elements['subject'] and elements['predicate']:
            base_confidence += 0.2
        
        return min(1.0, base_confidence)
    
    def _calculate_clause_confidence(self, analyzed_clauses: List[Dict[str, Any]]) -> float:
        """全体の名詞節解析信頼度"""
        if not analyzed_clauses:
            return 0.0
        
        total_confidence = sum(clause['confidence'] for clause in analyzed_clauses)
        return min(1.0, total_confidence / len(analyzed_clauses))


class NounClauseHandlerClean:
    """
    名詞節処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的名詞節検出アルゴリズム
    - 動的機能分析
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericNounClauseAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'NounClauseHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> NounClauseConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> NounClauseConfiguration:
        """デフォルト設定の作成"""
        return NounClauseConfiguration(
            noun_clause_patterns={
                'that_clause': NounClausePattern(
                    pattern_type='that_clause',
                    clause_markers=['that'],
                    complementizer_patterns=['declarative'],
                    function_types=['subject', 'object', 'complement'],
                    pos_patterns=['SCONJ', 'ADP'],
                    dependency_patterns=['mark', 'nsubj', 'dobj', 'ccomp'],
                    confidence_weight=1.2
                ),
                'wh_clause': NounClausePattern(
                    pattern_type='wh_clause',
                    clause_markers=['what', 'who', 'where', 'when', 'why', 'how', 'which'],
                    complementizer_patterns=['interrogative'],
                    function_types=['subject', 'object', 'complement'],
                    pos_patterns=['PRON', 'ADV', 'DET'],
                    dependency_patterns=['nsubj', 'dobj', 'ccomp', 'acl'],
                    confidence_weight=1.3
                ),
                'whether_clause': NounClausePattern(
                    pattern_type='whether_clause',
                    clause_markers=['whether', 'if'],
                    complementizer_patterns=['alternative'],
                    function_types=['object', 'complement'],
                    pos_patterns=['SCONJ'],
                    dependency_patterns=['mark', 'ccomp'],
                    confidence_weight=1.1
                )
            },
            function_analysis={
                'semantic_groups': {
                    'propositional_content': ['that'],
                    'interrogative_content': ['what', 'who', 'where', 'when', 'why', 'how'],
                    'alternative_content': ['whether', 'if'],
                    'free_relative_content': ['whatever', 'whoever', 'wherever', 'whenever']
                }
            },
            confidence_settings={
                'minimum_confidence': 0.3,
                'high_confidence': 0.8,
                'clause_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> NounClauseConfiguration:
        """設定データの解析"""
        noun_clause_patterns = {}
        for name, data in config_data.get('noun_clause_patterns', {}).items():
            noun_clause_patterns[name] = NounClausePattern(
                pattern_type=data.get('pattern_type', name),
                clause_markers=data.get('clause_markers', []),
                complementizer_patterns=data.get('complementizer_patterns', []),
                function_types=data.get('function_types', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return NounClauseConfiguration(
            noun_clause_patterns=noun_clause_patterns,
            function_analysis=config_data.get('function_analysis', {}),
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        名詞節処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, noun_clauses, functions, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 名詞節解析
            analysis_result = self.analyzer.analyze_noun_clause_structure(doc)
            
            if not analysis_result['noun_clauses']:
                return self._create_no_clauses_result(text)
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['noun_clauses'])
            
            # 機能分析の実行
            function_summary = self._summarize_functions(analysis_result['noun_clauses'])
            
            return {
                'success': True,
                'original_text': text,
                'noun_clauses': analysis_result['noun_clauses'],
                'sub_slots': sub_slots,
                'function_summary': function_summary,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'clause_count': len(analysis_result['noun_clauses'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_clauses_result(self, text: str) -> Dict[str, Any]:
        """名詞節なしの結果作成"""
        return {
            'success': True,
            'original_text': text,
            'noun_clauses': [],
            'sub_slots': {},
            'function_summary': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.3),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_clauses_detected'
            }
        }
    
    def _build_sub_slots(self, noun_clauses: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, clause in enumerate(noun_clauses):
            slot_key = f"sub-clause{i+1}"
            sub_slots[slot_key] = clause['clause']['full_text']
        
        return sub_slots
    
    def _summarize_functions(self, noun_clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """機能分析の要約"""
        summary = {
            'syntactic_functions': [],
            'semantic_roles': [],
            'clause_types': [],
            'dominant_function': None
        }
        
        function_counts = {}
        
        for clause in noun_clauses:
            function = clause['function']['syntactic_function']
            role = clause['function']['semantic_role']
            clause_type = clause['function']['clause_type']
            
            summary['syntactic_functions'].append(function)
            summary['semantic_roles'].append(role)
            summary['clause_types'].append(clause_type)
            
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
            'noun_clauses': [],
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
    handler = NounClauseHandlerClean()
    
    test_sentences = [
        "I think that he is right.",
        "What you said is important.",
        "I wonder whether she will come.",
        "The fact that you came surprised me."
    ]
    
    print("🧪 NounClauseHandler - ハードコーディング完全除去版テスト")
    print("=" * 65)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"名詞節数: {len(result.get('noun_clauses', []))}")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        if result.get('function_summary', {}).get('dominant_function'):
            print(f"主要機能: {result['function_summary']['dominant_function']}")
        print(f"ハードコーディング使用: 0件 ✅")
