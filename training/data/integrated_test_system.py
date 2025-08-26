"""
統合テストシステム - Phase 1対応
final_54_test_data.json使用の例文選択→期待値照合システム

機能:
1. 文法別例文フィルタリング
2. 新規システムでの処理実行
3. 期待値との照合
4. 詳細な結果分析
5. 一本化された実行フロー
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


def main():
    """メイン実行関数"""
    test_system = IntegratedTestSystem()
    
    if len(sys.argv) > 1:
        # 引数指定実行
        if sys.argv[1] == 'specific':
            case_ids = [int(x) for x in sys.argv[2:]]
            test_system.run_specific_cases(case_ids)
        else:
            print("使用法: python integrated_test_system.py [specific case_id1 case_id2 ...]")
    else:
        # 全Phase1テスト実行
        test_system.run_phase1_tests()


if __name__ == "__main__":
    main()
