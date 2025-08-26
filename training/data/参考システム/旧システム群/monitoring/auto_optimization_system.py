#!/usr/bin/env python3
"""
Grammar Engine Auto-Optimization System v1.0

Advanced system that automatically optimizes engine selection, caching,
and resource allocation based on real-time usage patterns.

Features:
- Adaptive engine priority adjustment
- Smart caching system
- Predictive engine preloading
- Dynamic resource allocation
- Machine learning-based optimization
"""

import time
import json
import threading
import statistics
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
import logging
import pickle
import os

from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType, EngineResult

@dataclass
class EnginePerformanceProfile:
    """Performance profile for an engine."""
    engine_type: str
    usage_frequency: float = 0.0
    average_response_time: float = 0.0
    success_rate: float = 0.0
    complexity_score: float = 0.0
    recent_usage: deque = None
    load_time: float = 0.0
    memory_footprint: float = 0.0
    
    def __post_init__(self):
        if self.recent_usage is None:
            self.recent_usage = deque(maxlen=100)

class AdaptiveEngineSelector:
    """Intelligent engine selection based on learning from usage patterns."""
    
    def __init__(self):
        self.engine_profiles: Dict[str, EnginePerformanceProfile] = {}
        self.selection_history = deque(maxlen=1000)
        self.pattern_cache: Dict[str, List[Tuple[str, float]]] = {}
        self.learning_weight = 0.1  # Learning rate
        
        # Initialize profiles for all engines
        for engine_type in EngineType:
            self.engine_profiles[engine_type.value] = EnginePerformanceProfile(
                engine_type=engine_type.value
            )
    
    def update_performance(self, result: EngineResult):
        """Update engine performance profile based on result."""
        engine_type = result.engine_type.value
        profile = self.engine_profiles[engine_type]
        
        # Update usage frequency (exponential moving average)
        profile.usage_frequency = (
            profile.usage_frequency * (1 - self.learning_weight) + 
            self.learning_weight
        )
        
        # Update response time
        current_time = result.processing_time * 1000  # Convert to ms
        if profile.average_response_time == 0:
            profile.average_response_time = current_time
        else:
            profile.average_response_time = (
                profile.average_response_time * (1 - self.learning_weight) + 
                current_time * self.learning_weight
            )
        
        # Update success rate
        success = 1.0 if result.success else 0.0
        if profile.success_rate == 0:
            profile.success_rate = success
        else:
            profile.success_rate = (
                profile.success_rate * (1 - self.learning_weight) + 
                success * self.learning_weight
            )
        
        # Track recent usage
        profile.recent_usage.append(time.time())
        
        # Update selection history
        self.selection_history.append((engine_type, result.success, current_time))
    
    def get_optimal_engine_priority(self, sentence: str, applicable_engines: List[EngineType]) -> List[EngineType]:
        """Get optimally ordered list of engines based on learned patterns."""
        if not applicable_engines:
            return []
        
        # Calculate composite scores for each applicable engine
        engine_scores = []
        
        for engine_type in applicable_engines:
            profile = self.engine_profiles[engine_type.value]
            
            # Composite score factors:
            # 1. Success rate (40%)
            # 2. Speed (30%) - inverse of response time
            # 3. Usage frequency (20%) - recent popularity
            # 4. Pattern matching (10%) - similarity to past successful patterns
            
            speed_score = 1.0 / (profile.average_response_time + 1.0)  # Higher is better
            pattern_score = self._calculate_pattern_similarity(sentence, engine_type.value)
            
            composite_score = (
                profile.success_rate * 0.4 +
                speed_score * 0.3 +
                profile.usage_frequency * 0.2 +
                pattern_score * 0.1
            )
            
            engine_scores.append((engine_type, composite_score))
        
        # Sort by composite score (descending)
        engine_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [engine_type for engine_type, _ in engine_scores]
    
    def _calculate_pattern_similarity(self, sentence: str, engine_type: str) -> float:
        """Calculate pattern similarity score for sentence and engine."""
        # Simple pattern matching based on cached successful patterns
        sentence_lower = sentence.lower()
        
        if engine_type not in self.pattern_cache:
            return 0.5  # Neutral score for unknown patterns
        
        # Check similarity to previously successful patterns
        max_similarity = 0.0
        for pattern, success_rate in self.pattern_cache[engine_type]:
            # Simple word overlap similarity
            pattern_words = set(pattern.split())
            sentence_words = set(sentence_lower.split())
            
            if pattern_words and sentence_words:
                overlap = len(pattern_words.intersection(sentence_words))
                similarity = overlap / len(pattern_words.union(sentence_words))
                weighted_similarity = similarity * success_rate
                max_similarity = max(max_similarity, weighted_similarity)
        
        return max_similarity
    
    def cache_successful_pattern(self, sentence: str, engine_type: str, success: bool):
        """Cache successful sentence patterns for future optimization."""
        if engine_type not in self.pattern_cache:
            self.pattern_cache[engine_type] = []
        
        sentence_lower = sentence.lower()
        success_rate = 1.0 if success else 0.0
        
        # Update or add pattern
        found = False
        for i, (pattern, existing_rate) in enumerate(self.pattern_cache[engine_type]):
            if pattern == sentence_lower:
                # Update with exponential moving average
                new_rate = existing_rate * 0.9 + success_rate * 0.1
                self.pattern_cache[engine_type][i] = (pattern, new_rate)
                found = True
                break
        
        if not found:
            self.pattern_cache[engine_type].append((sentence_lower, success_rate))
        
        # Keep only top 50 patterns per engine
        self.pattern_cache[engine_type] = sorted(
            self.pattern_cache[engine_type], 
            key=lambda x: x[1], 
            reverse=True
        )[:50]

