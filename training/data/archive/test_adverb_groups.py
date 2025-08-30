#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本的な副詞グループの動的分析テスト
"""

import json
from collections import defaultdict
from central_controller import CentralController
from dynamic_absolute_order_manager import DynamicAbsoluteOrderManager

def extract_adverb_groups():
    """basic_adverbsカテゴリからV_group_key別に例文を抽出"""
    
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    adverb_groups = defaultdict(list)
    
    for key, item in data['data'].items():
        if item.get('grammar_category') == 'basic_adverbs':
            v_group_key = item.get('V_group_key', 'unknown')
            sentence = item['sentence']
            adverb_groups[v_group_key].append(sentence)
    
    return adverb_groups

def test_adverb_group_analysis():
    """基本的な副詞グループの動的分析をテスト"""
    
    print("=== 基本的な副詞グループ抽出 ===")
    adverb_groups = extract_adverb_groups()
    
    for group_key, sentences in adverb_groups.items():
        print(f"\n【{group_key}グループ】({len(sentences)}件):")
        for i, sentence in enumerate(sentences, 1):
            print(f"  {i}. {sentence}")
    
    # 最も例文数の多いグループで動的分析をテスト
    target_groups = []
    for group_key, sentences in adverb_groups.items():
        if len(sentences) >= 3:  # 3例文以上のグループを対象
            target_groups.append((group_key, sentences))
    
    if not target_groups:
        print("\n⚠️ 十分な例文数のグループが見つかりません")
        return
    
    # 最も例文数の多いグループを選択
    target_group, target_sentences = max(target_groups, key=lambda x: len(x[1]))
    
    print(f"\n=== 動的分析対象: {target_group}グループ ===")
    print(f"例文数: {len(target_sentences)}件")
    
    # DynamicAbsoluteOrderManagerで分析
    manager = DynamicAbsoluteOrderManager()
    
    try:
        mapping = manager.analyze_group_elements(target_group, target_sentences)
        print(f"\n🎯 {target_group}グループの動的マッピング:")
        print(f"{mapping}")
        
        # CentralControllerを使って実際のテスト
        print(f"\n=== CentralController統合テスト ===")
        
        # CentralControllerに新しいグループを追加
        controller = CentralController()
        controller.absolute_order_manager.register_group_mapping(target_group, mapping)
        
        # テスト実行
        test_sentences = target_sentences[:3]  # 最初の3例文でテスト
        
        for i, sentence in enumerate(test_sentences, 1):
            print(f"\n【テスト{i}】: {sentence}")
            try:
                result = controller.process_sentence(sentence)
                if result['success']:
                    abs_order = result.get('absolute_order', {})
                    print(f"  ✅ 成功: {abs_order.get('group', 'unknown')}グループ")
                    print(f"  絶対順序: {abs_order.get('absolute_order', {})}")
                else:
                    print(f"  ❌ 処理失敗")
            except Exception as e:
                print(f"  ❌ エラー: {e}")
    
    except Exception as e:
        print(f"⚠️ 動的分析エラー: {e}")

if __name__ == "__main__":
    test_adverb_group_analysis()
