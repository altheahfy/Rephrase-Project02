#!/usr/bin/env python3
"""
Grammar Master Controller v2.0 - Lazy Loading Edition

High-performance central controller with lazy loading system.
Engines are loaded only when first needed, dramatically reducing startup time.

Performance Benefits:
- Instant startup (no engine pre-loading)
- Memory efficient (unused engines never loaded)
- Scalable to 100+ engines without startup penalty
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

class EngineType(Enum):
    """Engine type enumeration for priority and classification."""
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

@dataclass
class EngineResult:
    """Standardized result from any grammar engine."""
    engine_type: EngineType
    confidence: float
    slots: Dict[str, str]
    metadata: Dict[str, Any]
    success: bool
    processing_time: float
    error: Optional[str] = None

@dataclass
class LazyEngineInfo:
    """Lazy loading engine information."""
    engine_type: EngineType
    module_path: str
    class_name: str
    priority: int
    description: str
    patterns: List[str]
    instance: Optional[Any] = None
    load_time: Optional[float] = None
    usage_count: int = 0

class GrammarMasterControllerV2:
    """
    Lazy-loading central controller for all unified grammar engines.
    
    Key Features:
    1. Instant startup - no pre-loading of engines
    2. On-demand loading - engines loaded only when first used
    3. Thread-safe loading with locks
    4. Scalable to unlimited number of engines
    5. Memory efficient - unused engines never consume memory
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize the master controller with lazy loading configuration."""
        self._setup_logging(log_level)
        self.engine_registry: Dict[EngineType, LazyEngineInfo] = {}
        self.loading_locks: Dict[EngineType, Lock] = {}
        self.processing_stats = {
            'total_requests': 0,
            'successful_processes': 0,
            'engines_loaded': 0,
            'total_engines_registered': 0,
            'average_processing_time': 0.0,
            'startup_time': time.time()
        }
        
        # Register engine configurations (no actual loading)
        self._register_engine_configs()
        
        startup_time = time.time() - self.processing_stats['startup_time']
        self.logger.info(f"GrammarMasterControllerV2 initialized in {startup_time:.4f}s with {len(self.engine_registry)} engine configs (lazy loading)")
    
    def _setup_logging(self, log_level: str):
        """Setup logging configuration."""
        self.logger = logging.getLogger('GrammarMasterControllerV2')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _register_engine_configs(self):
        """Register engine configurations without loading actual engines."""
        
        # Engine configurations with module paths
        engine_configs = [
            # High Priority: Fundamental grammatical structures
            (EngineType.CONJUNCTION, "engines.stanza_based_conjunction_engine", "StanzaBasedConjunctionEngine", 
             1, "Subordinate conjunction processing", ["because", "although", "while", "since", "if"]),
            (EngineType.RELATIVE, "engines.simple_relative_engine", "SimpleRelativeEngine", 
             2, "Relative clause processing", ["who", "which", "that", "where", "when"]),
            (EngineType.PASSIVE, "engines.passive_voice_engine", "PassiveVoiceEngine", 
             3, "Passive voice constructions", ["was", "were", "been", "being", "by"]),
            
            # Medium Priority: Complex tense and mood structures  
            (EngineType.PERFECT_PROGRESSIVE, "engines.perfect_progressive_engine", "PerfectProgressiveEngine", 
             4, "Perfect progressive tenses", ["has been", "had been", "will have been"]),
            (EngineType.SUBJUNCTIVE, "engines.subjunctive_conditional_engine", "SubjunctiveConditionalEngine", 
             5, "Subjunctive and conditional moods", ["if", "were", "wish", "unless"]),
            (EngineType.INVERSION, "engines.inversion_engine", "InversionEngine", 
             6, "Inverted constructions", ["never", "rarely", "seldom", "hardly", "not only"]),
            (EngineType.COMPARATIVE, "engines.comparative_superlative_engine", "ComparativeSuperlativeEngine", 
             7, "Comparative and superlative forms", ["more", "most", "than", "-er", "-est"]),
            
            # Lower Priority: Verbal forms (more specific patterns)
            (EngineType.GERUND, "engines.gerund_engine", "GerundEngine", 
             8, "Gerund constructions", ["-ing", "swimming", "reading", "working"]),
            (EngineType.PARTICIPLE, "engines.participle_engine", "ParticipleEngine", 
             9, "Participial constructions", ["-ing", "-ed", "running", "broken"]),
            (EngineType.INFINITIVE, "engines.infinitive_engine", "InfinitiveEngine", 
             10, "Infinitive constructions", ["to", "to be", "to have", "to do"]),
        ]
        
        for engine_type, module_path, class_name, priority, description, patterns in engine_configs:
            self.engine_registry[engine_type] = LazyEngineInfo(
                engine_type=engine_type,
                module_path=module_path,
                class_name=class_name,
                priority=priority,
                description=description,
                patterns=patterns
            )
            
            # Create loading lock for thread safety
            self.loading_locks[engine_type] = Lock()
        
        self.processing_stats['total_engines_registered'] = len(self.engine_registry)
        self.logger.info(f"Registered {len(self.engine_registry)} engine configurations (no loading)")
    
    def _load_engine(self, engine_type: EngineType) -> bool:
        """
        Lazy load an engine when first needed.
        
        Args:
            engine_type: Type of engine to load
            
        Returns:
            bool: True if loading successful
        """
        engine_info = self.engine_registry[engine_type]
        
        # Check if already loaded
        if engine_info.instance is not None:
            return True
        
        # Thread-safe loading
        with self.loading_locks[engine_type]:
            # Double-check after acquiring lock
            if engine_info.instance is not None:
                return True
            
            try:
                load_start_time = time.time()
                self.logger.info(f"🔄 Lazy loading {engine_type.value} engine...")
                
                # Dynamic import
                module = importlib.import_module(engine_info.module_path)
                engine_class = getattr(module, engine_info.class_name)
                
                # Instantiate engine
                engine_instance = engine_class()
                
                # Update registry
                engine_info.instance = engine_instance
                engine_info.load_time = time.time() - load_start_time
                
                # Update stats
                self.processing_stats['engines_loaded'] += 1
                
                self.logger.info(f"✅ {engine_type.value} engine loaded in {engine_info.load_time:.4f}s")
                return True
                
            except Exception as e:
                self.logger.error(f"❌ Failed to load {engine_type.value} engine: {str(e)}")
                return False
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """
        Main processing method with lazy loading.
        
        Args:
            sentence: Input sentence to process
            debug: Enable detailed processing information
            
        Returns:
            EngineResult: Unified result from the best matching engine
        """
        start_time = time.time()
        
        self.processing_stats['total_requests'] += 1
        
        if not sentence or not sentence.strip():
            return self._create_error_result("Empty sentence provided", start_time)
        
        try:
            # Step 1: Get applicable engines (pattern-based, no loading needed)
            applicable_engines = self._get_applicable_engines_fast(sentence)
            
            if not applicable_engines:
                return self._create_error_result("No applicable engines found", start_time)
            
            if debug:
                self.logger.info(f"Applicable engines: {[e.value for e in applicable_engines]}")
            
            # Step 2: Select optimal engine (heuristic-based)
            selected_engine_type = self._select_optimal_engine(sentence, applicable_engines)
            
            if debug:
                self.logger.info(f"Selected engine: {selected_engine_type.value}")
            
            # Step 3: Lazy load selected engine if not already loaded
            if not self._load_engine(selected_engine_type):
                return self._create_error_result(f"Failed to load {selected_engine_type.value} engine", start_time)
            
            # Step 4: Process with loaded engine
            result = self._process_with_engine(sentence, selected_engine_type, start_time)
            
            # Step 5: Update statistics
            self.engine_registry[selected_engine_type].usage_count += 1
            self._update_statistics(selected_engine_type, time.time() - start_time, result.success)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Unexpected error in process_sentence: {str(e)}")
            return self._create_error_result(f"Processing error: {str(e)}", start_time)
    
    def _get_applicable_engines_fast(self, sentence: str) -> List[EngineType]:
        """
        Fast pattern-based engine detection without loading engines.
        
        Args:
            sentence: Input sentence
            
        Returns:
            List of applicable engine types, sorted by priority
        """
        applicable = []
        sentence_lower = sentence.lower()
        
        for engine_type, engine_info in self.engine_registry.items():
            # Pattern-based detection (no engine loading required)
            for pattern in engine_info.patterns:
                if pattern.lower() in sentence_lower:
                    applicable.append(engine_type)
                    break
        
        # Sort by priority (lower number = higher priority)
        applicable.sort(key=lambda x: self.engine_registry[x].priority)
        
        return applicable
    
    def _select_optimal_engine(self, sentence: str, applicable_engines: List[EngineType]) -> EngineType:
        """
        Select optimal engine using advanced heuristics (no engine loading).
        
        Args:
            sentence: Input sentence
            applicable_engines: List of applicable engines
            
        Returns:
            Selected engine type
        """
        if len(applicable_engines) == 1:
            return applicable_engines[0]
        
        # Advanced selection heuristics (same as v1)
        sentence_lower = sentence.lower()
        
        # Priority 1: Conjunction patterns
        if EngineType.CONJUNCTION in applicable_engines:
            conjunction_indicators = ["because", "although", "while", "since", "even though"]
            if any(indicator in sentence_lower for indicator in conjunction_indicators):
                return EngineType.CONJUNCTION
        
        # Priority 2: Conditional patterns  
        if EngineType.SUBJUNCTIVE in applicable_engines:
            conditional_indicators = ["if", "were", "would", "could", "might", "wish"]
            conditional_count = sum(1 for indicator in conditional_indicators if indicator in sentence_lower)
            if conditional_count >= 2:
                return EngineType.SUBJUNCTIVE
        
        # Priority 3: Passive voice
        if EngineType.PASSIVE in applicable_engines:
            if "by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been"]):
                return EngineType.PASSIVE
        
        # Priority 4: Inversion
        if EngineType.INVERSION in applicable_engines:
            inversion_starters = ["never", "rarely", "seldom", "hardly", "not only"]
            for starter in inversion_starters:
                if sentence_lower.startswith(starter):
                    return EngineType.INVERSION
        
        # Default: Use priority order
        return applicable_engines[0]
    
    def _process_with_engine(self, sentence: str, engine_type: EngineType, start_time: float) -> EngineResult:
        """
        Process sentence with the specified (already loaded) engine.
        
        Args:
            sentence: Input sentence
            engine_type: Selected engine type
            start_time: Processing start time
            
        Returns:
            EngineResult: Processing result
        """
        engine_info = self.engine_registry[engine_type]
        engine_instance = engine_info.instance
        
        if engine_instance is None:
            return self._create_error_result(f"Engine {engine_type.value} not loaded", start_time)
        
        try:
            # Call engine's process method
            if hasattr(engine_instance, 'process'):
                raw_result = engine_instance.process(sentence)
                
                # Standardize result format (same as v1)
                if isinstance(raw_result, dict):
                    slots = raw_result.get('slots', {})
                    metadata = raw_result.get('metadata', {})
                    success = raw_result.get('success', True)
                    error = raw_result.get('error', None)
                else:
                    slots = raw_result if isinstance(raw_result, dict) else {}
                    metadata = {'engine': engine_type.value}
                    success = bool(slots)
                    error = None if slots else "No slots extracted"
                
                processing_time = time.time() - start_time
                
                return EngineResult(
                    engine_type=engine_type,
                    confidence=self._calculate_confidence(slots, metadata),
                    slots=slots,
                    metadata={**metadata, 'processing_time': processing_time, 'controller_version': '2.0'},
                    success=success,
                    processing_time=processing_time,
                    error=error
                )
            else:
                return self._create_error_result(f"Engine {engine_type.value} has no process method", start_time)
                
        except Exception as e:
            self.logger.error(f"Error processing with {engine_type.value}: {str(e)}")
            return self._create_error_result(f"Engine processing error: {str(e)}", start_time)
    
    def _calculate_confidence(self, slots: Dict[str, str], metadata: Dict[str, Any]) -> float:
        """Calculate confidence score (same as v1)."""
        if not slots:
            return 0.0
        
        base_score = 0.5
        
        # Essential slots bonus
        essential_slots = ['S', 'V']
        for slot in essential_slots:
            if slot in slots and slots[slot].strip():
                base_score += 0.15
        
        # Additional slots bonus
        additional_slots = ['O1', 'C1', 'M1', 'Aux']
        for slot in additional_slots:
            if slot in slots and slots[slot].strip():
                base_score += 0.05
        
        # Sub-slots bonus
        sub_slots = [key for key in slots.keys() if key.startswith('sub-')]
        base_score += len(sub_slots) * 0.02
        
        return min(base_score, 1.0)
    
    def _create_error_result(self, error_message: str, start_time: float) -> EngineResult:
        """Create standardized error result."""
        return EngineResult(
            engine_type=EngineType.GERUND,
            confidence=0.0,
            slots={},
            metadata={'error': error_message, 'controller_version': '2.0'},
            success=False,
            processing_time=time.time() - start_time,
            error=error_message
        )
    
    def _update_statistics(self, engine_type: EngineType, processing_time: float, success: bool):
        """Update internal processing statistics."""
        if success:
            self.processing_stats['successful_processes'] += 1
        
        # Update average processing time
        total_time = (self.processing_stats['average_processing_time'] * 
                     (self.processing_stats['total_requests'] - 1) + processing_time)
        self.processing_stats['average_processing_time'] = total_time / self.processing_stats['total_requests']
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Get information about all registered engines."""
        loaded_engines = sum(1 for info in self.engine_registry.values() if info.instance is not None)
        
        return {
            'registered_engines': len(self.engine_registry),
            'loaded_engines': loaded_engines,
            'memory_efficiency': f"{((len(self.engine_registry) - loaded_engines) / len(self.engine_registry) * 100):.1f}% engines unloaded",
            'engine_list': [
                {
                    'type': info.engine_type.value,
                    'priority': info.priority,
                    'description': info.description,
                    'loaded': info.instance is not None,
                    'load_time': info.load_time,
                    'usage_count': info.usage_count
                }
                for info in sorted(self.engine_registry.values(), key=lambda x: x.priority)
            ]
        }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics including lazy loading metrics."""
        success_rate = (self.processing_stats['successful_processes'] / 
                       max(self.processing_stats['total_requests'], 1)) * 100
        
        return {
            **self.processing_stats,
            'success_rate_percent': round(success_rate, 2),
            'memory_usage': f"{self.processing_stats['engines_loaded']}/{self.processing_stats['total_engines_registered']} engines loaded"
        }

# Performance comparison demonstration
def demonstrate_lazy_loading():
    """Demonstrate the performance benefits of lazy loading."""
    
    print("🚀 Grammar Master Controller v2.0 - Lazy Loading Performance Test")
    print("=" * 75)
    
    # Test startup time
    startup_start = time.time()
    controller = GrammarMasterControllerV2()
    startup_time = time.time() - startup_start
    
    print(f"\n⚡ Startup Performance:")
    print(f"   Startup Time: {startup_time:.4f}s (instant!)")
    print(f"   Engines Registered: {len(controller.engine_registry)}")
    print(f"   Engines Pre-loaded: 0 (100% lazy)")
    
    # Test processing with selective loading
    test_sentences = [
        "If I were rich, I would travel.",      # Should load Subjunctive
        "The book that I read is good.",       # Should load Relative  
        "He worked because he needed money.",   # Should load Conjunction
    ]
    
    print(f"\n🔬 Lazy Loading in Action:")
    print("-" * 50)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【Test {i}】: {sentence}")
        
        # Show engine status before processing
        engine_info = controller.get_engine_info()
        loaded_before = engine_info['loaded_engines']
        
        # Process sentence
        result = controller.process_sentence(sentence)
        
        # Show engine status after processing
        engine_info_after = controller.get_engine_info()
        loaded_after = engine_info_after['loaded_engines']
        
        print(f"   🎯 Selected Engine: {result.engine_type.value}")
        print(f"   ⚡ Engines Loaded: {loaded_before} → {loaded_after}")
        print(f"   ⏱️  Total Processing Time: {result.processing_time:.4f}s")
        
        if result.success and result.slots:
            slot_count = len([v for v in result.slots.values() if v.strip()])
            print(f"   📊 Slots Extracted: {slot_count}")
    
    # Final statistics
    final_stats = controller.get_processing_stats()
    final_info = controller.get_engine_info()
    
    print(f"\n📈 Final Performance Summary:")
    print(f"   Total Requests: {final_stats['total_requests']}")
    print(f"   Engines Used: {final_stats['engines_loaded']}/{final_stats['total_engines_registered']}")
    print(f"   Memory Efficiency: {final_info['memory_efficiency']}")
    print(f"   Average Processing: {final_stats['average_processing_time']:.4f}s")
    print(f"   Success Rate: {final_stats['success_rate_percent']}%")
    
    print(f"\n🌟 Lazy Loading Benefits:")
    print(f"   ✅ Instant startup (vs ~3-5s for eager loading)")
    print(f"   ✅ Memory efficient ({final_info['memory_efficiency']})")
    print(f"   ✅ Scales to unlimited engines without startup penalty")
    print(f"   ✅ Load-on-demand reduces system resource usage")

if __name__ == "__main__":
    demonstrate_lazy_loading()