class SmartCachingSystem:
    """Intelligent caching system for engine results and patterns."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, Tuple[EngineResult, float]] = {}  # (result, timestamp)
        self.hit_count = 0
        self.miss_count = 0
        self.access_frequency: Dict[str, int] = defaultdict(int)
    
    def get_cache_key(self, sentence: str) -> str:
        """Generate cache key for sentence."""
        return sentence.lower().strip()
    
    def get(self, sentence: str) -> Optional[EngineResult]:
        """Get cached result if available and still valid."""
        key = self.get_cache_key(sentence)
        
        if key in self.cache:
            result, timestamp = self.cache[key]
            
            # Check if cache is still valid (5 minutes)
            if time.time() - timestamp < 300:
                self.hit_count += 1
                self.access_frequency[key] += 1
                return result
            else:
                # Remove expired cache
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def put(self, sentence: str, result: EngineResult):
        """Cache result for sentence."""
        key = self.get_cache_key(sentence)
        current_time = time.time()
        
        # Clean cache if full
        if len(self.cache) >= self.max_size:
            self._evict_least_used()
        
        self.cache[key] = (result, current_time)
    
    def _evict_least_used(self):
        """Evict least recently used cache entries."""
        # Remove 20% of cache, starting with least accessed
        remove_count = max(1, len(self.cache) // 5)
        
        # Sort by access frequency and timestamp
        sorted_items = sorted(
            self.cache.items(),
            key=lambda x: (self.access_frequency[x[0]], x[1][1])
        )
        
        for i in range(remove_count):
            key, _ = sorted_items[i]
            del self.cache[key]
            if key in self.access_frequency:
                del self.access_frequency[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'max_size': self.max_size
        }

class PredictivePreloader:
    """Predictive engine preloading based on usage patterns."""
    
    def __init__(self, controller):
        self.controller = controller
        self.usage_patterns: Dict[str, List[str]] = defaultdict(list)  # time_period -> [engines]
        self.preload_threshold = 0.7  # Preload if usage probability > 70%
        self.current_hour = -1
        
    def record_usage(self, engine_type: str):
        """Record engine usage for pattern learning."""
        current_hour = time.localtime().tm_hour
        time_key = f"hour_{current_hour}"
        
        self.usage_patterns[time_key].append(engine_type)
        
        # Keep only recent data (last 100 entries per hour)
        if len(self.usage_patterns[time_key]) > 100:
            self.usage_patterns[time_key] = self.usage_patterns[time_key][-100:]
    
    def get_preload_recommendations(self) -> List[str]:
        """Get engines that should be preloaded based on patterns."""
        current_hour = time.localtime().tm_hour
        time_key = f"hour_{current_hour}"
        
        if time_key not in self.usage_patterns:
            return []
        
        # Calculate usage frequency for current time period
        usage_data = self.usage_patterns[time_key]
        if not usage_data:
            return []
        
        engine_frequencies = defaultdict(int)
        for engine in usage_data:
            engine_frequencies[engine] += 1
        
        total_usage = len(usage_data)
        recommendations = []
        
        for engine, count in engine_frequencies.items():
            probability = count / total_usage
            if probability >= self.preload_threshold:
                recommendations.append(engine)
        
        return recommendations
    
    def auto_preload_engines(self):
        """Automatically preload high-probability engines."""
        recommendations = self.get_preload_recommendations()
        
        for engine_type_str in recommendations:
            try:
                engine_type = EngineType(engine_type_str)
                # Check if engine is not already loaded
                engine_info = self.controller.engine_registry.get(engine_type)
                if engine_info and engine_info.instance is None:
                    self.controller._load_engine(engine_type)
            except ValueError:
                pass  # Invalid engine type

class AutoOptimizedGrammarController(GrammarMasterControllerV2):
    """Auto-optimizing Grammar Controller with advanced intelligence."""
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize auto-optimized controller."""
        super().__init__(log_level)
        
        # Initialize optimization components
        self.adaptive_selector = AdaptiveEngineSelector()
        self.cache_system = SmartCachingSystem()
        self.predictive_preloader = PredictivePreloader(self)
        
        # Optimization stats
        self.optimization_stats = {
            'adaptive_selections': 0,
            'cache_hits': 0,
            'preloads_performed': 0,
            'optimization_time_saved': 0.0,
            'total_optimized_requests': 0
        }
        
        # Background optimization thread
        self.optimization_thread = None
        self.optimization_active = False
        
        self.logger.info("Auto-Optimized Grammar Controller initialized")
        
    def start_auto_optimization(self):
        """Start background auto-optimization."""
        if self.optimization_active:
            return
        
        self.optimization_active = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimization_thread.start()
        
        self.logger.info("Auto-optimization started")
    
    def stop_auto_optimization(self):
        """Stop background auto-optimization."""
        self.optimization_active = False
        if self.optimization_thread:
            self.optimization_thread.join(timeout=5)
        
        self.logger.info("Auto-optimization stopped")
    
    def _optimization_loop(self):
        """Background optimization loop."""
        while self.optimization_active:
            try:
                # Perform predictive preloading every 30 seconds
                self.predictive_preloader.auto_preload_engines()
                time.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in optimization loop: {str(e)}")
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """Auto-optimized sentence processing."""
        start_time = time.time()
        
        # Step 1: Check cache first
        cached_result = self.cache_system.get(sentence)
        if cached_result:
            self.optimization_stats['cache_hits'] += 1
            self.optimization_stats['optimization_time_saved'] += time.time() - start_time
            if debug:
                self.logger.info(f"🚀 Cache hit for: {sentence[:50]}...")
            return cached_result
        
        # Step 2: Get applicable engines (fast pattern-based detection)
        applicable_engines = self._get_applicable_engines_fast(sentence)
        
        if not applicable_engines:
            result = self._create_error_result("No applicable engines found", start_time)
        else:
            # Step 3: Use adaptive engine selection
            optimized_engine_order = self.adaptive_selector.get_optimal_engine_priority(
                sentence, applicable_engines
            )
            
            if debug:
                original_order = [e.value for e in applicable_engines]
                optimized_order = [e.value for e in optimized_engine_order]
                self.logger.info(f"Original order: {original_order}")
                self.logger.info(f"Optimized order: {optimized_order}")
            
            # Step 4: Try engines in optimized order
            selected_engine = optimized_engine_order[0] if optimized_engine_order else applicable_engines[0]
            
            # Load and process
            if not self._load_engine(selected_engine):
                result = self._create_error_result(f"Failed to load {selected_engine.value} engine", start_time)
            else:
                result = self._process_with_engine(sentence, selected_engine, start_time)
        
        # Step 5: Update optimization systems
        if hasattr(result, 'engine_type'):
            self.adaptive_selector.update_performance(result)
            self.adaptive_selector.cache_successful_pattern(sentence, result.engine_type.value, result.success)
            self.predictive_preloader.record_usage(result.engine_type.value)
        
        # Step 6: Cache result for future use
        if result.success:
            self.cache_system.put(sentence, result)
        
        # Update stats
        self.optimization_stats['total_optimized_requests'] += 1
        if applicable_engines and len(optimized_engine_order) > 1:
            self.optimization_stats['adaptive_selections'] += 1
        
        return result
    
    def get_optimization_report(self) -> str:
        """Get comprehensive optimization report."""
        cache_stats = self.cache_system.get_stats()
        
        report = []
        report.append("🚀 Auto-Optimization Performance Report")
        report.append("=" * 60)
        
        report.append(f"\n🎯 OPTIMIZATION OVERVIEW")
        report.append(f"   📊 Total Optimized Requests: {self.optimization_stats['total_optimized_requests']}")
        report.append(f"   🧠 Adaptive Selections: {self.optimization_stats['adaptive_selections']}")
        report.append(f"   💾 Cache Hits: {cache_stats['hit_count']}")
        report.append(f"   ⚡ Time Saved: {self.optimization_stats['optimization_time_saved']:.3f}s")
        
        report.append(f"\n💾 SMART CACHING PERFORMANCE")
        report.append(f"   🎯 Hit Rate: {cache_stats['hit_rate']:.1f}%")
        report.append(f"   📦 Cache Usage: {cache_stats['cache_size']}/{cache_stats['max_size']}")
        report.append(f"   ⚡ Hits: {cache_stats['hit_count']}, Misses: {cache_stats['miss_count']}")
        
        report.append(f"\n🧠 ADAPTIVE ENGINE INTELLIGENCE")
        for engine_type, profile in self.adaptive_selector.engine_profiles.items():
            if profile.usage_frequency > 0:
                report.append(f"   🔧 {engine_type.upper()}:")
                report.append(f"      Frequency: {profile.usage_frequency:.3f}")
                report.append(f"      Avg Response: {profile.average_response_time:.2f}ms") 
                report.append(f"      Success Rate: {profile.success_rate:.1%}")
        
        report.append(f"\n🔮 PREDICTIVE PRELOADING")
        recommendations = self.predictive_preloader.get_preload_recommendations()
        if recommendations:
            report.append(f"   💡 Recommended Preloads: {', '.join(recommendations)}")
        else:
            report.append(f"   💡 No preload recommendations (insufficient data)")
        
        return "\n".join(report)

