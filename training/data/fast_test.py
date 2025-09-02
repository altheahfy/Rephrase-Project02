#!/usr/bin/env python3
"""
高速テストシステム - 簡潔版
最小限のログで高速実行

【重要マイルストーン】2025年8月29日
- 成功率98.6%達成 (73/74成功)
- 現在完了を除く全カテゴリ100%成功
- 基本5文型、基本副詞、関係節、受動態、tellグループ完全制覇
- 曖昧語句解決システム実装完了
- 修飾語分離アルゴリズム完成
- AbsoluteOrderManage        print(f"📁 分解結果を保存: {output_file}")
    
    return results準備完了
"""

import json
import sys
import os
import argparse
from pathlib import Path

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

def load_test_data():
    """テストデータ読み込み"""
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_range(case_range: str):
    """ケース範囲文字列から数値リストを取得（複合範囲対応）"""
    # テストデータ読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    test_cases = data['data']
    
    # プリセット範囲定義
    presets = {
        'all': '1-170',         # 対象例文全て（不定詞構文156-170を追加）
        'basic': '1-17',        # 基本5文型
        'adverbs': '18-42',     # 基本副詞
        'relative': '56,58,64', # 関係節
        'passive': '66-69',     # 受動態
        'tell': '83-86',        # tellグループ
        'modal': '87-110',      # モーダルハンドラ（助動詞・疑問文）
        'relative_adverbs': '111-120',  # 関係副詞
        'noun_clauses': '121-130',      # 名詞節
        'conditional': '131-155',       # 仮定法
        'infinitive': '156-170',        # 不定詞構文
        'core': '1-163',        # コア機能（実装済み全範囲）
        'advanced': '164-170',  # 高度な不定詞構文
        'sample100': '1-100',   # サンプル100件
        'sample200': '1-200',   # サンプル200件（将来拡張用）
        'sample500': '1-500',   # サンプル500件（将来拡張用）
        'sample1000': '1-1000', # サンプル1000件（将来拡張用）
        'quick': '1,10,20,30,40,50,60,70,80,90,100',  # クイックテスト（10件サンプル）
        'stress': '1-1000',     # ストレステスト用（大量データ）
    }
    
    # プリセット確認
    if case_range in presets:
        case_range = presets[case_range]
    
    if case_range:
        target_cases = []
        
        # カンマで分割して各部分を処理
        for part in case_range.split(','):
            part = part.strip()
            
            if '-' in part:
                # 範囲指定 (例: "1-70" または "case156-case170")
                if part.startswith('case'):
                    # 文字列キー範囲 (例: "case156-case170")
                    start_str, end_str = part.split('-')
                    start_num = int(start_str.replace('case', ''))
                    end_num = int(end_str.replace('case', ''))
                    target_cases.extend([f"case{i}" for i in range(start_num, end_num + 1) if f"case{i}" in test_cases])
                else:
                    # 数値キー範囲 (例: "1-70")
                    start, end = map(int, part.split('-'))
                    for i in range(start, end + 1):
                        # 数値キーと文字列キー両方を確認
                        if str(i) in test_cases:
                            target_cases.append(str(i))
                        elif f"case{i}" in test_cases:
                            target_cases.append(f"case{i}")
            else:
                # 単一ケース (例: "83" または "case159")
                if part in test_cases:
                    target_cases.append(part)
        
        # 重複除去とソート（文字列キーと数値キーを分けて処理）
        target_cases = list(set(target_cases))
        # 数値キーと文字列キーを分けてソート
        numeric_cases = sorted([case for case in target_cases if case.isdigit()], key=int)
        string_cases = sorted([case for case in target_cases if case.startswith('case')], 
                             key=lambda x: int(x.replace('case', '')))
        target_cases = numeric_cases + string_cases
    else:
        target_cases = list(test_cases.keys())
    
    return target_cases


