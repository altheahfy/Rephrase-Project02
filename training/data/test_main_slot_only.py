"""
上位スロットのみ（入れ子なし）での精度テスト
基本5文型と基本パターンでの性能確認
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
import time

def test_main_slot_only():
    """上位スロット（主節）のみでの精度テスト"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # 入れ子構造なし - 純粋な主節のみの文
    main_slot_only_tests = [
        # 基本5文型
        {
            "sentence": "Birds fly.",
            "expected_pattern": "sv_pattern",
            "category": "SV Pattern (第1文型)",
            "complexity": "最シンプル"
        },
        {
            "sentence": "She reads books.",
            "expected_pattern": "svo_pattern", 
            "category": "SVO Pattern (第3文型)",
            "complexity": "基本"
        },
        {
            "sentence": "He is a teacher.",
            "expected_pattern": "svc_pattern",
            "category": "SVC Pattern (第2文型)",
            "complexity": "基本"
        },
        {
            "sentence": "She gave him a present.",
            "expected_pattern": "svoo_pattern",
            "category": "SVOO Pattern (第4文型)", 
            "complexity": "やや複雑"
        },
        {
            "sentence": "They made him happy.",
            "expected_pattern": "svoc_pattern",
            "category": "SVOC Pattern (第5文型)",
            "complexity": "やや複雑"
        },
        
        # 受動態パターン
        {
            "sentence": "The book was written by him.",
            "expected_pattern": "passive_pattern",
            "category": "Passive Pattern",
            "complexity": "基本"
        },
        {
            "sentence": "The house is being built.",
            "expected_pattern": "passive_pattern",
            "category": "Progressive Passive",
            "complexity": "やや複雑"
        },
        
        # 命令文パターン
        {
            "sentence": "Please sit down.",
            "expected_pattern": "imperative_pattern",
            "category": "Imperative Pattern",
            "complexity": "基本"
        },
        {
            "sentence": "Open the window.",
            "expected_pattern": "imperative_pattern", 
            "category": "Direct Imperative",
            "complexity": "基本"
        },
        
        # There構文
        {
            "sentence": "There are many students here.",
            "expected_pattern": "existential_there",
            "category": "Existential There",
            "complexity": "基本"
        },
        {
            "sentence": "There was a meeting yesterday.",
            "expected_pattern": "existential_there",
            "category": "Past Existential",
            "complexity": "基本"
        },
        
        # 比較構文
        {
            "sentence": "She is taller than him.",
            "expected_pattern": "comparative_pattern",
            "category": "Comparative Pattern",
            "complexity": "やや複雑"
        }
    ]
    
    print("🧪 Main Slot Only (No Nesting) Accuracy Test")
    print("=" * 60)
    print("対象: 入れ子構造なし - 純粋な主節のみ")
    print("期待: 高精度 (90%+) での検出")
    print()
    
    total_tests = len(main_slot_only_tests)
    perfect_matches = 0
    total_processing_time = 0
    
    results_by_category = {}
    
    for i, test_case in enumerate(main_slot_only_tests, 1):
        print(f"📝 Test {i}/{total_tests}: {test_case['category']}")
        print(f"Complexity: {test_case['complexity']}")
        print(f"Sentence: '{test_case['sentence']}'")
        
        # 解析実行
        start_time = time.time()
        result = detector.detect_hierarchical_grammar(test_case['sentence'])
        analysis_time = time.time() - start_time
        total_processing_time += analysis_time
        
        # 結果確認
        detected_main = result.main_clause.grammatical_pattern.value
        expected = test_case['expected_pattern']
        
        print(f"Expected: {expected}")
        print(f"Detected: {detected_main}")
        print(f"Confidence: {result.main_clause.confidence:.2f}")
        print(f"Processing: {analysis_time:.3f}s")
        
        # 従属節の有無確認
        subordinate_count = len(result.subordinate_clauses)
        if subordinate_count > 0:
            print(f"⚠️  Unexpected subordinates detected: {subordinate_count}")
            for j, sub in enumerate(result.subordinate_clauses, 1):
                print(f"   Sub {j}: {sub.grammatical_pattern.value} (conf: {sub.confidence:.2f})")
        else:
            print("✅ No subordinate clauses (expected for main-only)")
        
        # 評価
        is_perfect = detected_main == expected and subordinate_count == 0
        
        if is_perfect:
            print("🎯 PERFECT MATCH")
            perfect_matches += 1
            result_status = "Perfect"
        elif detected_main == expected:
            print("✅ CORRECT PATTERN (but unexpected subordinates)")  
            result_status = "Pattern Correct"
        else:
            print("❌ PATTERN MISMATCH")
            result_status = "Pattern Wrong"
        
        # カテゴリ別集計
        category = test_case['category']
        if category not in results_by_category:
            results_by_category[category] = {'total': 0, 'perfect': 0, 'pattern_correct': 0}
        
        results_by_category[category]['total'] += 1
        if is_perfect:
            results_by_category[category]['perfect'] += 1
        elif detected_main == expected:
            results_by_category[category]['pattern_correct'] += 1
        
        print()
        print("-" * 60)
        print()
    
    # 総合結果
    perfect_accuracy = perfect_matches / total_tests * 100
    avg_processing_time = total_processing_time / total_tests
    
    print("🏆 MAIN SLOT ONLY - OVERALL RESULTS")
    print("=" * 60)
    print(f"Perfect Matches: {perfect_matches}/{total_tests} = {perfect_accuracy:.1f}%")
    print(f"Average Processing Time: {avg_processing_time:.3f}s")
    print()
    
    # カテゴリ別結果
    print("📊 Results by Category:")
    for category, stats in results_by_category.items():
        perfect_rate = stats['perfect'] / stats['total'] * 100 if stats['total'] > 0 else 0
        pattern_rate = (stats['perfect'] + stats['pattern_correct']) / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  {category}: Perfect {perfect_rate:.1f}% | Pattern {pattern_rate:.1f}%")
    
    print()
    
    # 評価とインサイト
    if perfect_accuracy >= 90:
        print("🎉 EXCELLENT - Main slot detection is very reliable!")
        insight = "主節パターン検出は非常に高精度"
        recommendation = "複雑さの原因は入れ子構造にあることが確認された"
    elif perfect_accuracy >= 80:
        print("✅ VERY GOOD - Main slot detection works well")
        insight = "主節パターン検出は良好"
        recommendation = "一部のパターンで調整が必要"
    elif perfect_accuracy >= 70:
        print("🔶 GOOD - Main slot detection has some issues")
        insight = "主節パターン検出に改善の余地"
        recommendation = "基本パターンの調整が必要"
    else:
        print("❌ NEEDS IMPROVEMENT - Basic pattern detection issues")
        insight = "基本的なパターン検出に問題"
        recommendation = "根本的な改善が必要"
    
    print(f"💡 Insight: {insight}")
    print(f"📋 Recommendation: {recommendation}")
    
    # 入れ子構造との比較
    print()
    print("🔄 Complexity Impact Analysis:")
    print(f"Main-only accuracy: {perfect_accuracy:.1f}%")
    print(f"With nesting accuracy: 66.7% (previous test)")
    complexity_impact = perfect_accuracy - 66.7
    print(f"Nesting complexity impact: {complexity_impact:+.1f} percentage points")
    
    if complexity_impact > 20:
        print("📈 Major finding: Nesting significantly reduces accuracy")
    elif complexity_impact > 10:
        print("📊 Finding: Nesting moderately reduces accuracy")
    else:
        print("📉 Finding: Accuracy issues are not primarily due to nesting")
    
    return perfect_accuracy >= 85, perfect_accuracy

if __name__ == "__main__":
    success, accuracy = test_main_slot_only()
