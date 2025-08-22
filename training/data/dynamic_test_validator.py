#!/usr/bin/env python3
"""
動的文法認識システム テスト検証ツール
========================================

機能:
1. 53例文の完全テスト実行と結果照合
2. 文法項目別の部分テスト機能
3. 詳細な精度分析とレポート生成
4. 期待値との差分表示

使用法:
    python dynamic_test_validator.py --full              # 全テスト
    python dynamic_test_validator.py --grammar svc       # SVC文型のみ
    python dynamic_test_validator.py --grammar relative  # 関係詞のみ
    python dynamic_test_validator.py --compare results.json  # 結果照合
"""

import json
import argparse
import os
import sys
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass

@dataclass
class TestResult:
    """テスト結果データクラス"""
    test_id: str
    sentence: str
    expected: Dict[str, Any]
    actual: Dict[str, Any]
    status: str
    accuracy_score: float
    differences: List[str]

class DynamicTestValidator:
    """動的文法認識システムのテスト検証クラス"""
    
    def __init__(self, test_data_path: str = None):
        """初期化"""
        if test_data_path is None:
            test_data_path = os.path.join(
                os.path.dirname(__file__),
                "final_test_system",
                "final_54_test_data.json"
            )
        
        self.test_data_path = test_data_path
        self.test_data = self._load_test_data()
        
        # 文法項目別の例文IDマッピング
        self.grammar_categories = {
            "svc": [1, 3, 4, 5, 15, 16, 17, 18, 19, 58, 59, 60],  # SVC文型
            "svo": [2, 6, 7, 8, 20, 36, 44, 45, 61, 62, 63],      # SVO文型
            "svoo": [64, 65, 66],                                  # SVOO文型（シンプルのみ）
            "svoo_complex": [46, 47],                              # SVOO文型（複雑構文）
            "svoc": [67, 68, 69],                                  # SVOC文型（シンプルのみ）
            "svoc_complex": [48, 49],                              # SVOC文型（複雑構文）
            "sv": [55, 56, 57],                                    # SV文型（新規）
            "basic_patterns": [1, 2, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69],  # 基本5文型（全て）
            "relative": [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19],  # 関係詞
            "passive": [9, 10, 11, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33],  # 受動態
            "complex": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],     # 複雑構文
            "basic": [1, 2, 20, 29, 44, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63],  # 基本文型
            "auxiliary": [20, 24, 35, 38, 43, 46, 52, 53],  # 助動詞含む
            "modifier": [29, 34, 36, 37, 38, 39, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51]  # 修飾語多数
        }
    
    def _load_test_data(self) -> Dict[str, Any]:
        """テストデータを読み込む"""
        try:
            with open(self.test_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ テストデータファイルが見つかりません: {self.test_data_path}")
            return {}
    
    def run_test_category(self, category: str) -> List[TestResult]:
        """
        特定の文法項目カテゴリーのテストを実行
        
        Args:
            category: 文法項目カテゴリー名
            
        Returns:
            List[TestResult]: テスト結果リスト
        """
        if category not in self.grammar_categories:
            print(f"❌ 未知のカテゴリー: {category}")
            print(f"利用可能カテゴリー: {list(self.grammar_categories.keys())}")
            return []
        
        test_ids = self.grammar_categories[category]
        return self._run_selected_tests(test_ids, f"{category}文法項目")
    
    def run_full_test(self) -> List[TestResult]:
        """全53例文のテストを実行"""
        all_ids = list(self.test_data["data"].keys())
        test_ids = [int(tid) for tid in all_ids]
        return self._run_selected_tests(test_ids, "全例文")
    
    def _run_selected_tests(self, test_ids: List[int], category_name: str) -> List[TestResult]:
        """
        選択された例文のテストを実行
        
        Args:
            test_ids: テストするIDリスト
            category_name: カテゴリー名
            
        Returns:
            List[TestResult]: テスト結果リスト
        """
        from dynamic_grammar_mapper import DynamicGrammarMapper
        
        mapper = DynamicGrammarMapper()
        results = []
        
        print(f"\n=== {category_name}テスト実行 ({len(test_ids)}例文) ===\n")
        
        for test_id in test_ids:
            test_id_str = str(test_id)
            
            if test_id_str not in self.test_data["data"]:
                print(f"⚠️  テストID {test_id} が見つかりません")
                continue
            
            test_case = self.test_data["data"][test_id_str]
            sentence = test_case["sentence"]
            expected = test_case["expected"]
            
            print(f"テスト {test_id}: {sentence}")
            
            try:
                actual = mapper.analyze_sentence(sentence)
                
                # 結果を比較・評価
                result = self._compare_results(test_id_str, sentence, expected, actual)
                results.append(result)
                
                # 結果表示
                if result.status == "SUCCESS":
                    print(f"✅ 成功 (精度: {result.accuracy_score:.1f}%)")
                elif result.status == "PARTIAL":
                    print(f"🔶 部分的成功 (精度: {result.accuracy_score:.1f}%)")
                    for diff in result.differences:
                        print(f"   差分: {diff}")
                else:
                    print(f"❌ 失敗: {result.differences[0] if result.differences else '不明なエラー'}")
                
            except Exception as e:
                result = TestResult(
                    test_id=test_id_str,
                    sentence=sentence,
                    expected=expected,
                    actual={"error": str(e)},
                    status="ERROR",
                    accuracy_score=0.0,
                    differences=[f"例外エラー: {str(e)}"]
                )
                results.append(result)
                print(f"❌ 例外エラー: {str(e)}")
            
            print("-" * 60)
        
        # 結果サマリー表示
        self._print_summary(results, category_name)
        return results
    
    def _compare_results(self, test_id: str, sentence: str, expected: Dict, actual: Dict) -> TestResult:
        """
        期待値と実際の結果を比較
        
        Args:
            test_id: テストID
            sentence: テスト文
            expected: 期待値
            actual: 実際の結果
            
        Returns:
            TestResult: 比較結果
        """
        differences = []
        
        # エラーチェック
        if "error" in actual:
            return TestResult(
                test_id=test_id,
                sentence=sentence,
                expected=expected,
                actual=actual,
                status="ERROR",
                accuracy_score=0.0,
                differences=[f"処理エラー: {actual['error']}"]
            )
        
        # 実際の結果をRephrase形式に変換
        actual_rephrase = self._convert_to_rephrase_format(actual)
        
        # メインスロットの比較
        main_matches = 0
        main_total = len(expected.get("main_slots", {}))
        
        expected_main = expected.get("main_slots", {})
        actual_main = actual_rephrase.get("main_slots", {})
        
        for slot, exp_value in expected_main.items():
            if slot in actual_main:
                if self._normalize_text(actual_main[slot]) == self._normalize_text(exp_value):
                    main_matches += 1
                else:
                    differences.append(f"メインスロット {slot}: 期待「{exp_value}」→ 実際「{actual_main[slot]}」")
            else:
                differences.append(f"メインスロット {slot}: 期待「{exp_value}」→ 実際「なし」")
        
        # サブスロットの比較
        sub_matches = 0
        sub_total = len(expected.get("sub_slots", {}))
        
        expected_sub = expected.get("sub_slots", {})
        actual_sub = actual_rephrase.get("sub_slots", {})
        
        for slot, exp_value in expected_sub.items():
            if slot in actual_sub:
                if self._normalize_text(actual_sub[slot]) == self._normalize_text(exp_value):
                    sub_matches += 1
                else:
                    differences.append(f"サブスロット {slot}: 期待「{exp_value}」→ 実際「{actual_sub[slot]}」")
            else:
                differences.append(f"サブスロット {slot}: 期待「{exp_value}」→ 実際「なし」")
        
        # 精度計算
        total_slots = main_total + sub_total
        total_matches = main_matches + sub_matches
        
        if total_slots == 0:
            accuracy_score = 100.0
        else:
            accuracy_score = (total_matches / total_slots) * 100
        
        # ステータス決定
        if accuracy_score >= 100:
            status = "SUCCESS"
        elif accuracy_score >= 50:
            status = "PARTIAL"
        else:
            status = "FAILURE"
        
        return TestResult(
            test_id=test_id,
            sentence=sentence,
            expected=expected,
            actual=actual_rephrase,  # 🔧 見やすい形式で保存
            status=status,
            accuracy_score=accuracy_score,
            differences=differences
        )
    
    def _convert_to_rephrase_format(self, result: Dict) -> Dict[str, Any]:
        """
        動的システムの結果をRephrase形式に変換
        
        Args:
            result: 動的システムの結果
            
        Returns:
            Dict: Rephrase形式の結果
        """
        # 🔧 動的システムが既にmain_slotsを出力している場合は直接使用
        if "main_slots" in result:
            return {
                "main_slots": result["main_slots"],
                "sub_slots": result.get("sub_slots", {})
            }
        
        # 従来の変換ロジック（古いシステム用）
        rephrase_format = {
            "main_slots": {},
            "sub_slots": {}
        }
        
        # スロットとフレーズを対応付け
        slots = result.get("Slot", [])
        phrases = result.get("SlotPhrase", [])
        
        for i, slot in enumerate(slots):
            if i < len(phrases):
                phrase = phrases[i]
                
                # スロット名をRephrase形式に変換
                if slot == "S":
                    rephrase_format["main_slots"]["S"] = phrase
                elif slot == "V":
                    rephrase_format["main_slots"]["V"] = phrase
                elif slot == "O":
                    rephrase_format["main_slots"]["O1"] = phrase
                elif slot == "O1":  # 🔧 O1も処理
                    rephrase_format["main_slots"]["O1"] = phrase
                elif slot == "C":
                    rephrase_format["main_slots"]["C1"] = phrase
                elif slot == "C1":  # 🔧 C1も処理
                    rephrase_format["main_slots"]["C1"] = phrase
                elif slot == "C2":  # 🔧 C2も処理
                    rephrase_format["main_slots"]["C2"] = phrase
                elif slot == "Aux":
                    rephrase_format["main_slots"]["Aux"] = phrase
                elif slot.startswith("M"):
                    # 修飾語をそのまま使用
                    rephrase_format["main_slots"][slot] = phrase
        
        return rephrase_format
    
    def _normalize_text(self, text: str) -> str:
        """テキストを正規化"""
        if not text:
            return ""
        return text.strip().lower()
    
    def _print_summary(self, results: List[TestResult], category_name: str):
        """結果サマリーを表示"""
        total = len(results)
        success = len([r for r in results if r.status == "SUCCESS"])
        partial = len([r for r in results if r.status == "PARTIAL"])
        failure = len([r for r in results if r.status == "FAILURE"])
        error = len([r for r in results if r.status == "ERROR"])
        
        avg_accuracy = sum(r.accuracy_score for r in results) / total if total > 0 else 0
        
        print(f"\n=== {category_name}テスト結果サマリー ===")
        print(f"📊 総テスト数: {total}")
        print(f"✅ 完全成功: {success} ({success/total*100:.1f}%)")
        print(f"🔶 部分成功: {partial} ({partial/total*100:.1f}%)")
        print(f"❌ 失敗: {failure} ({failure/total*100:.1f}%)")
        print(f"🚫 エラー: {error} ({error/total*100:.1f}%)")
        print(f"🎯 平均精度: {avg_accuracy:.1f}%")
    
    def save_results(self, results: List[TestResult], output_path: str = None) -> str:
        """結果をJSONファイルに保存"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"dynamic_test_validation_{timestamp}.json"
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "validator": "dynamic_test_validator",
            "total_tests": len(results),
            "results": []
        }
        
        for result in results:
            output_data["results"].append({
                "test_id": result.test_id,
                "sentence": result.sentence,
                "expected": result.expected,
                "actual": result.actual,
                "status": result.status,
                "accuracy_score": result.accuracy_score,
                "differences": result.differences
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 検証結果を保存しました: {output_path}")
        return output_path

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="動的文法認識システム テスト検証ツール")
    parser.add_argument("--full", action="store_true", help="全53例文テスト")
    parser.add_argument("--grammar", type=str, help="文法項目別テスト (svc, svo, relative, passive, etc.)")
    parser.add_argument("--compare", type=str, help="結果ファイルの照合")
    parser.add_argument("--save", type=str, help="結果保存先ファイル名")
    parser.add_argument("--list-categories", action="store_true", help="利用可能な文法カテゴリーを表示")
    
    args = parser.parse_args()
    
    validator = DynamicTestValidator()
    
    if args.list_categories:
        print("利用可能な文法カテゴリー:")
        for category, test_ids in validator.grammar_categories.items():
            print(f"  {category}: {len(test_ids)}例文 (ID: {test_ids})")
        return
    
    results = []
    
    if args.full:
        results = validator.run_full_test()
    elif args.grammar:
        results = validator.run_test_category(args.grammar)
    elif args.compare:
        # TODO: 結果ファイルの照合機能を実装
        print("結果ファイル照合機能は未実装です")
        return
    else:
        # デフォルト: 基本文型テスト
        results = validator.run_test_category("basic")
    
    # 結果保存
    if results:
        output_path = args.save if args.save else None
        validator.save_results(results, output_path)

if __name__ == "__main__":
    main()
