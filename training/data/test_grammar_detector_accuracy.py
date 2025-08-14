#!/usr/bin/env python3
"""
Advanced Grammar Detector Test Suite
===================================

Comprehensive testing for high-precision grammar pattern detection.
Tests specific problem cases and measures accuracy improvements.
"""

from advanced_grammar_detector import AdvancedGrammarDetector, GrammarPattern
import time

def test_specific_patterns():
    """Test specific grammar patterns that were problematic."""
    detector = AdvancedGrammarDetector(log_level="DEBUG")
    
    test_cases = [
        # Imperative sentences
        ("Close the door.", GrammarPattern.IMPERATIVE_PATTERN, "Command with object"),
        ("Please sit down.", GrammarPattern.IMPERATIVE_PATTERN, "Polite command"),
        ("Don't run in the hallway.", GrammarPattern.IMPERATIVE_PATTERN, "Negative command"),
        ("Let me help you.", GrammarPattern.IMPERATIVE_PATTERN, "Let-command"),
        
        # Passive sentences
        ("The book was written by John.", GrammarPattern.PASSIVE_PATTERN, "Classic passive with agent"),
        ("The door was closed.", GrammarPattern.PASSIVE_PATTERN, "Passive without agent"),
        ("Mistakes were made.", GrammarPattern.PASSIVE_PATTERN, "Impersonal passive"),
        
        # SVC (Linking verb) sentences
        ("She seems happy today.", GrammarPattern.SVC_PATTERN, "Seem + adjective"),
        ("He is a teacher.", GrammarPattern.SVC_PATTERN, "Be + noun"),
        ("The food tastes good.", GrammarPattern.SVC_PATTERN, "Taste + adjective"),
        ("It looks beautiful.", GrammarPattern.SVC_PATTERN, "Look + adjective"),
        
        # Existential there
        ("There are many students here.", GrammarPattern.EXISTENTIAL_THERE, "There + be + NP"),
        ("There's a problem.", GrammarPattern.EXISTENTIAL_THERE, "There's contraction"),
        ("There were issues yesterday.", GrammarPattern.EXISTENTIAL_THERE, "There + past be"),
        
        # Basic patterns for comparison
        ("The cat sleeps.", GrammarPattern.SV_PATTERN, "Simple intransitive"),
        ("She reads books.", GrammarPattern.SVO_PATTERN, "Simple transitive"),
        ("I gave him money.", GrammarPattern.SVOO_PATTERN, "Ditransitive"),
        ("They made him captain.", GrammarPattern.SVOC_PATTERN, "Object complement"),
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    print("🔍 Testing Specific Grammar Patterns")
    print("=" * 60)
    
    for sentence, expected_pattern, description in test_cases:
        result = detector.detect_grammar_pattern(sentence)
        
        is_correct = result.primary_pattern == expected_pattern
        status = "✅ CORRECT" if is_correct else "❌ WRONG"
        
        if is_correct:
            correct_predictions += 1
        
        print(f"\nSentence: \"{sentence}\"")
        print(f"Description: {description}")
        print(f"Expected: {expected_pattern.value}")
        print(f"Detected: {result.primary_pattern.value}")
        print(f"Confidence: {result.confidence:.3f}")
        print(f"Status: {status}")
        
        if not is_correct:
            print(f"Secondary patterns: {[p.value for p in result.secondary_patterns]}")
            print(f"Expected in secondary? {expected_pattern in result.secondary_patterns}")
    
    accuracy = (correct_predictions / total_tests) * 100
    print(f"\n📊 Test Results Summary")
    print(f"=" * 60)
    print(f"Correct predictions: {correct_predictions}/{total_tests}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Target accuracy: 95%+")
    print(f"Performance: {'🎯 TARGET MET' if accuracy >= 95 else '⚠️ NEEDS IMPROVEMENT'}")
    
    # Performance stats
    stats = detector.get_performance_stats()
    print(f"\nAverage processing time: {stats['average_processing_time']:.3f}s")
    
    return accuracy >= 95

def debug_dependency_analysis():
    """Debug dependency analysis for problematic sentences."""
    detector = AdvancedGrammarDetector()
    
    problem_sentences = [
        "Close the door.",
        "The book was written by John.",
        "She seems happy today."
    ]
    
    print("\n🔧 Debugging Dependency Analysis")
    print("=" * 60)
    
    for sentence in problem_sentences:
        print(f"\n--- Analyzing: {sentence} ---")
        
        # Get detailed analysis
        stanza_analysis = detector._analyze_with_stanza(sentence)
        spacy_analysis = detector._analyze_with_spacy(sentence)
        
        print("Stanza Dependencies:")
        for dep in stanza_analysis.get('dependencies', []):
            print(f"  {dep.dependent} --{dep.relation}--> {dep.head}")
        
        print("Stanza POS Tags:")
        for word, pos in stanza_analysis.get('pos_tags', []):
            print(f"  {word}: {pos}")
        
        print("spaCy Dependencies:")
        for word, dep in spacy_analysis.get('dep_labels', []):
            print(f"  {word}: {dep}")
        
        # Get pattern scores
        pattern_scores = detector._calculate_pattern_scores(sentence, stanza_analysis, spacy_analysis)
        print("Pattern Scores:")
        sorted_scores = sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True)
        for pattern, score in sorted_scores[:5]:  # Top 5
            if score > 0:
                print(f"  {pattern.value}: {score:.3f}")

if __name__ == "__main__":
    # Run specific pattern tests
    success = test_specific_patterns()
    
    # Run debugging analysis
    debug_dependency_analysis()
    
    print(f"\n🎯 Overall Result: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
