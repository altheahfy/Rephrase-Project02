#!/usr/bin/env python3
"""
人間文法認識結果比較ツール
========================

人間文法認識システムの53例文テスト結果を期待値と比較し、
詳細な精度分析レポートを生成します。

使用法:
    python compare_human_grammar_results.py
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

def normalize_slot_data(data: Any) -> Dict[str, Any]:
    """
    スロットデータを統一形式に正規化
    """
    if isinstance(data, dict):
        # すでにnested形式の場合（expected値）
        if "main_slots" in data and "sub_slots" in data:
            return data
        
        # システム出力形式の場合
        if "main_slots" in data:
            return {
                "main_slots": data.get("main_slots", {}),
                "sub_slots": data.get("sub_slots", {})
            }
        
        # flat形式をnested形式に変換
        main_slots = {}
        sub_slots = {}
        
        for key, value in data.items():
            if key.startswith("sub-"):
                sub_slots[key] = value
            elif key in ["S", "V", "O1", "O2", "C1", "C2", "Aux", "M1", "M2", "M3", "Adv"]:
                main_slots[key] = value
                
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    return {"main_slots": {}, "sub_slots": {}}

def normalize_value(value: str) -> str:
    """値の正規化"""
    if not value:
        return ""
    return str(value).strip()

def compare_slots(actual: Dict[str, str], expected: Dict[str, str], slot_type: str) -> Tuple[bool, List[str]]:
    """スロットの比較"""
    errors = []
    
    # 期待値の全スロットをチェック
    for slot, expected_value in expected.items():
        actual_value = actual.get(slot, "")
        
        expected_norm = normalize_value(expected_value)
        actual_norm = normalize_value(actual_value)
        
        if expected_norm != actual_norm:
            errors.append(f"{slot_type}[{slot}]: 期待値='{expected_norm}', 実際値='{actual_norm}'")
    
    # 実際値に余分なスロットがあるかチェック
    for slot, actual_value in actual.items():
        if slot not in expected and normalize_value(actual_value):
            errors.append(f"{slot_type}[{slot}]: 予期しない値='{normalize_value(actual_value)}'")
    
    return len(errors) == 0, errors

def compare_human_grammar_results():
    """人間文法認識の結果を期待値と比較"""
    
    print("=" * 80)
    print("🧠 人間文法認識システム結果比較分析")
    print("=" * 80)
    
    # ファイルパス設定
    project_root = Path(__file__).parent
    results_file = project_root / "human_grammar_test_results.json"
    expected_file = project_root / "final_test_system" / "final_54_test_data.json"
    
    # 結果ファイルの存在確認
    if not results_file.exists():
        print(f"❌ 結果ファイルが見つかりません: {results_file}")
        print("   先にhuman_grammar_53_test.pyを実行してください。")
        return
    
    if not expected_file.exists():
        print(f"❌ 期待値ファイルが見つかりません: {expected_file}")
        return
    
    # データ読み込み
    with open(results_file, 'r', encoding='utf-8') as f:
        results_data = json.load(f)
    
    with open(expected_file, 'r', encoding='utf-8') as f:
        expected_data = json.load(f)
    
    results = results_data['results']
    expected_dict = {case['sentence']: case for case in expected_data['data'].values()}
    
    print(f"📊 比較対象: {len(results)}文")
    print(f"📊 期待値データ: {len(expected_dict)}文")
    print()
    
    # 比較処理
    total_count = 0
    perfect_matches = 0
    main_slot_errors = 0
    sub_slot_errors = 0
    missing_sentences = 0
    
    detailed_results = []
    
    for result in results:
        sentence = result['sentence']
        total_count += 1
        
        if sentence not in expected_dict:
            print(f"⚠️  期待値なし: {sentence}")
            missing_sentences += 1
            continue
        
        expected = expected_dict[sentence]['expected']
        
        # 実際値と期待値を正規化
        actual_norm = normalize_slot_data(result)
        expected_norm = normalize_slot_data(expected)
        
        # 主節スロット比較
        main_match, main_errors = compare_slots(
            actual_norm['main_slots'], 
            expected_norm['main_slots'], 
            "主節"
        )
        
        # 関係節スロット比較
        sub_match, sub_errors = compare_slots(
            actual_norm['sub_slots'], 
            expected_norm['sub_slots'], 
            "関係節"
        )
        
        # 完全一致判定
        is_perfect = main_match and sub_match
        
        if is_perfect:
            perfect_matches += 1
        else:
            if not main_match:
                main_slot_errors += 1
            if not sub_match:
                sub_slot_errors += 1
        
        # 詳細結果記録
        detailed_results.append({
            'sentence': sentence,
            'perfect_match': is_perfect,
            'main_match': main_match,
            'sub_match': sub_match,
            'main_errors': main_errors,
            'sub_errors': sub_errors,
            'actual_main': actual_norm['main_slots'],
            'expected_main': expected_norm['main_slots'],
            'actual_sub': actual_norm['sub_slots'],
            'expected_sub': expected_norm['sub_slots'],
            'processing_time': result.get('processing_time', 0),
            'has_error': 'error' in result
        })
    
    # 統計情報出力
    print("=" * 80)
    print("📈 分析結果サマリー")
    print("=" * 80)
    
    accuracy = (perfect_matches / total_count * 100) if total_count > 0 else 0
    print(f"✅ 完全一致: {perfect_matches}/{total_count} ({accuracy:.1f}%)")
    print(f"❌ 主節エラー: {main_slot_errors}/{total_count} ({main_slot_errors/total_count*100:.1f}%)")
    print(f"❌ 関係節エラー: {sub_slot_errors}/{total_count} ({sub_slot_errors/total_count*100:.1f}%)")
    
    if missing_sentences > 0:
        print(f"⚠️  期待値不明: {missing_sentences}文")
    
    # エラー文の詳細表示
    error_cases = [r for r in detailed_results if not r['perfect_match']]
    
    if error_cases:
        print()
        print("=" * 80)
        print("🔍 エラー文詳細分析")
        print("=" * 80)
        
        for i, case in enumerate(error_cases[:10], 1):  # 最初の10件のみ表示
            print(f"\n【エラー {i}】 {case['sentence']}")
            
            if case['main_errors']:
                print("  主節エラー:")
                for error in case['main_errors']:
                    print(f"    • {error}")
            
            if case['sub_errors']:
                print("  関係節エラー:")
                for error in case['sub_errors']:
                    print(f"    • {error}")
            
            if case['has_error']:
                print("  ⚠️ システムエラーあり")
        
        if len(error_cases) > 10:
            print(f"\n... 他{len(error_cases) - 10}件のエラーあり")
    
    # パフォーマンス統計
    processing_times = [r['processing_time'] for r in detailed_results if not r['has_error']]
    if processing_times:
        avg_time = sum(processing_times) / len(processing_times)
        max_time = max(processing_times)
        min_time = min(processing_times)
        
        print()
        print("=" * 80)
        print("⏱️  パフォーマンス統計")
        print("=" * 80)
        print(f"平均処理時間: {avg_time:.4f}秒")
        print(f"最大処理時間: {max_time:.4f}秒")
        print(f"最小処理時間: {min_time:.4f}秒")
    
    # スロット分解状況分析
    print()
    print("=" * 80)
    print("🎯 スロット分解状況分析")
    print("=" * 80)
    
    has_main_slots = sum(1 for r in detailed_results if r['actual_main'])
    has_sub_slots = sum(1 for r in detailed_results if r['actual_sub'])
    no_slots = sum(1 for r in detailed_results if not r['actual_main'] and not r['actual_sub'])
    
    print(f"主節スロット検出: {has_main_slots}/{total_count} ({has_main_slots/total_count*100:.1f}%)")
    print(f"関係節スロット検出: {has_sub_slots}/{total_count} ({has_sub_slots/total_count*100:.1f}%)")
    print(f"スロット未検出: {no_slots}/{total_count} ({no_slots/total_count*100:.1f}%)")
    
    # 推奨改善策
    print()
    print("=" * 80)
    print("💡 推奨改善策")
    print("=" * 80)
    
    if accuracy < 50:
        print("🔴 重大: 精度が50%未満です")
        print("   • 基本5文型の人間文法認識ハンドラーの実装が必要")
        print("   • 現在の3ハンドラーでは対応範囲が限定的")
    elif accuracy < 80:
        print("🟡 注意: 精度改善の余地があります")
        print("   • 特定の文型パターンの認識精度向上")
        print("   • エラーケースの詳細分析と対策")
    else:
        print("🟢 良好: 人間文法認識システムは期待通りに動作しています")
    
    if no_slots > total_count * 0.5:
        print("   • パターン検出範囲の拡張が急務")
        print("   • 基本文型ハンドラーの優先実装を推奨")
    
    # 結果ファイル出力
    report_file = project_root / f"human_grammar_comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report_data = {
        'meta': {
            'comparison_timestamp': datetime.now().isoformat(),
            'total_sentences': total_count,
            'perfect_matches': perfect_matches,
            'accuracy_percentage': accuracy,
            'main_slot_errors': main_slot_errors,
            'sub_slot_errors': sub_slot_errors
        },
        'detailed_results': detailed_results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 詳細レポート保存: {report_file}")

if __name__ == "__main__":
    compare_human_grammar_results()
