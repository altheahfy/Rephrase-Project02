#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
比較級・最上級エンジン テスト
統合アーキテクチャ Phase 2 テスト実行
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'engines'))

from comparative_superlative_engine import ComparativeSuperlativeEngine

def test_comparative_superlative_engine():
    """比較級・最上級エンジンの包括的テスト"""
    print("🔥 比較級・最上級エンジン 統合テスト開始")
    
    # エンジン初期化
    engine = ComparativeSuperlativeEngine()
    print()
    
    # テストケース定義
    test_cases = [
        # 基本比較級
        {
            'sentence': 'This book is more interesting than that one.',
            'expected_type': 'comparative',
            'description': '形容詞比較級 (more + than)'
        },
        {
            'sentence': 'She runs faster than him.',
            'expected_type': 'comparative', 
            'description': '副詞比較級 (-er + than)'
        },
        {
            'sentence': 'I have more money than you.',
            'expected_type': 'comparative',
            'description': '数量比較級 (more + than)'
        },
        
        # 最上級
        {
            'sentence': 'This is the most beautiful flower in the garden.',
            'expected_type': 'superlative',
            'description': '形容詞最上級 (most + scope)'
        },
        {
            'sentence': 'She speaks English most fluently among all students.',
            'expected_type': 'superlative',
            'description': '副詞最上級 (most + scope)'
        },
        
        # 特殊比較構文
        {
            'sentence': 'He is as tall as his brother.',
            'expected_type': 'equal_comparison',
            'description': '同等比較 (as...as)'
        },
        {
            'sentence': 'The harder you work, the more successful you become.',
            'expected_type': 'proportional_comparison', 
            'description': '比例比較 (the...the)'
        }
    ]
    
    # 独立文処理テスト
    print("📝 独立文処理テスト")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test_case['description']}")
        print(f"入力: {test_case['sentence']}")
        
        try:
            result = engine.process(test_case['sentence'])
            
            if result:
                print(f"✅ 処理成功: {test_case['expected_type']}")
                print("  📋 上位スロット:")
                for slot in ['S', 'V', 'O1', 'C1', 'M1', 'M2', 'M3']:
                    if slot in result:
                        print(f"    {slot}: '{result[slot]}'")
                
                print("  📋 サブスロット:")
                for slot in ['sub-s', 'sub-v', 'sub-o1', 'sub-c1', 'sub-m1', 'sub-m2', 'sub-m3']:
                    if slot in result:
                        print(f"    {slot}: '{result[slot]}'")
                
                if 'metadata' in result:
                    print(f"  📋 メタ情報: {result['metadata']}")
                    
            else:
                print("❌ 処理失敗: 結果なし")
                
        except Exception as e:
            print(f"💥 エラー: {str(e)}")
    
    # サブスロット専用処理テスト
    print("\n\n📝 サブスロット専用処理テスト")
    print("=" * 50)
    
    subslot_test_cases = [
        'this method is more efficient than the traditional approach',
        'the house is the most expensive in the neighborhood', 
        'the work is as important as the deadline'
    ]
    
    for i, sentence in enumerate(subslot_test_cases, 1):
        print(f"\n🔧 サブスロットテスト{i}: {sentence}")
        
        try:
            result = engine.process_as_subslot(sentence)
            
            if result:
                print("✅ サブスロット処理成功:")
                for slot, value in result.items():
                    print(f"    {slot}: '{value}'")
            else:
                print("❌ サブスロット処理失敗")
                
        except Exception as e:
            print(f"💥 エラー: {str(e)}")
    
    # 統合例テスト
    print("\n\n📝 統合例テスト: 接続詞 + 比較級")
    print("=" * 50)
    
    complex_sentence = "Because this method is more efficient than the traditional approach, we should adopt it."
    print(f"完全文: {complex_sentence}")
    
    # 従属節部分のみ抽出してサブスロット処理
    subordinate_clause = "this method is more efficient than the traditional approach"
    print(f"従属節: {subordinate_clause}")
    
    try:
        result = engine.process_as_subslot(subordinate_clause)
        print("🎯 接続詞節内比較級のサブスロット分解:")
        for slot, value in result.items():
            print(f"  {slot}: '{value}'")
        
        print("\n📊 統合結果想定:")
        print("  上位: M1='Because this method is more efficient than the traditional approach'")
        print("  上位: S='we', V='should adopt', O1='it'") 
        print("  サブ:", ', '.join([f"{k}='{v}'" for k, v in result.items()]))
        
    except Exception as e:
        print(f"💥 エラー: {str(e)}")
    
    print("\n🎉 比較級・最上級エンジン テスト完了")

if __name__ == "__main__":
    test_comparative_superlative_engine()
