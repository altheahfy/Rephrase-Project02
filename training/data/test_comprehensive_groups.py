#!/usr/bin/env python3
"""
AbsoluteOrderManager包括的グループテスト
tellグループと基本的副詞グループの検証とファイル出力
"""

import json
import datetime
from absolute_order_manager_group_fixed import AbsoluteOrderManager

def load_test_data():
    """テストデータの読み込み"""
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_group_cases(test_data, target_groups=None, target_categories=None):
    """指定されたグループ・カテゴリのケースを抽出"""
    cases = {}
    
    for case_id, case_data in test_data['data'].items():
        v_group_key = case_data.get('V_group_key')
        grammar_category = case_data.get('grammar_category')
        
        # 絶対順序データが存在するケースのみ
        if 'absolute_order' not in case_data:
            continue
            
        # グループフィルタ
        if target_groups and v_group_key not in target_groups:
            continue
            
        # カテゴリフィルタ
        if target_categories and grammar_category not in target_categories:
            continue
            
        cases[case_id] = case_data
        
    return cases

def test_group_cases(order_manager, cases, group_name):
    """指定されたケース群のテスト実行"""
    results = []
    success_count = 0
    
    print(f"\n🎯 {group_name} テスト実行")
    print("=" * 80)
    
    for case_id, case_data in cases.items():
        sentence = case_data['sentence']
        expected_order = case_data['absolute_order']
        main_slots = case_data['expected']['main_slots']
        v_group_key = case_data.get('V_group_key', 'unknown')
        wh_word = case_data.get('wh_word')
        
        print(f"\n📋 Case {case_id}: {sentence}")
        print(f"🔑 V_group_key: {v_group_key}")
        print(f"🔍 wh_word: {wh_word}")
        print(f"📊 Expected: {expected_order}")
        
        result_data = {
            'case_id': case_id,
            'sentence': sentence,
            'v_group_key': v_group_key,
            'wh_word': wh_word,
            'expected_order': expected_order,
            'main_slots': main_slots
        }
        
        try:
            # AbsoluteOrderManager実行
            result = order_manager.apply_absolute_order(
                slots=main_slots,
                v_group_key=v_group_key, 
                wh_word=wh_word
            )
            
            # 結果を辞書形式に変換
            actual_order = {}
            for item in result:
                actual_order[item['slot']] = item['absolute_position']
            
            print(f"📈 Actual:   {actual_order}")
            
            # 比較
            is_match = actual_order == expected_order
            
            if is_match:
                print("✅ MATCH")
                success_count += 1
                result_data['status'] = 'SUCCESS'
            else:
                print("❌ MISMATCH")
                differences = []
                print("🔍 Differences:")
                for slot in set(list(expected_order.keys()) + list(actual_order.keys())):
                    exp_pos = expected_order.get(slot, "なし")
                    act_pos = actual_order.get(slot, "なし")
                    if exp_pos != act_pos:
                        diff_info = f"{slot}: Expected={exp_pos}, Actual={act_pos}"
                        print(f"  - {diff_info}")
                        differences.append(diff_info)
                result_data['status'] = 'FAILED'
                result_data['differences'] = differences
            
            result_data['actual_order'] = actual_order
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            result_data['status'] = 'ERROR'
            result_data['error'] = str(e)
        
        results.append(result_data)
    
    total_count = len(cases)
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\n📊 {group_name} 結果: {success_count}/{total_count} ケース成功")
    print(f"📈 成功率: {success_rate:.1f}%")
    
    return results, success_count, total_count

def save_test_results(all_results, output_file):
    """テスト結果をJSONファイルに保存"""
    output_data = {
        'meta': {
            'test_timestamp': datetime.datetime.now().isoformat(),
            'total_groups': len(all_results),
            'total_cases': sum(result['total_count'] for result in all_results.values()),
            'total_success': sum(result['success_count'] for result in all_results.values())
        },
        'results': all_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 テスト結果を {output_file} に保存しました")

def main():
    """メイン実行関数"""
    print("🚀 AbsoluteOrderManager 包括的グループテスト開始")
    print("=" * 80)
    
    # テストデータ読み込み
    test_data = load_test_data()
    
    # AbsoluteOrderManager初期化
    order_manager = AbsoluteOrderManager()
    
    # テスト対象グループの定義
    test_groups = {
        'tell_group': {
            'target_groups': ['tell'],
            'target_categories': None,
            'description': 'tellグループ（Cases 83-86）'
        },
        'basic_adverbs': {
            'target_groups': None,
            'target_categories': ['basic_adverbs'],
            'description': '基本的副詞を含むグループ'
        },
        'action_group': {
            'target_groups': ['action'],
            'target_categories': None,
            'description': 'actionグループ'
        },
        'gave_group': {
            'target_groups': ['gave'],
            'target_categories': None,
            'description': 'gaveグループ'
        }
    }
    
    all_results = {}
    
    # 各グループのテスト実行
    for group_key, group_config in test_groups.items():
        cases = extract_group_cases(
            test_data, 
            target_groups=group_config['target_groups'],
            target_categories=group_config['target_categories']
        )
        
        if not cases:
            print(f"\n⚠️ {group_config['description']}: テストケースが見つかりません")
            continue
        
        results, success_count, total_count = test_group_cases(
            order_manager, 
            cases, 
            group_config['description']
        )
        
        all_results[group_key] = {
            'description': group_config['description'],
            'success_count': success_count,
            'total_count': total_count,
            'success_rate': (success_count / total_count * 100) if total_count > 0 else 0,
            'cases': results
        }
    
    # 全体サマリー
    total_cases = sum(result['total_count'] for result in all_results.values())
    total_success = sum(result['success_count'] for result in all_results.values())
    overall_rate = (total_success / total_cases * 100) if total_cases > 0 else 0
    
    print(f"\n🎯 全体結果サマリー")
    print("=" * 80)
    for group_key, result in all_results.items():
        print(f"📊 {result['description']}: {result['success_count']}/{result['total_count']} ({result['success_rate']:.1f}%)")
    
    print(f"\n🏆 総合結果: {total_success}/{total_cases} ケース成功 ({overall_rate:.1f}%)")
    
    # 結果をファイル保存
    output_file = f"comprehensive_test_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_test_results(all_results, output_file)
    
    if overall_rate == 100:
        print("🎉 全グループテスト完全成功！")
    else:
        print("⚠️ 一部のグループで修正が必要です")

if __name__ == "__main__":
    main()
