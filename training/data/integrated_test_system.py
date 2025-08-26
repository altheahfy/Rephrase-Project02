"""
統合テストシステム - Phase 2対応
final_54_test_data.json使用の例文選択→期待値照合システム

機能:
1. Phase別文法例文フィルタリング
2. 新規システムでの処理実行
3. sub_slots対応期待値照合
4. 詳細な結果分析
5. 段階的実行フロー（Phase 1→2→3）
"""

import json
import sys
from typing import Dict, List, Any, Tuple
from central_controller import CentralController


class IntegratedTestSystem:
    """
    統合テストシステム
    
    機能:
    - Phase別テストケース選択
    - 自動期待値照合
    - 詳細分析レポート
    - 実行忘れ防止
    """
    
    def __init__(self):
        """初期化"""
        self.controller = CentralController()
        self.test_data = self._load_test_data()
        
        # Phase 1: 基本5文型のテストケース番号（純粋な基本文型のみ）
        self.phase1_cases = [
            # 第1文型 (SV)
            55, 56, 57,  # Birds fly, Children play, Time passes
            # 第2文型 (SVC) 
            58, 59, 60,  # She looks happy, He became a doctor, The food tastes good
            # 第3文型 (SVO)
            61, 62, 63,  # I read books, She plays piano, We study English
            # 第4文型 (SVOO)
            64, 65, 66,  # I gave him a book, She told me a story, He bought her flowers
            # 第5文型 (SVOC)
            67, 68, 69,  # We call him Tom, I found it interesting, They made her happy
            # 基本文型（関係詞なし）
            1, 2         # The car is red, I love you
        ]
        
        # Phase 2: 関係節テストケース（基本5文型+関係節）
        self.phase2_cases = [
            # 主格関係代名詞
            3, 4, 5,     # The man who runs fast, The book which lies there, The person that works here
            # 目的格関係代名詞  
            6, 7, 8,     # The book which I bought, The man whom I met, The car that he drives
            # 所有格関係代名詞
            12, 13, 14,  # The man whose car is red, The student whose book I borrowed, The woman whose dog barks
            # 受動態+関係節（Phase 2で対応可能な範囲）
            9, 10, 11    # The car which was crashed, The book that was written, The letter which was sent
        ]
    
    def _load_test_data(self) -> Dict[str, Any]:
        """テストデータ読み込み"""
        try:
            with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("final_54_test_data.json が見つかりません")
    
    def run_phase1_tests(self) -> Dict[str, Any]:
        """
        Phase 1テスト実行
        基本5文型のテストケースを実行し、期待値と照合
        
        Returns:
            Dict: テスト結果サマリー
        """
        print("🚀 Phase 1 統合テスト開始")
        print("=" * 50)
        
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'details': [],
            'errors': []
        }
        
        for case_id in self.phase1_cases:
            case_id_str = str(case_id)
            
            if case_id_str not in self.test_data['data']:
                print(f"⚠️  テストケース {case_id} が見つかりません")
                continue
            
            test_case = self.test_data['data'][case_id_str]
            sentence = test_case['sentence']
            expected = test_case['expected']
            
            print(f"\n📝 テストケース {case_id}: {sentence}")
            
            # システムで処理実行
            try:
                result = self.controller.process_sentence(sentence)
                comparison = self._compare_results(result, expected, case_id)
                
                results['total'] += 1
                if comparison['passed']:
                    results['passed'] += 1
                    print("✅ PASS")
                else:
                    results['failed'] += 1
                    print("❌ FAIL")
                    print(f"   原因: {comparison['reason']}")
                
                results['details'].append({
                    'case_id': case_id,
                    'sentence': sentence,
                    'expected': expected,
                    'actual': result,
                    'comparison': comparison
                })
                
            except Exception as e:
                results['failed'] += 1
                results['total'] += 1
                error_msg = f"実行エラー: {str(e)}"
                print(f"💥 ERROR: {error_msg}")
                results['errors'].append({
                    'case_id': case_id,
                    'sentence': sentence,
                    'error': error_msg
                })
        
        self._print_summary(results)
        return results
    
    def _compare_results(self, actual: Dict[str, Any], expected: Dict[str, Any], case_id: int) -> Dict[str, Any]:
        """
        結果と期待値の詳細比較
        
        Args:
            actual: システムの実行結果
            expected: 期待値
            case_id: テストケース番号
            
        Returns:
            Dict: 比較結果
        """
        comparison = {
            'passed': False,
            'reason': '',
            'slot_matches': {},
            'missing_slots': [],
            'extra_slots': [],
            'value_mismatches': []
        }
        
        if not actual.get('success'):
            comparison['reason'] = f"システム処理失敗: {actual.get('error', '不明')}"
            return comparison
        
        actual_slots = actual.get('slots', {})
        expected_main = expected.get('main_slots', {})
        
        # スロット比較
        all_slots = set(actual_slots.keys()) | set(expected_main.keys())
        
        for slot in all_slots:
            if slot in expected_main and slot in actual_slots:
                if actual_slots[slot] == expected_main[slot]:
                    comparison['slot_matches'][slot] = True
                else:
                    comparison['slot_matches'][slot] = False
                    comparison['value_mismatches'].append({
                        'slot': slot,
                        'expected': expected_main[slot],
                        'actual': actual_slots[slot]
                    })
            elif slot in expected_main:
                comparison['missing_slots'].append(slot)
            else:
                comparison['extra_slots'].append(slot)
        
        # 総合判定
        if (not comparison['missing_slots'] and 
            not comparison['extra_slots'] and 
            not comparison['value_mismatches']):
            comparison['passed'] = True
            comparison['reason'] = 'Perfect match'
        else:
            reasons = []
            if comparison['missing_slots']:
                reasons.append(f"欠損スロット: {comparison['missing_slots']}")
            if comparison['extra_slots']:
                reasons.append(f"余分スロット: {comparison['extra_slots']}")
            if comparison['value_mismatches']:
                mismatches = [f"{m['slot']}(期待:{m['expected']}→実際:{m['actual']})" 
                             for m in comparison['value_mismatches']]
                reasons.append(f"値不一致: {mismatches}")
            comparison['reason'] = '; '.join(reasons)
        
        return comparison
    
    def _print_summary(self, results: Dict[str, Any]):
        """テスト結果サマリー表示"""
        print("\n" + "=" * 50)
        print("📊 Phase 1 テスト結果サマリー")
        print("=" * 50)
        
        total = results['total']
        passed = results['passed']
        failed = results['failed']
        
        print(f"総テスト数: {total}")
        print(f"✅ 成功: {passed}")
        print(f"❌ 失敗: {failed}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"🎯 成功率: {success_rate:.1f}%")
            
            if success_rate == 100.0:
                print("🎉 Phase 1 完全達成！")
            elif success_rate >= 90.0:
                print("🌟 優秀！ほぼ完成")
            elif success_rate >= 70.0:
                print("⚡ 良好！改善の余地あり")
            else:
                print("🔧 要改善")
        
        # 詳細失敗ケース表示
        if failed > 0:
            print("\n❌ 失敗ケース詳細:")
            for detail in results['details']:
                if not detail['comparison']['passed']:
                    print(f"  ケース{detail['case_id']}: {detail['sentence']}")
                    print(f"    理由: {detail['comparison']['reason']}")
    
    def run_specific_cases(self, case_ids: List[int]) -> Dict[str, Any]:
        """
        指定ケースのみテスト実行
        
        Args:
            case_ids: 実行するテストケース番号リスト
            
        Returns:
            Dict: テスト結果
        """
        print(f"🎯 指定ケーステスト実行: {case_ids}")
        
        original_cases = self.phase1_cases
        self.phase1_cases = case_ids
        
        results = self.run_phase1_tests()
        
        self.phase1_cases = original_cases
        return results
    
    def run_phase2_tests(self) -> Dict[str, Any]:
        """
        Phase 2テスト実行
        関係節+基本5文型のテストケースを実行し、期待値と照合
        
        Returns:
            Dict: テスト結果サマリー
        """
        print("🚀 Phase 2 統合テスト開始")
        print("=" * 50)
        
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'details': [],
            'errors': []
        }
        
        for case_id in self.phase2_cases:
            case_id_str = str(case_id)
            
            if case_id_str not in self.test_data['data']:
                print(f"⚠️  テストケース {case_id} が見つかりません")
                continue
            
            test_case = self.test_data['data'][case_id_str]
            sentence = test_case['sentence']
            expected = test_case['expected']
            
            results['total'] += 1
            
            print(f"\n📝 テストケース {case_id}: {sentence}")
            
            # システム実行
            actual = self.controller.process_sentence(sentence)
            
            # 期待値比較（sub_slots対応）
            comparison = self._compare_results_with_subs(actual, expected)
            
            if comparison['passed']:
                print("✅ PASS")
                results['passed'] += 1
            else:
                print("❌ FAIL")
                print(f"   原因: {comparison['reason']}")
                results['failed'] += 1
                results['errors'].append({
                    'case_id': case_id,
                    'sentence': sentence,
                    'reason': comparison['reason']
                })
            
            results['details'].append({
                'case_id': case_id,
                'sentence': sentence,
                'passed': comparison['passed'],
                'comparison': comparison
            })
        
        # サマリー表示
        self._print_phase2_summary(results)
        return results
    
    def _compare_results_with_subs(self, actual: Dict, expected: Dict) -> Dict[str, Any]:
        """
        sub_slots対応の結果比較
        
        Args:
            actual: システム出力結果
            expected: 期待値（main_slots + sub_slots）
            
        Returns:
            Dict: 比較結果詳細
        """
        comparison = {
            'passed': False,
            'reason': '',
            'main_slot_matches': {},
            'sub_slot_matches': {},
            'missing_main_slots': [],
            'missing_sub_slots': [],
            'extra_slots': [],
            'value_mismatches': []
        }
        
        if not actual.get('success'):
            comparison['reason'] = f"システム処理失敗: {actual.get('error', '不明')}"
            return comparison
        
        # メインスロット比較
        actual_main = actual.get('slots', {})
        expected_main = expected.get('main_slots', {})
        
        # サブスロット比較  
        actual_sub = actual.get('sub_slots', {})
        expected_sub = expected.get('sub_slots', {})
        
        # メインスロット照合
        for slot, expected_value in expected_main.items():
            if slot in actual_main:
                if actual_main[slot] == expected_value:
                    comparison['main_slot_matches'][slot] = True
                else:
                    comparison['main_slot_matches'][slot] = False
                    comparison['value_mismatches'].append({
                        'type': 'main',
                        'slot': slot,
                        'expected': expected_value,
                        'actual': actual_main[slot]
                    })
            else:
                comparison['missing_main_slots'].append(slot)
        
        # サブスロット照合
        for slot, expected_value in expected_sub.items():
            if slot in actual_sub:
                if actual_sub[slot] == expected_value:
                    comparison['sub_slot_matches'][slot] = True
                else:
                    comparison['sub_slot_matches'][slot] = False
                    comparison['value_mismatches'].append({
                        'type': 'sub',
                        'slot': slot,
                        'expected': expected_value,
                        'actual': actual_sub[slot]
                    })
            else:
                comparison['missing_sub_slots'].append(slot)
        
        # 総合判定
        if (not comparison['missing_main_slots'] and 
            not comparison['missing_sub_slots'] and 
            not comparison['value_mismatches']):
            comparison['passed'] = True
            comparison['reason'] = 'Perfect match'
        else:
            reasons = []
            if comparison['missing_main_slots']:
                reasons.append(f"欠損メインスロット: {comparison['missing_main_slots']}")
            if comparison['missing_sub_slots']:
                reasons.append(f"欠損サブスロット: {comparison['missing_sub_slots']}")
            if comparison['value_mismatches']:
                mismatches = [f"{m['type']}-{m['slot']}(期待:{m['expected']}→実際:{m['actual']})" 
                             for m in comparison['value_mismatches']]
                reasons.append(f"値不一致: {mismatches}")
            comparison['reason'] = '; '.join(reasons)
        
        return comparison
    
    def _print_phase2_summary(self, results: Dict[str, Any]):
        """Phase 2テスト結果サマリー表示"""
        print("\n" + "=" * 50)
        print("📊 Phase 2 テスト結果サマリー")
        print("=" * 50)
        print(f"総テスト数: {results['total']}")
        print(f"✅ 成功: {results['passed']}")
        print(f"❌ 失敗: {results['failed']}")
        
        if results['total'] > 0:
            success_rate = (results['passed'] / results['total']) * 100
            print(f"🎯 成功率: {success_rate:.1f}%")
            
            if results['failed'] == 0:
                print("🎉 Phase 2 完全達成！")
            elif success_rate >= 80:
                print("⚡ 良好！改善の余地あり")
            else:
                print("🔧 要改善")
            
            # 失敗ケース詳細
            if results['errors']:
                print(f"\n❌ 失敗ケース詳細:")
                for error in results['errors']:
                    print(f"  ケース{error['case_id']}: {error['sentence']}")
                    print(f"    理由: {error['reason']}")


def main():
    """メイン実行関数"""
    test_system = IntegratedTestSystem()
    
    if len(sys.argv) > 1:
        # 引数指定実行
        if sys.argv[1] == 'specific':
            case_ids = [int(x) for x in sys.argv[2:]]
            test_system.run_specific_cases(case_ids)
        elif sys.argv[1] == 'phase1':
            test_system.run_phase1_tests()
        elif sys.argv[1] == 'phase2':
            test_system.run_phase2_tests()
        else:
            print("使用法: python integrated_test_system.py [phase1|phase2|specific case_id1 case_id2 ...]")
    else:
        # デフォルトはPhase 2テスト実行
        test_system.run_phase2_tests()


if __name__ == "__main__":
    main()
