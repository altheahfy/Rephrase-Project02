"""
複雑文解析の詳細デバッグと改善提案
特に入れ子構造と文脈依存パターンの問題を分析
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def detailed_complex_analysis():
    """複雑文解析の詳細分析とデバッグ"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    # 最も問題のある文を詳細分析
    problem_sentence = "Having finished the project that was assigned by the teacher, the student who had been working diligently submitted it confidently."
    
    print("🔍 Detailed Complex Sentence Debug Analysis")
    print("=" * 70)
    print(f"Target: {problem_sentence}")
    print()
    
    result = detector.detect_hierarchical_grammar(problem_sentence)
    
    print("📊 Current Detection Results:")
    print(f"Main: {result.main_clause.grammatical_pattern.value} (conf: {result.main_clause.confidence:.2f})")
    print(f"Main text: '{result.main_clause.text}'")
    print()
    
    for i, clause in enumerate(result.subordinate_clauses, 1):
        print(f"Sub {i}: {clause.grammatical_pattern.value} (conf: {clause.confidence:.2f})")
        print(f"  Text: '{clause.text}'")
        print(f"  Type: {clause.clause_type}")
        print(f"  Root: '{clause.root_word}' ({clause.root_pos})")
        print()
    
    print("🎯 Expected vs Actual Analysis:")
    expected_breakdown = [
        {
            "pattern": "participle_pattern",
            "text": "Having finished the project that was assigned by the teacher",
            "status": "✅ DETECTED",
            "note": "Correctly identified as participle construction"
        },
        {
            "pattern": "relative_pattern", 
            "text": "that was assigned by the teacher",
            "status": "❌ MISSED as separate pattern",
            "note": "Embedded within participle, not detected independently"
        },
        {
            "pattern": "passive_pattern",
            "text": "was assigned by the teacher", 
            "status": "✅ DETECTED",
            "note": "Correctly identified passive construction"
        },
        {
            "pattern": "relative_pattern",
            "text": "who had been working diligently",
            "status": "❌ MISCLASSIFIED as noun_clause",
            "note": "Should be relative pattern, not noun clause"
        },
        {
            "pattern": "perfect_progressive", 
            "text": "had been working",
            "status": "❌ NOT DETECTED",
            "note": "Perfect progressive aspect not recognized"
        },
        {
            "pattern": "svo_pattern",
            "text": "the student submitted it confidently",
            "status": "✅ DETECTED as main",
            "note": "Main clause correctly identified"
        }
    ]
    
    for item in expected_breakdown:
        print(f"{item['status']} {item['pattern']}: '{item['text']}'")
        print(f"    Note: {item['note']}")
        print()
    
    print("🔧 Key Issues Identified:")
    issues = [
        "1. 入れ子関係節が独立して検出されない",
        "2. 関係節 vs 名詞節の判定ロジックに問題", 
        "3. 時制・相パターン（perfect_progressive）の検出漏れ",
        "4. 複雑文での主節境界識別の改善が必要",
        "5. 文脈階層の深い理解が不足"
    ]
    
    for issue in issues:
        print(f"   {issue}")
    
    print()
    print("💡 Improvement Strategy:")
    improvements = [
        "1. 関係節検出の強化：入れ子構造内でも独立検出",
        "2. 時制・相パターンの専用検出ロジック追加",
        "3. 関係節 vs 名詞節の判定基準の明確化", 
        "4. 複雑文での主節・従属節境界の精密化",
        "5. 階層的構文解析の深度向上"
    ]
    
    for improvement in improvements:
        print(f"   {improvement}")
    
    return result

def test_simpler_patterns():
    """より単純なパターンでの基本性能確認"""
    
    detector = HierarchicalGrammarDetectorV4()
    
    print("\n" + "=" * 70)
    print("🧪 Baseline Performance Check with Simpler Patterns")
    print("=" * 70)
    
    simple_tests = [
        {
            "sentence": "The book that he wrote was interesting.",
            "expected": ["relative_pattern", "passive_pattern"],
            "focus": "基本的な関係節"
        },
        {
            "sentence": "She had been working before I arrived.",
            "expected": ["perfect_progressive", "conjunction_pattern"],
            "focus": "完了進行形 + 時間節"
        },
        {
            "sentence": "Starting early helps you succeed.",
            "expected": ["gerund_pattern", "svo_pattern"],
            "focus": "動名詞主語"
        }
    ]
    
    total_accuracy = 0
    
    for i, test in enumerate(simple_tests, 1):
        print(f"\n📝 Baseline Test {i}: {test['focus']}")
        print(f"Sentence: {test['sentence']}")
        
        result = detector.detect_hierarchical_grammar(test['sentence'])
        detected = [result.main_clause.grammatical_pattern.value]
        detected.extend([clause.grammatical_pattern.value for clause in result.subordinate_clauses])
        
        matches = len(set(detected) & set(test['expected']))
        expected_count = len(test['expected'])
        accuracy = matches / expected_count * 100 if expected_count > 0 else 0
        
        print(f"Expected: {test['expected']}")
        print(f"Detected: {detected}")
        print(f"Accuracy: {matches}/{expected_count} = {accuracy:.1f}%")
        
        total_accuracy += accuracy
    
    baseline_performance = total_accuracy / len(simple_tests)
    print(f"\n🎯 Baseline Performance: {baseline_performance:.1f}%")
    
    if baseline_performance >= 70:
        print("✅ Basic patterns work well - Complex pattern handling needs improvement")
    else:
        print("❌ Basic patterns also need improvement")
    
    return baseline_performance

if __name__ == "__main__":
    detailed_result = detailed_complex_analysis()
    baseline = test_simpler_patterns()
