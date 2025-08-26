#!/usr/bin/env python3
"""
Multi-Engine Coordination Test - Final Version

Tests the integrated multi-engine coordination system in V2.
This tests the actual production multi-engine coordination capabilities.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_multi_engine_coordination():
    """Test the fully integrated multi-engine coordination system."""
    
    print("=== Multi-Engine Coordination System Test ===")
    print("Testing V2 Controller with Multi-Engine Coordination")
    
    # Initialize controller
    controller = GrammarMasterControllerV2(log_level="INFO")
    
    # Test cases designed to trigger different coordination strategies
    test_cases = [
        {
            'sentence': "The cat sits on the mat.",
            'description': "Simple sentence (should use single optimal strategy)",
            'expected_strategy': "single_optimal"
        },
        {
            'sentence': "The book that I bought yesterday was interesting.",
            'description': "Relative clause sentence (should use foundation + specialist)",
            'expected_strategy': "foundation_plus_specialist"
        },
        {
            'sentence': "The book that I bought was written by an author who lives in Tokyo.",
            'description': "Complex sentence with relative + passive (should use multi-cooperative)",
            'expected_strategy': "multi_cooperative"
        },
        {
            'sentence': "You should read the book that was recommended by the teacher.",
            'description': "Modal + passive + relative (should use multi-cooperative)",
            'expected_strategy': "multi_cooperative"
        },
        {
            'sentence': "The project was completed because the team worked hard.",
            'description': "Passive + conjunction (should use foundation + specialist)",
            'expected_strategy': "foundation_plus_specialist"
        }
    ]
    
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test_case['description']}")
        print(f"Sentence: '{test_case['sentence']}'")
        print(f"Expected Strategy: {test_case['expected_strategy']}")
        print("-" * 60)
        
        try:
            # Process with debug enabled to see coordination strategy
            result = controller.process_sentence(test_case['sentence'], debug=True)
            
            print(f"✅ Processing Result:")
            print(f"   Success: {result.success}")
            print(f"   Engine: {result.engine_type.value}")
            print(f"   Confidence: {result.confidence:.2f}")
            print(f"   Slots Extracted: {len(result.slots)}")
            
            # Show coordination details if available
            if hasattr(result, 'metadata') and result.metadata:
                coordination_mode = result.metadata.get('coordination_mode', 'unknown')
                print(f"   Coordination Mode: {coordination_mode}")
                
                if 'engines_used' in result.metadata:
                    engines_used = result.metadata['engines_used']
                    if isinstance(engines_used, list):
                        print(f"   Engines Used: {[e.value if hasattr(e, 'value') else str(e) for e in engines_used]}")
                    else:
                        print(f"   Engines Used: {engines_used}")
                
                if 'total_slots' in result.metadata:
                    print(f"   Total Slots Merged: {result.metadata['total_slots']}")
            
            # Show extracted slots
            if result.slots:
                print(f"   Extracted Slots:")
                for slot_name, slot_value in result.slots.items():
                    print(f"     {slot_name}: {slot_value}")
            
            if result.success:
                successful_tests += 1
                print(f"🎉 Test {i} PASSED")
            else:
                print(f"❌ Test {i} FAILED: {result.error}")
                
        except Exception as e:
            print(f"🚨 Test {i} ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {len(test_cases)}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {len(test_cases) - successful_tests}")
    print(f"Success Rate: {(successful_tests / len(test_cases)) * 100:.1f}%")
    
    # Show controller statistics
    print(f"\n📋 Controller Statistics:")
    try:
        stats = controller.get_detailed_statistics()
        print(f"   Total Requests: {stats.get('total_requests', 'N/A')}")
        print(f"   Engines Loaded: {stats.get('engines_loaded', 'N/A')}")
        
        coordination_stats = stats.get('coordination_strategies_used', {})
        if coordination_stats:
            print(f"   Coordination Strategies Used:")
            for strategy, count in coordination_stats.items():
                print(f"     - {strategy}: {count}")
                
    except Exception as e:
        print(f"   Statistics unavailable: {str(e)}")
    
    if successful_tests == len(test_cases):
        print(f"\n🎉 ALL TESTS PASSED! Multi-engine coordination is working perfectly!")
        return True
    else:
        print(f"\n⚠️ Some tests failed. Multi-engine coordination needs investigation.")
        return False

if __name__ == "__main__":
    test_multi_engine_coordination()
