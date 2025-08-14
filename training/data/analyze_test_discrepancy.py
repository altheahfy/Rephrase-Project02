"""
Comprehensive Test の評価ロジック問題を調査
なぜ 75% と表示されているかを分析
"""

def analyze_test_discrepancy():
    """テスト評価の矛盾を調査"""
    
    print("🔍 Test Evaluation Discrepancy Analysis")
    print("=" * 50)
    
    # Test Case 1 分析
    print("\n📝 Test Case 1 Analysis:")
    print("Sentence: 'Being a teacher, she knows how to explain difficult concepts.'")
    print("Comprehensive Test Result:")
    print("   Expected: ['gerund_pattern']")
    print("   Detected: ['participle_pattern', 'infinitive_pattern']")  
    print("   Matches: 0/1")
    print()
    print("Actual Analysis Result:")
    print("   Expected (correct): ['participle_pattern']")  
    print("   Detected: ['participle_pattern', 'infinitive_pattern']")
    print("   Matches: 1/1 (participle_pattern matches)")
    print("   Additional: infinitive_pattern is also correct (embedded construction)")
    
    print("\n🎯 Key Issues:")
    print("1. Test expectation values are incorrect:")
    print("   - 'Being a teacher' is PARTICIPLE, not GERUND")
    print("   - 'how to explain' should be recognized as embedded infinitive")
    
    print("\n2. Test counting logic may not handle multiple subordinate patterns correctly")
    
    print("\n3. Test case classification:")
    print("   - Some patterns are misclassified in expected values")
    print("   - System detects correctly but test framework counts as wrong")
    
    print("\n📊 Recommended Action:")
    print("1. Update test case expected values to match linguistic reality")
    print("2. Create more comprehensive subordinate clause test cases")  
    print("3. Add tests for edge cases that push accuracy toward 95%+")

if __name__ == "__main__":
    analyze_test_discrepancy()
