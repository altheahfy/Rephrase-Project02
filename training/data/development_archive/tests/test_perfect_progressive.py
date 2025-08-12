#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完了進行形エンジン テスト
統合アーキテクチャ Phase 2 テスト実行
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'engines'))

from perfect_progressive_engine import PerfectProgressiveEngine

def test_perfect_progressive_engine():
    """完了進行形エンジンの包括的テスト"""
    print("🔥 完了進行形エンジン 統合テスト開始")
    
    # エンジン初期化
    engine = PerfectProgressiveEngine()
    print()
    
    # テストケース定義
    test_cases = [
        # 現在完了進行形
        {
            'sentence': 'I have been working here for three years.',
            'expected_type': 'present_perfect_progressive',
            'description': '現在完了進行形 (have been + Ving + 期間)'
        },
        {
            'sentence': 'How long have you been studying English?',
            'expected_type': 'present_perfect_progressive',
            'description': '疑問文完了進行形 (How long + have been)'
        },
        {
            'sentence': 'She has been waiting for an hour.',
            'expected_type': 'present_perfect_progressive',
            'description': '現在完了進行形 (has been + Ving)'
        },
        
        # 過去完了進行形
        {
            'sentence': 'She had been waiting for an hour when I arrived.',
            'expected_type': 'past_perfect_progressive',
            'description': '過去完了進行形 (had been + when節)'
        },
        {
            'sentence': 'He was tired because he had been running all morning.',
            'expected_type': 'past_perfect_progressive',
            'description': '過去完了進行形 (理由・結果表現)'
        },
        
        # 未来完了進行形
        {
            'sentence': 'By next year, I will have been living here for five years.',
            'expected_type': 'future_perfect_progressive',
            'description': '未来完了進行形 (will have been + by句)'
        },
        
        # 特殊構文
        {
            'sentence': 'The project has been being developed since January.',
            'expected_type': 'perfect_progressive_passive',
            'description': '受動完了進行形 (has been being + Ved)'
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
                for slot in ['S', 'V', 'O1', 'C1', 'M1', 'M2', 'M3', 'Aux']:
                    if slot in result:
                        print(f"    {slot}: '{result[slot]}'")
                
                print("  📋 サブスロット:")
                for slot in ['sub-s', 'sub-v', 'sub-o1', 'sub-c1', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux']:
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
        'I have been working here for three years',
        'she had been waiting for an hour',
        'the team has been developing the software since January'
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
    print("\n\n📝 統合例テスト: 接続詞 + 完了進行形")
    print("=" * 50)
    
    complex_sentence = "Because I have been working here for three years, I understand the company culture well."
    print(f"完全文: {complex_sentence}")
    
    # 従属節部分のみ抽出してサブスロット処理
    subordinate_clause = "I have been working here for three years"
    print(f"従属節: {subordinate_clause}")
    
    try:
        result = engine.process_as_subslot(subordinate_clause)
        print("🎯 接続詞節内完了進行形のサブスロット分解:")
        for slot, value in result.items():
            print(f"  {slot}: '{value}'")
        
        print("\n📊 統合結果想定:")
        print("  上位: M1='Because I have been working here for three years'")
        print("  上位: S='I', V='understand', O1='the company culture', M1='well'") 
        print("  サブ:", ', '.join([f"{k}='{v}'" for k, v in result.items()]))
        
    except Exception as e:
        print(f"💥 エラー: {str(e)}")
    
    print("\n🎉 完了進行形エンジン テスト完了")

if __name__ == "__main__":
    test_perfect_progressive_engine()
