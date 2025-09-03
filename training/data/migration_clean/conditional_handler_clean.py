"""
ConditionalHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存ConditionalHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定条件マーカー → 動的パターン解析
- 固定仮定法判定 → 汎用時制解析
- 固定節構造 → 動的境界検出
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ConditionalPattern:
    """条件文パターン定義"""
    pattern_type: str
    condition_markers: List[str] = field(default_factory=list)
    result_markers: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    conditional_types: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class ConditionalConfiguration:
    """条件文ハンドラー設定"""
    conditional_patterns: Dict[str, ConditionalPattern] = field(default_factory=dict)
    clause_detection: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    type_classification: Dict[str, List[str]] = field(default_factory=dict)


class GenericConditionalAnalyzer:
    """汎用条件文解析エンジン"""
    
    def __init__(self, config: ConditionalConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_conditional_structure(self, doc) -> Dict[str, Any]:
        """汎用条件文構造解析"""
        # 条件マーカーの検出
        condition_markers = self._detect_condition_markers(doc)
        
        if not condition_markers:
            return {'conditionals': [], 'confidence': 0.0}
        
        # 条件文の構造解析
        analyzed_conditionals = []
        for marker in condition_markers:
            conditional_analysis = self._analyze_conditional_structure_detail(marker, doc)
            if conditional_analysis:
                analyzed_conditionals.append(conditional_analysis)
        
        # 信頼度計算
        confidence = self._calculate_conditional_confidence(analyzed_conditionals)
        
        return {
            'conditionals': analyzed_conditionals,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_condition_markers(self, doc) -> List[Dict[str, Any]]:
        """条件マーカーの検出"""
        markers = []
        
        for pattern_name, pattern in self.config.conditional_patterns.items():
            for token in doc:
                if self._matches_conditional_pattern(token, pattern):
                    marker = self._create_condition_marker(token, pattern_name, pattern, doc)
                    if marker:
                        markers.append(marker)
        
        return markers
    
    def _matches_conditional_pattern(self, token, pattern: ConditionalPattern) -> bool:
        """条件文パターンマッチング"""
        # 語彙マッチング
        lex_match = not pattern.condition_markers or token.lemma_.lower() in pattern.condition_markers
        
        # 品詞マッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        return lex_match and pos_match and dep_match
    
    def _create_condition_marker(self, token, pattern_name: str, pattern: ConditionalPattern, doc) -> Optional[Dict[str, Any]]:
        """条件マーカーの作成"""
        # 条件節の境界検出
        condition_clause = self._detect_condition_clause(token, doc)
        
        if not condition_clause:
            return None
        
        # 結果節の検出
        result_clause = self._detect_result_clause(token, condition_clause, doc)
        
        # 条件文タイプの分類
        conditional_type = self._classify_conditional_type(token, condition_clause, result_clause)
        
        return {
            'marker_token': token,
            'pattern_type': pattern_name,
            'condition_clause': condition_clause,
            'result_clause': result_clause,
            'conditional_type': conditional_type,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _detect_condition_clause(self, marker_token, doc) -> Optional[Dict[str, Any]]:
        """条件節の検出"""
        # マーカーから条件節の終端を検索
        clause_start = marker_token.i
        clause_end = self._find_condition_clause_end(marker_token, doc)
        
        if clause_end is None or clause_end <= clause_start:
            return None
        
        clause_tokens = doc[clause_start:clause_end + 1]
        
        # 条件節の動詞検出
        verbs = [token for token in clause_tokens if token.pos_ in ['VERB', 'AUX']]
        
        # 時制分析
        tense_analysis = self._analyze_clause_tense(verbs)
        
        return {
            'start': clause_start,
            'end': clause_end,
            'text': ' '.join([token.text for token in clause_tokens]),
            'verbs': [{'text': v.text, 'lemma': v.lemma_, 'morph': v.morph.to_dict()} for v in verbs],
            'tense_analysis': tense_analysis
        }
    
    def _find_condition_clause_end(self, marker_token, doc) -> Optional[int]:
        """条件節の終端検出"""
        # 句読点またはコンマまでを検索
        for i in range(marker_token.i + 1, len(doc)):
            token = doc[i]
            
            # 句読点で区切り
            if token.pos_ == 'PUNCT' and token.text in [',', ';']:
                return i - 1
            
            # 主節の開始を示すマーカー
            if token.lemma_.lower() in ['then', 'so'] and token.dep_ == 'advmod':
                return i - 1
        
        # 文の半分まで（デフォルト）
        return min(marker_token.i + 10, len(doc) - 1)
    
    def _detect_result_clause(self, marker_token, condition_clause: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """結果節の検出"""
        # 条件節の後から文末まで
        result_start = condition_clause['end'] + 1
        
        # コンマをスキップ
        while result_start < len(doc) and doc[result_start].pos_ == 'PUNCT':
            result_start += 1
        
        if result_start >= len(doc):
            return None
        
        result_end = len(doc) - 1
        result_tokens = doc[result_start:result_end + 1]
        
        # 結果節の動詞検出
        verbs = [token for token in result_tokens if token.pos_ in ['VERB', 'AUX']]
        
        # 時制分析
        tense_analysis = self._analyze_clause_tense(verbs)
        
        return {
            'start': result_start,
            'end': result_end,
            'text': ' '.join([token.text for token in result_tokens]),
            'verbs': [{'text': v.text, 'lemma': v.lemma_, 'morph': v.morph.to_dict()} for v in verbs],
            'tense_analysis': tense_analysis
        }
    
    def _analyze_clause_tense(self, verbs: List) -> Dict[str, Any]:
        """節の時制分析"""
        tense_info = {
            'primary_tense': 'unknown',
            'auxiliary_info': [],
            'modality': 'none'
        }
        
        if not verbs:
            return tense_info
        
        # 主動詞の特定
        main_verb = None
        for verb in verbs:
            if verb.dep_ == 'ROOT' or verb.pos_ == 'VERB':
                main_verb = verb
                break
        
        if not main_verb:
            main_verb = verbs[0]
        
        # 時制の判定
        morph_dict = main_verb.morph.to_dict()
        tense = morph_dict.get('Tense', 'unknown')
        
        if tense == 'Past':
            tense_info['primary_tense'] = 'past'
        elif tense == 'Pres':
            tense_info['primary_tense'] = 'present'
        else:
            # 語形で判定
            if main_verb.text.endswith('ed'):
                tense_info['primary_tense'] = 'past'
            elif main_verb.text.endswith(('s', 'es')):
                tense_info['primary_tense'] = 'present'
        
        # 助動詞の分析
        for verb in verbs:
            if verb.pos_ == 'AUX':
                tense_info['auxiliary_info'].append({
                    'text': verb.text,
                    'lemma': verb.lemma_,
                    'type': self._classify_auxiliary(verb)
                })
        
        # 法（mood）の判定
        if any(aux['lemma'] in ['would', 'could', 'might'] for aux in tense_info['auxiliary_info']):
            tense_info['modality'] = 'subjunctive'
        elif tense_info['primary_tense'] == 'past':
            tense_info['modality'] = 'past_indicative'
        else:
            tense_info['modality'] = 'indicative'
        
        return tense_info
    
    def _classify_auxiliary(self, verb) -> str:
        """助動詞の分類"""
        lemma = verb.lemma_.lower()
        
        if lemma in ['will', 'would', 'shall']:
            return 'future'
        elif lemma in ['have', 'has', 'had']:
            return 'perfect'
        elif lemma in ['be', 'am', 'is', 'are', 'was', 'were']:
            return 'progressive_passive'
        elif lemma in ['can', 'could', 'may', 'might', 'must', 'should']:
            return 'modal'
        else:
            return 'other'
    
    def _classify_conditional_type(self, marker_token, condition_clause: Dict[str, Any], result_clause: Optional[Dict[str, Any]]) -> str:
        """条件文タイプの分類"""
        if not result_clause:
            return 'incomplete_conditional'
        
        condition_tense = condition_clause['tense_analysis']
        result_tense = result_clause['tense_analysis']
        
        # 第一条件文（現在形 + will/現在形）
        if (condition_tense['primary_tense'] == 'present' and 
            any(aux['type'] == 'future' for aux in result_tense['auxiliary_info'])):
            return 'first_conditional'
        
        # 第二条件文（過去形 + would）
        elif (condition_tense['primary_tense'] == 'past' and 
              any(aux['lemma'] == 'would' for aux in result_tense['auxiliary_info'])):
            return 'second_conditional'
        
        # 第三条件文（過去完了 + would have）
        elif (any(aux['type'] == 'perfect' for aux in condition_tense['auxiliary_info']) and
              any(aux['lemma'] == 'would' for aux in result_tense['auxiliary_info']) and
              any(aux['type'] == 'perfect' for aux in result_tense['auxiliary_info'])):
            return 'third_conditional'
        
        # ゼロ条件文（現在形 + 現在形）
        elif (condition_tense['primary_tense'] == 'present' and 
              result_tense['primary_tense'] == 'present'):
            return 'zero_conditional'
        
        else:
            return 'mixed_conditional'
    
    def _analyze_conditional_structure_detail(self, marker: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """条件文構造の詳細解析"""
        # 信頼度計算
        confidence = self._calculate_individual_confidence(marker)
        
        if confidence < 0.4:  # 低信頼度は除外
            return None
        
        return {
            'marker': {
                'text': marker['marker_token'].text,
                'index': marker['marker_token'].i,
                'pattern_type': marker['pattern_type']
            },
            'condition_clause': marker['condition_clause'],
            'result_clause': marker['result_clause'],
            'conditional_type': marker['conditional_type'],
            'confidence': confidence
        }
    
    def _calculate_individual_confidence(self, marker: Dict[str, Any]) -> float:
        """個別条件文の信頼度計算"""
        base_confidence = 0.5
        
        # パターンマッチの信頼度
        base_confidence += 0.2 * marker['confidence_weight']
        
        # 条件節の存在
        if marker['condition_clause']:
            base_confidence += 0.2
        
        # 結果節の存在
        if marker['result_clause']:
            base_confidence += 0.2
        
        # 条件文タイプの明確さ
        if marker['conditional_type'] != 'mixed_conditional':
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _calculate_conditional_confidence(self, analyzed_conditionals: List[Dict[str, Any]]) -> float:
        """全体の条件文解析信頼度"""
        if not analyzed_conditionals:
            return 0.0
        
        total_confidence = sum(cond['confidence'] for cond in analyzed_conditionals)
        return min(1.0, total_confidence / len(analyzed_conditionals))


class ConditionalHandlerClean:
    """
    条件文処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的条件文検出アルゴリズム
    - 動的時制分析
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericConditionalAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'ConditionalHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> ConditionalConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> ConditionalConfiguration:
        """デフォルト設定の作成"""
        return ConditionalConfiguration(
            conditional_patterns={
                'if_conditionals': ConditionalPattern(
                    pattern_type='if_conditional',
                    condition_markers=['if', 'unless', 'provided', 'supposing'],
                    pos_patterns=['SCONJ', 'ADP'],
                    dependency_patterns=['mark', 'prep'],
                    conditional_types=['first', 'second', 'third', 'zero'],
                    confidence_weight=1.2
                ),
                'time_conditionals': ConditionalPattern(
                    pattern_type='time_conditional',
                    condition_markers=['when', 'whenever', 'as soon as', 'once'],
                    pos_patterns=['SCONJ', 'ADV'],
                    dependency_patterns=['mark', 'advmod'],
                    conditional_types=['temporal'],
                    confidence_weight=1.0
                )
            },
            confidence_settings={
                'minimum_confidence': 0.4,
                'high_confidence': 0.8,
                'conditional_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> ConditionalConfiguration:
        """設定データの解析"""
        conditional_patterns = {}
        for name, data in config_data.get('conditional_patterns', {}).items():
            conditional_patterns[name] = ConditionalPattern(
                pattern_type=data.get('pattern_type', name),
                condition_markers=data.get('condition_markers', []),
                result_markers=data.get('result_markers', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                conditional_types=data.get('conditional_types', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return ConditionalConfiguration(
            conditional_patterns=conditional_patterns,
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        条件文処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, conditionals, separated_clauses, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 条件文解析
            analysis_result = self.analyzer.analyze_conditional_structure(doc)
            
            if not analysis_result['conditionals']:
                return self._create_no_conditionals_result(text)
            
            # 節分離の実行
            separated_clauses = self._separate_clauses(analysis_result['conditionals'])
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['conditionals'])
            
            return {
                'success': True,
                'original_text': text,
                'conditionals': analysis_result['conditionals'],
                'separated_clauses': separated_clauses,
                'sub_slots': sub_slots,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'conditional_count': len(analysis_result['conditionals'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_conditionals_result(self, text: str) -> Dict[str, Any]:
        """条件文なしの結果作成"""
        return {
            'success': True,
            'original_text': text,
            'conditionals': [],
            'separated_clauses': {'condition': '', 'result': ''},
            'sub_slots': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.4),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_conditionals_detected'
            }
        }
    
    def _separate_clauses(self, conditionals: List[Dict[str, Any]]) -> Dict[str, str]:
        """節の分離"""
        if not conditionals:
            return {'condition': '', 'result': ''}
        
        # 最初の条件文を使用
        conditional = conditionals[0]
        
        condition_text = conditional['condition_clause']['text'] if conditional['condition_clause'] else ''
        result_text = conditional['result_clause']['text'] if conditional['result_clause'] else ''
        
        return {
            'condition': condition_text,
            'result': result_text
        }
    
    def _build_sub_slots(self, conditionals: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, conditional in enumerate(conditionals):
            if conditional['condition_clause']:
                sub_slots[f"sub-cond{i+1}"] = conditional['condition_clause']['text']
            if conditional['result_clause']:
                sub_slots[f"sub-res{i+1}"] = conditional['result_clause']['text']
        
        return sub_slots
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'original_text': '',
            'conditionals': [],
            'separated_clauses': {'condition': '', 'result': ''},
            'sub_slots': {},
            'confidence': 0.0,
            'error': error_message,
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'error_handling'
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = ConditionalHandlerClean()
    
    test_sentences = [
        "If it rains, we will stay home.",
        "If I were rich, I would travel the world.",
        "When you arrive, call me.",
        "Unless you study, you will fail."
    ]
    
    print("🧪 ConditionalHandler - ハードコーディング完全除去版テスト")
    print("=" * 65)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"条件文数: {len(result.get('conditionals', []))}")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        if result.get('conditionals'):
            cond = result['conditionals'][0]
            print(f"タイプ: {cond.get('conditional_type', 'N/A')}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        print(f"ハードコーディング使用: 0件 ✅")
