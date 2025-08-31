#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全120ケース統合テスト - 関係副詞含む完全版
最終的な全システム統合テスト
"""

import sys
import os
import json
from typing import Dict, Any, List

# パスを追加してモジュールをインポート
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from central_controller import CentralController

class ComprehensiveSystemTest:
    def __init__(self):
        self.controller = CentralController()
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def load_test_data(self) -> Dict[str, Any]:
        """テストデータを読み込み"""
        test_file = os.path.join(current_dir, 'final_54_test_data_with_absolute_order_corrected.json')
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ テストファイルが見つかりません: {test_file}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSONデコードエラー: {e}")
            return None
    
    def compare_structures(self, expected: Dict, actual: Dict, path: str = "") -> bool:
        """構造比較（順序を考慮しない）"""
        if type(expected) != type(actual):
            return False
            
        if isinstance(expected, dict):
            if set(expected.keys()) != set(actual.keys()):
                return False
            for key in expected.keys():
                if not self.compare_structures(expected[key], actual[key], f"{path}.{key}"):
                    return False
            return True
        elif isinstance(expected, list):
            return len(expected) == len(actual) and all(
                self.compare_structures(e, a, f"{path}[{i}]") 
                for i, (e, a) in enumerate(zip(expected, actual))
            )
        else:
            return expected == actual
    
    def test_single_case(self, case_id: str, test_case: Dict[str, Any]) -> bool:
        """単一ケースのテスト"""
        sentence = test_case['sentence']
        expected_main = test_case['expected'].get('main_slots', {})
        expected_sub = test_case['expected'].get('sub_slots', {})
        category = test_case.get('grammar_category', 'unknown')
        
        try:
            # 文法解析実行
            result = self.controller.process_sentence(sentence)
            
            if not result or not result.get('success'):
                print(f"❌ Case {case_id}: 解析失敗 - {sentence}")
                return False
            
            # 結果取得
            actual_main = result.get('main_slots', {})
            actual_sub = result.get('sub_slots', {})
            
            # 比較
            main_match = self.compare_structures(expected_main, actual_main)
            sub_match = self.compare_structures(expected_sub, actual_sub) if expected_sub else True
            
            success = main_match and sub_match
            
            # 詳細ログ
            if not success:
                print(f"❌ Case {case_id} [{category}]: {sentence}")
                if not main_match:
                    print(f"   主節不一致:")
                    print(f"     期待: {expected_main}")
                    print(f"     実際: {actual_main}")
                if not sub_match:
                    print(f"   従節不一致:")
                    print(f"     期待: {expected_sub}")
                    print(f"     実際: {actual_sub}")
            else:
                print(f"✅ Case {case_id} [{category}]: {sentence}")
            
            return success
            
        except Exception as e:
            print(f"❌ Case {case_id}: 例外発生 - {e}")
            return False
    
    def run_comprehensive_test(self):
        """全体テスト実行"""
        print("=" * 80)
        print("🔥 全120ケース統合テスト - 関係副詞含む完全版 🔥")
        print("=" * 80)
        
        # テストデータ読み込み
        test_data = self.load_test_data()
        if not test_data:
            print("❌ テストデータの読み込みに失敗しました")
            return
        
        meta = test_data.get('meta', {})
        cases = test_data.get('data', {})
        
        print(f"📊 テスト概要:")
        print(f"   総ケース数: {meta.get('total_count', len(cases))}")
        print(f"   カテゴリ別:")
        for category, count in meta.get('category_counts', {}).items():
            print(f"     {category}: {count}ケース")
        print()
        
        # カテゴリ別結果集計
        category_results = {}
        
        # 各ケースをテスト
        for case_id, test_case in cases.items():
            category = test_case.get('grammar_category', 'unknown')
            
            if category not in category_results:
                category_results[category] = {'passed': 0, 'total': 0}
            
            category_results[category]['total'] += 1
            
            success = self.test_single_case(case_id, test_case)
            
            if success:
                self.passed += 1
                category_results[category]['passed'] += 1
            else:
                self.failed += 1
            
            self.results.append({
                'case_id': case_id,
                'category': category,
                'sentence': test_case['sentence'],
                'success': success
            })
        
        # 最終結果表示
        print("\n" + "=" * 80)
        print("🎯 最終結果")
        print("=" * 80)
        
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"📊 総合結果: {self.passed}/{total} ({success_rate:.1f}%)")
        print(f"   ✅ 成功: {self.passed}")
        print(f"   ❌ 失敗: {self.failed}")
        print()
        
        print("📋 カテゴリ別結果:")
        for category, results in sorted(category_results.items()):
            passed = results['passed']
            total = results['total']
            rate = (passed / total * 100) if total > 0 else 0
            status = "✅" if passed == total else "❌"
            print(f"   {status} {category}: {passed}/{total} ({rate:.1f}%)")
        
        # 失敗ケース詳細
        if self.failed > 0:
            print("\n❌ 失敗ケース詳細:")
            failed_cases = [r for r in self.results if not r['success']]
            for case in failed_cases:
                print(f"   Case {case['case_id']} [{case['category']}]: {case['sentence']}")
        
        print("\n" + "=" * 80)
        if self.failed == 0:
            print("🎉 全ケース成功！完全なシステム統合達成！ 🎉")
        else:
            print(f"⚠️  {self.failed}ケースの改善が必要です")
        print("=" * 80)
        
        return success_rate == 100.0

def main():
    """メイン関数"""
    tester = ComprehensiveSystemTest()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
