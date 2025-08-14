"""
従属節精度の詳細分析
どの従属節パターンで精度が不足しているかを特定
"""

from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def analyze_subordinate_accuracy():
    """従属節精度の詳細分析"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # テストケースから従属節を持つものを抽出
    subordinate_test_cases = [
        {
            'sentence': "Being a teacher, she knows how to explain difficult concepts.",
            'expected_subordinate': ['gerund_pattern'],  # テストケース期待値
            'actual_expected': ['participle_pattern'],   # 実際に正しい期待値
            'expected_embedded': ['infinitive_pattern']
        },
        {
            'sentence': "The book that was written by John is very good.",
            'expected_subordinate': ['passive_pattern'],
            'actual_expected': ['passive_pattern'],
            'expected_embedded': []
        },
        {
            'sentence': "Please tell me if there are any problems.",
            'expected_subordinate': ['existential_there'],
            'actual_expected': ['existential_there'],
            'expected_embedded': []
        },
        {
            'sentence': "Having finished the work, she went home.",
            'expected_subordinate': ['participle_pattern'],
            'actual_expected': ['participle_pattern'],
            'expected_embedded': []
        }
    ]
    
    print("🔍 Detailed Subordinate Clause Accuracy Analysis")
    print("=" * 60)
    
    total_expected = 0
    total_detected = 0
    correct_matches = 0
    
    for i, case in enumerate(subordinate_test_cases, 1):
        sentence = case['sentence']
        expected = case['actual_expected']  # Use actual correct expectation
        
        print(f"\n📝 Test Case {i}: \"{sentence[:50]}...\"")
        print("-" * 50)
        
        # 完全な検出結果を取得
        result = detector.detect_grammar_pattern(sentence)
        
        # 詳細な節分解を取得
        stanza_analysis = detector._analyze_with_stanza(sentence)
        clauses = detector._decompose_into_clauses_v4(stanza_analysis, sentence)
        
        # 従属節のみを抽出
        subordinate_clauses = [c for c in clauses if c.clause_type != 'main']
        detected_patterns = []
        
        print(f"🏗️ Subordinate Clauses Found: {len(subordinate_clauses)}")
        
        for j, clause in enumerate(subordinate_clauses, 1):
            pattern_result = detector._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
            detected_patterns.append(pattern_result['pattern'].name.lower())
            
            print(f"   {j}. Type: {clause.clause_type}")
            print(f"      Root: {clause.root_word} ({clause.root_pos})")
            print(f"      Text: \"{clause.text[:30]}...\"")
            print(f"      Pattern: {pattern_result['pattern']}")
            print(f"      Confidence: {pattern_result['confidence']:.3f}")
            
            # 期待値との比較 - 正確なパターン名比較
            detected_pattern_name = pattern_result['pattern'].name.lower()
            
            # パターン名の正規化 (PARTICIPLE_PATTERN -> participle)
            normalized_detected = detected_pattern_name.replace('_pattern', '')
            
            # 期待値も正規化
            normalized_expected = [p.replace('_pattern', '') for p in expected]
            
            print(f"      Detected Pattern: {detected_pattern_name}")
            print(f"      Normalized: {normalized_detected}")
            print(f"      Expected (normalized): {normalized_expected}")
            
            is_expected = normalized_detected in normalized_expected
            status = "✅" if is_expected else "❌"
            print(f"      Status: {status}")
            
            if is_expected:
                correct_matches += 1
        
        total_expected += len(expected)
        total_detected += len(detected_patterns)
        
        print(f"\n📊 Case Summary:")
        print(f"   Expected: {expected}")
        print(f"   Detected: {detected_patterns}")
        print(f"   Match Rate: {correct_matches}/{total_expected} so far")
    
    print(f"\n📈 Overall Subordinate Accuracy:")
    print(f"   Total Expected Patterns: {total_expected}")
    print(f"   Total Detected Patterns: {total_detected}")  
    print(f"   Correct Matches: {correct_matches}")
    print(f"   Accuracy: {(correct_matches/total_expected)*100:.1f}%")
    print(f"   Gap to 90%: {90 - (correct_matches/total_expected)*100:.1f}%")
    
    # 失敗パターンの分析
    print(f"\n🎯 Improvement Opportunities:")
    if correct_matches < total_expected:
        print("   1. Pattern classification rules need refinement")
        print("   2. Contextual analysis could be enhanced")
        print("   3. Dependency relationship interpretation may need adjustment")

if __name__ == "__main__":
    analyze_subordinate_accuracy()
