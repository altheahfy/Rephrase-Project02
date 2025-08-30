#!/usr/bin/env python3
"""
実際のfinal_54_test_data_with_absolute_order_corrected.jsonから
basic_adverbsカテゴリのグループを抽出して動的分析をテストする
"""

import json
import sys
import os
from datetime import datetime
from collections import defaultdict

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_absolute_order_manager import DynamicAbsoluteOrderManager
from central_controller import CentralController

def load_test_data():
    """JSONファイルからテストデータを読み込み"""
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_basic_adverbs_groups(test_data):
    """basic_adverbsカテゴリからV_group_key別にグループ化"""
    basic_adverbs_groups = defaultdict(list)
    
    for test_id, test_case in test_data['data'].items():
        if test_case.get('grammar_category') == 'basic_adverbs':
            v_group_key = test_case.get('V_group_key')
            basic_adverbs_groups[v_group_key].append({
                'id': test_id,
                'sentence': test_case['sentence'],
                'expected': test_case['expected']
            })
    
    return dict(basic_adverbs_groups)

def analyze_basic_adverbs_group(group_name, test_cases):
    """指定されたbasic_adverbsグループの動的分析"""
    print(f"\n=== {group_name}グループ動的分析 ===")
    print(f"例文数: {len(test_cases)}件")
    
    if len(test_cases) < 2:
        print("⚠️ 例文が2件未満のため、動的分析をスキップ")
        return None
    
    # 例文のリストを作成
    sentences = [case['sentence'] for case in test_cases]
    
    print("\n📚 分析対象例文:")
    for i, sentence in enumerate(sentences, 1):
        print(f"  {i}. {sentence}")
    
    # DynamicAbsoluteOrderManagerで分析
    manager = DynamicAbsoluteOrderManager()
    
    try:
        mapping = manager.analyze_group_elements(group_name, sentences)
        print(f"\n🎯 {group_name}グループの動的マッピング:")
        print(mapping)
        return mapping
    except Exception as e:
        print(f"❌ 分析エラー: {e}")
        return None

def test_central_controller_integration(group_mappings):
    """CentralControllerとの統合テスト"""
    print(f"\n=== CentralController統合テスト ===")
    
    # テストデータの読み込み
    test_data = load_test_data()
    basic_adverbs_groups = extract_basic_adverbs_groups(test_data)
    
    # CentralControllerのセットアップ
    controller = CentralController()
    
    # 動的マッピングを手動で登録
    for group_name, mapping in group_mappings.items():
        if mapping:
            controller.absolute_order_manager.group_mappings[group_name] = mapping
            print(f"✅ {group_name}グループのマッピングを登録: {mapping}")
    
    # 各グループの例文をテスト
    success_count = 0
    total_count = 0
    
    for group_name, test_cases in basic_adverbs_groups.items():
        if group_name in group_mappings and group_mappings[group_name]:
            print(f"\n【{group_name}グループテスト】")
            for case in test_cases[:3]:  # 最初の3例文のみテスト
                total_count += 1
                sentence = case['sentence']
                expected = case['expected']
                
                print(f"\n【テスト{total_count}】: {sentence}")
                
                try:
                    # CentralControllerで処理
                    result = controller.process_sentence(sentence)
                    
                    if result.get('success', False):
                        print(f"  ✅ 成功: {group_name}グループ")
                        print(f"  絶対順序: {result.get('absolute_order', {})}")
                        success_count += 1
                    else:
                        print(f"  ❌ 失敗: {result.get('error', '不明なエラー')}")
                        
                except Exception as e:
                    print(f"  ❌ 処理エラー: {e}")
    
    print(f"\n=== 統合テスト結果 ===")
    if total_count > 0:
        print(f"成功: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    else:
        print("テスト対象となる有効なグループマッピングがありませんでした")

def main():
    """メイン処理"""
    print("=== 実際のbasic_adverbsグループ動的分析テスト ===")
    
    # テストデータの読み込み
    test_data = load_test_data()
    basic_adverbs_groups = extract_basic_adverbs_groups(test_data)
    
    print(f"\n📊 basic_adverbsカテゴリ統計:")
    print(f"総グループ数: {len(basic_adverbs_groups)}")
    for group_name, test_cases in basic_adverbs_groups.items():
        print(f"  {group_name}グループ: {len(test_cases)}件")
    
    # 各グループの動的分析
    group_mappings = {}
    for group_name, test_cases in basic_adverbs_groups.items():
        mapping = analyze_basic_adverbs_group(group_name, test_cases)
        group_mappings[group_name] = mapping
    
    # CentralControllerとの統合テスト
    test_central_controller_integration(group_mappings)

if __name__ == "__main__":
    main()
