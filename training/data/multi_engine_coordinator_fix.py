#!/usr/bin/env python3
"""
Multi-Engine Coordination Fix - Emergency Restoration

This script integrates the original multi-engine coordination architecture from V1
with the modern V2 enhancements (lazy loading, 5-pattern engine, boundary expansion, sublevel patterns).

Key Improvements:
1. Restore multi-engine simultaneous operation capability
2. Maintain lazy loading performance benefits
3. Preserve all V2 engine enhancements
4. Implement proper engine coordination mechanisms from documentation
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum
import time
from threading import Lock

# Import current V2 components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType, EngineResult, LazyEngineInfo

class MultiEngineCoordinator:
    """
    Emergency fix: Restore multi-engine coordination capabilities.
    
    This coordinator wraps the V2 controller and adds proper multi-engine
    coordination as documented in the original specifications.
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize with enhanced multi-engine coordination."""
        self._setup_logging(log_level)
        
        # Initialize V2 controller as base
        self.v2_controller = GrammarMasterControllerV2(log_level)
        
        # Multi-engine coordination state
        self.coordination_cache = {}
        self.engine_cooperation_results = {}
        
        self.logger.info("MultiEngineCoordinator initialized with V2 base + coordination layer")
    
    def _setup_logging(self, log_level: str):
        """Setup logging configuration."""
        self.logger = logging.getLogger('MultiEngineCoordinator')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """
        Enhanced processing with multi-engine coordination.
        
        Args:
            sentence: Input sentence to process
            debug: Enable detailed processing information
            
        Returns:
            EngineResult: Coordinated result from multiple engines
        """
        start_time = time.time()
        
        if not sentence or not sentence.strip():
            return self._create_error_result("Empty sentence provided", start_time)
        
        try:
            # Step 1: Get all applicable engines (using V2's detection)
            applicable_engines = self.v2_controller._get_applicable_engines_fast(sentence)
            
            if debug:
                self.logger.info(f"Detected applicable engines: {[e.value for e in applicable_engines]}")
            
            # Step 2: Multi-engine coordination decision
            coordination_strategy = self._determine_coordination_strategy(sentence, applicable_engines)
            
            if debug:
                self.logger.info(f"Coordination strategy: {coordination_strategy}")
            
            # Step 3: Execute coordination strategy
            if coordination_strategy == "single_optimal":
                # Use V2's single engine processing for simple cases
                return self.v2_controller.process_sentence(sentence, debug)
            
            elif coordination_strategy == "multi_cooperative":
                # Use multi-engine cooperation for complex structures
                return self._process_with_multi_engine_cooperation(sentence, applicable_engines, start_time, debug)
            
            elif coordination_strategy == "foundation_plus_specialist":
                # Use Basic Five Pattern + specialist engine
                return self._process_with_foundation_plus_specialist(sentence, applicable_engines, start_time, debug)
            
            else:
                # Fallback to V2 single engine
                return self.v2_controller.process_sentence(sentence, debug)
                
        except Exception as e:
            self.logger.error(f"Unexpected error in multi-engine coordination: {str(e)}")
            return self._create_error_result(f"Coordination error: {str(e)}", start_time)
    
    def _determine_coordination_strategy(self, sentence: str, applicable_engines: List[EngineType]) -> str:
        """
        Determine the optimal coordination strategy based on sentence complexity.
        
        Returns:
            str: Strategy name ("single_optimal", "multi_cooperative", "foundation_plus_specialist")
        """
        sentence_lower = sentence.lower()
        
        # Count complexity indicators
        complexity_indicators = {
            'conjunctions': sum(1 for conj in ["because", "although", "while", "since", "if", "when", "where"] if conj in sentence_lower),
            'relative_clauses': sum(1 for rel in ["who", "which", "that"] if rel in sentence_lower),
            'passive_voice': 1 if ("by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been"])) else 0,
            'modal_verbs': sum(1 for modal in ["can", "could", "will", "would", "must", "should", "may", "might"] if modal in sentence_lower),
            'multiple_verbs': len([word for word in sentence_lower.split() if word.endswith('ing') or word.endswith('ed')]) > 1
        }
        
        total_complexity = sum(complexity_indicators.values())
        
        # Strategy decision logic
        if total_complexity >= 3:
            return "multi_cooperative"  # Complex sentence needs multiple engines
        elif total_complexity >= 2:
            return "foundation_plus_specialist"  # Moderate complexity needs foundation + specialist
        elif len(applicable_engines) == 1:
            return "single_optimal"  # Simple case
        elif EngineType.BASIC_FIVE_PATTERN in applicable_engines and len(applicable_engines) >= 2:
            return "foundation_plus_specialist"  # Basic pattern + specialist
        else:
            return "single_optimal"  # Default to single engine
    
    def _process_with_multi_engine_cooperation(self, sentence: str, applicable_engines: List[EngineType], 
                                             start_time: float, debug: bool = False) -> EngineResult:
        """
        Process with multiple engines in cooperation mode.
        
        This implements the "エンジン協調の仕組み" from the documentation.
        """
        cooperation_results = {}
        
        # Load and process with each applicable engine
        for engine_type in applicable_engines[:3]:  # Limit to top 3 for performance
            try:
                # Load engine using V2's lazy loading
                self.v2_controller._load_engine(engine_type)
                
                # Process with this engine
                engine_result = self.v2_controller._process_with_engine(sentence, engine_type, start_time)
                
                if engine_result.success:
                    cooperation_results[engine_type] = engine_result
                    
                if debug:
                    self.logger.info(f"Engine {engine_type.value} result: {len(engine_result.slots)} slots extracted")
                    
            except Exception as e:
                if debug:
                    self.logger.warning(f"Engine {engine_type.value} failed: {str(e)}")
                continue
        
        # Merge results using priority-based coordination
        return self._merge_engine_results(cooperation_results, sentence, start_time)
    
    def _process_with_foundation_plus_specialist(self, sentence: str, applicable_engines: List[EngineType], 
                                               start_time: float, debug: bool = False) -> EngineResult:
        """
        Process with Basic Five Pattern Engine as foundation + specialist engine.
        
        This is the most common coordination pattern.
        """
        # Always use Basic Five Pattern as foundation
        foundation_result = None
        specialist_result = None
        
        try:
            # Foundation processing
            if EngineType.BASIC_FIVE_PATTERN in applicable_engines:
                self.v2_controller._load_engine(EngineType.BASIC_FIVE_PATTERN)
                foundation_result = self.v2_controller._process_with_engine(sentence, EngineType.BASIC_FIVE_PATTERN, start_time)
                
                if debug:
                    self.logger.info(f"Foundation result: {len(foundation_result.slots)} slots")
            
            # Specialist processing (select highest priority non-foundation engine)
            specialist_engine = None
            for engine_type in applicable_engines:
                if engine_type != EngineType.BASIC_FIVE_PATTERN:
                    specialist_engine = engine_type
                    break
            
            if specialist_engine:
                self.v2_controller._load_engine(specialist_engine)
                specialist_result = self.v2_controller._process_with_engine(sentence, specialist_engine, start_time)
                
                if debug:
                    self.logger.info(f"Specialist {specialist_engine.value} result: {len(specialist_result.slots)} slots")
            
        except Exception as e:
            if debug:
                self.logger.warning(f"Foundation+Specialist processing error: {str(e)}")
        
        # Merge foundation and specialist results
        return self._merge_foundation_specialist_results(foundation_result, specialist_result, sentence, start_time)
    
    def _merge_engine_results(self, results: Dict[EngineType, EngineResult], 
                            sentence: str, start_time: float) -> EngineResult:
        """
        Merge multiple engine results using priority and confidence.
        """
        if not results:
            return self._create_error_result("No successful engine results", start_time)
        
        # Select primary result (highest confidence)
        primary_result = max(results.values(), key=lambda r: r.confidence)
        
        # Enhance with additional slots from other engines
        merged_slots = primary_result.slots.copy()
        merged_metadata = primary_result.metadata.copy()
        
        for engine_type, result in results.items():
            if result != primary_result:
                # Add unique slots from other engines
                for slot_key, slot_value in result.slots.items():
                    if slot_key not in merged_slots or not merged_slots[slot_key]:
                        merged_slots[slot_key] = slot_value
                
                # Merge metadata
                merged_metadata[f"{engine_type.value}_contribution"] = len(result.slots)
        
        # Create enhanced result
        return EngineResult(
            engine_type=primary_result.engine_type,
            confidence=min(primary_result.confidence + 0.1, 1.0),  # Boost confidence for multi-engine
            slots=merged_slots,
            metadata={
                **merged_metadata,
                'coordination_mode': 'multi_cooperative',
                'engines_used': list(results.keys()),
                'total_slots': len(merged_slots)
            },
            success=True,
            processing_time=time.time() - start_time,
            error=None
        )
    
    def _merge_foundation_specialist_results(self, foundation_result: Optional[EngineResult], 
                                           specialist_result: Optional[EngineResult],
                                           sentence: str, start_time: float) -> EngineResult:
        """
        Merge foundation (Basic Five Pattern) with specialist engine results.
        """
        # Prioritize foundation result as base structure
        if foundation_result and foundation_result.success:
            base_result = foundation_result
            enhancement_result = specialist_result
        elif specialist_result and specialist_result.success:
            base_result = specialist_result
            enhancement_result = foundation_result
        else:
            return self._create_error_result("No successful results from foundation+specialist", start_time)
        
        # Start with base slots
        merged_slots = base_result.slots.copy()
        merged_metadata = base_result.metadata.copy()
        
        # Add enhancements from specialist
        if enhancement_result and enhancement_result.success:
            for slot_key, slot_value in enhancement_result.slots.items():
                if slot_key not in merged_slots or not merged_slots[slot_key]:
                    merged_slots[slot_key] = slot_value
                elif slot_value and len(slot_value) > len(merged_slots.get(slot_key, "")):
                    # Use longer/more detailed slot value
                    merged_slots[slot_key] = slot_value
            
            merged_metadata['enhancement_engine'] = enhancement_result.engine_type.value
            merged_metadata['enhancement_slots'] = len(enhancement_result.slots)
        
        return EngineResult(
            engine_type=base_result.engine_type,
            confidence=min(base_result.confidence + (0.05 if enhancement_result else 0), 1.0),
            slots=merged_slots,
            metadata={
                **merged_metadata,
                'coordination_mode': 'foundation_plus_specialist',
                'foundation_engine': base_result.engine_type.value,
                'total_slots': len(merged_slots)
            },
            success=True,
            processing_time=time.time() - start_time,
            error=None
        )
    
    def _create_error_result(self, error_message: str, start_time: float) -> EngineResult:
        """Create standardized error result."""
        return EngineResult(
            engine_type=EngineType.BASIC_FIVE_PATTERN,  # Default placeholder
            confidence=0.0,
            slots={},
            metadata={'error': error_message, 'coordination_mode': 'error'},
            success=False,
            processing_time=time.time() - start_time,
            error=error_message
        )
    
    def get_coordination_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics about engine coordination."""
        base_stats = self.v2_controller.get_processing_statistics()
        
        coordination_stats = {
            'coordination_layer_version': '1.0',
            'base_controller_stats': base_stats,
            'coordination_cache_size': len(self.coordination_cache),
            'cooperation_results_cached': len(self.engine_cooperation_results)
        }
        
        return coordination_stats

