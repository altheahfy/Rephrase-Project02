"""
Staged Grammar Detector Comprehensive Test Suite
段階処理システムの包括的テストと性能評価
"""

import time
from typing import List, Dict, Tuple
from staged_grammar_detector_v1 import StagedGrammarDetector
from advanced_grammar_detector import GrammarPattern
import sys
sys.path.append('.')

class StagedGrammarTestSuite:
    """段階処理システムテストスイート"""
    
    def __init__(self):
        """初期化"""
        print("🧪 Initializing Staged Grammar Test Suite...")
        self.detector = StagedGrammarDetector()
        self.test_cases = self._prepare_comprehensive_test_cases()
        
    def _prepare_comprehensive_test_cases(self) -> List[Dict]:
        """包括的テストケースの準備"""
        
        test_cases = [
            # === Rephrase対応: 分詞構文 ===
            {
                'sentence': "Having finished the project, the student submitted it confidently.",
                'expected_main': GrammarPattern.SVO_PATTERN,  # student submitted it
                'expected_subordinate': [GrammarPattern.SV_PATTERN],  # Having finished the project
                'complexity': 'moderate',
                'description': 'Participle phrase (adverbial)',
                'subordinate_functions': ['adverbial_participle']
            },
            {
                'sentence': "Walking to school, she met her friend.",
                'expected_main': GrammarPattern.SVO_PATTERN,  # she met friend
                'expected_subordinate': [GrammarPattern.SV_PATTERN],  # Walking to school
                'complexity': 'moderate',
                'description': 'Present participle phrase',
                'subordinate_functions': ['adverbial_participle']
            },
            
            # === Rephrase対応: 関係詞節 ===
            {
                'sentence': "The book that she bought was expensive.",
                'expected_main': GrammarPattern.SVC_PATTERN,  # book was expensive  
                'expected_subordinate': [GrammarPattern.SVO_PATTERN],  # that she bought
                'complexity': 'moderate',
                'description': 'Restrictive relative clause',
                'subordinate_functions': ['adjectival_relative']
            },
            {
                'sentence': "Students who study hard succeed in life.",
                'expected_main': GrammarPattern.SV_PATTERN,  # Students succeed
                'expected_subordinate': [GrammarPattern.SV_PATTERN],  # who study hard
                'complexity': 'moderate', 
                'description': 'Subject relative clause',
                'subordinate_functions': ['adjectival_relative']
            },
            
            # === Rephrase対応: 名詞節 ===
            {
                'sentence': "I know what you did yesterday.",
                'expected_main': GrammarPattern.SVO_PATTERN,  # I know [what...]
                'expected_subordinate': [GrammarPattern.SVO_PATTERN],  # what you did
                'complexity': 'moderate',
                'description': 'Object wh-clause',
                'subordinate_functions': ['noun_clause_object']
            },
            {
                'sentence': "What he said was interesting.",
                'expected_main': GrammarPattern.SVC_PATTERN,  # [What...] was interesting
                'expected_subordinate': [GrammarPattern.SVO_PATTERN],  # What he said
                'complexity': 'moderate',
                'description': 'Subject wh-clause',
                'subordinate_functions': ['noun_clause_subject']
            },
            
            # === Rephrase対応: 時間節 ===
            {
                'sentence': "When the rain stopped, we went outside.",
                'expected_main': GrammarPattern.SV_PATTERN,  # we went outside
                'expected_subordinate': [GrammarPattern.SV_PATTERN],  # When rain stopped
                'complexity': 'moderate',
                'description': 'Temporal adverbial clause',
                'subordinate_functions': ['adverbial_temporal']
            },
            
            # === シンプルパターン（基準値） ===
            {
                'sentence': "The cat sat on the mat.",
                'expected_main': GrammarPattern.SV_PATTERN,
                'expected_subordinate': [],
                'complexity': 'simple',
                'description': 'Simple SV pattern',
                'subordinate_functions': []
            },
            {
                'sentence': "Students study English very hard.",
                'expected_main': GrammarPattern.SVO_PATTERN,
                'expected_subordinate': [],
                'complexity': 'simple',
                'description': 'Simple SVO pattern',
                'subordinate_functions': []
            },
            
            # === 境界条件テスト ===
            {
                'sentence': "The presentation, having been completed successfully, was submitted to the committee.",
                'expected_main': GrammarPattern.SV_PATTERN,  # presentation was submitted
                'expected_subordinate': [GrammarPattern.SV_PATTERN],  # having been completed
                'complexity': 'complex',
                'description': 'Passive participle phrase',
                'subordinate_functions': ['adverbial_participle']
            }
        ]
        
        return test_cases
    
    def run_comprehensive_tests(self) -> Dict:
        """包括的テスト実行"""
        
        print("\n🚀 Starting Comprehensive Staged Grammar Tests...")
        print("=" * 60)
        
        results = {
            'total_tests': len(self.test_cases),
            'passed_tests': 0,
            'failed_tests': 0,
            'accuracy_by_complexity': {'simple': {'total': 0, 'passed': 0},
                                     'moderate': {'total': 0, 'passed': 0},
                                     'complex': {'total': 0, 'passed': 0}},
            'total_processing_time': 0.0,
            'average_processing_time': 0.0,
            'detailed_results': []
        }
        
        total_start_time = time.time()
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n📝 Test {i}/{len(self.test_cases)}: {test_case['description']}")
            print(f"🔍 Sentence: {test_case['sentence']}")
            
            # 段階処理実行
            test_result = self.detector.detect_staged_grammar(test_case['sentence'])
            
            # 結果評価
            evaluation = self._evaluate_test_result(test_case, test_result)
            
            # 統計更新
            complexity = test_case['complexity']
            results['accuracy_by_complexity'][complexity]['total'] += 1
            
            if evaluation['passed']:
                results['passed_tests'] += 1
                results['accuracy_by_complexity'][complexity]['passed'] += 1
                print(f"✅ PASSED - Overall confidence: {test_result.overall_confidence:.3f}")
            else:
                results['failed_tests'] += 1
                print(f"❌ FAILED - Issues: {', '.join(evaluation['issues'])}")
            
            # 詳細結果保存
            evaluation['test_case'] = test_case
            evaluation['processing_time'] = test_result.total_processing_time
            evaluation['stage_times'] = test_result.stage_times
            results['detailed_results'].append(evaluation)
            
            # パフォーマンス表示
            print(f"⏱️ Processing: {test_result.total_processing_time:.3f}s")
            print(f"📊 Stages: " + 
                  f"B:{test_result.stage_times['stage1']:.3f}s " +
                  f"C:{test_result.stage_times['stage2']:.3f}s " +
                  f"P:{test_result.stage_times['stage3']:.3f}s " +
                  f"I:{test_result.stage_times['stage4']:.3f}s")
        
        # 最終統計計算
        results['total_processing_time'] = time.time() - total_start_time
        results['average_processing_time'] = results['total_processing_time'] / len(self.test_cases)
        
        return results
    
    def _evaluate_test_result(self, test_case: Dict, result) -> Dict:
        """テスト結果評価"""
        
        evaluation = {
            'passed': True,
            'issues': [],
            'main_clause_correct': False,
            'subordinate_clauses_correct': False,
            'boundary_detection_correct': False,
            'confidence_score': result.overall_confidence
        }
        
        # 主節パターン評価
        if result.main_clause:
            if result.main_clause.grammar_pattern == test_case['expected_main']:
                evaluation['main_clause_correct'] = True
            else:
                evaluation['passed'] = False
                evaluation['issues'].append(
                    f"Main pattern mismatch: expected {test_case['expected_main'].value}, "
                    f"got {result.main_clause.grammar_pattern.value}"
                )
        else:
            evaluation['passed'] = False
            evaluation['issues'].append("Main clause not detected")
        
        # 従属節パターン評価
        expected_subs = test_case['expected_subordinate']
        detected_subs = [sub.grammar_pattern for sub in result.subordinate_clauses]
        
        if len(detected_subs) == len(expected_subs):
            # パターンマッチング（順序は考慮せず）
            for expected_pattern in expected_subs:
                if expected_pattern not in detected_subs:
                    evaluation['passed'] = False
                    evaluation['issues'].append(
                        f"Missing subordinate pattern: {expected_pattern.value}"
                    )
                    break
            else:
                evaluation['subordinate_clauses_correct'] = True
        else:
            evaluation['passed'] = False
            evaluation['issues'].append(
                f"Subordinate clause count mismatch: expected {len(expected_subs)}, "
                f"got {len(detected_subs)}"
            )
        
        # 境界検出評価
        expected_clause_count = 1 + len(expected_subs)  # 主節 + 従属節
        detected_clause_count = len(result.clause_boundaries)
        
        if detected_clause_count == expected_clause_count:
            evaluation['boundary_detection_correct'] = True
        else:
            evaluation['passed'] = False
            evaluation['issues'].append(
                f"Boundary detection error: expected {expected_clause_count} clauses, "
                f"got {detected_clause_count}"
            )
        
        return evaluation
    
    def print_summary_report(self, results: Dict):
        """サマリーレポート出力"""
        
        print("\n" + "=" * 60)
        print("🎯 STAGED GRAMMAR DETECTOR TEST SUMMARY")
        print("=" * 60)
        
        # 全体精度
        overall_accuracy = (results['passed_tests'] / results['total_tests']) * 100
        print(f"📊 Overall Accuracy: {overall_accuracy:.1f}% ({results['passed_tests']}/{results['total_tests']})")
        
        # 複雑度別精度
        print("\n📈 Accuracy by Complexity:")
        for complexity, stats in results['accuracy_by_complexity'].items():
            if stats['total'] > 0:
                accuracy = (stats['passed'] / stats['total']) * 100
                print(f"  {complexity.title()}: {accuracy:.1f}% ({stats['passed']}/{stats['total']})")
        
        # パフォーマンス
        print(f"\n⏱️ Performance:")
        print(f"  Total Processing Time: {results['total_processing_time']:.3f}s")
        print(f"  Average per Test: {results['average_processing_time']:.3f}s")
        
        # ステージ別平均時間
        stage_averages = {'stage1': 0, 'stage2': 0, 'stage3': 0, 'stage4': 0}
        for result in results['detailed_results']:
            for stage, time_val in result['stage_times'].items():
                stage_averages[stage] += time_val
        
        test_count = len(results['detailed_results'])
        print(f"  Stage Averages:")
        print(f"    Boundary Detection: {stage_averages['stage1']/test_count:.4f}s")
        print(f"    Function Classification: {stage_averages['stage2']/test_count:.4f}s")
        print(f"    Pattern Recognition: {stage_averages['stage3']/test_count:.4f}s")
        print(f"    Results Integration: {stage_averages['stage4']/test_count:.4f}s")
        
        # エラー分析
        print(f"\n🔍 Error Analysis:")
        error_counts = {}
        for result in results['detailed_results']:
            if not result['passed']:
                for issue in result['issues']:
                    error_type = issue.split(':')[0]
                    error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        for error_type, count in error_counts.items():
            print(f"  {error_type}: {count} occurrences")
        
        # 改善提案
        print(f"\n💡 Improvement Recommendations:")
        if overall_accuracy >= 80:
            print("  ✅ Excellent performance! Consider fine-tuning edge cases.")
        elif overall_accuracy >= 70:
            print("  🔄 Good foundation. Focus on subordinate clause detection accuracy.")
        else:
            print("  ⚠️ Needs improvement. Review boundary detection and pattern matching logic.")
        
        print("=" * 60)

if __name__ == "__main__":
    # テストスイート実行
    test_suite = StagedGrammarTestSuite()
    results = test_suite.run_comprehensive_tests()
    test_suite.print_summary_report(results)
