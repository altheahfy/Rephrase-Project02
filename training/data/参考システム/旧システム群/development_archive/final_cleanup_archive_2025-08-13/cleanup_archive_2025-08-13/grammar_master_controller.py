#!/usr/bin/env python3
"""
Grammar Master Controller - Unified Architecture Central Command

This is the central controller that unifies all 10 grammar engines under 
a single, coherent architecture. It provides intelligent engine selection,
conflict resolution, and unified processing interface.

Unified Engines Under Control:
1. Gerund Engine (動名詞)
2. Participle Engine (分詞)  
3. Infinitive Engine (不定詞)
4. Relative Engine (関係詞)
5. Conjunction Engine (接続詞)
6. Passive Voice Engine (受動態)
7. Comparative Engine (比較・最上級)
8. Perfect Progressive Engine (完了進行形)
9. Inversion Engine (倒置)
10. Subjunctive/Conditional Engine (仮定法・条件法)

Architecture: Centralized dispatch with priority-based conflict resolution
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum

# Import all unified engines
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engines.gerund_engine import GerundEngine
from engines.participle_engine import ParticipleEngine
from engines.infinitive_engine import InfinitiveEngine
from engines.simple_relative_engine import SimpleRelativeEngine
from engines.stanza_based_conjunction_engine import StanzaBasedConjunctionEngine
from engines.passive_voice_engine import PassiveVoiceEngine
from engines.comparative_superlative_engine import ComparativeSuperlativeEngine
from engines.perfect_progressive_engine import PerfectProgressiveEngine
from engines.inversion_engine import InversionEngine
from engines.subjunctive_conditional_engine import SubjunctiveConditionalEngine

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
class EngineInfo:
    """Engine registration information."""
    engine_type: EngineType
    engine_instance: Any
    priority: int
    description: str
    patterns: List[str]

class GrammarMasterController:
    """
    Central controller for all unified grammar engines.
    
    Responsibilities:
    1. Engine registration and management
    2. Intelligent engine selection based on sentence patterns
    3. Conflict resolution when multiple engines are applicable
    4. Unified processing interface
    5. Result validation and quality assurance
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize the master controller with all engines."""
        self._setup_logging(log_level)
        self.engines: Dict[EngineType, EngineInfo] = {}
        self.processing_stats = {
            'total_requests': 0,
            'successful_processes': 0,
            'engine_usage_count': {},
            'average_processing_time': 0.0
        }
        
        # Register all engines
        self._register_engines()
        
        self.logger.info(f"GrammarMasterController initialized with {len(self.engines)} engines")
    
    def _setup_logging(self, log_level: str):
        """Setup logging configuration."""
        self.logger = logging.getLogger('GrammarMasterController')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _register_engines(self):
        """Register all unified grammar engines with their configurations."""
        
        # Priority order: Lower number = higher priority
        engine_configs = [
            # High Priority: Fundamental grammatical structures
            (EngineType.CONJUNCTION, StanzaBasedConjunctionEngine(), 1, "Subordinate conjunction processing", 
             ["because", "although", "while", "since", "if"]),
            (EngineType.RELATIVE, SimpleRelativeEngine(), 2, "Relative clause processing",
             ["who", "which", "that", "where", "when"]),
            (EngineType.PASSIVE, PassiveVoiceEngine(), 3, "Passive voice constructions",
             ["was", "were", "been", "being", "by"]),
            
            # Medium Priority: Complex tense and mood structures  
            (EngineType.PERFECT_PROGRESSIVE, PerfectProgressiveEngine(), 4, "Perfect progressive tenses",
             ["has been", "had been", "will have been"]),
            (EngineType.SUBJUNCTIVE, SubjunctiveConditionalEngine(), 5, "Subjunctive and conditional moods",
             ["if", "were", "wish", "unless"]),
            (EngineType.INVERSION, InversionEngine(), 6, "Inverted constructions",
             ["never", "rarely", "seldom", "hardly", "not only"]),
            (EngineType.COMPARATIVE, ComparativeSuperlativeEngine(), 7, "Comparative and superlative forms",
             ["more", "most", "than", "-er", "-est"]),
            
            # Lower Priority: Verbal forms (more specific patterns)
            (EngineType.GERUND, GerundEngine(), 8, "Gerund constructions",
             ["-ing", "swimming", "reading", "working"]),
            (EngineType.PARTICIPLE, ParticipleEngine(), 9, "Participial constructions",
             ["-ing", "-ed", "running", "broken"]),
            (EngineType.INFINITIVE, InfinitiveEngine(), 10, "Infinitive constructions",
             ["to", "to be", "to have", "to do"]),
        ]
        
        for engine_type, instance, priority, description, patterns in engine_configs:
            self.engines[engine_type] = EngineInfo(
                engine_type=engine_type,
                engine_instance=instance,
                priority=priority,
                description=description,
                patterns=patterns
            )
            
            # Initialize usage statistics
            self.processing_stats['engine_usage_count'][engine_type.value] = 0
        
        self.logger.info(f"Registered {len(self.engines)} engines successfully")
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """
        Main processing method - analyzes sentence with optimal engine selection.
        
        Args:
            sentence: Input sentence to process
            debug: Enable detailed processing information
            
        Returns:
            EngineResult: Unified result from the best matching engine
        """
        import time
        start_time = time.time()
        
        self.processing_stats['total_requests'] += 1
        
        if not sentence or not sentence.strip():
            return self._create_error_result("Empty sentence provided", start_time)
        
        try:
            # Step 1: Get applicable engines
            applicable_engines = self._get_applicable_engines(sentence)
            
            if not applicable_engines:
                return self._create_error_result("No applicable engines found", start_time)
            
            if debug:
                self.logger.info(f"Applicable engines: {[e.value for e in applicable_engines]}")
            
            # Step 2: Select optimal engine
            selected_engine_type = self._select_optimal_engine(sentence, applicable_engines)
            
            if debug:
                self.logger.info(f"Selected engine: {selected_engine_type.value}")
            
            # Step 3: Process with selected engine
            result = self._process_with_engine(sentence, selected_engine_type, start_time)
            
            # Step 4: Update statistics
            self._update_statistics(selected_engine_type, time.time() - start_time, result.success)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Unexpected error in process_sentence: {str(e)}")
            return self._create_error_result(f"Processing error: {str(e)}", start_time)
    
    def _get_applicable_engines(self, sentence: str) -> List[EngineType]:
        """
        Determine which engines are applicable for the given sentence.
        
        Args:
            sentence: Input sentence
            
        Returns:
            List of applicable engine types, sorted by priority
        """
        applicable = []
        
        for engine_type, engine_info in self.engines.items():
            try:
                engine_instance = engine_info.engine_instance
                
                # Check if engine has is_applicable method
                if hasattr(engine_instance, 'is_applicable'):
                    if engine_instance.is_applicable(sentence):
                        applicable.append(engine_type)
                else:
                    # Fallback: pattern-based detection
                    sentence_lower = sentence.lower()
                    for pattern in engine_info.patterns:
                        if pattern.lower() in sentence_lower:
                            applicable.append(engine_type)
                            break
                            
            except Exception as e:
                self.logger.warning(f"Error checking applicability for {engine_type.value}: {str(e)}")
        
        # Sort by priority (lower number = higher priority)
        applicable.sort(key=lambda x: self.engines[x].priority)
        
        return applicable
    
    def _select_optimal_engine(self, sentence: str, applicable_engines: List[EngineType]) -> EngineType:
        """
        Select the optimal engine from applicable engines using advanced heuristics.
        
        Args:
            sentence: Input sentence
            applicable_engines: List of applicable engines
            
        Returns:
            Selected engine type
        """
        if len(applicable_engines) == 1:
            return applicable_engines[0]
        
        # Advanced selection heuristics
        sentence_lower = sentence.lower()
        
        # Priority 1: Conjunction patterns (complex sentence structure)
        if EngineType.CONJUNCTION in applicable_engines:
            conjunction_indicators = ["because", "although", "while", "since", "even though", "whereas"]
            if any(indicator in sentence_lower for indicator in conjunction_indicators):
                return EngineType.CONJUNCTION
        
        # Priority 2: Conditional/Subjunctive patterns  
        if EngineType.SUBJUNCTIVE in applicable_engines:
            conditional_indicators = ["if", "were", "would", "could", "might", "should", "wish"]
            conditional_count = sum(1 for indicator in conditional_indicators if indicator in sentence_lower)
            if conditional_count >= 2:  # Strong conditional signal
                return EngineType.SUBJUNCTIVE
        
        # Priority 3: Passive voice (clear structural indicators)
        if EngineType.PASSIVE in applicable_engines:
            if "by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been", "being"]):
                return EngineType.PASSIVE
        
        # Priority 4: Inversion (distinctive word order)
        if EngineType.INVERSION in applicable_engines:
            inversion_starters = ["never", "rarely", "seldom", "hardly", "not only", "little", "nowhere"]
            for starter in inversion_starters:
                if sentence_lower.startswith(starter):
                    return EngineType.INVERSION
        
        # Default: Use priority order (first in list has highest priority)
        return applicable_engines[0]
    
    def _process_with_engine(self, sentence: str, engine_type: EngineType, start_time: float) -> EngineResult:
        """
        Process sentence with the specified engine.
        
        Args:
            sentence: Input sentence
            engine_type: Selected engine type
            start_time: Processing start time
            
        Returns:
            EngineResult: Processing result
        """
        import time
        
        engine_info = self.engines[engine_type]
        engine_instance = engine_info.engine_instance
        
        try:
            # Call engine's process method
            if hasattr(engine_instance, 'process'):
                raw_result = engine_instance.process(sentence)
                
                # Standardize result format
                if isinstance(raw_result, dict):
                    slots = raw_result.get('slots', {})
                    metadata = raw_result.get('metadata', {})
                    success = raw_result.get('success', True)
                    error = raw_result.get('error', None)
                else:
                    # Legacy format support
                    slots = raw_result if isinstance(raw_result, dict) else {}
                    metadata = {'engine': engine_type.value}
                    success = bool(slots)
                    error = None if slots else "No slots extracted"
                
                processing_time = time.time() - start_time
                
                return EngineResult(
                    engine_type=engine_type,
                    confidence=self._calculate_confidence(slots, metadata),
                    slots=slots,
                    metadata={**metadata, 'processing_time': processing_time, 'controller_version': '1.0'},
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
        """
        Calculate confidence score based on slot extraction quality.
        
        Args:
            slots: Extracted slots
            metadata: Processing metadata
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not slots:
            return 0.0
        
        # Base confidence from slot count and content quality
        base_score = 0.5
        
        # Bonus for essential slots
        essential_slots = ['S', 'V']
        for slot in essential_slots:
            if slot in slots and slots[slot].strip():
                base_score += 0.15
        
        # Bonus for additional slots
        additional_slots = ['O1', 'C1', 'M1', 'Aux']
        for slot in additional_slots:
            if slot in slots and slots[slot].strip():
                base_score += 0.05
        
        # Bonus for sub-slots (detailed analysis)
        sub_slots = [key for key in slots.keys() if key.startswith('sub-')]
        base_score += len(sub_slots) * 0.02
        
        # Cap at 1.0
        return min(base_score, 1.0)
    
    def _create_error_result(self, error_message: str, start_time: float) -> EngineResult:
        """Create standardized error result."""
        import time
        
        return EngineResult(
            engine_type=EngineType.GERUND,  # Placeholder
            confidence=0.0,
            slots={},
            metadata={'error': error_message},
            success=False,
            processing_time=time.time() - start_time,
            error=error_message
        )
    
    def _update_statistics(self, engine_type: EngineType, processing_time: float, success: bool):
        """Update internal processing statistics."""
        if success:
            self.processing_stats['successful_processes'] += 1
        
        self.processing_stats['engine_usage_count'][engine_type.value] += 1
        
        # Update average processing time
        total_time = (self.processing_stats['average_processing_time'] * 
                     (self.processing_stats['total_requests'] - 1) + processing_time)
        self.processing_stats['average_processing_time'] = total_time / self.processing_stats['total_requests']
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Get information about all registered engines."""
        return {
            'registered_engines': len(self.engines),
            'engine_list': [
                {
                    'type': info.engine_type.value,
                    'priority': info.priority,
                    'description': info.description,
                    'patterns': info.patterns
                }
                for info in sorted(self.engines.values(), key=lambda x: x.priority)
            ]
        }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        success_rate = (self.processing_stats['successful_processes'] / 
                       max(self.processing_stats['total_requests'], 1)) * 100
        
        return {
            **self.processing_stats,
            'success_rate_percent': round(success_rate, 2)
        }
    
    def reset_statistics(self):
        """Reset all processing statistics."""
        self.processing_stats = {
            'total_requests': 0,
            'successful_processes': 0,
            'engine_usage_count': {engine_type.value: 0 for engine_type in self.engines.keys()},
            'average_processing_time': 0.0
        }
        self.logger.info("Statistics reset")

# Test and demonstration functions
def demonstrate_master_controller():
    """Demonstrate the Grammar Master Controller with various sentence types."""
    
    controller = GrammarMasterController()
    
    test_sentences = [
        # Various grammar patterns for comprehensive testing
        "Running in the park is relaxing.",                    # Gerund
        "The book written by Shakespeare is famous.",          # Participle  
        "I want to learn programming.",                        # Infinitive
        "The man who called you is here.",                     # Relative
        "He succeeded because he worked hard.",                # Conjunction
        "The letter was written by John.",                     # Passive
        "She is taller than her sister.",                     # Comparative
        "I have been working here for five years.",           # Perfect Progressive
        "Never have I seen such beauty.",                     # Inversion
        "If I were rich, I would travel the world.",          # Subjunctive
    ]
    
    print("🏛️  Grammar Master Controller - Comprehensive Demonstration")
    print("=" * 70)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【Test {i}】: {sentence}")
        print("-" * 50)
        
        # Process with debug information
        result = controller.process_sentence(sentence, debug=False)
        
        if result.success:
            print(f"✅ Engine: {result.engine_type.value}")
            print(f"🎯 Confidence: {result.confidence:.2f}")
            print(f"⏱️  Processing Time: {result.processing_time:.4f}s")
            
            print("\n📊 Extracted Slots:")
            for slot_name, value in result.slots.items():
                if value.strip():
                    print(f"   {slot_name}: '{value}'")
        else:
            print(f"❌ Processing failed: {result.error}")
        
        print("─" * 50)
    
    # Display final statistics
    print("\n📈 Final Processing Statistics:")
    stats = controller.get_processing_stats()
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Success Rate: {stats['success_rate_percent']}%")
    print(f"   Average Processing Time: {stats['average_processing_time']:.4f}s")
    
    print("\n🎯 Engine Usage Statistics:")
    for engine, count in stats['engine_usage_count'].items():
        if count > 0:
            print(f"   {engine}: {count} times")

if __name__ == "__main__":
    demonstrate_master_controller()
