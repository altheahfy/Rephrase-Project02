"""
改善されたHierarchicalGrammarDetectorV4をテスト
特に gerund_pattern と noun_clause の検出精度確認
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def test_improved_detection():
    """改善された検出機能をテスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    test_cases = [
        {
            "sentence": "Being a teacher, she knows how to explain difficult concepts.",
            "expected": ["participle_pattern", "infinitive_pattern"],
            "focus": "Participle pattern (should remain correct)"
        },
        {
            "sentence": "Having finished his work, he went home.",
            "expected": ["participle_pattern"],
            "focus": "Participle pattern (should remain correct)"
        },
        {
            "sentence": "She made him happy by encouraging him constantly.",
            "expected": ["gerund_pattern"],
            "focus": "🎯 GERUND PATTERN - Key improvement target"
        },
        {
            "sentence": "Please tell me what you think about this idea.",
            "expected": ["noun_clause"],
            "focus": "🎯 NOUN CLAUSE - Key improvement target"
        }
    ]
    
    print("🧪 Testing Improved HierarchicalGrammarDetectorV4")
    print("=" * 60)
    
    total_expected = 0
    total_correct = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {case['focus']}")
        print(f"Sentence: {case['sentence']}")
        print(f"Expected: {case['expected']}")
        
        result = detector.detect_hierarchical_grammar(case['sentence'])
        detected = [clause.grammatical_pattern.value for clause in result.subordinate_clauses]
        
        print(f"Detected: {detected}")
        
        # Detailed analysis
        print(f"Main clause: {result.main_clause.grammatical_pattern.value} (conf: {result.main_clause.confidence:.2f})")
        for j, clause in enumerate(result.subordinate_clauses):
            print(f"  Sub {j+1}: {clause.grammatical_pattern.value} (conf: {clause.confidence:.2f}) - '{clause.text[:50]}...'")
        
        # Calculate matches
        matches = len(set(detected) & set(case['expected']))
        expected_count = len(case['expected'])
        
        accuracy = matches / expected_count * 100 if expected_count > 0 else 0
        print(f"Matches: {matches}/{expected_count} = {accuracy:.1f}%")
        
        if accuracy >= 90:
            print("✅ TARGET ACHIEVED!")
        elif accuracy >= 50:
            print("🔶 PARTIAL SUCCESS")
        else:
            print("❌ NEEDS IMPROVEMENT")
        
        total_expected += expected_count
        total_correct += matches
    
    print("\n" + "=" * 60)
    print(f"🎯 OVERALL RESULTS:")
    final_accuracy = total_correct / total_expected * 100 if total_expected > 0 else 0
    print(f"Total Accuracy: {total_correct}/{total_expected} = {final_accuracy:.1f}%")
    
    if final_accuracy >= 90:
        print("\n🎉 🎯 90%+ TARGET ACHIEVED! 🎯 🎉")
        print("System ready for Grammar Master Controller v2 integration!")
    elif final_accuracy >= 75:
        print(f"\n🔶 Close to target - Gap: {90 - final_accuracy:.1f}%")
    else:
        print(f"\n❌ Still needs improvement - Gap: {90 - final_accuracy:.1f}%")
    
    return final_accuracy >= 90

if __name__ == "__main__":
    success = test_improved_detection()
