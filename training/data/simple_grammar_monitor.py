#!/usr/bin/env python3
"""
Simple Grammar Engine Monitoring System v1.0

Lightweight monitoring system for Grammar Master Controller.
Provides comprehensive performance insights and statistics.
"""

import time
import json
import threading
import datetime
from typing import Dict, List, Any
from collections import defaultdict
import logging

# Import our grammar controller
from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType, EngineResult

class SimpleMonitor:
    """Simple monitoring system for Grammar Engine performance."""
    
    def __init__(self, controller: GrammarMasterControllerV2):
        """Initialize simple monitor."""
        self.controller = controller
        self.start_time = time.time()
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'engine_usage': defaultdict(int),
            'engine_success': defaultdict(int),
            'engine_failures': defaultdict(int),
            'response_times': defaultdict(list),
            'first_request_time': {},
            'last_request_time': {}
        }
        
        # Setup logging
        self.logger = logging.getLogger('SimpleMonitor')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def record_request(self, result: EngineResult):
        """Record a request for monitoring."""
        engine_type = result.engine_type.value
        current_time = time.time()
        
        # Update overall stats
        self.stats['total_requests'] += 1
        
        if result.success:
            self.stats['successful_requests'] += 1
            self.stats['engine_success'][engine_type] += 1
        else:
            self.stats['failed_requests'] += 1
            self.stats['engine_failures'][engine_type] += 1
        
        # Update engine-specific stats
        self.stats['engine_usage'][engine_type] += 1
        self.stats['response_times'][engine_type].append(result.processing_time * 1000)  # Convert to ms
        
        # Track timing
        if engine_type not in self.stats['first_request_time']:
            self.stats['first_request_time'][engine_type] = current_time
        self.stats['last_request_time'][engine_type] = current_time
    
    def get_comprehensive_report(self) -> str:
        """Generate comprehensive monitoring report."""
        uptime = time.time() - self.start_time
        
        report = []
        report.append("🚀 Grammar Engine Performance Report")
        report.append("=" * 60)
        
        # Overall System Stats
        report.append(f"\n📊 SYSTEM OVERVIEW")
        report.append(f"   ⏱️  System Uptime: {self._format_time(uptime)}")
        report.append(f"   📈 Total Requests: {self.stats['total_requests']}")
        report.append(f"   ✅ Successful: {self.stats['successful_requests']}")
        report.append(f"   ❌ Failed: {self.stats['failed_requests']}")
        
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
            report.append(f"   🎯 Success Rate: {success_rate:.1f}%")
        
        # Controller Stats
        controller_info = self.controller.get_engine_info()
        report.append(f"\n⚙️ ENGINE CONTROLLER STATUS")
        report.append(f"   📦 Registered Engines: {controller_info['registered_engines']}")
        report.append(f"   🔧 Loaded Engines: {controller_info['loaded_engines']}")
        report.append(f"   💾 {controller_info['memory_efficiency']}")
        
        # Individual Engine Performance
        report.append(f"\n🔍 INDIVIDUAL ENGINE PERFORMANCE")
        report.append("-" * 50)
        
        # Sort engines by usage
        engines_by_usage = sorted(
            self.stats['engine_usage'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for engine_name, usage_count in engines_by_usage:
            if usage_count == 0:
                continue
                
            successes = self.stats['engine_success'][engine_name]
            failures = self.stats['engine_failures'][engine_name]
            engine_success_rate = (successes / usage_count * 100) if usage_count > 0 else 0
            
            # Response time stats
            response_times = self.stats['response_times'][engine_name]
            avg_response = sum(response_times) / len(response_times) if response_times else 0
            min_response = min(response_times) if response_times else 0
            max_response = max(response_times) if response_times else 0
            
            # Timing info
            first_used = self.stats['first_request_time'].get(engine_name)
            last_used = self.stats['last_request_time'].get(engine_name)
            
            report.append(f"\n🔧 {engine_name.upper()} ENGINE:")
            report.append(f"   📊 Usage Count: {usage_count}")
            report.append(f"   ✅ Success Rate: {engine_success_rate:.1f}% ({successes}/{usage_count})")
            report.append(f"   ⏱️  Avg Response: {avg_response:.2f}ms")
            report.append(f"   📈 Response Range: {min_response:.2f}ms - {max_response:.2f}ms")
            
            if first_used:
                time_since_first = time.time() - first_used
                time_since_last = time.time() - last_used
                report.append(f"   🕐 First Used: {self._format_time_ago(time_since_first)} ago")
                report.append(f"   🕐 Last Used: {self._format_time_ago(time_since_last)} ago")
        
        # Unused Engines
        unused_engines = []
        for engine_type in EngineType:
            if engine_type.value not in self.stats['engine_usage'] or self.stats['engine_usage'][engine_type.value] == 0:
                unused_engines.append(engine_type.value)
        
        if unused_engines:
            report.append(f"\n💤 UNUSED ENGINES:")
            for engine_name in unused_engines:
                report.append(f"   🔒 {engine_name.upper()}: Never loaded (memory efficient!)")
        
        # Performance Insights
        report.append(f"\n🧠 PERFORMANCE INSIGHTS")
        if self.stats['total_requests'] > 0:
            most_used = max(self.stats['engine_usage'], key=self.stats['engine_usage'].get)
            most_used_count = self.stats['engine_usage'][most_used]
            usage_percentage = (most_used_count / self.stats['total_requests']) * 100
            
            report.append(f"   🥇 Most Used Engine: {most_used.upper()} ({usage_percentage:.1f}% of requests)")
            
            # Response time analysis
            all_response_times = []
            for times in self.stats['response_times'].values():
                all_response_times.extend(times)
            
            if all_response_times:
                avg_global_response = sum(all_response_times) / len(all_response_times)
                report.append(f"   ⚡ Global Avg Response: {avg_global_response:.2f}ms")
                
                # Find fastest and slowest engines
                engine_avg_times = {}
                for engine, times in self.stats['response_times'].items():
                    if times:
                        engine_avg_times[engine] = sum(times) / len(times)
                
                if engine_avg_times:
                    fastest_engine = min(engine_avg_times, key=engine_avg_times.get)
                    slowest_engine = max(engine_avg_times, key=engine_avg_times.get)
                    
                    report.append(f"   🚀 Fastest Engine: {fastest_engine.upper()} ({engine_avg_times[fastest_engine]:.2f}ms)")
                    report.append(f"   🐌 Slowest Engine: {slowest_engine.upper()} ({engine_avg_times[slowest_engine]:.2f}ms)")
        
        # Memory Efficiency Analysis
        loaded_engines = controller_info['loaded_engines']
        total_engines = controller_info['registered_engines']
        memory_saved = total_engines - loaded_engines
        
        report.append(f"\n💾 MEMORY EFFICIENCY ANALYSIS")
        report.append(f"   🎯 Lazy Loading Success: {memory_saved}/{total_engines} engines not loaded")
        report.append(f"   💚 Memory Savings: ~{(memory_saved / total_engines * 100):.1f}% memory not used")
        report.append(f"   ⚡ Startup Impact: Instant startup regardless of total engines")
        
        return "\n".join(report)
    
    def _format_time(self, seconds: float) -> str:
        """Format time duration."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def _format_time_ago(self, seconds: float) -> str:
        """Format time ago."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m"
        else:
            return f"{seconds/3600:.1f}h"

class EnhancedGrammarControllerWithMonitoring(GrammarMasterControllerV2):
    """Enhanced Grammar Controller with integrated monitoring."""
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize enhanced controller with monitoring."""
        super().__init__(log_level)
        self.monitor = SimpleMonitor(self)
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """Enhanced process_sentence with monitoring."""
        result = super().process_sentence(sentence, debug)
        
        # Record for monitoring
        self.monitor.record_request(result)
        
        return result
    
    def get_performance_report(self) -> str:
        """Get comprehensive performance report."""
        return self.monitor.get_comprehensive_report()

# Demonstration
def demonstrate_monitoring_system():
    """Demonstrate the monitoring system."""
    
    print("🚀 Grammar Engine Monitoring System Demo")
    print("=" * 60)
    
    # Initialize enhanced controller
    controller = EnhancedGrammarControllerWithMonitoring()
    
    print(f"\n✅ Enhanced Grammar Controller initialized")
    print(f"📊 Monitoring system active")
    print(f"⚡ Lazy loading enabled")
    
    # Process test sentences
    test_sentences = [
        "If I were rich, I would travel the world.",
        "The book that you recommended is excellent.", 
        "She worked hard because she wanted to succeed.",
        "The letter was written by John yesterday.",
        "Never have I seen such a beautiful sunset.",
        "Swimming in the ocean is my favorite activity.",
        "Running quickly through the park, he felt free.",
        "I want to learn how to play the guitar.",
        "This is more interesting than I expected.",
        "I have been studying English for five years.",
        "Although it was raining, we went for a walk.",
        "The house which was built last year is beautiful.",
        "If I had known, I would have come earlier.",
        "Reading books is one of my hobbies.",
        "She is taller than her sister.",
    ]
    
    print(f"\n🧪 Processing {len(test_sentences)} test sentences...")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"   Processing {i:2d}/{len(test_sentences)}: {sentence[:50]}...")
        result = controller.process_sentence(sentence)
        time.sleep(0.1)  # Small delay
    
    print(f"\n✅ All test sentences processed!")
    
    # Generate and display report
    print(f"\n📈 Generating comprehensive performance report...")
    
    report = controller.get_performance_report()
    print(f"\n{report}")
    
    print(f"\n🎯 Monitoring Features Demonstrated:")
    print(f"   ✅ Request tracking and success rates")
    print(f"   ✅ Response time analysis per engine")
    print(f"   ✅ Memory efficiency monitoring")
    print(f"   ✅ Engine usage patterns")
    print(f"   ✅ Performance insights and recommendations")
    print(f"   ✅ Lazy loading effectiveness tracking")

if __name__ == "__main__":
    demonstrate_monitoring_system()
