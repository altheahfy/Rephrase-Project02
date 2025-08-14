"""
Rephrase設計範囲に適した実際のテスト評価
二重入れ子構造までの例文での性能確認
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
import time

def test_proper_rephrase_complexity():
    """Rephrase設計範囲内での適切な複雑性テスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # Rephrase設計範囲に適した例文 (二重入れ子まで)
    proper_test_cases = [
        {
            "sentence": "Having finished the project, the student submitted it confidently.",
            "expected_patterns": ["participle_pattern", "svo_pattern"],
            "structure": "分詞構文 + 主節",
            "complexity": "基本的二重構造"
        },
        {
            "sentence": "While she was reading, she discovered what made the story compelling.",
            "expected_patterns": ["conjunction_pattern", "svo_pattern", "noun_clause", "svoc_pattern"],
            "structure": "時間節 + 主節 + 名詞節",
            "complexity": "並列二重構造"
        },
        {
            "sentence": "The book that he wrote became very popular.",
            "expected_patterns": ["relative_pattern", "svc_pattern"],
            "structure": "関係節 + 主節",
            "complexity": "基本的二重構造"
        },
        {
            "sentence": "She made him happy by encouraging him constantly.",
            "expected_patterns": ["svoc_pattern", "gerund_pattern"],
            "structure": "主節 + 動名詞句",
            "complexity": "基本的二重構造"
        },
        {
            "sentence": "Please tell me what you think about this idea.",
            "expected_patterns": ["imperative_pattern", "noun_clause"],
            "structure": "命令文 + 名詞節",
            "complexity": "基本的二重構造"
        },
        {
            "sentence": "Being tired, he decided to rest for a while.",
            "expected_patterns": ["participle_pattern", "svo_pattern", "infinitive_pattern"],
            "structure": "分詞構文 + 主節 + 不定詞",
            "complexity": "連続二重構造"
        }
    ]
    
    print("🧪 Proper Rephrase Complexity Test")
    print("=" * 60)
    print("対象: Rephrase設計範囲内 (二重入れ子まで)")
    print("目標: 実用的な文での80%+精度達成")
    print()
    
    total_tests = len(proper_test_cases)
    successful_tests = 0
    total_patterns = 0
    total_detected = 0
    
    for i, test_case in enumerate(proper_test_cases, 1):
        print(f"📝 Test {i}/{total_tests}: {test_case['complexity']}")
        print(f"Structure: {test_case['structure']}")
        print(f"Sentence: {test_case['sentence']}")
        
        # 解析実行
        start_time = time.time()
        result = detector.detect_hierarchical_grammar(test_case['sentence'])
        analysis_time = time.time() - start_time
        
        # 検出されたパターンの収集
        detected_patterns = [result.main_clause.grammatical_pattern.value]
        detected_patterns.extend([clause.grammatical_pattern.value for clause in result.subordinate_clauses])
        
        # 評価
        expected = set(test_case['expected_patterns'])
        detected = set(detected_patterns)
        
        matches = len(expected & detected)
        expected_count = len(expected)
        accuracy = matches / expected_count * 100 if expected_count > 0 else 0
        
        print(f"Expected: {sorted(list(expected))}")
        print(f"Detected: {sorted(detected_patterns)}")
        print(f"Accuracy: {matches}/{expected_count} = {accuracy:.1f}%")
        print(f"Time: {analysis_time:.3f}s")
        
        # 詳細結果
        if accuracy >= 80:
            print("✅ EXCELLENT")
            successful_tests += 1
        elif accuracy >= 60:
            print("🔶 GOOD")
        elif accuracy >= 40:
            print("🔷 MODERATE")
        else:
            print("❌ NEEDS IMPROVEMENT")
        
        total_patterns += expected_count
        total_detected += matches
        
        print()
        print("-" * 60)
        print()
    
    # 総合評価
    overall_accuracy = total_detected / total_patterns * 100 if total_patterns > 0 else 0
    success_rate = successful_tests / total_tests * 100
    
    print("🏆 OVERALL REPHRASE-COMPATIBLE TEST RESULTS")
    print("=" * 60)
    print(f"Pattern Detection Accuracy: {total_detected}/{total_patterns} = {overall_accuracy:.1f}%")
    print(f"Excellent Test Success Rate: {successful_tests}/{total_tests} = {success_rate:.1f}%")
    print()
    
    if overall_accuracy >= 80:
        print("🎉 EXCELLENT - Ready for Rephrase integration!")
        status = "Production Ready"
    elif overall_accuracy >= 70:
        print("✅ GOOD - Minor improvements recommended")
        status = "Near Production Ready"
    elif overall_accuracy >= 60:
        print("🔶 MODERATE - Some improvements needed")
        status = "Needs Improvement"
    else:
        print("❌ SIGNIFICANT IMPROVEMENT NEEDED")
        status = "Major Improvement Required"
    
    print(f"System Status: {status}")
    print()
    
    # 改善提案
    if overall_accuracy < 80:
        print("💡 Specific Improvement Areas:")
        
        # パターン別の成功率分析
        pattern_performance = {}
        for test_case in proper_test_cases:
            for pattern in test_case['expected_patterns']:
                if pattern not in pattern_performance:
                    pattern_performance[pattern] = {'total': 0, 'detected': 0}
                pattern_performance[pattern]['total'] += 1
        
        # 改善が必要なパターンを特定
        weak_patterns = []
        for pattern, stats in pattern_performance.items():
            if stats['total'] > 0:
                success_rate_pattern = stats['detected'] / stats['total'] * 100
                if success_rate_pattern < 70:
                    weak_patterns.append(pattern)
        
        if weak_patterns:
            print(f"Focus on: {', '.join(weak_patterns)}")
        
        print("Recommended: Fine-tune pattern detection rules")
    
    return overall_accuracy >= 70, overall_accuracy

if __name__ == "__main__":
    success, accuracy = test_proper_rephrase_complexity()
