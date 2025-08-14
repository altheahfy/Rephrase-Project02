"""
実際のHierarchicalGrammarDetectorV4の実行結果を取得して
テストケースとの矛盾を詳細分析
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def verify_actual_performance():
    """実際の検出結果とテスト期待値を比較"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # テストケースの実際の検出結果を確認
    test_cases = [
        {
            "sentence": "Being a teacher, she knows how to explain difficult concepts.",
            "test_expected": ["gerund_pattern"],  # テストの期待値
            "reality_expected": ["participle_pattern"]  # 言語学的に正しい期待値
        },
        {
            "sentence": "Having finished his work, he went home.",
            "test_expected": ["gerund_pattern"],
            "reality_expected": ["participle_pattern"]
        },
        {
            "sentence": "She made him happy by encouraging him constantly.",
            "test_expected": ["causative_pattern", "gerund_pattern"],
            "reality_expected": ["causative_pattern", "gerund_pattern"]
        },
        {
            "sentence": "Please tell me what you think about this idea.",
            "test_expected": ["imperative_pattern", "relative_clause"],
            "reality_expected": ["imperative_pattern", "noun_clause"]
        }
    ]
    
    print("🔍 Actual Detection vs Test Expectations")
    print("=" * 60)
    
    total_test_matches = 0
    total_reality_matches = 0
    total_patterns = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Sentence: {case['sentence']}")
        
        result = detector.detect_hierarchical_grammar(case['sentence'])
        
        print(f"Debug - Result structure: {type(result)}")
        print(f"Debug - Subordinate clauses: {len(result.subordinate_clauses)}")
        
        # subordinate_clauses の構造を確認
        detected = []
        for clause in result.subordinate_clauses:
            print(f"Debug - Clause: {clause.grammatical_pattern} (confidence: {clause.confidence})")
            detected.append(clause.grammatical_pattern.value)
        
        print(f"Detected: {detected}")
        print(f"Test Expected: {case['test_expected']}")
        print(f"Reality Expected: {case['reality_expected']}")
        
        # テスト方式での評価
        test_matches = len(set(detected) & set(case['test_expected']))
        test_total = len(case['test_expected'])
        
        # 現実に合わせた評価
        reality_matches = len(set(detected) & set(case['reality_expected']))
        reality_total = len(case['reality_expected'])
        
        print(f"Test Matches: {test_matches}/{test_total} = {test_matches/test_total*100:.1f}%")
        print(f"Reality Matches: {reality_matches}/{reality_total} = {reality_matches/reality_total*100:.1f}%")
        
        total_test_matches += test_matches
        total_reality_matches += reality_matches
        total_patterns += reality_total  # 現実の期待値基準
        
        if test_matches != reality_matches:
            print("⚠️  TEST EXPECTATION ERROR DETECTED!")
    
    print("\n" + "=" * 60)
    print(f"🎯 FINAL COMPARISON:")
    print(f"Test Framework Accuracy: {total_test_matches}/{total_patterns} = {total_test_matches/total_patterns*100:.1f}%")
    print(f"Actual System Accuracy: {total_reality_matches}/{total_patterns} = {total_reality_matches/total_patterns*100:.1f}%")
    
    if total_reality_matches/total_patterns >= 0.9:
        print("\n✅ 90%+ TARGET ACHIEVED!")
    else:
        print(f"\n❌ Gap to 90%: {90 - total_reality_matches/total_patterns*100:.1f}%")

if __name__ == "__main__":
    verify_actual_performance()
