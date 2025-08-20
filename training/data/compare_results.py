#!/usr/bin/env python3
"""
結果照合ツール v1.0
==================

バッチ処理結果の精度分析用独立スクリプト
- unified_stanza_rephrase_mapper.py の結果ファイルを解析
- 期待値との照合
- 詳細な精度レポート生成

使用法:
    python compare_results.py --results batch_results_20250817_143022.json
    python compare_results.py --results batch_results.json --detail
"""

import json
import argparse
from typing import Dict, List, Any, Tuple
from datetime import datetime

def normalize_slot_data(data: Any) -> Dict[str, Any]:
    """
    スロットデータを統一形式に正規化
    
    flat形式 {"S": "...", "V": "...", "O1": "..."} 
    ↓
    nested形式 {"main_slots": {"S": "...", "V": "...", "O1": "..."}, "sub_slots": {...}}
    """
    if isinstance(data, dict):
        # すでにnested形式の場合（expected値）
        if "main_slots" in data and "sub_slots" in data:
            return data
        
        # flat形式をnested形式に変換（actual値）
        if "slots" in data and "sub_slots" in data:
            # システム出力形式: {"slots": {...}, "sub_slots": {...}}
            return {
                "main_slots": data.get("slots", {}),
                "sub_slots": data.get("sub_slots", {})
            }
        
        # 直接スロット形式の場合
        main_slots = {}
        sub_slots = {}
        
        for key, value in data.items():
            if key.startswith("sub-"):
                sub_slots[key] = value
            elif key in ["S", "V", "O1", "O2", "C1", "C2", "Aux", "M1", "M2", "M3", "Adv"]:
                main_slots[key] = value
        
        return {
            "main_slots": main_slots,
            "sub_slots": sub_slots
        }
    
    return {"main_slots": {}, "sub_slots": {}}

