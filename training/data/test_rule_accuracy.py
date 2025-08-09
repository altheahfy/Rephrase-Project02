#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ルール辞書の精度検証スクリプト
基本的な例文でルールの精度を評価
"""

import sys
import os
from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_rule_accuracy():
    """ルール辞書の精度を基本例文でテスト"""
    print("🔍 ルール辞書精度検証テスト")
    
    # パーシングエンジン初期化
    engine = RephraseParsingEngine()
    
    # 基本的な例文（正解が明確なもの）
    test_cases = [
        {
            "sentence": "I love you.",
            "expected": {
                "S": "I",
                "V": "love", 
                "O1": "you"
            },
            "description": "第3文型（SVO）基本形"
        },
        {
            "sentence": "That afternoon, I love you.",
            "expected": {
                "M3": "That afternoon",
                "S": "I",
                "V": "love", 
                "O1": "you"
            },
            "description": "時間修飾語付きSVO"
        },
        {
            "sentence": "Yesterday morning, she gave him a book.",
            "expected": {
                "M3": "Yesterday morning",
                "S": "she",
                "V": "gave",
                "O1": "him",
                "O2": "a book"
            },
            "description": "第4文型（SVOO）時間修飾語付き"
        },
        {
            "sentence": "He left New York a few days ago.",
            "expected": {
                "S": "He",
                "V": "left",
                "O1": "New York",
                "M3": "a few days ago"
            },
            "description": "SVO + 時間修飾語"
        },
        {
            "sentence": "I can't afford it.",
            "expected": {
                "S": "I", 
                "Aux": "can't",  # または "cannot"
                "V": "afford",
                "O1": "it"
            },
            "description": "助動詞縮約形"
        }
    ]
    
    print(f"📊 {len(test_cases)} 個の基本例文をテスト\n")
    
    total_score = 0
    max_score = 0
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        print(f"=== テスト {i}: {description} ===")
        print(f"例文: {sentence}")
        print(f"期待値: {expected}")
        
        try:
            # パーシング実行
            result = engine.analyze_sentence(sentence)
            print(f"実結果: {result}")
            
            # スコア計算
            case_score = 0
            case_max = len(expected)
            max_score += case_max
            
            for slot, expected_value in expected.items():
                if slot in result:
                    # 複数要素がある場合は最初の要素をチェック
                    actual_values = result[slot]
                    if isinstance(actual_values, list) and len(actual_values) > 0:
                        actual_value = actual_values[0]['value'] if isinstance(actual_values[0], dict) else str(actual_values[0])
                        # 部分一致でもOK（"can't"と"cannot"など）
                        if expected_value.lower() in actual_value.lower() or actual_value.lower() in expected_value.lower():
                            case_score += 1
                            print(f"  ✅ {slot}: {expected_value} ≈ {actual_value}")
                        else:
                            print(f"  ❌ {slot}: 期待値'{expected_value}' ≠ 実際値'{actual_value}'")
                    else:
                        print(f"  ❌ {slot}: スロットが空または形式が不正")
                else:
                    print(f"  ❌ {slot}: スロットが存在しない")
            
            total_score += case_score
            accuracy = (case_score / case_max) * 100
            print(f"🎯 ケース精度: {case_score}/{case_max} ({accuracy:.1f}%)\n")
            
        except Exception as e:
            print(f"❌ パーシングエラー: {e}\n")
    
    # 全体的な精度
    overall_accuracy = (total_score / max_score) * 100 if max_score > 0 else 0
    print(f"📋 総合精度: {total_score}/{max_score} ({overall_accuracy:.1f}%)")
    
    if overall_accuracy < 50:
        print("🚨 ルール辞書の精度が極めて低い状態です")
        print("   → 根本的な見直しが必要")
    elif overall_accuracy < 80:
        print("⚠️  ルール辞書の精度が不十分です")
        print("   → 大幅な改良が必要")
    else:
        print("✅ ルール辞書の基本精度は良好です")

if __name__ == "__main__":
    test_rule_accuracy()
