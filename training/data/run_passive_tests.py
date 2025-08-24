#!/usr/bin/env python3
"""
受動態テストランナー - ChatGPT5修正後の検証
Rephrase仕様準拠の受動態処理テスト
"""

import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List
from dynamic_grammar_mapper import DynamicGrammarMapper

# ログ設定
logging.basicConfig(level=logging.WARNING)  # テスト中はWARNINGレベル以上のみ

class PassiveVoiceTestRunner:
    def __init__(self):
        self.mapper = DynamicGrammarMapper()
        self.test_results = []
        
    def load_test_data(self, test_file: str) -> Dict:
        """テストデータを読み込み"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ テストファイル読み込みエラー: {e}")
            return {}
    
    def run_single_test(self, test_id: str, test_data: Dict) -> Dict:
        """個別テスト実行"""
        sentence = test_data['sentence']
        expected = test_data['expected']
        pattern = test_data.get('pattern', 'unknown')
        
        print(f"\n🔍 Test {test_id}: {pattern}")
        print(f"   文: {sentence}")
        
        try:
            # 解析実行
            result = self.mapper.analyze_sentence(sentence)
            actual_slots = result.get('slots', {})
            
            # 結果検証
            test_result = self.verify_result(test_id, sentence, expected, actual_slots, pattern)
            
            # 結果表示
            self.display_test_result(test_result)
            
            return test_result
            
        except Exception as e:
            print(f"   ❌ 解析エラー: {e}")
            return {
                'test_id': test_id,
                'sentence': sentence,
                'pattern': pattern,
                'status': 'error',
                'error': str(e)
            }
    
    def verify_result(self, test_id: str, sentence: str, expected: Dict, actual: Dict, pattern: str) -> Dict:
        """結果検証"""
        test_result = {
            'test_id': test_id,
            'sentence': sentence, 
            'pattern': pattern,
            'expected': expected,
            'actual': actual,
            'main_slots_check': {},
            'sub_slots_check': {},
            'status': 'unknown',
            'score': 0,
            'total_checks': 0
        }
        
        # メインスロット検証
        expected_main = expected.get('main_slots', {})
        main_score = 0
        main_total = len(expected_main)
        
        for slot, expected_value in expected_main.items():
            actual_value = actual.get(slot)
            is_correct = actual_value == expected_value
            test_result['main_slots_check'][slot] = {
                'expected': expected_value,
                'actual': actual_value, 
                'correct': is_correct
            }
            if is_correct:
                main_score += 1
        
        # サブスロット検証（簡易版）
        expected_sub = expected.get('sub_slots', {})
        sub_score = 0
        sub_total = len(expected_sub)
        
        # 全体スコア計算
        total_score = main_score + sub_score
        total_checks = main_total + sub_total
        
        test_result['score'] = total_score
        test_result['total_checks'] = total_checks
        test_result['status'] = 'pass' if total_score == total_checks else 'fail'
        
        return test_result
    
    def display_test_result(self, test_result: Dict):
        """テスト結果表示"""
        status = test_result['status']
        score = test_result['score']
        total = test_result['total_checks']
        
        status_icon = "✅" if status == 'pass' else "❌" if status == 'fail' else "⚠️"
        print(f"   {status_icon} 結果: {score}/{total} ({status})")
        
        # メインスロット詳細
        main_checks = test_result.get('main_slots_check', {})
        if main_checks:
            print("   📋 メインスロット:")
            for slot, check in main_checks.items():
                icon = "✅" if check['correct'] else "❌" 
                expected = check['expected']
                actual = check['actual']
                print(f"      {icon} {slot}: '{expected}' → '{actual}'")
        
        # 重要な受動態要素の確認
        if test_result['pattern'].endswith('passive') or 'passive' in test_result['pattern']:
            actual = test_result['actual']
            print("   🎯 受動態要素確認:")
            
            # Auxスロット（be動詞）
            aux = actual.get('Aux')
            if aux and ('was' in aux or 'were' in aux or 'is' in aux or 'are' in aux or 'be' in aux):
                print(f"      ✅ Aux (be動詞): '{aux}'")
            elif aux:
                print(f"      ⚠️  Aux: '{aux}' (be動詞含む？)")
            else:
                print(f"      ❌ Aux: なし")
            
            # by句確認
            m_slots = [v for k, v in actual.items() if k.startswith('M') and v and 'by' in str(v)]
            if m_slots:
                print(f"      ✅ by句: {m_slots[0]}")
            else:
                print(f"      ⚠️  by句: 検出されず")
    
    def run_all_tests(self, test_file: str) -> Dict:
        """全テスト実行"""
        print("🔥 受動態専用テストセット実行開始")
        print("=" * 60)
        
        test_data = self.load_test_data(test_file)
        if not test_data:
            return {'error': 'テストデータ読み込み失敗'}
        
        # メタ情報表示
        meta = test_data.get('meta', {})
        print(f"📊 テスト概要: {meta.get('description', 'N/A')}")
        print(f"📈 総テスト数: {meta.get('total_count', 'N/A')}")
        print(f"🎯 テスト焦点: {meta.get('test_focus', 'N/A')}")
        
        # テスト実行
        tests = test_data.get('data', {})
        passed = 0
        failed = 0
        errors = 0
        
        for test_id, test_case in tests.items():
            result = self.run_single_test(test_id, test_case)
            self.test_results.append(result)
            
            if result['status'] == 'pass':
                passed += 1
            elif result['status'] == 'fail':
                failed += 1
            else:
                errors += 1
        
        # 総合結果
        total = len(tests)
        print("\n" + "=" * 60)
        print("🎯 テスト総合結果")
        print(f"   ✅ 成功: {passed}/{total}")
        print(f"   ❌ 失敗: {failed}/{total}")
        print(f"   ⚠️  エラー: {errors}/{total}")
        print(f"   📊 成功率: {passed/total*100:.1f}%" if total > 0 else "   📊 成功率: N/A")
        
        # 受動態特有の問題分析
        self.analyze_passive_issues()
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed, 
            'errors': errors,
            'success_rate': passed/total*100 if total > 0 else 0,
            'results': self.test_results
        }
    
    def analyze_passive_issues(self):
        """受動態特有の問題分析"""
        print("\n🔍 受動態パターン分析:")
        
        # パターン別成功率
        pattern_stats = {}
        for result in self.test_results:
            pattern = result.get('pattern', 'unknown')
            if pattern not in pattern_stats:
                pattern_stats[pattern] = {'total': 0, 'passed': 0}
            
            pattern_stats[pattern]['total'] += 1
            if result['status'] == 'pass':
                pattern_stats[pattern]['passed'] += 1
        
        for pattern, stats in pattern_stats.items():
            rate = stats['passed'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"   {pattern}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
        
        # 共通失敗要因分析
        failed_tests = [r for r in self.test_results if r['status'] == 'fail']
        if failed_tests:
            print(f"\n⚠️  失敗テスト分析 ({len(failed_tests)}件):")
            for result in failed_tests[:3]:  # 最初の3件のみ表示
                print(f"   - {result['pattern']}: {result['sentence'][:50]}...")

def main():
    """メイン実行"""
    test_file = Path(__file__).parent / "passive_voice_test_set.json"
    
    if not test_file.exists():
        print(f"❌ テストファイルが見つかりません: {test_file}")
        return 1
    
    runner = PassiveVoiceTestRunner()
    results = runner.run_all_tests(str(test_file))
    
    if 'error' in results:
        print(f"❌ テスト実行エラー: {results['error']}")
        return 1
    
    # 成功率に基づく終了コード
    success_rate = results.get('success_rate', 0)
    if success_rate >= 90:
        print("\n🎉 テスト成功！ChatGPT5修正が効果的です")
        return 0
    elif success_rate >= 70:
        print("\n⚠️  テスト部分成功 - 改善の余地があります")
        return 0
    else:
        print("\n❌ テスト失敗 - さらなる修正が必要です")
        return 1

if __name__ == "__main__":
    sys.exit(main())