# Demonstration function
def demonstrate_multi_engine_coordination():
    """Demonstrate the restored multi-engine coordination system."""
    coordinator = MultiEngineCoordinator(log_level="INFO")
    
    test_sentences = [
        # Simple sentence (should use single engine)
        "The cat sits on the mat.",
        
        # Complex sentence with multiple patterns (should use multi-cooperative)
        "The book that I bought yesterday was written by an author who lives in Tokyo because he wanted to be near the publishing companies.",
        
        # Moderate complexity (should use foundation + specialist)
        "She has been working in the office since morning.",
        
        # Passive voice with relative clause
        "The project which was completed by the team will be presented tomorrow."
    ]
    
    print("=== Multi-Engine Coordination Demonstration ===")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{i}. Testing: '{sentence}'")
        
        result = coordinator.process_sentence(sentence, debug=True)
        
        print(f"   Result: {result.success}")
        print(f"   Engine: {result.engine_type.value}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Slots: {len(result.slots)}")
        print(f"   Coordination: {result.metadata.get('coordination_mode', 'unknown')}")
        
        if 'engines_used' in result.metadata:
            print(f"   Engines Used: {[e.value for e in result.metadata['engines_used']]}")

if __name__ == "__main__":
    demonstrate_multi_engine_coordination()
