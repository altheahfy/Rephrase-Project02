"""
Comprehensive Test for Hierarchical Grammar Detector v4.0
=========================================================
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4, GrammarPattern

def test_hierarchical_v4_comprehensive():
    """Comprehensive test of v4.0 ultra-precise hierarchical detection system."""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # Extended test cases for thorough evaluation
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
        },
        # Additional test cases for better coverage
        {
            'sentence': "She is a teacher.",
            'expected_main': GrammarPattern.SVC_PATTERN,  # She is teacher
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "I gave him a book.",
            'expected_main': GrammarPattern.SVOO_PATTERN,  # I gave him book
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "They are playing football.",
            'expected_main': GrammarPattern.SVO_PATTERN,  # They are playing football
            'expected_subordinate': [],
            'expected_embedded': []
        },
        {
            'sentence': "The cat sleeps.",
            'expected_main': GrammarPattern.SV_PATTERN,  # cat sleeps
            'expected_subordinate': [],
            'expected_embedded': []
        }
    ]
    
    print("🧪 Comprehensive Hierarchical Grammar Test v4.0")
    print("=" * 65)
    
    main_correct = 0
    subordinate_correct = 0
    total_subordinate_expected = 0
    total_subordinate_detected = 0
    processing_times = []
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_main = test_case['expected_main']
        expected_subordinate = test_case['expected_subordinate']
        expected_embedded = test_case['expected_embedded']
        
        print(f"\n📝 Test Case {i}: \"{sentence}\"")
        print("=" * 55)
        
        result = detector.detect_hierarchical_grammar(sentence)
        processing_times.append(result.processing_time)
        
        # Check main clause
        detected_main = result.main_clause.grammatical_pattern if result.main_clause else None
        main_status = "✅" if detected_main == expected_main else "❌"
        if detected_main == expected_main:
            main_correct += 1
        
        print(f"🏗️ Main Clause:")
        print(f"   Expected: {expected_main.value if expected_main else 'None'}")
        print(f"   Detected: {detected_main.value if detected_main else 'None'}")
        print(f"   Status: {main_status}")
        if result.main_clause:
            print(f"   Confidence: {result.main_clause.confidence:.3f}")
            print(f"   Features: {result.main_clause.linguistic_features}")
        
        # Check subordinate clauses
        detected_subordinate = [clause.grammatical_pattern for clause in result.subordinate_clauses]
        subordinate_matches = 0
        
        print(f"\n📋 Subordinate Clauses:")
        print(f"   Expected: {[p.value for p in expected_subordinate]}")
        print(f"   Detected: {[p.value for p in detected_subordinate]}")
        
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
        print(f"   Expected: {[p.value for p in expected_embedded]}")
        print(f"   Detected: {[p.value for p in detected_embedded]}")
        
        # Assessment
        print(f"\n📊 Assessment:")
        print(f"   Complexity: {result.overall_complexity:.3f}")
        print(f"   Engines: {result.recommended_engines}")
        print(f"   Strategy: {result.coordination_strategy}")
        print(f"   Processing Time: {result.processing_time:.3f}s")
    
    # Calculate overall statistics
    main_accuracy = (main_correct / len(test_cases)) * 100
    subordinate_accuracy = (subordinate_correct / max(total_subordinate_expected, 1)) * 100
    avg_processing_time = sum(processing_times) / len(processing_times)
    
    print(f"\n📈 Final Test Results v4.0")
    print("=" * 65)
    print(f"Main clause accuracy: {main_correct}/{len(test_cases)} ({main_accuracy:.1f}%)")
    print(f"Subordinate clause accuracy: {subordinate_correct}/{total_subordinate_expected} ({subordinate_accuracy:.1f}%)")
    print(f"Total subordinate patterns expected: {total_subordinate_expected}")
    print(f"Total subordinate patterns detected: {total_subordinate_detected}")
    print(f"Average processing time: {avg_processing_time:.3f}s")
    
    overall_accuracy = (main_accuracy + subordinate_accuracy) / 2
    print(f"Overall hierarchical accuracy: {overall_accuracy:.1f}%")
    
    # Performance assessment
    if overall_accuracy >= 85:
        status = "🎉 EXCELLENT - Production ready"
        color = "✅"
    elif overall_accuracy >= 70:
        status = "✅ GOOD - Minor improvements needed"
        color = "✅"
    elif overall_accuracy >= 50:
        status = "⚠️ ACCEPTABLE - Some improvements needed"
        color = "⚠️"
    else:
        status = "❌ POOR - Significant improvements needed"
        color = "❌"
    
    print(f"{color} Status: {status}")
    
    # Detailed analysis
    print(f"\n🔍 Performance Analysis v4.0")
    print("=" * 65)
    
    print("💡 Key Improvements from v3.0:")
    print(f"   - Main clause accuracy: Targeting {main_accuracy:.1f}%")
    print(f"   - Subordinate clause accuracy: {subordinate_accuracy:.1f}%")
    print(f"   - Processing efficiency: {avg_processing_time:.3f}s average")
    
    if overall_accuracy >= 80:
        print("\n🎯 System Ready for Integration:")
        print("   - High accuracy achieved")
        print("   - Reliable pattern recognition")
        print("   - Ready for Grammar Master Controller integration")
        print("   - Can replace existing single-pattern detection")
    else:
        print("\n🔧 Areas for Further Improvement:")
        if main_accuracy < 80:
            print("   - Main clause pattern recognition needs refinement")
            print("   - Improve structural analysis accuracy")
        if subordinate_accuracy < 80:
            print("   - Subordinate clause detection needs enhancement") 
            print("   - Better clause boundary identification required")
        
        print("\n📝 Next Steps:")
        print("   - Fine-tune pattern detection rules")
        print("   - Enhance dependency relationship analysis")
        print("   - Add more contextual pattern matching")

if __name__ == "__main__":
    test_hierarchical_v4_comprehensive()
