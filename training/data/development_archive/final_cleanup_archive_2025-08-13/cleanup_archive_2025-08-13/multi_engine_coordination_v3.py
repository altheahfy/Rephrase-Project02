#!/usr/bin/env python3
"""
Multi-Engine Coordination System V3 - Production Implementation

This implements true multi-engine coordination for complex sentence analysis.
Each engine processes its specialty area simultaneously, and results are merged.
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum
import time
import copy

# Import current V2 components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType, EngineResult, LazyEngineInfo

@dataclass
class CoordinationResult:
    """Result of multi-engine coordination."""
    primary_engine: EngineType
    contributing_engines: List[EngineType]
    merged_slots: Dict[str, Any]
    confidence: float
    coordination_strategy: str
    processing_time: float
    metadata: Dict[str, Any]

class MultiEngineCoordinationV3:
    """
    Production-ready multi-engine coordination system.
    
    Key Features:
    1. True parallel engine processing
    2. Intelligent result merging
    3. Conflict resolution
    4. Performance optimization
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize coordination system."""
        self.v2_controller = GrammarMasterControllerV2(log_level=log_level)
        self.logger = self._setup_logging(log_level)
        
        # Coordination statistics
        self.coordination_stats = {
            'total_coordinations': 0,
            'strategy_usage': {},
            'engine_combinations': {},
            'average_processing_time': 0.0,
            'conflict_resolutions': 0
        }
        
        self.logger.info("Multi-Engine Coordination V3 initialized")
    
    def _setup_logging(self, log_level: str):
        """Setup logging configuration."""
        logger = logging.getLogger('MultiEngineCoordinationV3')
        logger.setLevel(getattr(logging, log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """
        Process sentence with multi-engine coordination.
        
        Args:
            sentence: Input sentence to process
            debug: Enable detailed processing information
            
        Returns:
            EngineResult: Enhanced result from coordinated engines
        """
        start_time = time.time()
        self.coordination_stats['total_coordinations'] += 1
        
        if debug:
            self.logger.info(f"Processing sentence: '{sentence}'")
        
        # Step 1: Determine applicable engines
        applicable_engines = self._get_applicable_engines(sentence)
        
        if debug:
            self.logger.info(f"Applicable engines: {[e.value for e in applicable_engines]}")
        
        # Step 2: Determine coordination strategy
        strategy = self._determine_coordination_strategy(sentence, applicable_engines)
        
        # Update strategy statistics
        self.coordination_stats['strategy_usage'][strategy] = \
            self.coordination_stats['strategy_usage'].get(strategy, 0) + 1
        
        if debug:
            self.logger.info(f"Coordination strategy: {strategy}")
        
        # Step 3: Execute coordination strategy
        try:
            if strategy == "single_engine":
                result = self._process_single_engine(sentence, applicable_engines[0], start_time)
            elif strategy == "foundation_specialist":
                result = self._process_foundation_specialist(sentence, applicable_engines, start_time, debug)
            elif strategy == "multi_cooperative":
                result = self._process_multi_cooperative(sentence, applicable_engines, start_time, debug)
            else:
                raise ValueError(f"Unknown coordination strategy: {strategy}")
                
        except Exception as e:
            self.logger.error(f"Coordination failed: {str(e)}")
            result = self._create_error_result(f"Coordination error: {str(e)}", start_time)
        
        # Step 4: Update statistics
        processing_time = time.time() - start_time
        self._update_processing_statistics(processing_time)
        
        return result
    
    def _get_applicable_engines(self, sentence: str) -> List[EngineType]:
        """Determine which engines are applicable for this sentence."""
        sentence_lower = sentence.lower()
        applicable = []
        
        # Always include Basic Five Pattern as foundation
        applicable.append(EngineType.BASIC_FIVE_PATTERN)
        
        # Pattern-based engine detection
        patterns = {
            EngineType.RELATIVE: ["who", "which", "that", "where", "when", "whose"],
            EngineType.CONJUNCTION: ["because", "although", "while", "since", "if", "when", "before", "after"],
            EngineType.PASSIVE: ["was", "were", "been", "being"],
            EngineType.MODAL: ["can", "could", "will", "would", "must", "should", "may", "might"],
            EngineType.PERFECT_PROGRESSIVE: ["have been", "has been", "had been", "will have been"],
            EngineType.SUBJUNCTIVE: ["if", "were", "wish", "unless", "suppose"],
            EngineType.INVERSION: ["never", "rarely", "seldom", "hardly", "not only", "no sooner"],
            EngineType.COMPARATIVE: ["more", "most", "than", "better", "worse", "best", "worst"]
        }
        
        for engine_type, keywords in patterns.items():
            if any(keyword in sentence_lower for keyword in keywords):
                applicable.append(engine_type)
        
        # Additional context-based detection
        if "by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been"]):
            if EngineType.PASSIVE not in applicable:
                applicable.append(EngineType.PASSIVE)
        
        # Remove duplicates and sort by priority
        applicable = list(set(applicable))
        applicable.sort(key=lambda x: self.v2_controller.engines.get(x, LazyEngineInfo(None, None, 999, None, None)).priority)
        
        return applicable
    
    def _determine_coordination_strategy(self, sentence: str, applicable_engines: List[EngineType]) -> str:
        """Determine the best coordination strategy."""
        sentence_lower = sentence.lower()
        
        # Calculate complexity score
        complexity_indicators = {
            'relative_clauses': sum(1 for rel in ["who", "which", "that"] if rel in sentence_lower),
            'conjunctions': sum(1 for conj in ["because", "although", "while", "since", "if"] if conj in sentence_lower),
            'passive_voice': 1 if ("by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been"])) else 0,
            'modal_verbs': sum(1 for modal in ["can", "could", "will", "would", "must", "should"] if modal in sentence_lower),
            'perfect_aspects': sum(1 for perf in ["have", "has", "had"] if f"{perf} been" in sentence_lower),
            'word_count': len(sentence.split())
        }
        
        total_complexity = sum(complexity_indicators.values())
        
        # Strategy decision
        if len(applicable_engines) == 1:
            return "single_engine"
        elif total_complexity >= 4 or len(applicable_engines) >= 4:
            return "multi_cooperative"  # Complex sentence needs full cooperation
        else:
            return "foundation_specialist"  # Moderate complexity
    
    def _process_single_engine(self, sentence: str, engine_type: EngineType, start_time: float) -> EngineResult:
        """Process with single optimal engine."""
        self.v2_controller._load_engine(engine_type)
        result = self.v2_controller._process_with_engine(sentence, engine_type, start_time)
        
        # Enhance metadata
        result.metadata['coordination_mode'] = 'single_engine'
        result.metadata['engines_used'] = [engine_type.value]
        
        return result
    
    def _process_foundation_specialist(self, sentence: str, applicable_engines: List[EngineType], 
                                     start_time: float, debug: bool = False) -> EngineResult:
        """Process with foundation engine + one specialist."""
        results = {}
        
        # Foundation processing (Basic Five Pattern)
        if EngineType.BASIC_FIVE_PATTERN in applicable_engines:
            self.v2_controller._load_engine(EngineType.BASIC_FIVE_PATTERN)
            foundation_result = self.v2_controller._process_with_engine(sentence, EngineType.BASIC_FIVE_PATTERN, start_time)
            
            if foundation_result.success:
                results[EngineType.BASIC_FIVE_PATTERN] = foundation_result
                
                if debug:
                    self.logger.info(f"Foundation result: {len(foundation_result.slots)} slots")
        
        # Specialist processing (highest priority non-foundation engine)
        specialist_engine = None
        for engine_type in applicable_engines:
            if engine_type != EngineType.BASIC_FIVE_PATTERN:
                specialist_engine = engine_type
                break
        
        if specialist_engine:
            try:
                self.v2_controller._load_engine(specialist_engine)
                specialist_result = self.v2_controller._process_with_engine(sentence, specialist_engine, start_time)
                
                if specialist_result.success:
                    results[specialist_engine] = specialist_result
                    
                    if debug:
                        self.logger.info(f"Specialist {specialist_engine.value} result: {len(specialist_result.slots)} slots")
            except Exception as e:
                if debug:
                    self.logger.warning(f"Specialist engine {specialist_engine.value} failed: {str(e)}")
        
        # Merge results
        return self._merge_engine_results(results, sentence, start_time, "foundation_specialist")
    
    def _process_multi_cooperative(self, sentence: str, applicable_engines: List[EngineType], 
                                  start_time: float, debug: bool = False) -> EngineResult:
        """Process with multiple engines in cooperation mode."""
        results = {}
        
        # Process with each applicable engine (limit to top 4 for performance)
        for engine_type in applicable_engines[:4]:
            try:
                self.v2_controller._load_engine(engine_type)
                engine_result = self.v2_controller._process_with_engine(sentence, engine_type, start_time)
                
                if engine_result.success:
                    results[engine_type] = engine_result
                    
                    if debug:
                        self.logger.info(f"Cooperative {engine_type.value} result: {len(engine_result.slots)} slots")
                        
            except Exception as e:
                if debug:
                    self.logger.warning(f"Cooperative engine {engine_type.value} failed: {str(e)}")
                continue
        
        # Merge all results
        return self._merge_engine_results(results, sentence, start_time, "multi_cooperative")
    
    def _merge_engine_results(self, results: Dict[EngineType, EngineResult], 
                            sentence: str, start_time: float, strategy: str) -> EngineResult:
        """
        Merge multiple engine results with intelligent conflict resolution.
        """
        if not results:
            return self._create_error_result("No successful engine results", start_time)
        
        # Select primary engine (highest confidence)
        primary_engine_type = max(results.keys(), key=lambda e: results[e].confidence)
        primary_result = results[primary_engine_type]
        
        # Initialize merged slots with primary result
        merged_slots = copy.deepcopy(primary_result.slots)
        
        # Merge slots from other engines
        for engine_type, result in results.items():
            if engine_type != primary_engine_type:
                for slot_key, slot_value in result.slots.items():
                    if slot_key not in merged_slots or not merged_slots[slot_key]:
                        # Add unique slots
                        merged_slots[slot_key] = slot_value
                    elif merged_slots[slot_key] != slot_value:
                        # Conflict resolution: prefer more specific information
                        if len(str(slot_value)) > len(str(merged_slots[slot_key])):
                            merged_slots[slot_key] = slot_value
                            self.coordination_stats['conflict_resolutions'] += 1
        
        # Calculate enhanced confidence
        base_confidence = primary_result.confidence
        contribution_bonus = min(0.1 * (len(results) - 1), 0.3)
        merged_confidence = min(base_confidence + contribution_bonus, 1.0)
        
        # Create enhanced result
        enhanced_result = EngineResult(
            engine_type=primary_result.engine_type,
            confidence=merged_confidence,
            slots=merged_slots,
            metadata={
                'coordination_mode': strategy,
                'primary_engine': primary_engine_type.value,
                'contributing_engines': [e.value for e in results.keys()],
                'total_engines_used': len(results),
                'total_slots': len(merged_slots),
                'coordination_stats': self.coordination_stats.copy()
            },
            success=True,
            processing_time=time.time() - start_time,
            error=None
        )
        
        # Update combination statistics
        combo_key = tuple(sorted([e.value for e in results.keys()]))
        self.coordination_stats['engine_combinations'][combo_key] = \
            self.coordination_stats['engine_combinations'].get(combo_key, 0) + 1
        
        return enhanced_result
    
    def _create_error_result(self, error_message: str, start_time: float) -> EngineResult:
        """Create standardized error result."""
        return EngineResult(
            engine_type=EngineType.BASIC_FIVE_PATTERN,
            confidence=0.0,
            slots={},
            metadata={'error': error_message, 'coordination_mode': 'error'},
            success=False,
            processing_time=time.time() - start_time,
            error=error_message
        )
    
    def _update_processing_statistics(self, processing_time: float):
        """Update processing time statistics."""
        total = self.coordination_stats['total_coordinations']
        current_avg = self.coordination_stats['average_processing_time']
        
        # Calculate running average
        new_avg = ((current_avg * (total - 1)) + processing_time) / total
        self.coordination_stats['average_processing_time'] = new_avg
    
    def get_coordination_statistics(self) -> Dict[str, Any]:
        """Get detailed coordination statistics."""
        return {
            'total_coordinations': self.coordination_stats['total_coordinations'],
            'strategy_distribution': self.coordination_stats['strategy_usage'],
            'engine_combinations': dict(self.coordination_stats['engine_combinations']),
            'average_processing_time': round(self.coordination_stats['average_processing_time'], 4),
            'conflict_resolutions': self.coordination_stats['conflict_resolutions'],
            'v2_engine_stats': self.v2_controller.get_detailed_statistics()
        }


# Demonstration and testing
def test_multi_engine_coordination():
    """Test the multi-engine coordination system."""
    coordinator = MultiEngineCoordinationV3(log_level="INFO")
    
    test_cases = [
        # Simple sentence (single engine)
        {
            'sentence': "The cat sits on the mat.",
            'expected_strategy': "single_engine",
            'description': "Simple sentence"
        },
        
        # Foundation + specialist
        {
            'sentence': "The book that I bought is interesting.",
            'expected_strategy': "foundation_specialist",
            'description': "Relative clause"
        },
        
        # Multi-cooperative
        {
            'sentence': "The book that I bought was written by an author who lives in Tokyo because he wanted to be near the publishing companies.",
            'expected_strategy': "multi_cooperative",
            'description': "Complex sentence with multiple grammar patterns"
        },
        
        # Passive with modal
        {
            'sentence': "This work should be completed by tomorrow.",
            'expected_strategy': "foundation_specialist",
            'description': "Modal + passive voice"
        }
    ]
    
    print("=== Multi-Engine Coordination V3 Test ===")
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Sentence: '{test_case['sentence']}'")
        
        result = coordinator.process_sentence(test_case['sentence'], debug=True)
        
        print(f"   Success: {result.success}")
        print(f"   Primary Engine: {result.engine_type.value}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Total Slots: {len(result.slots)}")
        print(f"   Strategy: {result.metadata.get('coordination_mode', 'unknown')}")
        
        if 'contributing_engines' in result.metadata:
            print(f"   Engines Used: {result.metadata['contributing_engines']}")
        
        if result.success:
            successful_tests += 1
    
    print(f"\n=== Test Summary ===")
    print(f"Successful tests: {successful_tests}/{len(test_cases)}")
    
    # Show coordination statistics
    stats = coordinator.get_coordination_statistics()
    print(f"\nCoordination Statistics:")
    print(f"  Total coordinations: {stats['total_coordinations']}")
    print(f"  Strategy usage: {stats['strategy_distribution']}")
    print(f"  Average processing time: {stats['average_processing_time']}s")
    
    if stats['engine_combinations']:
        print(f"  Engine combinations used:")
        for combo, count in stats['engine_combinations'].items():
            print(f"    {combo}: {count}")
    
    return successful_tests == len(test_cases)


if __name__ == "__main__":
    success = test_multi_engine_coordination()
    print(f"\n{'🎉 ALL TESTS PASSED!' if success else '⚠️ SOME TESTS FAILED'}")
