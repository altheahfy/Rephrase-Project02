#!/usr/bin/env python3
"""
Phase 2無効化版 Grammar Master Controller
従来システムの実際の処理能力を確認するため、Phase 2サブレベルパターン処理を無効化したテスト版
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any, Type
import logging
import time
import importlib
from dataclasses import dataclass
from enum import Enum
from threading import Lock

# Phase 2を無効化するため、サブレベルパターンライブラリのインポートをコメントアウト
# from sublevel_pattern_lib import SublevelPatternLib

# 境界拡張のみ有効（Phase 1）
from boundary_expansion_lib import BoundaryExpansionLib

class EngineType(Enum):
    """Engine type enumeration for priority and classification."""
    BASIC_FIVE = "basic_five"
    GERUND = "gerund"
    PARTICIPLE = "participle"
    INFINITIVE = "infinitive"
    RELATIVE = "relative"
    CONJUNCTION = "conjunction"
    PASSIVE = "passive"
    COMPARATIVE = "comparative"
    PERFECT_PROGRESSIVE = "perfect_progressive"
    INVERSION = "inversion"
    SUBJUNCTIVE = "subjunctive"
    MODAL = "modal"
    QUESTION = "question"
    PROGRESSIVE = "progressive"
    PREPOSITIONAL = "prepositional"

@dataclass
class EngineResult:
    """Unified engine result structure."""
    engine_type: EngineType
    success: bool
    slots: Optional[Dict[str, str]]
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'engine_type': self.engine_type.value,
            'success': self.success,
            'slots': self.slots,
            'processing_time': self.processing_time,
            'metadata': self.metadata or {}
        }

@dataclass
class EngineInfo:
    """Engine configuration and runtime information."""
    engine_type: EngineType
    priority: int
    description: str
    module_path: str
    class_name: str
    instance: Optional[Any] = None
    load_time: Optional[float] = None
    usage_count: int = 0

class GrammarMasterControllerV2_NoPhase2:
    """Phase 2無効化版 Grammar Master Controller"""
    
    def __init__(self):
        """Initialize controller with Phase 1 only (no Phase 2 sublevel patterns)"""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Phase 1: 境界拡張ライブラリ初期化
        try:
            self.boundary_lib = BoundaryExpansionLib()
            self.logger.info("✅ 統一境界拡張ライブラリ統合完了")
        except Exception as e:
            self.logger.warning(f"⚠️ 境界拡張ライブラリ初期化失敗: {e}")
            self.boundary_lib = None
        
        # Phase 2: サブレベルパターンライブラリは無効化
        self.sublevel_lib = None
        self.logger.info("🔧 Phase 2サブレベルパターン処理は無効化されています")
        
        # Engine registry and loading system
        self.engine_registry: Dict[EngineType, EngineInfo] = {}
        self.load_lock = Lock()
        
        # Processing statistics
        self.processing_stats = {
            'total_requests': 0,
            'successful_processes': 0,
            'engines_loaded': 0,
            'total_engines_registered': 0,
            'average_processing_time': 0.0,
            'boundary_expansions_applied': 0,
            'sublevel_patterns_applied': 0  # 常に0（無効化のため）
        }
        
        # Register all engines (lazy loading configs)
        self._register_engines()
        
        self.logger.info("GrammarMasterControllerV2_NoPhase2 initialized with Phase 1 only")

    def _register_engines(self):
        """Register engine configurations (no actual loading)."""
        engine_configs = [
            # Basic Five Pattern Engine (Priority 0 - Highest)
            (EngineType.BASIC_FIVE, 0, "Basic five sentence patterns", "engines.basic_five_pattern_engine", "BasicFivePatternEngine"),
            
            # Specialized engines
            (EngineType.GERUND, 1, "Gerund constructions", "engines.gerund_engine_unified", "GerundEngine"),
            (EngineType.PARTICIPLE, 2, "Participial constructions", "engines.participle_engine_unified", "ParticipleEngine"),
            (EngineType.INFINITIVE, 3, "Infinitive constructions", "engines.infinitive_engine_unified", "InfinitiveEngine"),
            (EngineType.RELATIVE, 4, "Relative clause constructions", "engines.simple_relative_engine_unified", "SimpleRelativeEngine"),
            (EngineType.CONJUNCTION, 5, "Conjunction and compound sentences", "engines.conjunction_engine_unified", "ConjunctionEngine"),
            (EngineType.PASSIVE, 6, "Passive voice constructions", "engines.passive_engine_unified", "PassiveEngine"),
            (EngineType.COMPARATIVE, 7, "Comparative and superlative", "engines.comparative_engine_unified", "ComparativeEngine"),
            (EngineType.PERFECT_PROGRESSIVE, 8, "Perfect and progressive aspects", "engines.perfect_progressive_engine", "PerfectProgressiveEngine"),
            (EngineType.INVERSION, 9, "Inversion constructions", "engines.inversion_engine_unified", "InversionEngine"),
            (EngineType.SUBJUNCTIVE, 10, "Subjunctive mood", "engines.subjunctive_engine_unified", "SubjunctiveEngine"),
            (EngineType.MODAL, 11, "Modal auxiliary verbs", "engines.modal_engine_unified", "ModalEngine"),
            (EngineType.QUESTION, 12, "Question formation", "engines.question_engine_unified", "QuestionEngine"),
            (EngineType.PROGRESSIVE, 13, "Progressive tense aspects", "engines.progressive_tense_engine", "ProgressiveTenseEngine"),
            (EngineType.PREPOSITIONAL, 14, "Prepositional phrase structures", "engines.prepositional_phrase_engine", "PrepositionalPhraseEngine"),
        ]
        
        for engine_type, priority, description, module_path, class_name in engine_configs:
            self.engine_registry[engine_type] = EngineInfo(
                engine_type=engine_type,
                priority=priority,
                description=description,
                module_path=module_path,
                class_name=class_name
            )
        
        self.processing_stats['total_engines_registered'] = len(self.engine_registry)
        self.logger.info(f"Registered {len(self.engine_registry)} engine configurations (no loading)")

    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """Main processing method with lazy loading (Phase 2 disabled)."""
        start_time = time.time()
        
        self.processing_stats['total_requests'] += 1
        
        if not sentence or not sentence.strip():
            return self._create_error_result("Empty sentence provided", start_time)
        
        try:
            # Step 0: Phase 1のみ - 境界拡張処理
            enhanced_sentence = self._apply_boundary_expansion(sentence, debug)
            
            # Step 1: Get applicable engines
            applicable_engines = self._get_applicable_engines_fast(enhanced_sentence)
            
            if not applicable_engines:
                return self._create_error_result("No applicable engines found", start_time)
            
            if debug:
                self.logger.info(f"Applicable engines: {[e.value for e in applicable_engines]}")
            
            # Step 2: Select optimal engine
            selected_engine_type = self._select_optimal_engine(enhanced_sentence, applicable_engines)
            
            if debug:
                self.logger.info(f"Selected engine: {selected_engine_type.value}")
            
            # Step 3: Lazy load selected engine
            if not self._load_engine(selected_engine_type):
                return self._create_error_result(f"Failed to load {selected_engine_type.value} engine", start_time)
            
            # Step 4: Process with loaded engine
            result = self._process_with_engine(enhanced_sentence, selected_engine_type, start_time)
            
            # Step 5: Phase 1のみの境界拡張最適化（Phase 2は無効化）
            result = self._enhance_result_slots_phase1_only(result, debug)
            
            # Step 6: Update statistics
            self.engine_registry[selected_engine_type].usage_count += 1
            self._update_statistics(selected_engine_type, time.time() - start_time, result.success)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Processing error: {e}")
            return self._create_error_result(f"Processing failed: {str(e)}", start_time)

    def _enhance_result_slots_phase1_only(self, result: EngineResult, debug: bool = False) -> EngineResult:
        """Phase 1のみの境界拡張最適化（Phase 2サブレベルパターン処理は無効化）"""
        if not self.boundary_lib or not result.success or not result.slots:
            return result
        
        try:
            enhanced_slots = {}
            enhancement_stats = {'enhanced': 0, 'unchanged': 0}
            
            for slot, value in result.slots.items():
                if value and value.strip():
                    # Phase 1: Pure Stanza V3.1スロット特化境界拡張のみ
                    enhanced_value = self.boundary_lib.expand_span_for_slot(value, slot)
                    enhanced_slots[slot] = enhanced_value
                    
                    # 拡張効果統計
                    if enhanced_value != value:
                        enhancement_stats['enhanced'] += 1
                        if debug:
                            self.logger.info(f"🔧 {slot}スロット特化拡張: '{value}' → '{enhanced_value}'")
                    else:
                        enhancement_stats['unchanged'] += 1
                else:
                    enhanced_slots[slot] = value
                    enhancement_stats['unchanged'] += 1
            
            # 結果更新
            result.slots = enhanced_slots
            
            # メタデータに境界拡張情報のみ追加（Phase 2情報なし）
            if 'boundary_expansion' not in result.metadata:
                result.metadata['boundary_expansion'] = {}
            
            result.metadata['boundary_expansion'].update({
                'phase1_applied': True,
                'phase2_disabled': True,  # Phase 2が無効化されていることを明示
                'enhancement_stats': enhancement_stats,
                'library_version': '1.0'
            })
            
            # グローバル統計更新
            self.processing_stats['boundary_expansions_applied'] += enhancement_stats['enhanced']
            
            if debug:
                self.logger.info(f"📊 Phase 1拡張統計: {enhancement_stats['enhanced']}個拡張, {enhancement_stats['unchanged']}個維持")
            
            return result
            
        except Exception as e:
            self.logger.warning(f"⚠️ Phase 1境界拡張エラー: {e}")
            return result

    def _apply_boundary_expansion(self, sentence: str, debug: bool = False) -> str:
        """Phase 1境界拡張の前処理"""
        if not self.boundary_lib:
            return sentence
        
        try:
            expanded_sentence = self.boundary_lib.expand_span_generic(sentence)
            
            if debug and expanded_sentence != sentence:
                self.logger.info(f"🔧 境界拡張適用: '{sentence}' → '{expanded_sentence}'")
            
            self.processing_stats['boundary_expansions_applied'] += 1
            return expanded_sentence
            
        except Exception as e:
            self.logger.warning(f"⚠️ 境界拡張処理エラー: {e}")
            return sentence

    def _get_applicable_engines_fast(self, sentence: str) -> List[EngineType]:
        """Fast engine applicability check using patterns."""
        applicable = []
        sentence_lower = sentence.lower()
        
        # Always include basic five as fallback
        applicable.append(EngineType.BASIC_FIVE)
        
        # Pattern-based quick checks
        if any(word in sentence_lower for word in ['who', 'which', 'that', 'whose', 'whom']):
            applicable.append(EngineType.RELATIVE)
        
        if any(word in sentence_lower for word in ['is being', 'was being', 'are being', 'were being']):
            applicable.append(EngineType.PROGRESSIVE)
        
        if any(word in sentence_lower for word in ['in ', 'on ', 'at ', 'by ', 'for ', 'with ', 'under ']):
            applicable.append(EngineType.PREPOSITIONAL)
        
        return applicable

    def _select_optimal_engine(self, sentence: str, applicable_engines: List[EngineType]) -> EngineType:
        """Select the optimal engine based on priorities."""
        return min(applicable_engines, key=lambda e: self.engine_registry[e].priority)

    def _load_engine(self, engine_type: EngineType) -> bool:
        """Lazy load an engine if not already loaded."""
        with self.load_lock:
            engine_info = self.engine_registry[engine_type]
            
            if engine_info.instance is not None:
                return True
            
            try:
                self.logger.info(f"🔄 Lazy loading {engine_type.value} engine...")
                
                start_time = time.time()
                module = importlib.import_module(engine_info.module_path)
                engine_class = getattr(module, engine_info.class_name)
                engine_info.instance = engine_class()
                engine_info.load_time = time.time() - start_time
                
                self.processing_stats['engines_loaded'] += 1
                self.logger.info(f"✅ {engine_type.value} engine loaded in {engine_info.load_time:.4f}s")
                
                return True
                
            except Exception as e:
                self.logger.error(f"❌ Failed to load {engine_type.value} engine: {e}")
                return False

    def _process_with_engine(self, sentence: str, engine_type: EngineType, start_time: float) -> EngineResult:
        """Process sentence with specific engine."""
        engine_info = self.engine_registry[engine_type]
        
        try:
            # Process with engine
            if hasattr(engine_info.instance, 'process_sentence'):
                slots = engine_info.instance.process_sentence(sentence)
            else:
                slots = engine_info.instance.process(sentence)
            
            processing_time = time.time() - start_time
            
            return EngineResult(
                engine_type=engine_type,
                success=bool(slots),
                slots=slots if slots else {},
                processing_time=processing_time,
                metadata={'phase2_disabled': True}  # Phase 2無効化を明示
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"Engine {engine_type.value} processing error: {e}")
            
            return EngineResult(
                engine_type=engine_type,
                success=False,
                slots={},
                processing_time=processing_time,
                metadata={'error': str(e), 'phase2_disabled': True}
            )

    def _create_error_result(self, error_message: str, start_time: float) -> EngineResult:
        """Create error result."""
        return EngineResult(
            engine_type=EngineType.BASIC_FIVE,
            success=False,
            slots={},
            processing_time=time.time() - start_time,
            metadata={'error': error_message, 'phase2_disabled': True}
        )

    def _update_statistics(self, engine_type: EngineType, processing_time: float, success: bool):
        """Update processing statistics."""
        if success:
            self.processing_stats['successful_processes'] += 1
        
        # Update average processing time
        total_time = (self.processing_stats['average_processing_time'] * 
                     (self.processing_stats['total_requests'] - 1) + processing_time)
        self.processing_stats['average_processing_time'] = total_time / self.processing_stats['total_requests']

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        success_rate = (self.processing_stats['successful_processes'] / 
                       max(self.processing_stats['total_requests'], 1)) * 100
        
        return {
            **self.processing_stats,
            'success_rate_percent': round(success_rate, 2),
            'memory_usage': f"{self.processing_stats['engines_loaded']}/{self.processing_stats['total_engines_registered']} engines loaded",
            'phase2_status': 'DISABLED'  # Phase 2が無効化されていることを明示
        }

if __name__ == "__main__":
    print("🔧 Phase 2無効化版 Grammar Master Controller V2")
    print("従来システムの実際の処理能力確認用テスト版です。")
    
    controller = GrammarMasterControllerV2_NoPhase2()
    
    # 簡単なテスト
    test_sentence = "I think that he is smart."
    result = controller.process_sentence(test_sentence, debug=True)
    
    print(f"\nテスト結果:")
    print(f"文: {test_sentence}")
    print(f"エンジン: {result.engine_type.value}")
    print(f"成功: {result.success}")
    print(f"スロット: {result.slots}")
    print(f"メタデータ: {result.metadata}")
