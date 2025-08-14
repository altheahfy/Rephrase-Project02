#!/usr/bin/env python3
"""
Hierarchical Grammar Detector v5.1 - Universal Clause Detection
汎用的階層文法検出システム (Stanza/spaCy構文解析ベース)

設計思想:
1. Type phrase(V持つ)/clause(SV持つ)自動特定 - Stanza/spaCy依存構造活用
2. 上位スロット高精度判定活用 - 既存83.3%システム再利用
3. 構造タイプ判定 - 分詞構文、接続節、関係代名詞等の汎用検出
4. 再帰的文法判定 - phrase/clause内部の階層的解析
"""

import stanza
import spacy
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from advanced_grammar_detector import GrammarPattern
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

@dataclass
class UniversalClauseInfo:
    """汎用的節情報 - あらゆる文法構造に対応"""
    text: str                           # 節のテキスト
    clause_type: str                   # spaCy依存関係 (ccomp, advcl, relcl等)
    has_subject: bool                  # Type clause判定 (SV構造)
    has_verb: bool                     # Type phrase判定 (V構造)
    root_token: str                    # 節の中心語
    placeholder: str                   # 置換用プレースホルダー
    start_idx: int                     # 文中の開始位置
    end_idx: int                      # 文中の終了位置
    grammatical_pattern: Optional[GrammarPattern] = None  # 内部文法パターン
    confidence: float = 0.0           # 解析信頼度

@dataclass
class UniversalHierarchicalResult:
    """汎用的階層解析結果"""
    sentence: str
    main_result: Any                                      # 主構造の解析結果
    clause_results: List[UniversalClauseInfo] = field(default_factory=list)
    processing_method: str = "universal_hierarchical"
    total_confidence: float = 0.0
    processing_time: float = 0.0

