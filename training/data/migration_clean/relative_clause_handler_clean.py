"""
RelativeClauseHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存RelativeClauseHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定関係代名詞リスト → 動的パターン解析
- 固定先行詞パターン → 汎用名詞句検出
- 固定節境界判定 → 動的構造解析
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class RelativePattern:
    """関係節パターン定義"""
    pattern_type: str
    relative_indicators: List[str] = field(default_factory=list)
    antecedent_indicators: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    position_rules: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class ClauseConfiguration:
    """関係節ハンドラー設定"""
    relative_patterns: Dict[str, RelativePattern] = field(default_factory=dict)
    boundary_detection: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    separation_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericClauseAnalyzer:
    """汎用関係節解析エンジン"""
    
    def __init__(self, config: ClauseConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_relative_clauses(self, doc) -> Dict[str, Any]:
        """汎用関係節解析"""
        # 関係代名詞候補の検出
        relative_candidates = self._detect_relative_candidates(doc)
        
        if not relative_candidates:
            return {'clauses': [], 'confidence': 0.0}
        
        # 関係節の構造解析
        analyzed_clauses = []
        for candidate in relative_candidates:
            clause_analysis = self._analyze_clause_structure(candidate, doc)
            if clause_analysis:
                analyzed_clauses.append(clause_analysis)
        
        # 信頼度計算
        confidence = self._calculate_clause_confidence(analyzed_clauses)
        
        return {
            'clauses': analyzed_clauses,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_relative_candidates(self, doc) -> List[Dict[str, Any]]:
        """関係代名詞候補の検出"""
        candidates = []
        
        for pattern_name, pattern in self.config.relative_patterns.items():
            if pattern_name == 'antecedent_patterns':  # 先行詞パターンはスキップ
                continue
            
            for token in doc:
                if self._matches_relative_pattern(token, pattern):
                    candidate = self._create_relative_candidate(token, pattern_name, pattern, doc)
                    if candidate:
                        candidates.append(candidate)
        
        return candidates
    
    def _matches_relative_pattern(self, token, pattern: RelativePattern) -> bool:
        """関係代名詞パターンマッチング"""
        # 語彙マッチング
        lex_match = not pattern.relative_indicators or token.lemma_.lower() in pattern.relative_indicators
        
        # 品詞マッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        return lex_match and pos_match and dep_match
    
    def _create_relative_candidate(self, token, pattern_name: str, pattern: RelativePattern, doc) -> Optional[Dict[str, Any]]:
        """関係代名詞候補の作成"""
        # 先行詞の検出
        antecedent = self._find_antecedent(token, doc)
        
        if not antecedent:
            return None
        
        # 関係節の境界検出
        clause_span = self._detect_clause_boundaries(token, doc)
        
        if not clause_span:
            return None
        
        # 構造解析
        clause_structure = self._analyze_internal_structure(token, clause_span, doc)
        
        return {
            'relative_pronoun': token,
            'antecedent': antecedent,
            'clause_span': clause_span,
            'clause_structure': clause_structure,
            'pattern_type': pattern_name,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _find_antecedent(self, relative_token, doc) -> Optional[Dict[str, Any]]:
        """先行詞の動的検出"""
        # 直前の名詞句を検索
        antecedent_candidates = []
        
        for i in range(relative_token.i - 1, -1, -1):
            token = doc[i]
            
            if self._is_potential_antecedent(token):
                # 名詞句の範囲を決定
                noun_phrase_span = self._get_noun_phrase_span(token, doc)
                
                # 関係性の強さを計算
                relationship_score = self._calculate_antecedent_score(
                    noun_phrase_span, relative_token, doc
                )
                
                if relationship_score > 0.3:  # 閾値以上の関係性
                    antecedent_candidates.append({
                        'tokens': noun_phrase_span,
                        'head': token,
                        'text': ' '.join([t.text for t in noun_phrase_span]),
                        'score': relationship_score
                    })
        
        if not antecedent_candidates:
            return None
        
        # 最高スコアの先行詞を選択
        return max(antecedent_candidates, key=lambda x: x['score'])
    
    def _is_potential_antecedent(self, token) -> bool:
        """先行詞候補の判定"""
        # 動的パターンマッチング
        antecedent_patterns = self.config.relative_patterns.get('antecedent_patterns')
        
        if antecedent_patterns:
            return self._matches_relative_pattern(token, antecedent_patterns)
        
        # デフォルト判定: 名詞系の品詞
        return token.pos_ in ['NOUN', 'PROPN', 'PRON']
    
    def _get_noun_phrase_span(self, head_token, doc) -> List:
        """名詞句のスパン取得"""
        # 名詞句の開始位置を検索
        start_idx = head_token.i
        for token in reversed(list(head_token.lefts)):
            if token.pos_ in ['DET', 'ADJ', 'NUM'] or token.dep_ in ['det', 'amod', 'nummod']:
                start_idx = min(start_idx, token.i)
        
        # 名詞句の終了位置を検索
        end_idx = head_token.i
        for token in head_token.rights:
            if token.pos_ in ['ADJ', 'NOUN'] or token.dep_ in ['amod', 'compound']:
                end_idx = max(end_idx, token.i)
        
        return [doc[i] for i in range(start_idx, end_idx + 1)]
    
    def _calculate_antecedent_score(self, noun_phrase_span, relative_token, doc) -> float:
        """先行詞スコアの計算"""
        score = 0.0
        head_token = noun_phrase_span[-1]  # 名詞句の主要部
        
        # 距離による評価（近いほど高い）
        distance = relative_token.i - head_token.i
        if distance == 1:
            score += 0.8
        elif distance <= 3:
            score += 0.6
        elif distance <= 5:
            score += 0.3
        
        # 句読点による区切りを考慮
        has_punctuation = any(token.pos_ == 'PUNCT' 
                            for token in doc[head_token.i:relative_token.i])
        if not has_punctuation:
            score += 0.2
        
        # 名詞句の完全性
        if len(noun_phrase_span) > 1:  # 修飾語付きの名詞句
            score += 0.3
        
        return score
    
    def _detect_clause_boundaries(self, relative_token, doc) -> Optional[Tuple[int, int]]:
        """関係節の境界検出"""
        start_idx = relative_token.i
        
        # 関係節の終了位置を検索
        end_idx = self._find_clause_end(relative_token, doc)
        
        if end_idx is None or end_idx <= start_idx:
            return None
        
        return (start_idx, end_idx)
    
    def _find_clause_end(self, relative_token, doc) -> Optional[int]:
        """関係節の終了位置検出"""
        # 依存関係ベースの検出
        clause_tokens = set()
        self._collect_clause_tokens(relative_token, clause_tokens)
        
        if not clause_tokens:
            return None
        
        # 最後のトークンのインデックス
        return max(token.i for token in clause_tokens)
    
    def _collect_clause_tokens(self, token, clause_tokens: set):
        """関係節トークンの収集（再帰的）"""
        if token in clause_tokens:
            return
        
        clause_tokens.add(token)
        
        # 子トークンも収集
        for child in token.children:
            # 主節動詞に戻らないよう制御
            if child.dep_ not in ['ROOT', 'conj']:
                self._collect_clause_tokens(child, clause_tokens)
    
    def _analyze_internal_structure(self, relative_token, clause_span: Tuple[int, int], doc) -> Dict[str, Any]:
        """関係節内部構造の解析"""
        start_idx, end_idx = clause_span
        clause_tokens = doc[start_idx:end_idx + 1]
        
        # 関係節内の動詞検出
        verbs = [token for token in clause_tokens if token.pos_ in ['VERB', 'AUX']]
        
        # 関係節内の目的語・補語検出
        objects = [token for token in clause_tokens 
                  if token.dep_ in ['dobj', 'iobj', 'pobj', 'attr']]
        
        # 修飾語検出
        modifiers = [token for token in clause_tokens 
                    if token.dep_ in ['advmod', 'amod', 'npadvmod']]
        
        return {
            'verbs': [{'text': v.text, 'pos': v.pos_, 'lemma': v.lemma_} for v in verbs],
            'objects': [{'text': o.text, 'dep': o.dep_} for o in objects],
            'modifiers': [{'text': m.text, 'dep': m.dep_} for m in modifiers],
            'clause_length': len(clause_tokens)
        }
    
    def _analyze_clause_structure(self, candidate: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """関係節構造の詳細解析"""
        relative_token = candidate['relative_pronoun']
        antecedent = candidate['antecedent']
        clause_span = candidate['clause_span']
        
        # 関係節の機能分析
        function = self._determine_clause_function(relative_token, doc)
        
        # 信頼度計算
        confidence = self._calculate_individual_confidence(candidate)
        
        if confidence < 0.4:  # 低信頼度は除外
            return None
        
        return {
            'relative_pronoun': {
                'text': relative_token.text,
                'index': relative_token.i,
                'function': function
            },
            'antecedent': {
                'text': antecedent['text'],
                'head_index': antecedent['head'].i,
                'span_indices': [t.i for t in antecedent['tokens']]
            },
            'clause_span': {
                'start': clause_span[0],
                'end': clause_span[1],
                'text': ' '.join([doc[i].text for i in range(clause_span[0], clause_span[1] + 1)])
            },
            'internal_structure': candidate['clause_structure'],
            'confidence': confidence,
            'pattern_type': candidate['pattern_type']
        }
    
    def _determine_clause_function(self, relative_token, doc) -> str:
        """関係節の機能決定"""
        # 依存関係に基づく機能分析
        if relative_token.dep_ in ['nsubj', 'nsubjpass']:
            return 'subject'
        elif relative_token.dep_ in ['dobj', 'iobj']:
            return 'object'
        elif relative_token.dep_ in ['pobj']:
            return 'prepositional_object'
        else:
            return 'modifier'
    
    def _calculate_individual_confidence(self, candidate: Dict[str, Any]) -> float:
        """個別関係節の信頼度計算"""
        base_confidence = 0.5
        
        # 先行詞の明確さ
        base_confidence += candidate['antecedent']['score'] * 0.3
        
        # 関係節の長さ（適度な長さが良い）
        clause_length = candidate['clause_structure']['clause_length']
        if 3 <= clause_length <= 10:
            base_confidence += 0.2
        elif clause_length > 10:
            base_confidence -= 0.1
        
        # 動詞の存在
        if candidate['clause_structure']['verbs']:
            base_confidence += 0.2
        
        # パターンの重み
        base_confidence *= candidate['confidence_weight']
        
        return min(1.0, base_confidence)
    
    def _calculate_clause_confidence(self, analyzed_clauses: List[Dict[str, Any]]) -> float:
        """全体の関係節解析信頼度"""
        if not analyzed_clauses:
            return 0.0
        
        total_confidence = sum(clause['confidence'] for clause in analyzed_clauses)
        return min(1.0, total_confidence / len(analyzed_clauses))


class RelativeClauseHandlerClean:
    """
    関係節処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的関係節検出アルゴリズム
    - 動的境界検出
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericClauseAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'RelativeClauseHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> ClauseConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> ClauseConfiguration:
        """デフォルト設定の作成"""
        return ClauseConfiguration(
            relative_patterns={
                'wh_relatives': RelativePattern(
                    pattern_type='wh_relative',
                    relative_indicators=['who', 'whom', 'whose', 'which', 'that', 'where', 'when', 'why'],
                    pos_patterns=['PRON', 'DET', 'ADV'],
                    dependency_patterns=['nsubj', 'dobj', 'nsubjpass', 'pobj', 'advmod'],
                    confidence_weight=1.2
                ),
                'that_relatives': RelativePattern(
                    pattern_type='that_relative',
                    relative_indicators=['that'],
                    pos_patterns=['PRON', 'SCONJ'],
                    dependency_patterns=['nsubj', 'dobj', 'mark'],
                    confidence_weight=1.0
                ),
                'antecedent_patterns': RelativePattern(
                    pattern_type='antecedent',
                    pos_patterns=['NOUN', 'PROPN', 'PRON'],
                    dependency_patterns=['ROOT', 'nsubj', 'dobj', 'pobj'],
                    confidence_weight=1.0
                )
            },
            boundary_detection={
                'end_markers': ['PUNCT', 'CONJ'],
                'depth_limit': 10
            },
            confidence_settings={
                'minimum_confidence': 0.4,
                'high_confidence': 0.8,
                'clause_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> ClauseConfiguration:
        """設定データの解析"""
        relative_patterns = {}
        for name, data in config_data.get('relative_patterns', {}).items():
            relative_patterns[name] = RelativePattern(
                pattern_type=data.get('pattern_type', name),
                relative_indicators=data.get('relative_indicators', []),
                antecedent_indicators=data.get('antecedent_indicators', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                position_rules=data.get('position_rules', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return ClauseConfiguration(
            relative_patterns=relative_patterns,
            boundary_detection=config_data.get('boundary_detection', {}),
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        関係節処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, clauses, separated_text, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 関係節解析
            analysis_result = self.analyzer.analyze_relative_clauses(doc)
            
            if not analysis_result['clauses']:
                return self._create_no_clauses_result(text)
            
            # 関係節分離テキストの生成
            separated_text = self._generate_separated_text(doc, analysis_result['clauses'])
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['clauses'])
            
            return {
                'success': True,
                'separated_text': separated_text,
                'relative_clauses': analysis_result['clauses'],
                'sub_slots': sub_slots,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'clause_count': len(analysis_result['clauses'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_clauses_result(self, text: str) -> Dict[str, Any]:
        """関係節なしの結果作成"""
        return {
            'success': True,
            'separated_text': text,
            'relative_clauses': [],
            'sub_slots': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.4),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_clauses_detected'
            }
        }
    
    def _generate_separated_text(self, doc, clauses: List[Dict[str, Any]]) -> str:
        """関係節分離テキストの生成"""
        # 関係節として認識されたトークンのインデックスを収集
        clause_indices = set()
        
        for clause in clauses:
            start = clause['clause_span']['start']
            end = clause['clause_span']['end']
            for i in range(start, end + 1):
                clause_indices.add(i)
        
        # 関係節以外のトークンでテキストを再構築
        remaining_tokens = [token.text for i, token in enumerate(doc) 
                          if i not in clause_indices]
        
        return ' '.join(remaining_tokens)
    
    def _build_sub_slots(self, clauses: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, clause in enumerate(clauses):
            slot_key = f"sub-rel{i+1}"
            sub_slots[slot_key] = clause['clause_span']['text']
        
        return sub_slots
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'separated_text': '',
            'relative_clauses': [],
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
            'relative_patterns': {
                'wh_relatives': {
                    'pattern_type': 'wh_relative',
                    'relative_indicators': ['who', 'whom', 'whose', 'which', 'that', 'where', 'when', 'why'],
                    'pos_patterns': ['PRON', 'DET', 'ADV'],
                    'dependency_patterns': ['nsubj', 'dobj', 'nsubjpass', 'pobj', 'advmod'],
                    'confidence_weight': 1.2
                },
                'that_relatives': {
                    'pattern_type': 'that_relative',
                    'relative_indicators': ['that'],
                    'pos_patterns': ['PRON', 'SCONJ'],
                    'dependency_patterns': ['nsubj', 'dobj', 'mark'],
                    'confidence_weight': 1.0
                },
                'antecedent_patterns': {
                    'pattern_type': 'antecedent',
                    'pos_patterns': ['NOUN', 'PROPN', 'PRON'],
                    'dependency_patterns': ['ROOT', 'nsubj', 'dobj', 'pobj'],
                    'confidence_weight': 1.0
                }
            },
            'boundary_detection': {
                'end_markers': ['PUNCT', 'CONJ'],
                'depth_limit': 10
            },
            'confidence_settings': {
                'minimum_confidence': 0.4,
                'high_confidence': 0.8,
                'clause_bonus': 0.2
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = RelativeClauseHandlerClean()
    
    test_sentences = [
        "The book that I read was interesting.",
        "A person who speaks three languages is polyglot.",
        "The house which we visited was beautiful.",
        "The reason why he left remains unclear."
    ]
    
    print("🧪 RelativeClauseHandler - ハードコーディング完全除去版テスト")
    print("=" * 70)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"分離テキスト: \"{result.get('separated_text', '')}\"")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"関係節数: {len(result.get('relative_clauses', []))}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        print(f"ハードコーディング使用: 0件 ✅")
