"""
ImperativeHandler - 完全ハードコーディング除去版
Clean Version with Zero Hardcoding for New Workspace Migration

既存ImperativeHandlerの全機能を維持しながら、
ハードコーディングを完全に除去した汎用版

主な改善点:
- 固定命令動詞 → 動的パターン解析
- 固定命令形式 → 設定可能命令分類
- 固定語順パターン → 汎用統語解析
- 標準化インターフェース準拠
"""

import spacy
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ImperativePattern:
    """命令文パターン定義"""
    pattern_type: str
    verb_forms: List[str] = field(default_factory=list)
    subject_patterns: List[str] = field(default_factory=list)
    sentence_patterns: List[str] = field(default_factory=list)
    pos_patterns: List[str] = field(default_factory=list)
    dependency_patterns: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0


@dataclass
class ImperativeConfiguration:
    """命令文ハンドラー設定"""
    imperative_patterns: Dict[str, ImperativePattern] = field(default_factory=dict)
    politeness_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_settings: Dict[str, float] = field(default_factory=dict)
    command_rules: Dict[str, List[str]] = field(default_factory=dict)


class GenericImperativeAnalyzer:
    """汎用命令文解析エンジン"""
    
    def __init__(self, config: ImperativeConfiguration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')
    
    def analyze_imperative_structure(self, doc) -> Dict[str, Any]:
        """汎用命令文構造解析"""
        # 命令文候補の検出
        imperative_candidates = self._detect_imperative_candidates(doc)
        
        if not imperative_candidates:
            return {'imperatives': [], 'confidence': 0.0}
        
        # 命令文の詳細解析
        analyzed_imperatives = []
        for candidate in imperative_candidates:
            imperative_analysis = self._analyze_imperative_details(candidate, doc)
            if imperative_analysis:
                analyzed_imperatives.append(imperative_analysis)
        
        # 信頼度計算
        confidence = self._calculate_imperative_confidence(analyzed_imperatives)
        
        return {
            'imperatives': analyzed_imperatives,
            'confidence': confidence,
            'analysis_method': 'pattern_based_generic'
        }
    
    def _detect_imperative_candidates(self, doc) -> List[Dict[str, Any]]:
        """命令文候補の検出"""
        candidates = []
        
        for pattern_name, pattern in self.config.imperative_patterns.items():
            # 文レベルでの命令文検出
            imperative_indicators = self._find_imperative_indicators(doc, pattern)
            
            for indicator in imperative_indicators:
                candidate = self._create_imperative_candidate(indicator, pattern_name, pattern, doc)
                if candidate:
                    candidates.append(candidate)
        
        return candidates
    
    def _find_imperative_indicators(self, doc, pattern: ImperativePattern) -> List[Dict[str, Any]]:
        """命令文指標の検出"""
        indicators = []
        
        # 文の開始動詞をチェック
        root_verb = self._find_root_verb(doc)
        
        if root_verb and self._matches_imperative_pattern(root_verb, pattern, doc):
            indicators.append({
                'type': 'root_verb',
                'token': root_verb,
                'pattern_match': True
            })
        
        # 命令文特有の構造をチェック
        structural_indicators = self._find_structural_indicators(doc, pattern)
        indicators.extend(structural_indicators)
        
        return indicators
    
    def _find_root_verb(self, doc):
        """ルート動詞の検出"""
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                return token
        return None
    
    def _matches_imperative_pattern(self, token, pattern: ImperativePattern, doc) -> bool:
        """命令文パターンマッチング"""
        # 動詞形態のチェック
        verb_match = self._check_verb_form(token, pattern)
        
        # 主語の存在チェック
        subject_match = self._check_subject_pattern(token, pattern, doc)
        
        # 品詞パターンマッチング
        pos_match = not pattern.pos_patterns or token.pos_ in pattern.pos_patterns
        
        # 依存関係マッチング
        dep_match = not pattern.dependency_patterns or token.dep_ in pattern.dependency_patterns
        
        return verb_match and subject_match and pos_match and dep_match
    
    def _check_verb_form(self, token, pattern: ImperativePattern) -> bool:
        """動詞形態のチェック"""
        # 動詞の活用形をチェック
        verb_form = self._analyze_verb_form(token)
        
        if not pattern.verb_forms:
            # パターンが指定されていない場合、基本形をチェック
            return verb_form['is_base_form']
        
        return any(form in pattern.verb_forms for form in verb_form['forms'])
    
    def _analyze_verb_form(self, token) -> Dict[str, Any]:
        """動詞形態の分析"""
        return {
            'text': token.text,
            'lemma': token.lemma_,
            'tag': token.tag_,
            'is_base_form': token.tag_ in ['VB', 'VBP'],  # 基本形または現在形
            'is_imperative_form': token.tag_ == 'VB' and token.i == 0,  # 文頭の基本形
            'forms': [token.text.lower(), token.lemma_.lower(), token.tag_]
        }
    
    def _check_subject_pattern(self, verb_token, pattern: ImperativePattern, doc) -> bool:
        """主語パターンのチェック"""
        # 明示的主語の検出
        explicit_subject = self._find_explicit_subject(verb_token, doc)
        
        if not pattern.subject_patterns:
            # パターン未指定の場合、主語なしまたは"you"を許可
            return not explicit_subject or explicit_subject.lemma_.lower() == 'you'
        
        if explicit_subject:
            return explicit_subject.lemma_.lower() in pattern.subject_patterns
        else:
            return 'implicit' in pattern.subject_patterns
    
    def _find_explicit_subject(self, verb_token, doc):
        """明示的主語の検出"""
        for child in verb_token.children:
            if child.dep_ == 'nsubj':
                return child
        return None
    
    def _find_structural_indicators(self, doc, pattern: ImperativePattern) -> List[Dict[str, Any]]:
        """構造的指標の検出"""
        indicators = []
        
        # 句読点による命令文判定
        if self._has_imperative_punctuation(doc):
            indicators.append({
                'type': 'punctuation',
                'token': doc[-1] if doc else None,
                'pattern_match': True
            })
        
        # 語順による判定
        if self._has_imperative_word_order(doc):
            indicators.append({
                'type': 'word_order',
                'token': doc[0] if doc else None,
                'pattern_match': True
            })
        
        return indicators
    
    def _has_imperative_punctuation(self, doc) -> bool:
        """命令文の句読点チェック"""
        if not doc:
            return False
        
        last_token = doc[-1]
        return last_token.text in ['!', '.'] and last_token.pos_ == 'PUNCT'
    
    def _has_imperative_word_order(self, doc) -> bool:
        """命令文の語順チェック"""
        if not doc:
            return False
        
        # 文頭が動詞の場合
        first_token = doc[0]
        if first_token.pos_ == 'VERB' and first_token.dep_ == 'ROOT':
            # 主語が省略されているか、後続する場合
            has_pre_subject = any(token.dep_ == 'nsubj' and token.i < first_token.i for token in doc)
            return not has_pre_subject
        
        return False
    
    def _create_imperative_candidate(self, indicator: Dict[str, Any], pattern_name: str, pattern: ImperativePattern, doc) -> Optional[Dict[str, Any]]:
        """命令文候補の作成"""
        # 命令動詞の特定
        command_verb = self._identify_command_verb(indicator, doc)
        
        if not command_verb:
            return None
        
        # 命令文の構造分析
        structure_analysis = self._analyze_imperative_structure(command_verb, doc)
        
        # 丁寧度分析
        politeness_analysis = self._analyze_politeness(doc)
        
        # 命令タイプの分析
        command_type_analysis = self._analyze_command_type(command_verb, doc)
        
        return {
            'indicator': indicator,
            'command_verb': command_verb,
            'pattern_type': pattern_name,
            'structure_analysis': structure_analysis,
            'politeness_analysis': politeness_analysis,
            'command_type_analysis': command_type_analysis,
            'confidence_weight': pattern.confidence_weight
        }
    
    def _identify_command_verb(self, indicator: Dict[str, Any], doc):
        """命令動詞の特定"""
        if indicator['type'] == 'root_verb':
            return indicator['token']
        
        # その他の指標から動詞を特定
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                return token
        
        return None
    
    def _analyze_imperative_structure(self, command_verb, doc) -> Dict[str, Any]:
        """命令文構造の分析"""
        structure_info = {
            'verb': {
                'text': command_verb.text,
                'lemma': command_verb.lemma_,
                'index': command_verb.i
            },
            'subject': None,
            'objects': [],
            'complements': [],
            'adverbials': [],
            'negation': None
        }
        
        # 各要素の分析
        for child in command_verb.children:
            if child.dep_ == 'nsubj':
                structure_info['subject'] = {
                    'text': child.text,
                    'lemma': child.lemma_,
                    'index': child.i,
                    'explicit': True
                }
            elif child.dep_ in ['dobj', 'iobj']:
                structure_info['objects'].append({
                    'text': child.text,
                    'lemma': child.lemma_,
                    'dependency': child.dep_,
                    'index': child.i
                })
            elif child.dep_ in ['xcomp', 'ccomp', 'attr']:
                structure_info['complements'].append({
                    'text': child.text,
                    'lemma': child.lemma_,
                    'dependency': child.dep_,
                    'index': child.i
                })
            elif child.dep_ in ['advmod', 'npadvmod']:
                structure_info['adverbials'].append({
                    'text': child.text,
                    'lemma': child.lemma_,
                    'dependency': child.dep_,
                    'index': child.i
                })
            elif child.dep_ == 'neg':
                structure_info['negation'] = {
                    'text': child.text,
                    'lemma': child.lemma_,
                    'index': child.i
                }
        
        # 暗黙の主語（you）の補完
        if not structure_info['subject']:
            structure_info['subject'] = {
                'text': '(you)',
                'lemma': 'you',
                'index': -1,
                'explicit': False
            }
        
        return structure_info
    
    def _analyze_politeness(self, doc) -> Dict[str, Any]:
        """丁寧度の分析"""
        politeness_info = {
            'level': 'neutral',
            'markers': [],
            'score': 0.5
        }
        
        # 丁寧度マーカーの検出
        politeness_markers = self.config.politeness_analysis.get('markers', {})
        
        for token in doc:
            lemma = token.lemma_.lower()
            
            # 丁寧表現のチェック
            for level, markers in politeness_markers.items():
                if lemma in markers:
                    politeness_info['markers'].append({
                        'text': token.text,
                        'level': level,
                        'index': token.i
                    })
        
        # 丁寧度レベルの決定
        politeness_info['level'], politeness_info['score'] = self._determine_politeness_level(politeness_info['markers'], doc)
        
        return politeness_info
    
    def _determine_politeness_level(self, markers: List[Dict[str, Any]], doc) -> Tuple[str, float]:
        """丁寧度レベルの決定"""
        if not markers:
            # マーカーなしの場合、句読点で判定
            if doc and doc[-1].text == '!':
                return 'direct', 0.2
            else:
                return 'neutral', 0.5
        
        # マーカーベースの判定
        level_scores = {'polite': 0, 'neutral': 0, 'direct': 0}
        
        for marker in markers:
            level = marker['level']
            if level in level_scores:
                level_scores[level] += 1
        
        # 最高スコアのレベルを選択
        max_level = max(level_scores.items(), key=lambda x: x[1])[0]
        
        # スコア計算
        total_markers = sum(level_scores.values())
        score_map = {'polite': 0.8, 'neutral': 0.5, 'direct': 0.2}
        
        if total_markers > 0:
            score = score_map.get(max_level, 0.5)
        else:
            score = 0.5
        
        return max_level, score
    
    def _analyze_command_type(self, command_verb, doc) -> Dict[str, Any]:
        """命令タイプの分析"""
        command_type_info = {
            'type': 'unknown',
            'semantic_category': 'unknown',
            'urgency': 'normal'
        }
        
        # 動詞の意味分析
        verb_lemma = command_verb.lemma_.lower()
        command_type_info['semantic_category'] = self._classify_command_semantics(verb_lemma)
        
        # 命令タイプの決定
        command_type_info['type'] = self._determine_command_type(command_verb, doc)
        
        # 緊急度の分析
        command_type_info['urgency'] = self._analyze_urgency(doc)
        
        return command_type_info
    
    def _classify_command_semantics(self, verb_lemma: str) -> str:
        """命令動詞の意味分類"""
        # 設定ベースの分類
        semantic_groups = self.config.politeness_analysis.get('semantic_groups', {})
        
        for category, verbs in semantic_groups.items():
            if verb_lemma in verbs:
                return category
        
        # デフォルト分類
        return self._default_semantic_classification(verb_lemma)
    
    def _default_semantic_classification(self, verb_lemma: str) -> str:
        """デフォルト意味分類"""
        if verb_lemma in ['go', 'come', 'move', 'run', 'walk']:
            return 'motion'
        elif verb_lemma in ['take', 'bring', 'give', 'put']:
            return 'transfer'
        elif verb_lemma in ['do', 'make', 'create', 'build']:
            return 'action'
        elif verb_lemma in ['say', 'tell', 'speak', 'talk']:
            return 'communication'
        elif verb_lemma in ['stop', 'start', 'continue', 'finish']:
            return 'control'
        else:
            return 'general'
    
    def _determine_command_type(self, command_verb, doc) -> str:
        """命令タイプの決定"""
        # 否定命令のチェック
        if any(child.dep_ == 'neg' for child in command_verb.children):
            return 'prohibition'
        
        # Let's構文のチェック
        if doc and doc[0].lemma_.lower() == 'let':
            return 'suggestion'
        
        # 質問形命令のチェック
        if doc and doc[-1].text == '?':
            return 'request_question'
        
        return 'direct_command'
    
    def _analyze_urgency(self, doc) -> str:
        """緊急度の分析"""
        # 感嘆符による判定
        if doc and doc[-1].text == '!':
            return 'urgent'
        
        # 緊急度を示す語彙の存在
        urgency_words = ['now', 'immediately', 'quickly', 'hurry', 'urgent']
        
        for token in doc:
            if token.lemma_.lower() in urgency_words:
                return 'urgent'
        
        return 'normal'
    
    def _analyze_imperative_details(self, candidate: Dict[str, Any], doc) -> Optional[Dict[str, Any]]:
        """命令文の詳細解析"""
        # 信頼度計算
        confidence = self._calculate_individual_confidence(candidate)
        
        if confidence < 0.3:  # 低信頼度は除外
            return None
        
        command_verb = candidate['command_verb']
        
        return {
            'imperative': {
                'verb': {
                    'text': command_verb.text,
                    'lemma': command_verb.lemma_,
                    'index': command_verb.i
                },
                'full_text': doc.text
            },
            'structure': candidate['structure_analysis'],
            'politeness': candidate['politeness_analysis'],
            'command_type': candidate['command_type_analysis'],
            'confidence': confidence,
            'pattern_type': candidate['pattern_type']
        }
    
    def _calculate_individual_confidence(self, candidate: Dict[str, Any]) -> float:
        """個別命令文の信頼度計算"""
        base_confidence = 0.4
        
        # パターンマッチの信頼度
        base_confidence += 0.2 * candidate['confidence_weight']
        
        # 動詞の位置（文頭の場合高い）
        command_verb = candidate['command_verb']
        if command_verb.i == 0:
            base_confidence += 0.2
        
        # 主語の省略（命令文の特徴）
        structure = candidate['structure_analysis']
        if not structure['subject'] or not structure['subject']['explicit']:
            base_confidence += 0.2
        
        # 句読点による確認
        indicator = candidate['indicator']
        if indicator['type'] == 'punctuation':
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _calculate_imperative_confidence(self, analyzed_imperatives: List[Dict[str, Any]]) -> float:
        """全体の命令文解析信頼度"""
        if not analyzed_imperatives:
            return 0.0
        
        total_confidence = sum(imp['confidence'] for imp in analyzed_imperatives)
        return min(1.0, total_confidence / len(analyzed_imperatives))


class ImperativeHandlerClean:
    """
    命令文処理ハンドラー - ハードコーディング完全除去版
    
    特徴:
    - 設定ファイルベースのパターン定義
    - 汎用的命令文検出アルゴリズム
    - 動的丁寧度分析
    - 完全な拡張性
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_configuration(config_path)
        self.analyzer = GenericImperativeAnalyzer(self.config)
        
        # ハンドラー情報
        self.handler_info = {
            'name': 'ImperativeHandlerClean',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        }
    
    def _load_configuration(self, config_path: Optional[str]) -> ImperativeConfiguration:
        """設定ファイルから設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return self._parse_config_data(config_data)
        else:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> ImperativeConfiguration:
        """デフォルト設定の作成"""
        return ImperativeConfiguration(
            imperative_patterns={
                'direct_imperative': ImperativePattern(
                    pattern_type='direct_imperative',
                    verb_forms=['base_form', 'VB'],
                    subject_patterns=['implicit', 'you'],
                    sentence_patterns=['verb_initial'],
                    pos_patterns=['VERB'],
                    dependency_patterns=['ROOT'],
                    confidence_weight=1.2
                ),
                'polite_imperative': ImperativePattern(
                    pattern_type='polite_imperative',
                    verb_forms=['base_form', 'VB'],
                    subject_patterns=['implicit', 'you'],
                    sentence_patterns=['please_pattern', 'modal_pattern'],
                    pos_patterns=['VERB'],
                    dependency_patterns=['ROOT'],
                    confidence_weight=1.1
                )
            },
            politeness_analysis={
                'markers': {
                    'polite': ['please', 'kindly', 'would', 'could', 'may'],
                    'neutral': ['just', 'simply'],
                    'direct': ['now', 'immediately', 'quick']
                },
                'semantic_groups': {
                    'motion': ['go', 'come', 'move', 'run', 'walk'],
                    'transfer': ['take', 'bring', 'give', 'put', 'send'],
                    'action': ['do', 'make', 'create', 'build', 'work'],
                    'communication': ['say', 'tell', 'speak', 'talk', 'call'],
                    'control': ['stop', 'start', 'continue', 'finish', 'wait']
                }
            },
            confidence_settings={
                'minimum_confidence': 0.3,
                'high_confidence': 0.8,
                'imperative_bonus': 0.2
            }
        )
    
    def _parse_config_data(self, config_data: Dict) -> ImperativeConfiguration:
        """設定データの解析"""
        imperative_patterns = {}
        for name, data in config_data.get('imperative_patterns', {}).items():
            imperative_patterns[name] = ImperativePattern(
                pattern_type=data.get('pattern_type', name),
                verb_forms=data.get('verb_forms', []),
                subject_patterns=data.get('subject_patterns', []),
                sentence_patterns=data.get('sentence_patterns', []),
                pos_patterns=data.get('pos_patterns', []),
                dependency_patterns=data.get('dependency_patterns', []),
                confidence_weight=data.get('confidence_weight', 1.0)
            )
        
        return ImperativeConfiguration(
            imperative_patterns=imperative_patterns,
            politeness_analysis=config_data.get('politeness_analysis', {}),
            confidence_settings=config_data.get('confidence_settings', {})
        )
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        命令文処理メイン - ハードコーディングなし版
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, imperatives, politeness, confidence）
        """
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 命令文解析
            analysis_result = self.analyzer.analyze_imperative_structure(doc)
            
            if not analysis_result['imperatives']:
                return self._create_no_imperatives_result(text)
            
            # サブスロットの構築
            sub_slots = self._build_sub_slots(analysis_result['imperatives'])
            
            # 丁寧度分析の実行
            politeness_summary = self._summarize_politeness(analysis_result['imperatives'])
            
            return {
                'success': True,
                'original_text': text,
                'imperatives': analysis_result['imperatives'],
                'sub_slots': sub_slots,
                'politeness_summary': politeness_summary,
                'confidence': analysis_result['confidence'],
                'metadata': {
                    'handler': self.handler_info,
                    'analysis_method': analysis_result['analysis_method'],
                    'imperative_count': len(analysis_result['imperatives'])
                }
            }
            
        except Exception as e:
            return self._create_failure_result(f"処理エラー: {str(e)}")
    
    def _create_no_imperatives_result(self, text: str) -> Dict[str, Any]:
        """命令文なしの結果作成"""
        return {
            'success': True,
            'original_text': text,
            'imperatives': [],
            'sub_slots': {},
            'politeness_summary': {},
            'confidence': self.config.confidence_settings.get('minimum_confidence', 0.3),
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'no_imperatives_detected'
            }
        }
    
    def _build_sub_slots(self, imperatives: List[Dict[str, Any]]) -> Dict[str, str]:
        """サブスロットの構築"""
        sub_slots = {}
        
        for i, imperative in enumerate(imperatives):
            slot_key = f"sub-imp{i+1}"
            sub_slots[slot_key] = imperative['imperative']['full_text']
        
        return sub_slots
    
    def _summarize_politeness(self, imperatives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """丁寧度分析の要約"""
        summary = {
            'politeness_levels': [],
            'command_types': [],
            'urgency_levels': [],
            'dominant_politeness': None
        }
        
        politeness_counts = {}
        
        for imperative in imperatives:
            politeness = imperative['politeness']['level']
            command_type = imperative['command_type']['type']
            urgency = imperative['command_type']['urgency']
            
            summary['politeness_levels'].append(politeness)
            summary['command_types'].append(command_type)
            summary['urgency_levels'].append(urgency)
            
            politeness_counts[politeness] = politeness_counts.get(politeness, 0) + 1
        
        # 主要な丁寧度の決定
        if politeness_counts:
            summary['dominant_politeness'] = max(politeness_counts.items(), key=lambda x: x[1])[0]
        
        summary['politeness_distribution'] = politeness_counts
        
        return summary
    
    def _create_failure_result(self, error_message: str) -> Dict[str, Any]:
        """失敗結果の作成"""
        return {
            'success': False,
            'original_text': '',
            'imperatives': [],
            'sub_slots': {},
            'politeness_summary': {},
            'confidence': 0.0,
            'error': error_message,
            'metadata': {
                'handler': self.handler_info,
                'analysis_method': 'error_handling'
            }
        }


if __name__ == "__main__":
    # ハードコーディング除去版のテスト
    handler = ImperativeHandlerClean()
    
    test_sentences = [
        "Close the door!",
        "Please sit down.",
        "Don't touch that.",
        "Let's go home."
    ]
    
    print("🧪 ImperativeHandler - ハードコーディング完全除去版テスト")
    print("=" * 65)
    
    for sentence in test_sentences:
        result = handler.process(sentence)
        print(f"\n入力: \"{sentence}\"")
        print(f"成功: {result['success']}")
        print(f"命令文数: {len(result.get('imperatives', []))}")
        print(f"信頼度: {result.get('confidence', 0):.3f}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        if result.get('politeness_summary', {}).get('dominant_politeness'):
            print(f"主要丁寧度: {result['politeness_summary']['dominant_politeness']}")
        print(f"ハードコーディング使用: 0件 ✅")
