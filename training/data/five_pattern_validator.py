#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5文型Rephrase準拠スロット構造テスト・照合ツール
==================================================

基本5文型のRephrase準拠スロット分解テスト用照合システム
- five_pattern_test_cases.jsonの期待値と実際の出力を比較
- rephrase_slots形式の詳細照合
- 文型別正解率レポート生成

使用法:
    python five_pattern_validator.py
    python five_pattern_validator.py --detail
    python five_pattern_validator.py --pattern SVC
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Tuple
from datetime import datetime

# システムパス追加
sys.path.append('.')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class FivePatternValidator:
    """5文型Rephrase構造照合器"""
    
    def __init__(self, test_cases_file: str = "five_pattern_test_cases.json"):
        self.test_cases_file = test_cases_file
        self.mapper = None
        self.test_cases = []
        self.results = []
        
    def load_test_cases(self):
        """テストケース読み込み"""
        try:
            with open(self.test_cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.test_cases = data['test_cases']
                print(f"✅ テストケース読み込み完了: {len(self.test_cases)}件")
                return True
        except Exception as e:
            print(f"❌ テストケース読み込みエラー: {e}")
            return False
    
    def initialize_mapper(self):
        """UnifiedStanzaRephraseMapper初期化"""
        try:
            print("🔧 UnifiedStanzaRephraseMapper初期化中...")
            self.mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')
            print("✅ 初期化完了")
            return True
        except Exception as e:
            print(f"❌ Mapper初期化エラー: {e}")
            return False
    
    def process_sentence(self, sentence: str) -> Dict:
        """文を処理してrephrase_slots取得"""
        try:
            result = self.mapper.process(sentence)
            return result
        except Exception as e:
            print(f"❌ 文処理エラー '{sentence}': {e}")
            return {}
    
    def compare_rephrase_slots(self, actual_slots: List[Dict], expected_slots: List[Dict]) -> Dict:
        """rephrase_slots詳細比較"""
        comparison = {
            "perfect_match": True,
            "slot_count_match": len(actual_slots) == len(expected_slots),
            "slot_details": [],
            "missing_slots": [],
            "extra_slots": [],
            "position_errors": []
        }
        
        # スロット数チェック
        if not comparison["slot_count_match"]:
            comparison["perfect_match"] = False
            print(f"  ⚠️ スロット数不一致: 実際={len(actual_slots)}, 期待={len(expected_slots)}")
        
        # 位置順でソート
        actual_sorted = sorted(actual_slots, key=lambda x: x.get('Slot_display_order', 0))
        expected_sorted = sorted(expected_slots, key=lambda x: x.get('Slot_display_order', 0))
        
        # 各スロットの詳細比較
        max_len = max(len(actual_sorted), len(expected_sorted))
        
        for i in range(max_len):
            slot_detail = {"position": i + 1}
            
            if i < len(actual_sorted) and i < len(expected_sorted):
                actual_slot = actual_sorted[i]
                expected_slot = expected_sorted[i]
                
                # 重要フィールドの比較
                slot_match = True
                fields_to_compare = ['Slot', 'SlotPhrase', 'Slot_display_order']
                
                for field in fields_to_compare:
                    actual_val = actual_slot.get(field, '')
                    expected_val = expected_slot.get(field, '')
                    
                    field_match = actual_val == expected_val
                    slot_detail[f"{field}_match"] = field_match
                    slot_detail[f"{field}_actual"] = actual_val
                    slot_detail[f"{field}_expected"] = expected_val
                    
                    if not field_match:
                        slot_match = False
                        comparison["perfect_match"] = False
                
                slot_detail["slot_perfect"] = slot_match
                
            elif i < len(actual_sorted):
                # 実際にはあるが期待値にない
                slot_detail["status"] = "extra"
                slot_detail["actual_slot"] = actual_sorted[i]
                comparison["extra_slots"].append(actual_sorted[i])
                comparison["perfect_match"] = False
                
            else:
                # 期待値にはあるが実際にはない
                slot_detail["status"] = "missing"
                slot_detail["expected_slot"] = expected_sorted[i]
                comparison["missing_slots"].append(expected_sorted[i])
                comparison["perfect_match"] = False
            
            comparison["slot_details"].append(slot_detail)
        
        return comparison
    
    def run_single_test(self, test_case: Dict) -> Dict:
        """単一テストケース実行"""
        sentence = test_case['sentence']
        expected_slots = test_case['expected_rephrase_slots']
        pattern = test_case['pattern']
        test_id = test_case['id']
        
        print(f"\n🧪 テスト実行: {test_id} ({pattern})")
        print(f"   文: '{sentence}'")
        
        # システム処理
        result = self.process_sentence(sentence)
        actual_slots = result.get('rephrase_slots', [])
        
        # 比較実行
        comparison = self.compare_rephrase_slots(actual_slots, expected_slots)
        
        # 結果記録
        test_result = {
            "test_id": test_id,
            "pattern": pattern,
            "sentence": sentence,
            "success": comparison["perfect_match"],
            "comparison": comparison,
            "actual_slots": actual_slots,
            "expected_slots": expected_slots
        }
        
        # 結果表示
        if comparison["perfect_match"]:
            print(f"   ✅ 完全一致")
        else:
            print(f"   ❌ 不一致検出")
            if not comparison["slot_count_match"]:
                print(f"      - スロット数: 実際={len(actual_slots)} vs 期待={len(expected_slots)}")
            for detail in comparison["slot_details"]:
                if not detail.get("slot_perfect", True):
                    pos = detail["position"]
                    print(f"      - Position {pos}: スロット不一致")
        
        return test_result
    
    def run_all_tests(self, target_pattern: str = None) -> Dict:
        """全テスト実行"""
        print("🚀 5文型Rephrase準拠スロット構造テスト開始")
        print("=" * 60)
        
        # フィルタリング
        target_cases = self.test_cases
        if target_pattern:
            target_cases = [case for case in self.test_cases if case['pattern'] == target_pattern]
            print(f"🎯 対象文型: {target_pattern} ({len(target_cases)}件)")
        
        # 各テスト実行
        results = []
        for test_case in target_cases:
            result = self.run_single_test(test_case)
            results.append(result)
        
        # 統計分析
        stats = self.analyze_results(results)
        self.print_summary(stats)
        
        return {
            "results": results,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """結果統計分析"""
        total = len(results)
        success_count = sum(1 for r in results if r['success'])
        
        # 文型別統計
        pattern_stats = {}
        for result in results:
            pattern = result['pattern']
            if pattern not in pattern_stats:
                pattern_stats[pattern] = {"total": 0, "success": 0}
            
            pattern_stats[pattern]["total"] += 1
            if result['success']:
                pattern_stats[pattern]["success"] += 1
        
        # 成功率計算
        for pattern in pattern_stats:
            stats = pattern_stats[pattern]
            stats["success_rate"] = stats["success"] / stats["total"] * 100
        
        return {
            "total_tests": total,
            "successful_tests": success_count,
            "overall_success_rate": success_count / total * 100 if total > 0 else 0,
            "pattern_statistics": pattern_stats
        }
    
    def print_summary(self, stats: Dict):
        """結果サマリー表示"""
        print("\n" + "=" * 60)
        print("📊 テスト結果サマリー")
        print("=" * 60)
        
        total = stats["total_tests"]
        success = stats["successful_tests"]
        rate = stats["overall_success_rate"]
        
        print(f"総テスト数: {total}")
        print(f"成功数: {success}")
        print(f"全体成功率: {rate:.1f}%")
        
        print(f"\n📈 文型別詳細:")
        for pattern, pattern_stats in stats["pattern_statistics"].items():
            p_total = pattern_stats["total"]
            p_success = pattern_stats["success"]
            p_rate = pattern_stats["success_rate"]
            print(f"  {pattern:>5}: {p_success:>2}/{p_total:>2} ({p_rate:>5.1f}%)")
        
        # 全体評価
        print(f"\n🎯 評価:")
        if rate >= 95:
            print("  🥇 優秀 - システム実装完了レベル")
        elif rate >= 80:
            print("  🥈 良好 - 微調整で完成")
        elif rate >= 60:
            print("  🥉 改善要 - 追加実装必要")
        else:
            print("  ❌ 要修正 - 根本的見直し必要")

def main():
    parser = argparse.ArgumentParser(description='5文型Rephrase準拠スロット構造テスト')
    parser.add_argument('--pattern', type=str, help='特定文型のテスト (SV, SVC, SVO, SVOO, SVOC)')
    parser.add_argument('--detail', action='store_true', help='詳細結果表示')
    
    args = parser.parse_args()
    
    # バリデーター初期化
    validator = FivePatternValidator()
    
    # テストケース読み込み
    if not validator.load_test_cases():
        return 1
    
    # Mapper初期化
    if not validator.initialize_mapper():
        return 1
    
    # テスト実行
    try:
        results = validator.run_all_tests(target_pattern=args.pattern)
        
        # 詳細表示
        if args.detail:
            print("\n" + "=" * 60)
            print("🔍 詳細結果")
            print("=" * 60)
            for result in results["results"]:
                print(f"\n{result['test_id']}: {result['sentence']}")
                if result['success']:
                    print("  ✅ 完全一致")
                else:
                    print("  ❌ 不一致詳細:")
                    comp = result['comparison']
                    for detail in comp['slot_details']:
                        if not detail.get('slot_perfect', True):
                            pos = detail['position']
                            print(f"    Position {pos}:")
                            for key, val in detail.items():
                                if key.endswith('_expected') or key.endswith('_actual'):
                                    print(f"      {key}: {val}")
        
        return 0
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
