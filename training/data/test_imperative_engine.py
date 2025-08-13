#!/usr/bin/env python3
"""
Test script for Imperative Engine (Priority 15)

Tests various imperative sentence patterns:
- Simple commands
- Polite requests
- Negative imperatives
- Complex imperatives with objects
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.imperative_engine import ImperativeEngine
import time

def test_imperative_engine():
    """Test the imperative engine with various sentence patterns."""
    print("🧪 Testing Imperative Engine (Priority 15)")
    print("=" * 60)
    
    # Initialize engine
    try:
        engine = ImperativeEngine()
        print("✅ Imperative engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize imperative engine: {e}")
        return False
    
    # Test sentences with expected results
    test_cases = [
        # Simple commands
        ("Go!", {"expected_slots": ["V"], "expected_confidence": 0.8}),
        ("Stop!", {"expected_slots": ["V"], "expected_confidence": 0.8}),
        ("Run!", {"expected_slots": ["V"], "expected_confidence": 0.8}),
        ("Wait.", {"expected_slots": ["V"], "expected_confidence": 0.6}),
        
        # Polite requests
        ("Please come here.", {"expected_slots": ["M1", "V"], "expected_confidence": 0.7}),
        ("Please help me.", {"expected_slots": ["M1", "V", "O1"], "expected_confidence": 0.8}),
        ("Kindly wait a moment.", {"expected_slots": ["M1", "V", "O1"], "expected_confidence": 0.7}),
        
        # Negative imperatives
        ("Don't go!", {"expected_slots": ["Aux", "V"], "expected_confidence": 0.8}),
        ("Don't do that!", {"expected_slots": ["Aux", "V", "O1"], "expected_confidence": 0.8}),
        ("Do not enter.", {"expected_slots": ["Aux", "V"], "expected_confidence": 0.7}),
        ("Never give up!", {"expected_slots": ["Aux", "V"], "expected_confidence": 0.7}),
        
        # Commands with objects
        ("Take this book.", {"expected_slots": ["V", "O1"], "expected_confidence": 0.7}),
        ("Give me the pen.", {"expected_slots": ["V", "O2", "O1"], "expected_confidence": 0.8}),
        ("Open the door.", {"expected_slots": ["V", "O1"], "expected_confidence": 0.7}),
        ("Close the window.", {"expected_slots": ["V", "O1"], "expected_confidence": 0.7}),
        
        # Complex imperatives
        ("Please bring me the book from the table.", {"expected_slots": ["M1", "V", "O2", "O1", "C2"], "expected_confidence": 0.7}),
        ("Don't leave the keys on the desk.", {"expected_slots": ["Aux", "V", "O1", "C2"], "expected_confidence": 0.7}),
        ("You go first!", {"expected_slots": ["S", "V"], "expected_confidence": 0.7}),
        
        # Edge cases (should have low confidence or fail)
        ("I am going home.", {"expected_slots": [], "expected_confidence": 0.3}),  # Not imperative
        ("Are you coming?", {"expected_slots": [], "expected_confidence": 0.3}),   # Question
        ("He is running fast.", {"expected_slots": [], "expected_confidence": 0.3}), # Statement
    ]
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    print(f"\n📋 Running {total_tests} test cases...")
    print("-" * 60)
    
    for i, (sentence, expectations) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{sentence}'")
        
        try:
            # Process sentence
            result = engine.process(sentence, debug=False)
            
            # Check success
            expected_slots = expectations["expected_slots"]
            expected_confidence = expectations["expected_confidence"]
            
            print(f"   Slots: {result.slots}")
            print(f"   Confidence: {result.confidence:.3f}")
            print(f"   Success: {result.success}")
            print(f"   Processing time: {result.processing_time:.4f}s")
            
            # Validate results
            success = True
            
            # Check if expected slots are present
            if expected_slots:
                missing_slots = [slot for slot in expected_slots if slot not in result.slots]
                if missing_slots:
                    print(f"   ⚠️  Missing expected slots: {missing_slots}")
                    if result.confidence >= expected_confidence:
                        success = False  # Should have these slots with good confidence
            else:
                # Should have low confidence (not imperative)
                if result.confidence >= expected_confidence:
                    print(f"   ⚠️  Unexpected high confidence for non-imperative")
                    success = False
            
            # Check confidence range
            if expected_slots and result.confidence < (expected_confidence - 0.2):
                print(f"   ⚠️  Confidence too low: {result.confidence:.3f} < {expected_confidence - 0.2:.3f}")
                success = False
            
            if success:
                print(f"   ✅ Test passed")
                successful_tests += 1
            else:
                print(f"   ❌ Test failed")
                
        except Exception as e:
            print(f"   ❌ Error processing sentence: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {successful_tests}/{total_tests} passed ({successful_tests/total_tests*100:.1f}%)")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Imperative engine is working correctly.")
        return True
    else:
        print(f"⚠️  {total_tests - successful_tests} tests failed. Please review the results.")
        return False

def test_engine_info():
    """Test engine information retrieval."""
    print("\n🔍 Testing Engine Information")
    print("-" * 40)
    
    try:
        engine = ImperativeEngine()
        info = engine.get_engine_info()
        
        print(f"Engine Name: {info['name']}")
        print(f"Priority: {info['priority']}")
        print(f"Description: {info['description']}")
        print(f"Patterns: {info['patterns']}")
        print(f"Coverage: {info['coverage']}")
        print(f"Supported Slots: {info['slots_supported']}")
        print("✅ Engine info retrieved successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to get engine info: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Imperative Engine Test Suite")
    print("Testing Priority 15: Imperative Sentences")
    print("Coverage: 25% frequency → +7% coverage rate")
    print("=" * 60)
    
    start_time = time.time()
    
    # Run tests
    engine_test_passed = test_imperative_engine()
    info_test_passed = test_engine_info()
    
    end_time = time.time()
    
    print(f"\n⏱️  Total test time: {end_time - start_time:.3f} seconds")
    
    if engine_test_passed and info_test_passed:
        print("🎉 All imperative engine tests completed successfully!")
        print("✅ Ready for integration with Grammar Master Controller v2")
        return True
    else:
        print("❌ Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
