#!/usr/bin/env python3
"""
All Engines Integration Test
Comprehensive test of all 17 registered engines in Grammar Master Controller v2
"""

from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType
import time

def test_all_engines():
    """Test all 17 engines with representative sentences."""
    controller = GrammarMasterControllerV2()
    
    # Test cases for each engine with expected engine type
    test_cases = [
        # Priority 0: Basic Five Pattern
        ("I love you.", EngineType.BASIC_FIVE),
        ("She gave him a book.", EngineType.BASIC_FIVE),
        
        # Priority 1: Modal
        ("You can do it.", EngineType.MODAL),
        ("We should leave now.", EngineType.MODAL),
        
        # Priority 2: Conjunction
        ("I stayed home because it was raining.", EngineType.CONJUNCTION),
        ("Although he was tired, he continued working.", EngineType.CONJUNCTION),
        
        # Priority 3: Relative
        ("The book that I bought is interesting.", EngineType.RELATIVE),
        ("The person who called you is waiting.", EngineType.RELATIVE),
        
        # Priority 4: Passive
        ("The cake was eaten by the children.", EngineType.PASSIVE),
        ("The letter has been written.", EngineType.PASSIVE),
        
        # Priority 5: Progressive
        ("She is reading a book.", EngineType.PROGRESSIVE),
        ("They were playing football.", EngineType.PROGRESSIVE),
        
        # Priority 6: Prepositional
        ("The cat is on the table.", EngineType.PREPOSITIONAL),
        ("We walked through the park.", EngineType.PREPOSITIONAL),
        
        # Priority 7: Perfect Progressive
        ("I have been waiting for hours.", EngineType.PERFECT_PROGRESSIVE),
        ("She had been studying all night.", EngineType.PERFECT_PROGRESSIVE),
        
        # Priority 8: Subjunctive
        ("If I were you, I would go.", EngineType.SUBJUNCTIVE),
        ("I wish he were here.", EngineType.SUBJUNCTIVE),
        
        # Priority 9: Inversion
        ("Never have I seen such beauty.", EngineType.INVERSION),
        ("Rarely does he speak in public.", EngineType.INVERSION),
        
        # Priority 10: Comparative
        ("She is taller than her sister.", EngineType.COMPARATIVE),
        ("This is the most beautiful place.", EngineType.COMPARATIVE),
        
        # Priority 11: Gerund
        ("Swimming is my favorite sport.", EngineType.GERUND),
        ("I enjoy reading books.", EngineType.GERUND),
        
        # Priority 12: Participle
        ("The running water was cold.", EngineType.PARTICIPLE),
        ("Excited by the news, she called everyone.", EngineType.PARTICIPLE),
        
        # Priority 13: Infinitive
        ("I want to learn English.", EngineType.INFINITIVE),
        ("She decided to move to Tokyo.", EngineType.INFINITIVE),
        
        # Priority 14: Question
        ("What are you doing?", EngineType.QUESTION),
        ("Where did you go?", EngineType.QUESTION),
        
        # Priority 15: Imperative
        ("Please close the door.", EngineType.IMPERATIVE),
        ("Don't forget to call me.", EngineType.IMPERATIVE),
        
        # Priority 16: Existential There
        ("There is a book on the table.", EngineType.EXISTENTIAL_THERE),
        ("There are many students here.", EngineType.EXISTENTIAL_THERE),
    ]
    
    print("🧪 Testing All 17 Engines Integration")
    print("=" * 60)
    
    results = {
        'total_tests': len(test_cases),
        'correct_engine_selection': 0,
        'successful_processing': 0,
        'failed_tests': [],
        'engine_coverage': set()
    }
    
    for i, (sentence, expected_engine) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i:02d}: '{sentence}'")
        print(f"   Expected: {expected_engine.value}")
        
        try:
            start_time = time.time()
            result = controller.process_sentence(sentence)
            processing_time = time.time() - start_time
            
            print(f"   Selected: {result.engine_type.value}")
            print(f"   Slots: {result.slots}")
            print(f"   Confidence: {result.confidence:.3f}")
            print(f"   Time: {processing_time:.4f}s")
            
            # Check results
            if result.engine_type == expected_engine:
                results['correct_engine_selection'] += 1
                print("   ✅ Correct engine selected")
            else:
                print(f"   ⚠️  Different engine: {result.engine_type.value}")
            
            if result.success:
                results['successful_processing'] += 1
                print("   ✅ Processing successful")
            else:
                print("   ❌ Processing failed")
                results['failed_tests'].append(f"Test {i}: {sentence}")
            
            results['engine_coverage'].add(result.engine_type)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results['failed_tests'].append(f"Test {i}: {sentence} - Error: {e}")
        
        print("-" * 50)
    
    # Final results
    print(f"\n📊 Final Results:")
    print(f"   Total tests: {results['total_tests']}")
    print(f"   Correct engine selection: {results['correct_engine_selection']}/{results['total_tests']} ({results['correct_engine_selection']/results['total_tests']*100:.1f}%)")
    print(f"   Successful processing: {results['successful_processing']}/{results['total_tests']} ({results['successful_processing']/results['total_tests']*100:.1f}%)")
    print(f"   Engines tested: {len(results['engine_coverage'])}/17")
    print(f"   Engine coverage: {sorted([e.value for e in results['engine_coverage']])}")
    
    if results['failed_tests']:
        print(f"\n❌ Failed tests:")
        for failed in results['failed_tests']:
            print(f"   - {failed}")
    
    print(f"\n🏁 Overall status: {'✅ All engines working' if len(results['failed_tests']) == 0 else '⚠️  Some issues found'}")

if __name__ == "__main__":
    test_all_engines()
