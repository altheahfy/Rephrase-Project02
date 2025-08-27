#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合テストシステム - Integrated Test System
固定データ源（final_54_test_data.json）を使用した標準化されたテスト環境

主要機能:
- 固定テストデータ使用: final_54_test_data.jsonの期待値込みデータを毎回同じ条件で使用
- 自動期待値照合: 手動比較の必要なし、自動で期待値と実際の結果を比較
- Official結果比較: run_official.pyを自動実行して比較（忘れ防止）
- 一本完結: すべてが統合されており、操作ミスを防止

使用方法:
    python integrated_test_system.py --all                # 全テスト実行
    python integrated_test_system.py --phase1             # Phase1のみ
    python integrated_test_system.py --phase2             # Phase2のみ
    python integrated_test_system.py --case ex001         # 特定ケースのみ
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import importlib.util

# スクリプトのディレクトリを基準にパスを設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = SCRIPT_DIR

# 必要なファイルパス
FINAL_TEST_DATA = DATA_DIR / "final_54_test_data.json"
CENTRAL_CONTROLLER = DATA_DIR / "central_controller.py"
RUN_OFFICIAL = DATA_DIR / "run_official.py"
GRAMMAR_HANDLER = DATA_DIR / "grammar_handler_fix_priorities.py"

class IntegratedTestSystem:
    """統合テストシステムのメインクラス"""
    
    def __init__(self):
        self.test_data = None
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'details': []
        }
        
    def load_test_data(self) -> bool:
        """固定テストデータ（final_54_test_data.json）を読み込み"""
        try:
            with open(FINAL_TEST_DATA, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
            print(f"✅ テストデータ読み込み完了: {len(self.test_data)} ケース")
            return True
        except Exception as e:
            print(f"❌ テストデータ読み込み失敗: {e}")
            return False
    
    def import_modules(self) -> Dict[str, Any]:
        """必要なモジュールを動的インポート"""
        modules = {}
        
        try:
            # central_controller.py をインポート
            spec = importlib.util.spec_from_file_location("central_controller", CENTRAL_CONTROLLER)
            central_controller = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(central_controller)
            modules['central_controller'] = central_controller
            
            # grammar_handler_fix_priorities.py をインポート
            spec = importlib.util.spec_from_file_location("grammar_handler", GRAMMAR_HANDLER)
            grammar_handler = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(grammar_handler)
            modules['grammar_handler'] = grammar_handler
            
            print("✅ モジュールインポート完了")
            return modules
            
        except Exception as e:
            print(f"❌ モジュールインポート失敗: {e}")
            return {}
    
    def run_single_test(self, test_case: Dict[str, Any], modules: Dict[str, Any]) -> Dict[str, Any]:
        """単一テストケースを実行"""
        case_id = test_case.get('例文ID', 'unknown')
        expected = test_case.get('期待値', {})
        
        result = {
            'case_id': case_id,
            'status': 'unknown',
            'expected': expected,
            'actual': {},
            'errors': [],
            'match': False
        }
        
        try:
            # central_controllerを使用してテスト実行
            if 'central_controller' in modules:
                controller = modules['central_controller']
                
                # テストケースに応じた処理を実行
                # （実際の処理内容はcentral_controllerの実装に依存）
                actual_result = self.execute_test_case(test_case, controller)
                result['actual'] = actual_result
                
                # 期待値との照合
                if self.compare_results(expected, actual_result):
                    result['status'] = 'passed'
                    result['match'] = True
                else:
                    result['status'] = 'failed'
                    result['match'] = False
                    
            else:
                result['status'] = 'error'
                result['errors'].append('central_controller not available')
                
        except Exception as e:
            result['status'] = 'error'
            result['errors'].append(str(e))
            
        return result
    
    def execute_test_case(self, test_case: Dict[str, Any], controller) -> Dict[str, Any]:
        """テストケースを実際に実行"""
        # この部分は具体的な実装に応じて調整が必要
        # 現在は基本的なプレースホルダー
        try:
            # テストケースの内容に基づいて処理を実行
            input_data = test_case.get('入力データ', {})
            
            # central_controllerの適切な関数を呼び出し
            # （実際の関数名は実装に依存）
            if hasattr(controller, 'process_sentence'):
                result = controller.process_sentence(input_data)
                return result
            else:
                return {'status': 'no_processor_available'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def compare_results(self, expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """期待値と実際の結果を比較"""
        if not expected:
            return True  # 期待値が設定されていない場合はパス
            
        try:
            # JSONの深い比較
            return self.deep_compare(expected, actual)
        except Exception:
            return False
    
    def deep_compare(self, obj1: Any, obj2: Any) -> bool:
        """深い比較を行う"""
        if type(obj1) != type(obj2):
            return False
            
        if isinstance(obj1, dict):
            if set(obj1.keys()) != set(obj2.keys()):
                return False
            return all(self.deep_compare(obj1[key], obj2[key]) for key in obj1.keys())
            
        elif isinstance(obj1, list):
            if len(obj1) != len(obj2):
                return False
            return all(self.deep_compare(a, b) for a, b in zip(obj1, obj2))
            
        else:
            return obj1 == obj2
    
    def run_official_comparison(self) -> Dict[str, Any]:
        """run_official.pyを実行して結果を比較"""
        try:
            print("🔄 Official結果との比較を実行中...")
            result = subprocess.run([
                sys.executable, str(RUN_OFFICIAL)
            ], capture_output=True, text=True, cwd=str(DATA_DIR))
            
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def filter_test_cases(self, phase: Optional[str] = None, case_id: Optional[str] = None, case_number: Optional[int] = None, case_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """テストケースをフィルタリング"""
        if not self.test_data:
            return []
            
        filtered = self.test_data.copy()
        
        if case_id:
            filtered = [case for case in filtered if case.get('例文ID') == case_id]
        elif case_number is not None:
            # 番号での選択（1から開始）
            if 1 <= case_number <= len(filtered):
                filtered = [filtered[case_number - 1]]
            else:
                print(f"❌ 無効な番号: {case_number} (有効範囲: 1-{len(filtered)})")
                filtered = []
        elif case_range:
            # 範囲での選択（例: "1-5", "10-15"）
            try:
                if '-' in case_range:
                    start, end = map(int, case_range.split('-'))
                    start = max(1, start)
                    end = min(len(filtered), end)
                    if start <= end:
                        filtered = filtered[start-1:end]
                    else:
                        print(f"❌ 無効な範囲: {case_range}")
                        filtered = []
                else:
                    # 単一番号として処理
                    num = int(case_range)
                    if 1 <= num <= len(filtered):
                        filtered = [filtered[num - 1]]
                    else:
                        print(f"❌ 無効な番号: {num} (有効範囲: 1-{len(filtered)})")
                        filtered = []
            except ValueError:
                print(f"❌ 無効な範囲形式: {case_range} (例: '1-5' または '10')")
                filtered = []
        elif phase:
            # Phase1/Phase2の分類ロジック（実装に応じて調整）
            if phase.lower() == 'phase1':
                # Phase1の条件を定義
                filtered = [case for case in filtered if self.is_phase1_case(case)]
            elif phase.lower() == 'phase2':
                # Phase2の条件を定義
                filtered = [case for case in filtered if self.is_phase2_case(case)]
                
        return filtered
    
    def is_phase1_case(self, case: Dict[str, Any]) -> bool:
        """Phase1のケースかどうか判定"""
        # 実装に応じて調整
        return True  # プレースホルダー
    
    def is_phase2_case(self, case: Dict[str, Any]) -> bool:
        """Phase2のケースかどうか判定"""
        # 実装に応じて調整
        return True  # プレースホルダー
    
    def run_tests(self, phase: Optional[str] = None, case_id: Optional[str] = None, case_number: Optional[int] = None, case_range: Optional[str] = None) -> Dict[str, Any]:
        """テストを実行"""
        print("🎯 統合テストシステム開始")
        print("=" * 50)
        
        # テストデータ読み込み
        if not self.load_test_data():
            return {'error': 'Failed to load test data'}
        
        # モジュールインポート
        modules = self.import_modules()
        if not modules:
            return {'error': 'Failed to import required modules'}
        
        # テストケースフィルタリング
        test_cases = self.filter_test_cases(phase, case_id, case_number, case_range)
        print(f"📊 実行対象: {len(test_cases)} ケース")
        
        if not test_cases:
            return {'error': 'No test cases found'}
        
        # テスト実行
        self.results['total'] = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔄 [{i}/{len(test_cases)}] {test_case.get('例文ID', 'unknown')} 実行中...")
            
            result = self.run_single_test(test_case, modules)
            self.results['details'].append(result)
            
            if result['status'] == 'passed':
                self.results['passed'] += 1
                print(f"✅ {result['case_id']}: 成功")
            else:
                self.results['failed'] += 1
                print(f"❌ {result['case_id']}: 失敗 ({result['status']})")
                if result['errors']:
                    self.results['errors'].extend(result['errors'])
        
        # Official結果との比較
        official_result = self.run_official_comparison()
        self.results['official_comparison'] = official_result
        
        return self.results
    
    def print_summary(self):
        """結果サマリーを表示"""
        print("\n" + "=" * 50)
        print("📊 テスト結果サマリー")
        print("=" * 50)
        print(f"総ケース数: {self.results['total']}")
        print(f"成功: {self.results['passed']}")
        print(f"失敗: {self.results['failed']}")
        print(f"成功率: {(self.results['passed']/self.results['total']*100):.1f}%" if self.results['total'] > 0 else "N/A")
        
        if self.results['errors']:
            print(f"\n❌ エラー詳細:")
            for error in self.results['errors'][:5]:  # 最初の5つのエラーのみ表示
                print(f"  - {error}")
            if len(self.results['errors']) > 5:
                print(f"  ... その他 {len(self.results['errors']) - 5} 件")
        
        # Official比較結果
        if 'official_comparison' in self.results:
            official = self.results['official_comparison']
            if official.get('success'):
                print("\n✅ Official結果との比較: 成功")
            else:
                print("\n❌ Official結果との比較: 失敗")
                if 'error' in official:
                    print(f"  エラー: {official['error']}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='統合テストシステム')
    parser.add_argument('--all', action='store_true', help='全テストを実行')
    parser.add_argument('--phase1', action='store_true', help='Phase1のみ実行')
    parser.add_argument('--phase2', action='store_true', help='Phase2のみ実行')
    parser.add_argument('--case', type=str, help='特定ケースのみ実行 (例: ex001)')
    parser.add_argument('--number', type=int, help='番号で特定ケースを実行 (例: 1, 2, 3...)')
    parser.add_argument('--range', type=str, help='範囲でケースを実行 (例: "1-5", "10-15")')
    parser.add_argument('--list', action='store_true', help='利用可能なテストケース一覧を表示')
    
    args = parser.parse_args()
    
    # テストシステム初期化
    test_system = IntegratedTestSystem()
    
    # リスト表示
    if args.list:
        if test_system.load_test_data():
            print("📋 利用可能なテストケース:")
            print("=" * 50)
            for i, case in enumerate(test_system.test_data, 1):
                case_id = case.get('例文ID', 'unknown')
                print(f"{i:3d}. {case_id}")
            print(f"\n総計: {len(test_system.test_data)} ケース")
        return
    
    # 引数チェック
    if not any([args.all, args.phase1, args.phase2, args.case, args.number, args.range]):
        print("使用方法:")
        print("  python integrated_test_system.py --all              # 全テスト実行")
        print("  python integrated_test_system.py --phase1           # Phase1のみ")
        print("  python integrated_test_system.py --phase2           # Phase2のみ")
        print("  python integrated_test_system.py --case ex001       # 特定ケース（ID指定）")
        print("  python integrated_test_system.py --number 5         # 特定ケース（番号指定）")
        print("  python integrated_test_system.py --range 1-10       # 範囲指定")
        print("  python integrated_test_system.py --list             # ケース一覧表示")
        return
    
    # テスト実行
    if args.all:
        results = test_system.run_tests()
    elif args.phase1:
        results = test_system.run_tests(phase='phase1')
    elif args.phase2:
        results = test_system.run_tests(phase='phase2')
    elif args.case:
        results = test_system.run_tests(case_id=args.case)
    elif args.number:
        results = test_system.run_tests(case_number=args.number)
    elif args.range:
        results = test_system.run_tests(case_range=args.range)
    
    # 結果表示
    test_system.print_summary()
    
    # 終了コード
    if 'error' in results:
        print(f"\n❌ システムエラー: {results['error']}")
        sys.exit(1)
    elif test_system.results['failed'] > 0:
        sys.exit(1)
    else:
        print("\n🎉 全テスト成功!")
        sys.exit(0)

if __name__ == "__main__":
    main()