def compare_slots(actual: Dict[str, Any], expected: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    スロット比較
    
    Returns:
        (完全一致フラグ, 詳細分析)
    """
    # 正規化
    actual_norm = normalize_slot_data(actual)
    expected_norm = normalize_slot_data(expected)
    
    # 詳細分析用
    analysis = {
        "main_slots_match": {},
        "sub_slots_match": {},
        "main_perfect": True,
        "sub_perfect": True,
        "overall_perfect": False
    }
    
    # メインスロット比較
    actual_main = actual_norm.get("main_slots", {})
    expected_main = expected_norm.get("main_slots", {})
    
    all_main_keys = set(actual_main.keys()) | set(expected_main.keys())
    
    for key in all_main_keys:
        # 存在しないスロットと空文字スロットを区別
        actual_exists = key in actual_main
        expected_exists = key in expected_main
        
        if actual_exists and expected_exists:
            # 両方存在する場合は値を比較
            actual_val = actual_main[key]
            expected_val = expected_main[key]
            match = actual_val == expected_val
        elif not actual_exists and not expected_exists:
            # 両方存在しない場合は一致
            actual_val = "(not present)"
            expected_val = "(not present)"
            match = True
        else:
            # 一方のみ存在する場合は不一致
            actual_val = actual_main[key] if actual_exists else "(not present)"
            expected_val = expected_main[key] if expected_exists else "(not present)"
            match = False
        
        analysis["main_slots_match"][key] = {
            "actual": actual_val,
            "expected": expected_val,
            "match": match
        }
        
        if not match:
            analysis["main_perfect"] = False
    
    # サブスロット比較
    actual_sub = actual_norm.get("sub_slots", {})
    expected_sub = expected_norm.get("sub_slots", {})
    
    all_sub_keys = set(actual_sub.keys()) | set(expected_sub.keys())
    
    for key in all_sub_keys:
        # 存在しないスロットと空文字スロットを区別
        actual_exists = key in actual_sub
        expected_exists = key in expected_sub
        
        if actual_exists and expected_exists:
            # 両方存在する場合は値を比較
            actual_val = actual_sub[key]
            expected_val = expected_sub[key]
            match = actual_val == expected_val
        elif not actual_exists and not expected_exists:
            # 両方存在しない場合は一致
            actual_val = "(not present)"
            expected_val = "(not present)"
            match = True
        else:
            # 一方のみ存在する場合は不一致
            actual_val = actual_sub[key] if actual_exists else "(not present)"
            expected_val = expected_sub[key] if expected_exists else "(not present)"
            match = False
        
        analysis["sub_slots_match"][key] = {
            "actual": actual_val,
            "expected": expected_val,
            "match": match
        }
        
        if not match:
            analysis["sub_perfect"] = False
    
    # 全体判定
    analysis["overall_perfect"] = analysis["main_perfect"] and analysis["sub_perfect"]
    
    return analysis["overall_perfect"], analysis

def analyze_results(results_file: str, show_details: bool = False) -> Dict[str, Any]:
    """
    結果ファイルの精度分析
    """
    print(f"📊 結果解析開始: {results_file}")
    
    # 結果ファイル読み込み
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 結果ファイルが見つかりません: {results_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        return None
    
    # 期待値ファイルも読み込み（results_fileに期待値がない場合のため）
    expected_data = {}
    expected_file = "final_test_system/final_54_test_data.json"
    try:
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_file_data = json.load(f)
            expected_data = expected_file_data.get("data", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ 期待値ファイル読み込み失敗: {expected_file}")
    
    # 分析結果格納
    analysis_report = {
        "meta": {
            "analyzed_at": datetime.now().isoformat(),
            "source_file": results_file,
            "total_cases": 0,
            "perfect_matches": 0,
            "partial_matches": 0,
            "failures": 0,
            "accuracy": 0.0
        },
        "case_details": {},
        "error_summary": {},
        "slot_analysis": {
            "main_slot_accuracy": {},
            "sub_slot_accuracy": {}
        }
    }
    
    results = results_data.get("results", {})
    analysis_report["meta"]["total_cases"] = len(results)
    
    # 各テストケース分析
    slot_stats = {}
    
    for test_id, result in results.items():
        if result["status"] != "success":
            analysis_report["meta"]["failures"] += 1
            continue
        
        # 期待値取得 (results内 または expected_data から)
        expected = result.get("expected", {})
        if not expected and test_id in expected_data:
            expected = expected_data[test_id].get("expected", {})
        
        # 実際の結果取得 (analysis_result または slots/sub_slots から直接)
        actual = result.get("analysis_result", {})
        if not actual:
            # analysis_resultがnullの場合、結果を再処理
            print(f"⚠️ Test[{test_id}]: analysis_result is null, attempting direct processing...")
            continue
        
        if not expected:
            # 期待値がない場合はスキップ
            print(f"⚠️ Test[{test_id}]: No expected data found")
            continue
        
        # スロット比較実行
        is_perfect, detail_analysis = compare_slots(actual, expected)
        
        if is_perfect:
            analysis_report["meta"]["perfect_matches"] += 1
        else:
            analysis_report["meta"]["partial_matches"] += 1
        
        # 詳細記録
        analysis_report["case_details"][test_id] = {
            "sentence": result["sentence"],
            "perfect_match": is_perfect,
            "analysis": detail_analysis
        }
        
        # スロット統計更新
        for slot_name, slot_info in detail_analysis["main_slots_match"].items():
            if slot_name not in slot_stats:
                slot_stats[slot_name] = {"correct": 0, "total": 0}
            slot_stats[slot_name]["total"] += 1
            if slot_info["match"]:
                slot_stats[slot_name]["correct"] += 1
    
    # 精度計算
    valid_cases = analysis_report["meta"]["perfect_matches"] + analysis_report["meta"]["partial_matches"]
    if valid_cases > 0:
        analysis_report["meta"]["accuracy"] = (analysis_report["meta"]["perfect_matches"] / valid_cases) * 100
    
    # スロット別精度
    for slot_name, stats in slot_stats.items():
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            analysis_report["slot_analysis"]["main_slot_accuracy"][slot_name] = {
                "accuracy": accuracy,
                "correct": stats["correct"],
                "total": stats["total"]
            }
    
    return analysis_report

def print_analysis_report(report: Dict[str, Any], show_details: bool = False):
    """
    分析レポート表示
    """
    meta = report["meta"]
    
    print("\n" + "="*60)
    print("📊 精度分析レポート")
    print("="*60)
    print(f"📁 対象ファイル: {meta['source_file']}")
    print(f"⏰ 分析時刻: {meta['analyzed_at']}")
    print()
    print(f"📈 全体統計:")
    print(f"   総ケース数: {meta['total_cases']}")
    print(f"   完全一致: {meta['perfect_matches']}")
    print(f"   部分一致: {meta['partial_matches']}")
    print(f"   失敗: {meta['failures']}")
    print(f"   🎯 完全一致率: {meta['accuracy']:.1f}%")
    
    # スロット別精度
    if report["slot_analysis"]["main_slot_accuracy"]:
        print(f"\n🔍 スロット別精度:")
        for slot_name, stats in sorted(report["slot_analysis"]["main_slot_accuracy"].items()):
            print(f"   {slot_name}: {stats['accuracy']:.1f}% ({stats['correct']}/{stats['total']})")
    
    # 詳細表示
    if show_details:
        print(f"\n📝 詳細分析:")
        for test_id, detail in report["case_details"].items():
            if not detail["perfect_match"]:
                print(f"\n❌ [{test_id}] {detail['sentence']}")
                analysis = detail["analysis"]
                
                for slot_name, slot_info in analysis["main_slots_match"].items():
                    if not slot_info["match"]:
                        print(f"   {slot_name}: '{slot_info['actual']}' ≠ '{slot_info['expected']}'")

def main():
    parser = argparse.ArgumentParser(
        description="結果照合ツール - バッチ処理結果の精度分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な精度チェック
  python compare_results.py --results batch_results_20250817_143022.json
  
  # 詳細分析（失敗ケース表示）
  python compare_results.py --results batch_results.json --detail
  
  # レポートファイル保存
  python compare_results.py --results batch_results.json --save-report accuracy_report.json
        """
    )
    
    parser.add_argument(
        '--results', '-r',
        required=True,
        help='バッチ処理結果ファイル (JSON)'
    )
    
    parser.add_argument(
        '--detail', '-d',
        action='store_true',
        help='詳細分析表示（失敗ケース詳細）'
    )
    
    parser.add_argument(
        '--save-report', '-s',
        help='分析レポートを指定ファイルに保存'
    )
    
    args = parser.parse_args()
    
    # 分析実行
    report = analyze_results(args.results, args.detail)
    
    if report is None:
        print("❌ 分析に失敗しました")
        exit(1)
    
    # レポート表示
    print_analysis_report(report, args.detail)
    
    # レポート保存
    if args.save_report:
        try:
            with open(args.save_report, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 レポート保存: {args.save_report}")
        except Exception as e:
            print(f"\n❌ レポート保存エラー: {e}")
    
    print(f"\n🎯 完全一致率: {report['meta']['accuracy']:.1f}%")

if __name__ == "__main__":
    main()