def run_single_case(case_id, show_output=False):
    """個別ケース実行 - サブスロット詳細表示対応"""
    try:
        # JSON データを読み込み
        with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # dataキーの中のケースを取得
        case_data = test_data['data'].get(case_id)
        if not case_data:
            print(f"❌ ケース {case_id} が見つかりません")
            return None
        
        input_sentence = case_data['sentence']
        print(f"\n🔍 ケース {case_id}: {input_sentence}")
        
        # CentralController でテスト実行
        from central_controller import CentralController
        controller = CentralController()
        result = controller.process_sentence(input_sentence)
        
        # サブスロット分解が含まれている場合の詳細表示
        if show_output:
            print(f"📊 実行結果:")
            
            # サブスロット詳細表示
            if 'sub_slots' in result and result['sub_slots']:
                print("\n📝 サブスロット分解:")
                for slot_type, content in result['sub_slots'].items():
                    if slot_type != '_parent_slot':
                        if isinstance(content, dict):
                            order = content.get('order', 'N/A')
                            text = content.get('text', str(content))
                            print(f"  📝 {slot_type}: '{text}' → order: {order}")
                        else:
                            print(f"  📝 {slot_type}: '{content}' → order: N/A")
            else:
                print("\n📝 サブスロット: なし")
                        
            # メインスロット詳細表示
            if 'main_slots' in result and result['main_slots']:
                print("\n📝 メインスロット:")
                for slot_type, content in result['main_slots'].items():
                    if isinstance(content, dict):
                        order = content.get('order', 'N/A')
                        text = content.get('text', str(content))
                        print(f"  📝 {slot_type}: '{text}' → order: {order}")
                    else:
                        print(f"  📝 {slot_type}: '{content}' → order: N/A")
            
            # 完全な JSON 出力
            print(f"\n🗂️ 完全な分解結果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        return {'case_id': case_id, 'input_sentence': input_sentence, 'result': result}
        
    except Exception as e:
        print(f"❌ ケース {case_id} の実行エラー: {e}")
        return {'case_id': case_id, 'error': str(e)}


def run_fast_test(case_range=None, show_details=False, output_file="decomposition_results.json"):
    """高速テスト実行 - 大量データ対応版"""
    import time
    
    # データ読み込み
    data = load_test_data()
    test_cases = data['data']
    
    # central_controller インポート
    from central_controller import CentralController
    controller = CentralController()
    
    # 対象ケース決定（parse_range関数を使用）
    target_cases = parse_range(case_range)
    total_cases = len(target_cases)
    
    print(f"🎯 分解結果出力実行: {total_cases} ケース")
    
    # 大量データの場合は進行状況表示間隔を調整
    progress_interval = 1 if total_cases <= 100 else 10 if total_cases <= 1000 else 50
    
    results = {}
    success = 0
    failed = 0
    failed_cases = []  # 失敗ケースを記録
    start_time = time.time()
    
    for i, case_id in enumerate(target_cases, 1):
        case_data = test_cases[str(case_id)]  # 文字列キーに変換
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        try:
            # 実行
            actual = controller.process_sentence(sentence)
            
            # 期待値との比較
            is_match = compare_simple(expected, actual)
            
            # 分解結果を保存（メモリ効率化）
            if show_details:
                # 詳細表示時のみ完全なデータを保存
                results[f"case_{case_id}"] = {
                    "sentence": sentence,
                    "expected": expected,
                    "actual": actual,
                    "match": is_match
                }
            else:
                # 通常時は簡潔なデータのみ
                results[f"case_{case_id}"] = {
                    "sentence": sentence,
                    "match": is_match,
                    "main_slots": actual.get('main_slots', {}),
                    "sub_slots": actual.get('sub_slots', {})
                }
            
            if is_match:
                success += 1
                if show_details:
                    print(f"\n✅ case_{case_id}: 一致")
                    print(f"例文: {sentence}")
                    print(f"分解結果:")
                    print(json.dumps(actual, ensure_ascii=False, indent=2))
                elif total_cases <= 100:
                    print(f"✅ case_{case_id}: {sentence}")
            else:
                failed_cases.append(case_id)  # 失敗ケースを記録
                failed += 1
                if show_details:
                    print(f"\n❌ case_{case_id}: 不一致")
                    print(f"例文: {sentence}")
                    print(f"実際: {actual.get('main_slots', {})}")
                    print(f"期待: {expected.get('main_slots', {})}")
                elif total_cases <= 100:
                    print(f"❌ case_{case_id}: {sentence}")
                
        except Exception as e:
            failed_cases.append(case_id)  # エラーケースも記録
            failed += 1
            results[f"case_{case_id}"] = {
                "sentence": sentence,
                "error": str(e),
                "match": False
            }
            if total_cases <= 100:
                print(f"💥 case_{case_id}: {str(e)}")
        
        # 進行状況表示（大量データ対応）
        if total_cases > 100 and i % progress_interval == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total_cases - i) / rate if rate > 0 else 0
            success_rate = (success / i * 100) if i > 0 else 0
            print(f"📊 進行状況: {i}/{total_cases} ({i/total_cases*100:.1f}%) | 成功率: {success_rate:.1f}% | 処理速度: {rate:.1f}件/秒 | 予想残り時間: {eta:.0f}秒")
    
    # 最終結果
    elapsed_total = time.time() - start_time
    success_rate = (success / total_cases * 100) if total_cases > 0 else 0
    avg_speed = total_cases / elapsed_total if elapsed_total > 0 else 0
    
    print(f"\n📊 処理完了: {success}成功 / {failed}失敗 / {total_cases}総計 ({success_rate:.1f}%)")
    print(f"⏱️ 実行時間: {elapsed_total:.2f}秒 | 平均処理速度: {avg_speed:.1f}件/秒")
    
    # カテゴリ別統計（失敗ケースがある場合）
    if failed_cases:
        print(f"❌ 失敗ケース: {', '.join(map(str, failed_cases[:20]))}")  # 最初の20件のみ表示
        if len(failed_cases) > 20:
            print(f"   ... 他 {len(failed_cases)-20} 件")
        
        # 失敗パターン分析
        analyze_failure_patterns(failed_cases, test_cases, results)
    else:
        print("🎉 全ケース成功！")
    
    # ファイル出力
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📁 分解結果を保存: {output_file}")
    
    return results