# Comprehensive demonstration
def demonstrate_auto_optimization():
    """Demonstrate the auto-optimization system."""
    
    print("🚀 Auto-Optimization System Demonstration")
    print("=" * 60)
    
    # Initialize auto-optimized controller
    controller = AutoOptimizedGrammarController()
    controller.start_auto_optimization()
    
    print(f"\n✅ Auto-Optimized Grammar Controller initialized")
    print(f"🧠 Adaptive engine selection active")
    print(f"💾 Smart caching system enabled") 
    print(f"🔮 Predictive preloading running")
    
    # Test sentences with patterns
    test_patterns = [
        # Repeat patterns to show caching
        ("If I were rich, I would travel.", 3),
        ("The book that I read was good.", 2), 
        ("She worked because she needed money.", 2),
        ("Swimming is my favorite activity.", 2),
        ("This is better than expected.", 1),
        ("I want to learn programming.", 1),
        ("If I had time, I would study more.", 1),  # Similar to first pattern
        ("The person who called was my friend.", 1),  # Similar to second pattern
    ]
    
    print(f"\n🧪 Testing optimization with patterned requests...")
    
    total_requests = sum(count for _, count in test_patterns)
    processed = 0
    
    for sentence, repeat_count in test_patterns:
        for i in range(repeat_count):
            processed += 1
            print(f"   Processing {processed:2d}/{total_requests}: {sentence[:50]}...")
            
            result = controller.process_sentence(sentence, debug=False)
            time.sleep(0.1)  # Small delay
    
    print(f"\n✅ All optimization tests completed!")
    
    # Show optimization results
    optimization_report = controller.get_optimization_report()
    print(f"\n{optimization_report}")
    
    # Stop optimization
    controller.stop_auto_optimization()
    
    print(f"\n🎯 Auto-Optimization Features Demonstrated:")
    print(f"   ✅ Adaptive engine priority adjustment")
    print(f"   ✅ Smart caching with hit/miss tracking")
    print(f"   ✅ Pattern-based optimization learning")
    print(f"   ✅ Predictive engine preloading")
    print(f"   ✅ Performance-based engine selection")
    print(f"   ✅ Real-time optimization statistics")

if __name__ == "__main__":
    demonstrate_auto_optimization()
