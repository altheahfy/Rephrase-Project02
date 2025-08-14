"""
Comprehensive Test for Hierarchical Grammar Detector v3.0
=========================================================

Compare v3.0 results against expected patterns to validate improvements.
"""

from hierarchical_grammar_detector_v3 import HierarchicalGrammarDetectorV3, GrammarPattern

def test_hierarchical_v3_comprehensive():
    """Comprehensive test of v3.0 hierarchical detection system."""
    
    detector = HierarchicalGrammarDetectorV3()
    
    # Test cases with expected patterns
    test_cases = [
        {
            'sentence': "Being a teacher, she knows how to explain difficult concepts.",
            'expected_main': GrammarPattern.SVO_PATTERN,  # she knows concepts
            'expected_subordinate': [GrammarPattern.GERUND_PATTERN],  # Being a teacher
            'expected_embedded': [GrammarPattern.INFINITIVE_PATTERN]  # to explain
        },
        {
            'sentence': "The book that was written by John is very good.",
            'expected_main': GrammarPattern.SVC_PATTERN,  # book is good
            'expected_subordinate': [GrammarPattern.PASSIVE_PATTERN],  # was written
            'expected_embedded': []
        },
        {
            'sentence': "Please tell me if there are any problems.",
            'expected_main': GrammarPattern.IMPERATIVE_PATTERN,  # Please tell
            'expected_subordinate': [GrammarPattern.EXISTENTIAL_THERE],  # there are
            'expected_embedded': []
        },
        {
            'sentence': "Having finished the work, she went home.",
            'expected_main': GrammarPattern.SV_PATTERN,  # she went
            'expected_subordinate': [GrammarPattern.PARTICIPLE_PATTERN],  # Having finished
            'expected_embedded': []
        },
        {
            'sentence': "The students were given homework by the teacher.",
            'expected_main': GrammarPattern.PASSIVE_PATTERN,  # were given
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "She made him happy.",
            'expected_main': GrammarPattern.SVOC_PATTERN,  # made him happy
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "There are many books on the table.",
            'expected_main': GrammarPattern.EXISTENTIAL_THERE,  # There are books
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "Go to school now.",
            'expected_main': GrammarPattern.IMPERATIVE_PATTERN,  # Go
            'expected_subordinate': [],
            'expected_embedded': []
        }
    ]
    
    print("🧪 Comprehensive Hierarchical Grammar Test v3.0")
    print("=" * 60)
    
    main_correct = 0
    subordinate_correct = 0
    total_subordinate_expected = 0
    total_subordinate_detected = 0
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_main = test_case['expected_main']
        expected_subordinate = test_case['expected_subordinate']
        expected_embedded = test_case['expected_embedded']
        
        print(f"\n📝 Test Case {i}: \"{sentence}\"")
        print("=" * 50)
        
        result = detector.detect_hierarchical_grammar(sentence)
        
        # Check main clause
        detected_main = result.main_clause.grammatical_pattern if result.main_clause else None
        main_status = "✅" if detected_main == expected_main else "❌"
        if detected_main == expected_main:
            main_correct += 1
        
        print(f"🏗️ Main Clause:")
        print(f"   Expected: {expected_main}")
        print(f"   Detected: {detected_main}")
        print(f"   Status: {main_status}")
        print(f"   Confidence: {result.main_clause.confidence:.3f}" if result.main_clause else "N/A")
        
        # Check subordinate clauses
        detected_subordinate = [clause.grammatical_pattern for clause in result.subordinate_clauses]
        subordinate_matches = 0
        
        print(f"\n📋 Subordinate Clauses:")
        print(f"   Expected: {expected_subordinate}")
        print(f"   Detected: {detected_subordinate}")
        
        for expected in expected_subordinate:
            if expected in detected_subordinate:
                subordinate_matches += 1
        
        total_subordinate_expected += len(expected_subordinate)
        total_subordinate_detected += len(detected_subordinate)
        subordinate_correct += subordinate_matches
        
        print(f"   Matches: {subordinate_matches}/{len(expected_subordinate)}")
        
        # Check embedded constructions
        detected_embedded = [const.grammatical_pattern for const in result.embedded_constructions]
        
        print(f"\n🔧 Embedded Constructions:")
        print(f"   Expected: {expected_embedded}")
        print(f"   Detected: {detected_embedded}")
        
        # Overall assessment
        print(f"\n📊 Assessment:")
        print(f"   Complexity: {result.overall_complexity:.3f}")
        print(f"   Engines: {result.recommended_engines}")
        print(f"   Strategy: {result.coordination_strategy}")
        print(f"   Processing Time: {result.processing_time:.3f}s")
    
    # Calculate overall statistics
    main_accuracy = (main_correct / len(test_cases)) * 100
    subordinate_accuracy = (subordinate_correct / max(total_subordinate_expected, 1)) * 100
    
    print(f"\n📈 Test Summary v3.0")
    print("=" * 60)
    print(f"Main clause accuracy: {main_correct}/{len(test_cases)} ({main_accuracy:.1f}%)")
    print(f"Subordinate clause accuracy: {subordinate_correct}/{total_subordinate_expected} ({subordinate_accuracy:.1f}%)")
    print(f"Total subordinate patterns expected: {total_subordinate_expected}")
    print(f"Total subordinate patterns detected: {total_subordinate_detected}")
    
    overall_accuracy = (main_accuracy + subordinate_accuracy) / 2
    print(f"Overall hierarchical accuracy: {overall_accuracy:.1f}%")
    
    if overall_accuracy >= 80:
        print("✅ Status: EXCELLENT - Ready for production")
    elif overall_accuracy >= 60:
        print("✅ Status: GOOD - Minor improvements needed")
    elif overall_accuracy >= 40:
        print("⚠️ Status: ACCEPTABLE - Some improvements needed")
    else:
        print("❌ Status: POOR - Significant improvements needed")
    
    print(f"\n🔍 Improvement Analysis v3.0")
    print("=" * 60)
    
    if overall_accuracy < 90:
        print("💡 Identified Improvement Opportunities:")
        print("\n1. 🎯 Pattern Recognition Refinement:")
        print("   - Fine-tune contextual pattern scoring")
        print("   - Improve clause boundary detection")
        print("   - Enhance special construction recognition")
        
        print("\n2. 📊 Dependency Analysis Enhancement:")
        print("   - Better utilize Stanza's dependency structure")
        print("   - Improve clause type classification")
        print("   - Refine embedded construction detection")
        
        print("\n3. 🤖 Engine Coordination Optimization:")
        print("   - Optimize engine selection based on pattern hierarchy")
        print("   - Improve coordination strategy determination")
        print("   - Enhance multi-pattern processing")
    else:
        print("🎉 System performing excellently!")
        print("   - Pattern recognition is highly accurate")
        print("   - Hierarchical analysis working well")
        print("   - Ready for integration with Grammar Master Controller")

if __name__ == "__main__":
    test_hierarchical_v3_comprehensive()
