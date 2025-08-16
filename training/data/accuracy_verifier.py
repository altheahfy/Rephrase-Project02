#!/usr/bin/env python3
"""
精度検証スクリプト - 正解データベースとシステム出力の詳細比較
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def load_expected_results():
    """正解データベースを読み込み"""
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # correct_answersからリスト形式に変換
        correct_answers = data.get('correct_answers', {})
        results = []
        
        for key, value in correct_answers.items():
            if value.get('sentence') and value.get('expected'):
                results.append({
                    'sentence': value['sentence'],
                    'expected_result': value['expected']
                })
        
        return results
    except FileNotFoundError:
        print("❌ expected_results_progress.json が見つかりません")
        return []

def compare_results(expected, actual):
    """結果を比較して差異を特定"""
    mismatches = []
    
    # メインスロットの比較
    for slot in ['M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']:
        expected_val = expected.get('main_slots', {}).get(slot, "")
        actual_val = actual.get('main_slots', {}).get(slot, "")
        
        if expected_val != actual_val:
            mismatches.append({
                'type': 'main_slot',
                'slot': slot,
                'expected': expected_val,
                'actual': actual_val
            })
    
    # サブスロットの比較
    expected_subs = expected.get('sub_slots', {})
    actual_subs = actual.get('sub_slots', {})
    
    # 全てのサブスロットキーを取得
    all_sub_keys = set(expected_subs.keys()) | set(actual_subs.keys())
    
    for sub_key in all_sub_keys:
        expected_val = expected_subs.get(sub_key, "")
        actual_val = actual_subs.get(sub_key, "")
        
        if expected_val != actual_val:
            mismatches.append({
                'type': 'sub_slot',
                'slot': sub_key,
                'expected': expected_val,
                'actual': actual_val
            })
    
    return mismatches

def main():
    """メイン検証処理"""
    print("🔍 精度検証開始")
    
    # 正解データ読み込み
    expected_results = load_expected_results()
    if not expected_results:
        print("❌ 正解データが見つかりません")
        return
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='WARNING')  # ログを抑制
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    print(f"📊 検証対象: {len(expected_results)}例文")
    print("=" * 60)
    
    total_errors = 0
    detailed_errors = []
    
    for i, expected_data in enumerate(expected_results, 1):
        sentence = expected_data.get('sentence', '')
        expected_result = expected_data.get('expected_result', {})
        
        if not sentence:
            continue
        
        print(f"\n🧪 例文{i}: {sentence}")
        
        # システム実行
        try:
            system_output = mapper.process(sentence)
            
            # システム出力を正解データ形式に変換
            actual_result = {
                'main_slots': system_output.get('slots', {}),
                'sub_slots': system_output.get('sub_slots', {})
            }
            
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            total_errors += 1
            continue
        
        # 結果比較
        mismatches = compare_results(expected_result, actual_result)
        
        if mismatches:
            total_errors += 1
            print(f"❌ 不一致検出: {len(mismatches)}箇所")
            
            for mismatch in mismatches:
                print(f"  {mismatch['type']} [{mismatch['slot']}]:")
                print(f"    期待値: '{mismatch['expected']}'")
                print(f"    実際値: '{mismatch['actual']}'")
            
            detailed_errors.append({
                'sentence_num': i,
                'sentence': sentence,
                'mismatches': mismatches
            })
        else:
            print("✅ 完全一致")
    
    # 最終結果
    print("\n" + "=" * 60)
    print(f"📈 最終結果:")
    print(f"  総例文数: {len(expected_results)}")
    print(f"  エラー数: {total_errors}")
    print(f"  正解率: {((len(expected_results) - total_errors) / len(expected_results) * 100):.1f}%")
    
    if detailed_errors:
        print(f"\n🚨 詳細エラー分析:")
        for error in detailed_errors:
            print(f"  例文{error['sentence_num']}: {len(error['mismatches'])}箇所の不一致")
    
    if total_errors == 0:
        print("🎉 全例文で完全一致を達成！")
    else:
        print(f"⚠️ {total_errors}例文で修正が必要です")

if __name__ == "__main__":
    main()
