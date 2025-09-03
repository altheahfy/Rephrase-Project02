#!/usr/bin/env python3
"""
新旧システム統合テストスイート
期待値との照合による信頼性の高い比較検証システム

機能:
1. final_54_test_data_with_absolute_order_corrected.json の期待値を使用
2. 新旧両システムの実行と期待値照合
3. 詳細な差異分析とパフォーマンス比較
4. fast_test.py互換インターフェース
"""

import json
import sys
import os
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# システムインポート
from central_controller import CentralController
from central_controller_v2 import CentralControllerV2


class ExpectedValueValidator:
    """期待値検証システム"""
    
    def __init__(self):
        self.validation_rules = {
            'main_slots': ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3'],
            'sub_slots': ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
        }
    
    def validate_against_expected(self, actual_result: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """実際の結果と期待値の照合"""
        
        validation_result = {
            'overall_match': False,
            'main_slots_match': False,
            'sub_slots_match': False,
            'differences': {
                'main_slots': {},
                'sub_slots': {}
            },
            'scores': {
                'main_slots_accuracy': 0.0,
                'sub_slots_accuracy': 0.0,
                'overall_accuracy': 0.0
            }
        }
        
        # メインスロット検証
        main_validation = self._validate_slots(
            actual_result.get('main_slots', {}), 
            expected.get('main_slots', {}),
            'main_slots'
        )
        
        # サブスロット検証
        sub_validation = self._validate_slots(
            actual_result.get('sub_slots', {}),
            expected.get('sub_slots', {}), 
            'sub_slots'
        )
        
        validation_result['main_slots_match'] = main_validation['perfect_match']
        validation_result['sub_slots_match'] = sub_validation['perfect_match']
        validation_result['differences']['main_slots'] = main_validation['differences']
        validation_result['differences']['sub_slots'] = sub_validation['differences']
        validation_result['scores']['main_slots_accuracy'] = main_validation['accuracy']
        validation_result['scores']['sub_slots_accuracy'] = sub_validation['accuracy']
        
        # 全体評価
        validation_result['overall_match'] = (
            validation_result['main_slots_match'] and 
            validation_result['sub_slots_match']
        )
        
        validation_result['scores']['overall_accuracy'] = (
            (main_validation['accuracy'] + sub_validation['accuracy']) / 2
        )
        
        return validation_result
    
    def _validate_slots(self, actual_slots: Dict[str, str], expected_slots: Dict[str, str], slot_type: str) -> Dict[str, Any]:
        """スロット単位の詳細検証"""
        
        relevant_slots = self.validation_rules[slot_type]
        differences = {
            'missing': [],      # 期待値にあるが実際にない
            'extra': [],        # 実際にあるが期待値にない  
            'incorrect': []     # 値が異なる
        }
        
        total_expected = len(expected_slots)
        correct_count = 0
        
        # 期待値の各スロットをチェック
        for slot_key, expected_value in expected_slots.items():
            if slot_key in actual_slots:
                actual_value = actual_slots[slot_key]
                if self._normalize_value(actual_value) == self._normalize_value(expected_value):
                    correct_count += 1
                else:
                    differences['incorrect'].append({
                        'slot': slot_key,
                        'expected': expected_value,
                        'actual': actual_value
                    })
            else:
                differences['missing'].append({
                    'slot': slot_key,
                    'expected': expected_value
                })
        
        # 実際の結果で期待値にないスロットをチェック
        for slot_key, actual_value in actual_slots.items():
            if slot_key not in expected_slots and actual_value and actual_value.strip():
                differences['extra'].append({
                    'slot': slot_key,
                    'actual': actual_value
                })
        
        # 精度計算
        accuracy = correct_count / total_expected if total_expected > 0 else 1.0
        perfect_match = (
            len(differences['missing']) == 0 and 
            len(differences['extra']) == 0 and 
            len(differences['incorrect']) == 0
        )
        
        return {
            'perfect_match': perfect_match,
            'accuracy': accuracy,
            'differences': differences,
            'correct_count': correct_count,
            'total_expected': total_expected
        }
    
    def _normalize_value(self, value: str) -> str:
        """値の正規化（比較用）"""
        if not value:
            return ""
        return str(value).strip().lower()


class UnifiedTestSystem:
    """新旧システム統合テストシステム"""
    
    def __init__(self):
        print("🔬 新旧システム統合テスト 初期化開始")
        
        # テストデータ読み込み
        self.test_data = self._load_test_data()
        print(f"📋 テストデータ読み込み完了: {self.test_data['meta']['total_count']}件")
        
        # 期待値検証システム初期化
        self.validator = ExpectedValueValidator()
        
        # 既存システム初期化
        self.legacy_controller = None
        self.v2_controller = None
        
        self._initialize_systems()
        
        self.test_results = []
    
    def _load_test_data(self) -> Dict[str, Any]:
        """テストデータ読み込み"""
        try:
            with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ テストデータファイルが見つかりません")
            sys.exit(1)
    
    def _initialize_systems(self):
        """両システムの初期化"""
        
        # 既存システム
        try:
            self.legacy_controller = CentralController()
            print("✅ 既存システム初期化完了")
        except Exception as e:
            print(f"❌ 既存システム初期化失敗: {e}")
        
        # 新システム
        try:
            self.v2_controller = CentralControllerV2()
            print("✅ 新システム初期化完了")
        except Exception as e:
            print(f"❌ 新システム初期化失敗: {e}")
    
    def parse_range(self, case_range: str) -> List[str]:
        """ケース範囲解析（fast_test.py互換）"""
        
        # プリセット範囲定義
        presets = {
            'all': list(self.test_data['data'].keys()),
            'basic': [str(i) for i in range(1, 18)],
            'adverbs': [str(i) for i in range(18, 43)],
            'modal': [str(i) for i in range(87, 111)],
            'relative': ['56', '58', '64'],
            'passive': [str(i) for i in range(66, 70)],
            'v2_test': ['1', '2', '3', '87', '88', '56']  # Phase 6a テスト用
        }
        
        if case_range in presets:
            return presets[case_range]
        
        # 数値範囲解析
        case_numbers = []
        for part in case_range.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                case_numbers.extend([str(i) for i in range(start, end + 1)])
            else:
                case_numbers.append(part.strip())
        
        return case_numbers
    
    def run_unified_test(self, case_range: str = 'v2_test', verbose: bool = True) -> Dict[str, Any]:
        """統合テスト実行"""
        
        case_numbers = self.parse_range(case_range)
        print(f"\n🚀 統合テスト開始: {len(case_numbers)}件")
        print("=" * 80)
        
        results = {
            'test_summary': {
                'total_cases': len(case_numbers),
                'case_range': case_range,
                'timestamp': time.time()
            },
            'system_results': {
                'legacy': {'success': 0, 'failure': 0, 'total_time': 0},
                'v2': {'success': 0, 'failure': 0, 'total_time': 0}
            },
            'accuracy_results': {
                'legacy': {'perfect_matches': 0, 'total_accuracy': 0},
                'v2': {'perfect_matches': 0, 'total_accuracy': 0}
            },
            'individual_results': []
        }
        
        for i, case_num in enumerate(case_numbers, 1):
            if case_num not in self.test_data['data']:
                print(f"⚠️ ケース {case_num} が見つかりません")
                continue
            
            case_data = self.test_data['data'][case_num]
            sentence = case_data['sentence']
            expected = case_data['expected']
            
            if verbose:
                print(f"\n📝 ケース {i}/{len(case_numbers)}: {case_num}")
                print(f"   文: {sentence}")
            
            # 個別テスト実行
            test_result = self._run_single_test(case_num, sentence, expected, verbose)
            results['individual_results'].append(test_result)
            
            # 統計更新
            self._update_statistics(results, test_result)
            
            if verbose and i % 5 == 0:
                print(f"\n⏳ 進捗: {i}/{len(case_numbers)} ({i/len(case_numbers)*100:.1f}%)")
        
        # 最終統計計算
        self._finalize_statistics(results)
        
        return results
    
    def _run_single_test(self, case_num: str, sentence: str, expected: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
        """単一テストケースの実行"""
        
        result = {
            'case_number': case_num,
            'sentence': sentence,
            'expected': expected,
            'legacy_result': None,
            'v2_result': None,
            'validations': {
                'legacy': None,
                'v2': None
            },
            'performance': {
                'legacy_time': None,
                'v2_time': None
            },
            'errors': {
                'legacy': None,
                'v2': None
            }
        }
        
        # 既存システムテスト
        if self.legacy_controller:
            try:
                start_time = time.time()
                # 正しいメソッド名を使用
                legacy_output = self.legacy_controller.process_sentence(sentence)
                result['performance']['legacy_time'] = time.time() - start_time
                result['legacy_result'] = legacy_output
                
                # 期待値照合
                validation = self.validator.validate_against_expected(legacy_output, expected)
                result['validations']['legacy'] = validation
                
                if verbose:
                    status = "✅" if validation['overall_match'] else "❌"
                    print(f"   既存: {status} 精度={validation['scores']['overall_accuracy']:.2f}")
                    
            except Exception as e:
                result['errors']['legacy'] = str(e)
                if verbose:
                    print(f"   既存: ❌ エラー: {e}")
        
        # 新システムテスト
        if self.v2_controller:
            try:
                start_time = time.time()
                v2_analysis = self.v2_controller.analyze_grammar_structure_v2(sentence)
                result['performance']['v2_time'] = time.time() - start_time
                
                # V2結果を既存形式に変換（期待値照合用）
                v2_converted = self._convert_v2_to_legacy_format(v2_analysis)
                result['v2_result'] = v2_converted
                
                # 期待値照合
                validation = self.validator.validate_against_expected(v2_converted, expected)
                result['validations']['v2'] = validation
                
                if verbose:
                    status = "✅" if validation['overall_match'] else "❌"
                    print(f"   新システム: {status} 精度={validation['scores']['overall_accuracy']:.2f}")
                    
            except Exception as e:
                result['errors']['v2'] = str(e)
                if verbose:
                    print(f"   新システム: ❌ エラー: {e}")
        
        return result
    
    def _convert_v2_to_legacy_format(self, v2_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """V2結果を既存システム形式に変換（期待値照合用）"""
        
        # V2システムは既にmain_slots、sub_slotsを返している
        # 直接それらを使用して既存形式に変換
        converted_result = {
            'main_slots': v2_analysis.get('main_slots', {}),
            'sub_slots': v2_analysis.get('sub_slots', {}),
            'detected_grammar': v2_analysis.get('detected_grammar', []),
            'confidence': v2_analysis.get('confidence', 0.0),
            'v2_metadata': v2_analysis.get('v2_metadata', {})
        }
        
        return converted_result
    
    def _update_statistics(self, results: Dict[str, Any], test_result: Dict[str, Any]):
        """統計情報の更新"""
        
        # 成功/失敗カウント
        if test_result['errors']['legacy'] is None:
            results['system_results']['legacy']['success'] += 1
        else:
            results['system_results']['legacy']['failure'] += 1
            
        if test_result['errors']['v2'] is None:
            results['system_results']['v2']['success'] += 1
        else:
            results['system_results']['v2']['failure'] += 1
        
        # 実行時間累計
        if test_result['performance']['legacy_time']:
            results['system_results']['legacy']['total_time'] += test_result['performance']['legacy_time']
        if test_result['performance']['v2_time']:
            results['system_results']['v2']['total_time'] += test_result['performance']['v2_time']
        
        # 精度統計
        if test_result['validations']['legacy']:
            if test_result['validations']['legacy']['overall_match']:
                results['accuracy_results']['legacy']['perfect_matches'] += 1
            results['accuracy_results']['legacy']['total_accuracy'] += test_result['validations']['legacy']['scores']['overall_accuracy']
            
        if test_result['validations']['v2']:
            if test_result['validations']['v2']['overall_match']:
                results['accuracy_results']['v2']['perfect_matches'] += 1
            results['accuracy_results']['v2']['total_accuracy'] += test_result['validations']['v2']['scores']['overall_accuracy']
    
    def _finalize_statistics(self, results: Dict[str, Any]):
        """最終統計計算"""
        
        total_cases = results['test_summary']['total_cases']
        
        # 成功率計算
        results['system_results']['legacy']['success_rate'] = (
            results['system_results']['legacy']['success'] / total_cases if total_cases > 0 else 0
        )
        results['system_results']['v2']['success_rate'] = (
            results['system_results']['v2']['success'] / total_cases if total_cases > 0 else 0
        )
        
        # 平均精度計算
        results['accuracy_results']['legacy']['average_accuracy'] = (
            results['accuracy_results']['legacy']['total_accuracy'] / total_cases if total_cases > 0 else 0
        )
        results['accuracy_results']['v2']['average_accuracy'] = (
            results['accuracy_results']['v2']['total_accuracy'] / total_cases if total_cases > 0 else 0
        )
        
        # 完全一致率計算
        results['accuracy_results']['legacy']['perfect_match_rate'] = (
            results['accuracy_results']['legacy']['perfect_matches'] / total_cases if total_cases > 0 else 0
        )
        results['accuracy_results']['v2']['perfect_match_rate'] = (
            results['accuracy_results']['v2']['perfect_matches'] / total_cases if total_cases > 0 else 0
        )
    
    def print_summary(self, results: Dict[str, Any]):
        """テスト結果サマリー表示"""
        
        print(f"\n📊 統合テスト結果サマリー")
        print("=" * 60)
        
        print(f"📋 テスト概要:")
        print(f"   総テスト数: {results['test_summary']['total_cases']}")
        print(f"   テスト範囲: {results['test_summary']['case_range']}")
        
        print(f"\n🔧 システム成功率:")
        print(f"   既存システム: {results['system_results']['legacy']['success_rate']:.1%} ({results['system_results']['legacy']['success']}/{results['test_summary']['total_cases']})")
        print(f"   新システム: {results['system_results']['v2']['success_rate']:.1%} ({results['system_results']['v2']['success']}/{results['test_summary']['total_cases']})")
        
        print(f"\n🎯 期待値一致精度:")
        print(f"   既存システム: 平均={results['accuracy_results']['legacy']['average_accuracy']:.1%}, 完全一致={results['accuracy_results']['legacy']['perfect_match_rate']:.1%}")
        print(f"   新システム: 平均={results['accuracy_results']['v2']['average_accuracy']:.1%}, 完全一致={results['accuracy_results']['v2']['perfect_match_rate']:.1%}")
        
        print(f"\n⚡ パフォーマンス:")
        legacy_avg = results['system_results']['legacy']['total_time'] / results['test_summary']['total_cases']
        v2_avg = results['system_results']['v2']['total_time'] / results['test_summary']['total_cases']
        print(f"   既存システム: 平均={legacy_avg:.3f}s")
        print(f"   新システム: 平均={v2_avg:.3f}s")
        if legacy_avg > 0:
            print(f"   性能比: 新システムが{legacy_avg/v2_avg:.1f}倍高速" if v2_avg < legacy_avg else f"   性能比: 既存システムが{v2_avg/legacy_avg:.1f}倍高速")

        # 不一致案件の詳細表示
        self.print_mismatch_details(results)
    
    def print_mismatch_details(self, results: Dict[str, Any]):
        """不一致案件の詳細表示"""
        print(f"\n📋 不一致案件詳細分析:")
        print("=" * 60)
        
        # 新システムの不一致案件を抽出
        v2_mismatches = []
        legacy_mismatches = []
        
        for case_result in results.get('individual_results', []):
            case_id = case_result.get('case_number')
            text = case_result.get('sentence', '')
            expected = case_result.get('expected', {})
            
            # 新システムの不一致チェック
            v2_validation = case_result.get('validations', {}).get('v2', {})
            if v2_validation and not v2_validation.get('overall_match', False):
                v2_result = case_result.get('v2_result', {})
                v2_mismatches.append({
                    'case_id': case_id,
                    'text': text,
                    'expected': expected.get('main_slots', {}),
                    'actual': v2_result.get('main_slots', {}),
                    'accuracy': v2_validation.get('scores', {}).get('overall_accuracy', 0),
                    'differences': v2_validation.get('differences', {}),
                    'errors': case_result.get('errors', {}).get('v2')
                })
            
            # 既存システムの不一致チェック  
            legacy_validation = case_result.get('validations', {}).get('legacy', {})
            if legacy_validation and not legacy_validation.get('overall_match', False):
                legacy_result = case_result.get('legacy_result', {})
                legacy_mismatches.append({
                    'case_id': case_id,
                    'text': text,
                    'expected': expected.get('main_slots', {}),
                    'actual': legacy_result.get('main_slots', {}),
                    'accuracy': legacy_validation.get('scores', {}).get('overall_accuracy', 0),
                    'differences': legacy_validation.get('differences', {}),
                    'errors': case_result.get('errors', {}).get('legacy')
                })
        
        # 新システムの不一致表示
        if v2_mismatches:
            print(f"🔴 新システム不一致案件: {len(v2_mismatches)}件")
            for i, mismatch in enumerate(v2_mismatches, 1):
                print(f"\n  {i}. ケース{mismatch['case_id']}: \"{mismatch['text']}\"")
                print(f"     精度: {mismatch['accuracy']:.1%}")
                
                if mismatch.get('errors'):
                    print(f"     エラー: {mismatch['errors']}")
                    continue
                
                print(f"     期待値: {mismatch['expected']}")
                print(f"     実際値: {mismatch['actual']}")
                
                # 差分詳細（differences構造を使用）
                main_diff = mismatch.get('differences', {}).get('main_slots', {})
                if main_diff.get('missing'):
                    print(f"     不足スロット: {[item['slot'] for item in main_diff['missing']]}")
                if main_diff.get('extra'):
                    print(f"     余分スロット: {[item['slot'] for item in main_diff['extra']]}")
                if main_diff.get('incorrect'):
                    print(f"     値違いスロット:")
                    for item in main_diff['incorrect']:
                        print(f"       {item['slot']}: 期待=\"{item['expected']}\" → 実際=\"{item['actual']}\"")
        else:
            print(f"✅ 新システム: 全件完全一致")
        
        # 既存システムの不一致表示
        if legacy_mismatches:
            print(f"\n🔴 既存システム不一致案件: {len(legacy_mismatches)}件")
            for i, mismatch in enumerate(legacy_mismatches, 1):
                print(f"\n  {i}. ケース{mismatch['case_id']}: \"{mismatch['text']}\"")
                print(f"     精度: {mismatch['accuracy']:.1%}")
                
                if mismatch.get('errors'):
                    print(f"     エラー: {mismatch['errors']}")
                    continue
                
                print(f"     期待値: {mismatch['expected']}")
                print(f"     実際値: {mismatch['actual']}")
        else:
            print(f"✅ 既存システム: 全件完全一致")


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description='新旧システム統合テスト')
    parser.add_argument('case_range', nargs='?', default='v2_test', 
                       help='テストケース範囲 (例: 1-10, basic, modal, v2_test)')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='詳細ログ表示')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='最小ログ表示')
    
    args = parser.parse_args()
    
    # テストシステム初期化
    test_system = UnifiedTestSystem()
    
    # テスト実行
    results = test_system.run_unified_test(
        case_range=args.case_range,
        verbose=not args.quiet
    )
    
    # 結果表示
    test_system.print_summary(results)
    
    # 結果保存
    output_file = f"unified_test_results_{args.case_range}_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 詳細結果を保存: {output_file}")


if __name__ == "__main__":
    main()