def analyze_failure_patterns(failed_cases, test_cases, results):
    """失敗パターンの分析"""
    print(f"\n🔍 失敗パターン分析:")
    
    # V_group_key別集計
    group_failures = {}
    grammar_failures = {}
    
    for case_id in failed_cases:
        case_data = test_cases.get(str(case_id), {})
        v_group = case_data.get('V_group_key', 'unknown')
        grammar = case_data.get('grammar_category', 'unknown')
        
        group_failures[v_group] = group_failures.get(v_group, 0) + 1
        grammar_failures[grammar] = grammar_failures.get(grammar, 0) + 1
    
    # V_group_key別失敗率
    print(f"📊 V_group_key別失敗数:")
    for group, count in sorted(group_failures.items()):
        print(f"   {group}: {count}件")
    
    # grammar_category別失敗率（上位5位）
    print(f"📊 文法カテゴリ別失敗数（上位5位）:")
    top_grammar_failures = sorted(grammar_failures.items(), key=lambda x: x[1], reverse=True)[:5]
    for grammar, count in top_grammar_failures:
        print(f"   {grammar}: {count}件")

def compare_simple(expected, actual):
    """包括的比較 - main_slots と sub_slots 両方をチェック"""
    if 'error' in actual:
        return False
        
    # main_slots比較
    exp_main = expected.get('main_slots', {})
    act_main = actual.get('main_slots', {})
    
    if exp_main != act_main:
        return False
    
    # sub_slots比較（重要！）
    exp_sub = expected.get('sub_slots', {})
    act_sub = actual.get('sub_slots', {})
    
    # _parent_slotは無視して比較
    exp_sub_filtered = {k: v for k, v in exp_sub.items() if k != '_parent_slot'}
    act_sub_filtered = {k: v for k, v in act_sub.items() if k != '_parent_slot'}
    
    return exp_sub_filtered == act_sub_filtered

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='英文法分解システム テストツール - 大量データ対応版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python fast_test.py all                    # 全てのケース (1-170)
  python fast_test.py core                   # コア機能 (1-163)  
  python fast_test.py sample100              # サンプル100件
  python fast_test.py quick                  # クイックテスト（10件）
  python fast_test.py stress                 # ストレステスト（1000件）
  python fast_test.py 1-50                   # 範囲指定
  python fast_test.py case161-case170        # 文字列キー範囲
  python fast_test.py 1,5,10,20              # 個別指定
  python fast_test.py infinitive --show      # 詳細表示
  python fast_test.py 1-100 -o results.json  # 出力ファイル指定

