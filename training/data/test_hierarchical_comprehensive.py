#!/usr/bin/env python3
"""
Enhanced Hierarchical Grammar Detection Test
============================================

Comprehensive test to validate the hierarchical detection system
and identify areas for further improvement.
"""

from hierarchical_grammar_detector import HierarchicalGrammarDetector, HierarchicalGrammarResult
from advanced_grammar_detector import GrammarPattern

def comprehensive_hierarchical_test():
    """Comprehensive test of hierarchical grammar detection."""
    
    detector = HierarchicalGrammarDetector()
    
    # Test cases with expected results
    test_cases = [
        {
            'sentence': "Being a teacher, she knows how to explain difficult concepts.",
            'expected': {
                'main_pattern': GrammarPattern.SVO_PATTERN,  # "she knows [something]"
                'subordinate_patterns': [GrammarPattern.GERUND_PATTERN],  # "Being a teacher"
                'embedded_patterns': [GrammarPattern.INFINITIVE_PATTERN]  # "how to explain"
            }
        },
        
        {
            'sentence': "The book that was written by John is very good.",
            'expected': {
                'main_pattern': GrammarPattern.SVC_PATTERN,  # "book is good"
                'subordinate_patterns': [GrammarPattern.PASSIVE_PATTERN],  # "was written by John" (relative)
                'embedded_patterns': []
            }
        },
        
        {
            'sentence': "Please tell me if there are any problems.",
            'expected': {
                'main_pattern': GrammarPattern.IMPERATIVE_PATTERN,  # "Please tell"
                'subordinate_patterns': [GrammarPattern.EXISTENTIAL_THERE],  # "there are problems"
                'embedded_patterns': []
            }
        },
        
        {
            'sentence': "Having finished the work, she went home.",
            'expected': {
                'main_pattern': GrammarPattern.SV_PATTERN,  # "she went"
                'subordinate_patterns': [GrammarPattern.PARTICIPLE_PATTERN],  # "Having finished"
                'embedded_patterns': []
            }
        }
    ]
    
    print("🧪 Comprehensive Hierarchical Grammar Test")
    print("=" * 60)
    
    total_tests = 0
    correct_main = 0
    correct_subordinate = 0
    total_subordinate_expected = 0
    total_subordinate_detected = 0
    
    for test_case in test_cases:
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"\n📝 Sentence: \"{sentence}\"")
        print("=" * 50)
        
        result = detector.detect_hierarchical_grammar(sentence)
        
        # Check main clause pattern
        actual_main = result.main_clause.grammatical_pattern if result.main_clause else None
        expected_main = expected['main_pattern']
        main_correct = actual_main == expected_main
        
        if main_correct:
            correct_main += 1
            
        print(f"🏗️ Main Clause:")
        print(f"   Expected: {expected_main.value}")
        print(f"   Detected: {actual_main.value if actual_main else 'None'}")
        print(f"   Status: {'✅' if main_correct else '❌'}")
        
        # Check subordinate clauses
        actual_subordinate = [clause.grammatical_pattern for clause in result.subordinate_clauses 
                             if clause.grammatical_pattern]
        expected_subordinate = expected['subordinate_patterns']
        
        print(f"\n📋 Subordinate Clauses:")
        print(f"   Expected: {[p.value for p in expected_subordinate]}")
        print(f"   Detected: {[p.value for p in actual_subordinate]}")
        
        # Count matches
        subordinate_matches = len(set(expected_subordinate) & set(actual_subordinate))
        if subordinate_matches == len(expected_subordinate) and len(actual_subordinate) <= len(expected_subordinate) + 1:
            correct_subordinate += 1
        
        total_subordinate_expected += len(expected_subordinate)
        total_subordinate_detected += len(actual_subordinate)
        
        print(f"   Matches: {subordinate_matches}/{len(expected_subordinate)}")
        
        # Check embedded constructions
        actual_embedded = [clause.grammatical_pattern for clause in result.embedded_constructions 
                          if clause.grammatical_pattern]
        expected_embedded = expected['embedded_patterns']
        
        print(f"\n🔧 Embedded Constructions:")
        print(f"   Expected: {[p.value for p in expected_embedded]}")
        print(f"   Detected: {[p.value for p in actual_embedded]}")
        
        # Overall assessment
        print(f"\n📊 Assessment:")
        print(f"   Complexity: {result.overall_complexity:.3f}")
        print(f"   Engines: {result.recommended_engines}")
        print(f"   Strategy: {result.coordination_strategy}")
        
        total_tests += 1
    
    # Summary statistics
    print(f"\n📈 Test Summary")
    print("=" * 60)
    print(f"Main clause accuracy: {correct_main}/{total_tests} ({correct_main/total_tests*100:.1f}%)")
    print(f"Subordinate clause accuracy: {correct_subordinate}/{total_tests} ({correct_subordinate/total_tests*100:.1f}%)")
    print(f"Total subordinate patterns expected: {total_subordinate_expected}")
    print(f"Total subordinate patterns detected: {total_subordinate_detected}")
    
    overall_accuracy = (correct_main + correct_subordinate) / (total_tests * 2) * 100
    print(f"Overall hierarchical accuracy: {overall_accuracy:.1f}%")
    
    if overall_accuracy >= 75:
        print("🎯 Status: GOOD - Hierarchical detection working well")
    elif overall_accuracy >= 50:
        print("⚠️ Status: FAIR - Needs some improvements")
    else:
        print("❌ Status: POOR - Significant improvements needed")

def analyze_improvement_opportunities():
    """Analyze specific areas where the hierarchical system can be improved."""
    
    print(f"\n🔍 Improvement Analysis")
    print("=" * 60)
    
    print("💡 Identified Improvement Opportunities:")
    
    print("\n1. 🎯 Pattern Recognition Refinement:")
    print("   - Gerund vs. Participle distinction in adverbial clauses")
    print("   - Imperative detection in complex sentences")
    print("   - SVC vs. SV distinction in main clauses")
    
    print("\n2. 📊 Clause Boundary Detection:")
    print("   - Better separation of embedded infinitive constructions")
    print("   - More precise clause type classification")
    print("   - Handling of coordinate vs. subordinate clauses")
    
    print("\n3. 🤖 Engine Recommendation Enhancement:")
    print("   - Specialized engines for each detected pattern")
    print("   - Priority ordering based on clause hierarchy")
    print("   - Coordination strategy optimization")
    
    print("\n4. 🎮 Integration with Existing System:")
    print("   - Replace single-pattern detector with hierarchical version")
    print("   - Update Grammar Master Controller to use hierarchical results")
    print("   - Maintain backward compatibility with current engines")

if __name__ == "__main__":
    comprehensive_hierarchical_test()
    analyze_improvement_opportunities()