class UniversalHierarchicalDetector:
    """汎用的階層文法検出器 - あらゆる文法構造に対応"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # V4の高精度システムを活用
        self.v4_detector = HierarchicalGrammarDetectorV4()
        
        # NLPパイプライン初期化
        self._initialize_nlp()
        
        # 節タイプ別プレースホルダー定義
        self.placeholder_map = {
            'ccomp': 'something',      # 補文節
            'xcomp': 'something',      # 動詞補文
            'advcl': 'somehow',        # 副詞節
            'acl': 'something',        # 形容詞節
            'relcl': 'something',      # 関係節
            'pcomp': 'something',      # 前置詞補文
        }
        
    def _initialize_nlp(self):
        """NLPパイプライン初期化"""
        try:
            self.nlp_stanza = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
            self.nlp_spacy = spacy.load("en_core_web_sm")
            self.logger.info("✅ Universal NLP pipelines initialized")
        except Exception as e:
            self.logger.error(f"❌ NLP initialization failed: {e}")
            raise
    
    def detect_universal_hierarchical_grammar(self, sentence: str) -> UniversalHierarchicalResult:
        """汎用的階層文法検出 - 4段階処理"""
        start_time = time.time()
        
        print(f"🌍 Universal Processing: {sentence}")
        
        # Stage 1: Type phrase/clause特定
        clauses = self._detect_clause_structures(sentence)
        print(f"    📊 Stage 1: Detected {len(clauses)} clause structures")
        
        # Stage 2: プレースホルダー置換 + 上位スロット文法判定
        main_sentence, main_result = self._analyze_main_structure(sentence, clauses)
        print(f"    📊 Stage 2: Main structure = {main_result.main_clause.grammatical_pattern.value if main_result.main_clause else 'Unknown'}")
        
        # Stage 3: 構造タイプ判定
        for clause in clauses:
            clause.grammatical_pattern = self._classify_clause_type(clause)
        print(f"    📊 Stage 3: Clause types classified")
            
        # Stage 4: 再帰的内部解析
        self._analyze_clause_internals(clauses)
        print(f"    📊 Stage 4: Internal analysis completed")
        
        # 結果統合
        total_confidence = self._calculate_total_confidence(main_result, clauses)
        
        result = UniversalHierarchicalResult(
            sentence=sentence,
            main_result=main_result,
            clause_results=clauses,
            total_confidence=total_confidence,
            processing_time=time.time() - start_time
        )
        
        print(f"✅ Universal Complete: {len(clauses)} clauses processed")
        return result
    
    def _detect_clause_structures(self, sentence: str) -> List[UniversalClauseInfo]:
        """Stage 1: Type phrase/clause構造の汎用的検出"""
        
        # spaCy解析
        doc = self.nlp_spacy(sentence)
        
        clauses = []
        clause_deps = ['ccomp', 'xcomp', 'advcl', 'acl', 'relcl', 'pcomp']
        
        for token in doc:
            if token.dep_ in clause_deps:
                # 節範囲特定
                clause_tokens = list(token.subtree)
                clause_text = ' '.join([t.text for t in clause_tokens])
                
                # SV構造判定
                has_subject = any(t.dep_ == 'nsubj' for t in clause_tokens)
                has_verb = any(t.pos_ == 'VERB' for t in clause_tokens)
                
                # プレースホルダー生成
                placeholder = self.placeholder_map.get(token.dep_, 'something')
                
                clause_info = UniversalClauseInfo(
                    text=clause_text,
                    clause_type=token.dep_,
                    has_subject=has_subject,
                    has_verb=has_verb,
                    root_token=token.text,
                    placeholder=placeholder,
                    start_idx=clause_tokens[0].idx,
                    end_idx=clause_tokens[-1].idx + len(clause_tokens[-1].text)
                )
                
                clauses.append(clause_info)
                print(f"      🔍 {token.dep_}: '{clause_text}' ({'SV' if has_subject and has_verb else 'phrase'})")
        
        return clauses
    
    def _analyze_main_structure(self, sentence: str, clauses: List[UniversalClauseInfo]) -> Tuple[str, Any]:
        """Stage 2: プレースホルダー置換 + 高精度文法判定"""
        
        # 文字列置換でプレースホルダー生成
        main_sentence = sentence
        for clause in sorted(clauses, key=lambda x: x.start_idx, reverse=True):  # 後ろから置換
            main_sentence = (
                main_sentence[:clause.start_idx] + 
                clause.placeholder + 
                main_sentence[clause.end_idx:]
            )
        
        print(f"    🔄 Modified: '{main_sentence}'")
        
        # 既存高精度システムで解析
        main_result = self.v4_detector.detect_hierarchical_grammar(main_sentence)
        
        return main_sentence, main_result
    
    def _classify_clause_type(self, clause: UniversalClauseInfo) -> GrammarPattern:
        """Stage 3: 構造タイプの汎用的判定"""
        
        # spaCy依存関係に基づく分類
        type_mapping = {
            'ccomp': GrammarPattern.NOUN_CLAUSE,          # that節等
            'xcomp': GrammarPattern.INFINITIVE_PATTERN,   # 不定詞句
            'advcl': GrammarPattern.CONJUNCTION_PATTERN,  # 副詞節
            'acl': GrammarPattern.PARTICIPLE_PATTERN,     # 分詞句
            'relcl': GrammarPattern.RELATIVE_PATTERN,     # 関係節
            'pcomp': GrammarPattern.GERUND_PATTERN        # 動名詞句
        }
        
        return type_mapping.get(clause.clause_type, GrammarPattern.SV_PATTERN)
    
    def _analyze_clause_internals(self, clauses: List[UniversalClauseInfo]):
        """Stage 4: 節内部の再帰的文法解析"""
        
        for clause in clauses:
            if clause.has_subject and clause.has_verb:  # Type clause
                # 再帰的に文法判定
                internal_result = self.v4_detector.detect_hierarchical_grammar(clause.text)
                clause.confidence = getattr(internal_result, 'confidence_breakdown', {}).get('overall', 0.7)
                print(f"      📎 Internal '{clause.text}' = {internal_result.main_clause.grammatical_pattern.value if internal_result.main_clause else 'Unknown'}")
            else:  # Type phrase
                clause.confidence = 0.6  # phrase固定信頼度
                print(f"      📎 Phrase '{clause.text}' = {clause.grammatical_pattern.value}")
    
    def _calculate_total_confidence(self, main_result: Any, clauses: List[UniversalClauseInfo]) -> float:
        """総合信頼度計算"""
        main_confidence = getattr(main_result, 'confidence_breakdown', {}).get('overall', 0.8)
        clause_confidences = [clause.confidence for clause in clauses]
        
        if not clause_confidences:
            return main_confidence
        
        # 重み付け平均
        total_confidence = (main_confidence * 0.7 + sum(clause_confidences) / len(clause_confidences) * 0.3)
        return min(total_confidence, 1.0)

# テスト実行
if __name__ == "__main__":
    detector = UniversalHierarchicalDetector()
    
    test_cases = [
        "I think that he is smart.",
        "Being a teacher, she knows students well.",
        "The book that I read yesterday was interesting.",
        "Having finished the work, she went home.",
        "If I were rich, I would travel around the world."
    ]
    
    print("🌍 Universal Hierarchical Grammar Detection Test")
    print("=" * 60)
    
    for sentence in test_cases:
        print(f"\n📝 Testing: \"{sentence}\"")
        print("-" * 50)
        
        try:
            result = detector.detect_universal_hierarchical_grammar(sentence)
            
            print(f"🏗️ Main: {result.main_result.main_clause.grammatical_pattern.value if result.main_result.main_clause else 'Unknown'}")
            print(f"📊 Clauses: {len(result.clause_results)}")
            for clause in result.clause_results:
                sv_type = "SV-clause" if clause.has_subject and clause.has_verb else "phrase"
                print(f"  📎 {clause.clause_type}: '{clause.text}' ({sv_type}) -> {clause.grammatical_pattern.value}")
            print(f"🎯 Total Confidence: {result.total_confidence:.3f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
