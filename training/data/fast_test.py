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
        'all': '1-120',         # 対象例文全て（関係副詞111-120を追加）
        'basic': '1-17',        # 基本5文型
        'adverbs': '18-42',     # 基本副詞
        'relative': '56,58,64', # 関係節
        'passive': '66-69',     # 受動態
        'tell': '83-86',        # tellグループ
        'modal': '87-110',      # モーダルハンドラ（助動詞・疑問文）
        'relative_adverbs': '111-120'  # 関係副詞
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
                # 範囲指定 (例: "1-70")
                start, end = map(int, part.split('-'))
                target_cases.extend([int(i) for i in range(start, end + 1) if str(i) in test_cases])
            else:
                # 単一ケース (例: "83")
                if part in test_cases:
                    target_cases.append(int(part))
        
        # 重複除去とソート
        target_cases = sorted(list(set(target_cases)))
    else:
        target_cases = list(map(int, test_cases.keys()))
    
    return target_cases


def run_single_case(case_id, show_output=False):
    """個別ケース実行 - サブスロット詳細表示対応"""
    try:
        # JSON データを読み込み
        with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # dataキーの中のケースを取得
        case_data = test_data['data'].get(str(case_id))
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
    """高速テスト実行 - 分解結果出力対応"""
    # データ読み込み
    data = load_test_data()
    test_cases = data['data']
    
    # central_controller インポート
    from central_controller import CentralController
    controller = CentralController()
    
    # 対象ケース決定（parse_range関数を使用）
    target_cases = parse_range(case_range)
    
    print(f"🎯 分解結果出力実行: {len(target_cases)} ケース")
    
    results = {}
    success = 0
    failed = 0
    failed_cases = []  # 失敗ケースを記録
    
    for case_id in target_cases:
        case_data = test_cases[str(case_id)]  # 文字列キーに変換
        sentence = case_data['sentence']
        expected = case_data['expected']
        
        try:
            # 実行
            actual = controller.process_sentence(sentence)
            
            # 期待値との比較
            is_match = compare_simple(expected, actual)
            
            # 分解結果を保存
            results[f"case_{case_id}"] = {
                "sentence": sentence,
                "expected": expected,
                "actual": actual,
                "match": is_match
            }
            
            if is_match:
                if show_details:
                    print(f"\n✅ case_{case_id}: 一致")
                    print(f"例文: {sentence}")
                    print(f"分解結果:")
                    print(json.dumps(actual, ensure_ascii=False, indent=2))
                else:
                    print(f"✅ case_{case_id}: {sentence}")
                success += 1
            else:
                failed_cases.append(case_id)  # 失敗ケースを記録
                if show_details:
                    print(f"\n❌ case_{case_id}: 不一致")
                    print(f"例文: {sentence}")
                    print(f"実際: {actual.get('main_slots', {})}")
                    print(f"期待: {expected.get('main_slots', {})}")
                else:
                    print(f"❌ case_{case_id}: {sentence}")
                failed += 1
                
        except Exception as e:
            failed_cases.append(case_id)  # エラーケースも記録
            results[f"case_{case_id}"] = {
                "sentence": sentence,
                "expected": expected,
                "error": str(e),
                "match": False
            }
            print(f"💥 case_{case_id}: {str(e)}")
            failed += 1
    
    success_rate = (success / len(target_cases) * 100) if len(target_cases) > 0 else 0
    print(f"\n📊 処理完了: {success}成功 / {failed}失敗 / {len(target_cases)}総計 ({success_rate:.1f}%)")
    
    # 失敗ケースのリストを表示
    if failed_cases:
        print(f"❌ 失敗ケース: {', '.join(map(str, failed_cases))}")
    else:
        print("🎉 全ケース成功！")
    
    # ファイル出力
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"� 分解結果を保存: {output_file}")
    
    return results

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
    
    parser = argparse.ArgumentParser(description='分解結果出力システム')
    parser.add_argument('range', nargs='?', help='対象ケース範囲 (例: 1-10, 1,2,3, 35)')
    parser.add_argument('--output', '-o', help='分解結果の出力ファイル名')
    parser.add_argument('--show', '-s', action='store_true', help='コンソールに詳細表示')
    
    args = parser.parse_args()
    
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
            min_case = min(case_numbers)
            max_case = max(case_numbers)
            output_file = f"decomposition_results_{min_case}-{max_case}_{case_count}cases.json"
    elif not output_file:
        output_file = "decomposition_results_all.json"
    
    results = run_fast_test(args.range, args.show, output_file)
    
    print(f"📁 分解結果を保存しました: {output_file}")
