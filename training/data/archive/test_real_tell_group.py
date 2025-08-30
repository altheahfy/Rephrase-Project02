#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実際のtellグループデータ抽出・処理テスト
真のランダマイズ可能な動的テンプレート生成
"""

import json
from central_controller import CentralController
from dynamic_absolute_order_manager import DynamicAbsoluteOrderManager

def extract_real_tell_group():
    """実際のデータベースから真のtellグループを抽出"""
    
    # まず全データを読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # tellグループの文章を抽出（absolute_order_testは除外）
    real_tell_sentences = []
    tell_test_sentences = []
    
    for key, item in data['data'].items():
        if item.get('V_group_key') == 'tell':
            sentence = item['sentence']
            category = item.get('grammar_category', 'unknown')
            
            if category == 'absolute_order_test':
                tell_test_sentences.append(sentence)
                print(f"  テスト用: {sentence}")
            else:
                real_tell_sentences.append(sentence)
                print(f"  実データ: {sentence}")
    
    print(f"\n=== 抽出結果 ===")
    print(f"実際のtellグループ例文: {len(real_tell_sentences)}件")
    print(f"テスト用例文: {len(tell_test_sentences)}件")
    
    return real_tell_sentences, tell_test_sentences

def test_real_tell_group():
    """実際のtellグループで動的分析をテスト"""
    
    print("=== 実際のtellグループデータ抽出 ===")
    real_sentences, test_sentences = extract_real_tell_group()
    
    if not real_sentences:
        print("\n⚠️ 実際のtellグループデータが見つかりません。テスト用データで確認します。")
        real_sentences = test_sentences
    
    print(f"\n=== 使用する例文 ({len(real_sentences)}件) ===")
    for i, sentence in enumerate(real_sentences, 1):
        print(f"{i}. {sentence}")
    
    # DynamicAbsoluteOrderManagerで分析
    print(f"\n=== 動的分析実行 ===")
    manager = DynamicAbsoluteOrderManager()
    mapping = manager.analyze_group_elements("tell", real_sentences)
    
    print(f"\n=== 生成された動的テンプレート ===")
    print(f"tellグループ絶対順序マッピング: {mapping}")
    
    # CentralControllerに統合してテスト
    print(f"\n=== CentralController統合テスト ===")
    controller = CentralController()
    
    # テスト文章でランダマイズ可能性を確認
    test_cases = [
        "He told me the truth yesterday.",
        "What did she tell you?", 
        "I will tell him a story tomorrow.",
        "Tell me what happened!",
        "Did you tell her the secret?"
    ]
    
    for sentence in test_cases:
        print(f"\n【テスト】: {sentence}")
        try:
            result = controller.process_sentence(sentence)
            if result['success']:
                abs_order = result.get('absolute_order', {})
                if 'absolute_order' in abs_order:
                    print(f"  ✅ 成功: {abs_order['absolute_order']}")
                else:
                    print(f"  ⚠️ 処理成功だが絶対順序なし")
            else:
                print(f"  ❌ 処理失敗")
        except Exception as e:
            print(f"  ❌ エラー: {e}")

if __name__ == "__main__":
    test_real_tell_group()
