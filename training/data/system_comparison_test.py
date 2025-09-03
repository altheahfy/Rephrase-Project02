"""
新旧システム比較テストスイート (Phase 6a)
既存システムと新中央管理システムの並行運用・比較検証
"""

import sys
import time
from typing import Dict, List, Any
from central_controller import CentralController
from central_controller_v2 import CentralControllerV2


class SystemComparison:
    """新旧システムの比較検証システム"""
    
    def __init__(self):
        print("🔬 システム比較検証 初期化開始")
        
        # 既存システム初期化
        try:
            self.legacy_controller = CentralController()
            print("✅ 既存システム初期化完了")
        except Exception as e:
            print(f"❌ 既存システム初期化失敗: {e}")
            self.legacy_controller = None
        
        # 新システム初期化
        try:
            self.v2_controller = CentralControllerV2()
            print("✅ 新システム初期化完了")
        except Exception as e:
            print(f"❌ 新システム初期化失敗: {e}")
            self.v2_controller = None
            
        self.test_results = []
    
    def run_comparison_test(self, text: str) -> Dict[str, Any]:
        """単一テストケースの比較実行"""
        
        print(f"\n🧪 比較テスト実行: '{text}'")
        print("=" * 60)
        
        # 既存システムでの処理
        legacy_result = None
        legacy_time = None
        legacy_error = None
        
        if self.legacy_controller:
            try:
                start_time = time.time()
                legacy_result = self.legacy_controller.analyze_grammar_structure(text)
                legacy_time = time.time() - start_time
                print(f"📊 既存システム結果: {legacy_result} (実行時間: {legacy_time:.3f}s)")
            except Exception as e:
                legacy_error = str(e)
                print(f"❌ 既存システムエラー: {e}")
        
        # 新システムでの処理
        v2_result = None
        v2_time = None
        v2_error = None
        
        if self.v2_controller:
            try:
                start_time = time.time()
                v2_analysis = self.v2_controller.analyze_grammar_structure_v2(text)
                v2_result = v2_analysis['legacy_format']
                v2_time = time.time() - start_time
                print(f"🆕 新システム結果: {v2_result} (実行時間: {v2_time:.3f}s)")
                print(f"   信頼度: {v2_analysis['v2_result'].confidence_score:.2f}")
                print(f"   使用ハンドラー: {list(v2_analysis['v2_result'].handler_reports.keys())}")
            except Exception as e:
                v2_error = str(e)
                print(f"❌ 新システムエラー: {e}")
        
        # 比較分析
        comparison_result = self._analyze_comparison(
            text, legacy_result, v2_result, legacy_time, v2_time, 
            legacy_error, v2_error, v2_analysis if 'v2_analysis' in locals() else None
        )
        
        self.test_results.append(comparison_result)
        return comparison_result
    
    def _analyze_comparison(self, text: str, legacy_result: List[str], v2_result: List[str], 
                           legacy_time: float, v2_time: float, legacy_error: str, v2_error: str,
                           v2_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """比較結果の詳細分析"""
        
        # 結果一致性分析
        results_match = False
        if legacy_result is not None and v2_result is not None:
            # ソートして順序に依存しない比較
            legacy_sorted = sorted(legacy_result) if legacy_result else []
            v2_sorted = sorted(v2_result) if v2_result else []
            results_match = legacy_sorted == v2_sorted
        
        # 差分分析
        differences = {}
        if legacy_result is not None and v2_result is not None:
            legacy_set = set(legacy_result) if legacy_result else set()
            v2_set = set(v2_result) if v2_result else set()
            
            differences = {
                'v2_extra': list(v2_set - legacy_set),
                'legacy_extra': list(legacy_set - v2_set),
                'common': list(v2_set & legacy_set)
            }
        
        # パフォーマンス分析
        performance_analysis = {}
        if legacy_time is not None and v2_time is not None:
            performance_analysis = {
                'legacy_faster': legacy_time < v2_time,
                'time_difference': abs(v2_time - legacy_time),
                'performance_ratio': v2_time / legacy_time if legacy_time > 0 else None
            }
        
        # 品質評価
        quality_assessment = {
            'both_successful': legacy_error is None and v2_error is None,
            'legacy_error': legacy_error,
            'v2_error': v2_error,
            'results_match': results_match,
            'v2_confidence': v2_analysis['v2_result'].confidence_score if v2_analysis else None
        }
        
        # 結果表示
        print(f"\n📈 比較分析結果:")
        print(f"   結果一致: {'✅' if results_match else '❌'} {results_match}")
        if differences:
            print(f"   差分: V2独自={differences['v2_extra']}, 既存独自={differences['legacy_extra']}")
        if performance_analysis:
            print(f"   パフォーマンス: {'既存' if performance_analysis['legacy_faster'] else 'V2'}が高速")
        
        return {
            'text': text,
            'timestamp': time.time(),
            'results': {
                'legacy': legacy_result,
                'v2': v2_result
            },
            'timing': {
                'legacy': legacy_time,
                'v2': v2_time
            },
            'errors': {
                'legacy': legacy_error,
                'v2': v2_error
            },
            'analysis': {
                'results_match': results_match,
                'differences': differences,
                'performance': performance_analysis,
                'quality': quality_assessment
            },
            'v2_metadata': v2_analysis['v2_result'] if v2_analysis else None
        }
    
    def run_batch_test(self, test_cases: List[str]) -> Dict[str, Any]:
        """バッチテストの実行"""
        
        print(f"\n🔄 バッチテスト開始 - {len(test_cases)}件のテストケース")
        print("=" * 80)
        
        batch_results = []
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n📝 テストケース {i}/{len(test_cases)}")
            result = self.run_comparison_test(text)
            batch_results.append(result)
            
            # 進捗表示
            if i % 5 == 0 or i == len(test_cases):
                print(f"\n⏳ 進捗: {i}/{len(test_cases)} ({i/len(test_cases)*100:.1f}%)")
        
        # バッチ結果の統計分析
        batch_summary = self._generate_batch_summary(batch_results)
        
        return {
            'individual_results': batch_results,
            'batch_summary': batch_summary
        }
    
    def _generate_batch_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """バッチテスト結果の統計サマリー"""
        
        total_tests = len(results)
        successful_tests = len([r for r in results if r['analysis']['quality']['both_successful']])
        matching_results = len([r for r in results if r['analysis']['results_match']])
        
        # エラー分析
        legacy_errors = len([r for r in results if r['errors']['legacy'] is not None])
        v2_errors = len([r for r in results if r['errors']['v2'] is not None])
        
        # パフォーマンス分析
        performance_data = [r['analysis']['performance'] for r in results 
                          if r['analysis']['performance']]
        v2_faster_count = len([p for p in performance_data if not p['legacy_faster']])
        
        # 信頼度分析
        confidence_scores = [r['v2_metadata'].confidence_score for r in results 
                           if r['v2_metadata']]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        summary = {
            'test_statistics': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
                'matching_results': matching_results,
                'match_rate': matching_results / total_tests if total_tests > 0 else 0
            },
            'error_analysis': {
                'legacy_errors': legacy_errors,
                'v2_errors': v2_errors,
                'legacy_error_rate': legacy_errors / total_tests if total_tests > 0 else 0,
                'v2_error_rate': v2_errors / total_tests if total_tests > 0 else 0
            },
            'performance_analysis': {
                'total_performance_tests': len(performance_data),
                'v2_faster_count': v2_faster_count,
                'v2_faster_rate': v2_faster_count / len(performance_data) if performance_data else 0
            },
            'quality_analysis': {
                'average_v2_confidence': avg_confidence,
                'high_confidence_tests': len([s for s in confidence_scores if s > 0.7]),
                'low_confidence_tests': len([s for s in confidence_scores if s < 0.5])
            }
        }
        
        # サマリー表示
        print(f"\n📊 バッチテスト サマリー:")
        print(f"   総テスト数: {total_tests}")
        print(f"   成功率: {summary['test_statistics']['success_rate']:.1%}")
        print(f"   結果一致率: {summary['test_statistics']['match_rate']:.1%}")
        print(f"   V2平均信頼度: {avg_confidence:.2f}")
        print(f"   V2高速化率: {summary['performance_analysis']['v2_faster_rate']:.1%}")
        
        return summary


def main():
    """メイン実行関数"""
    print("🚀 新旧システム比較テスト開始")
    
    # 比較システム初期化
    comparison = SystemComparison()
    
    # Phase 6a テストケース（基本的なもの）
    test_cases = [
        # 基本5文型
        "I love you.",
        "She is beautiful.",
        "He gave me a book.",
        
        # 助動詞
        "I can speak English.",
        "You should study hard.",
        "We must go now.",
        
        # 関係節
        "The book that I read was interesting.",
        "The person who called you is here.",
        "This is the house which I bought.",
        
        # 複合文法
        "I wish I could fly.",
        "What did you see yesterday?",
        "The man who can speak Japanese is my teacher."
    ]
    
    # バッチテスト実行
    batch_results = comparison.run_batch_test(test_cases)
    
    print(f"\n🎯 Phase 6a テスト完了!")
    print(f"   詳細結果は comparison.test_results に保存されています")


if __name__ == "__main__":
    main()