プリセット:
  all, core, basic, adverbs, infinitive, modal, conditional
  quick, sample100, sample200, sample500, sample1000, stress
        """)
    
    parser.add_argument('range', nargs='?', default='core', 
                       help='対象ケース範囲 (デフォルト: core)')
    parser.add_argument('--output', '-o', help='分解結果の出力ファイル名')
    parser.add_argument('--show', '-s', action='store_true', help='コンソールに詳細表示')
    parser.add_argument('--list-presets', action='store_true', help='利用可能なプリセット一覧を表示')
    
    args = parser.parse_args()
    
    # プリセット一覧表示
    if args.list_presets:
        print("📋 利用可能なプリセット:")
        presets = {
            'all': '1-170 (全ケース)',
            'core': '1-163 (実装済みコア機能)',
            'basic': '1-17 (基本5文型)',
            'adverbs': '18-42 (基本副詞)',
            'infinitive': '156-170 (不定詞構文)',
            'modal': '87-110 (助動詞・疑問文)',
            'conditional': '131-155 (仮定法)',
            'quick': '10件サンプル',
            'sample100': '1-100 (100件サンプル)',
            'sample500': '1-500 (500件サンプル)',
            'sample1000': '1-1000 (1000件サンプル)',
            'stress': '1-1000 (ストレステスト)',
        }
        for preset, desc in presets.items():
            print(f"  {preset:15} : {desc}")
        exit(0)
    
    # デフォルトの出力ファイル名（長いファイル名を避ける）
    output_file = args.output
    if not output_file and args.range:
        # ケース数に応じてファイル名を短縮
        case_numbers = parse_range(args.range)
        case_count = len(case_numbers)
        
        if case_count == 1:
            # 単一ケース：そのまま表示
            output_file = f"decomposition_results_{case_numbers[0]}.json"
        elif case_count <= 5:
            # 少数ケース：すべて表示
            case_str = '_'.join(map(str, case_numbers))
            output_file = f"decomposition_results_{case_str}.json"
        else:
            # 多数ケース：範囲表示+ケース数
            min_case = min([int(str(c).replace('case', '')) for c in case_numbers])
            max_case = max([int(str(c).replace('case', '')) for c in case_numbers])
            if args.range in ['all', 'core', 'stress', 'sample100', 'sample200', 'sample500', 'sample1000']:
                output_file = f"decomposition_results_{args.range}_{case_count}cases.json"
            else:
                output_file = f"decomposition_results_{min_case}-{max_case}_{case_count}cases.json"
    elif not output_file:
        output_file = "decomposition_results_default.json"
    
    print(f"🚀 英文法分解システム テスト開始")
    print(f"📁 結果保存先: {output_file}")
    
    results = run_fast_test(args.range, args.show, output_file)
    
    print(f"📁 分解結果を保存しました: {output_file}")
