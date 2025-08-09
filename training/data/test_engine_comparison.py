#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版エンジン vs 旧エンジンの比較テスト
段階的に性能を検証
"""

import sys
import os
from ImprovedRephraseParsingEngine import ImprovedRephraseParsingEngine
from Rephrase_Parsing_Engine import RephraseParsingEngine

def compare_engines():
    """新旧エンジンの比較テスト"""
    print("🔍 改良版 vs 旧版エンジンの比較テスト\n")
    
    # エンジン初期化
    try:
        old_engine = RephraseParsingEngine()
        new_engine = ImprovedRephraseParsingEngine()
        print("✅ 両エンジン初期化完了\n")
    except Exception as e:
        print(f"❌ エンジン初期化エラー: {e}")
        return
    
    # テストケース（段階的に複雑度を上げる）
    test_cases = [
        {
            "sentence": "I love you.",
            "level": "基本",
            "expected": {"S": "I", "V": "love", "O1": "you"}
        },
        {
            "sentence": "That afternoon, I love you.", 
            "level": "時間修飾語",
            "expected": {"M3": "That afternoon", "S": "I", "V": "love", "O1": "you"}
        },
        {
            "sentence": "He left New York a few days ago.",
            "level": "SVO+時間",
            "expected": {"S": "He", "V": "left", "O1": "New York", "M3": "a few days ago"}
        },
        {
            "sentence": "Yesterday morning, she gave him a book.",
            "level": "SVOO+時間",
            "expected": {"M3": "Yesterday morning", "S": "she", "V": "gave", "O1": "him", "O2": "a book"}
        },
        {
            "sentence": "The teacher who had just returned gave the student a book.",
            "level": "関係詞節",
            "expected": {"S": "The teacher who had just returned", "V": "gave", "O1": "the student", "O2": "a book"}
        }
    ]
    
    print(f"📊 {len(test_cases)} 段階のテストを実行\n")
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        level = test_case["level"]
        expected = test_case["expected"]
        
        print(f"=== テスト {i}: {level} ===")
        print(f"例文: {sentence}")
        print(f"期待値: {expected}")
        
        # 旧エンジンでテスト
        try:
            old_result = old_engine.analyze_sentence(sentence)
            print(f"旧エンジン: {simplify_result(old_result)}")
        except Exception as e:
            print(f"旧エンジンエラー: {e}")
            old_result = {}
        
        # 新エンジンでテスト
        try:
            new_result = new_engine.analyze_sentence(sentence)
            print(f"新エンジン: {simplify_result(new_result)}")
        except Exception as e:
            print(f"新エンジンエラー: {e}")
            new_result = {}
        
        # 比較評価
        old_score = evaluate_result(expected, old_result)
        new_score = evaluate_result(expected, new_result)
        
        print(f"📊 精度比較:")
        print(f"  旧エンジン: {old_score:.1f}%")
        print(f"  新エンジン: {new_score:.1f}%")
        
        if new_score > old_score:
            print("  ✅ 改良版が優秀")
        elif new_score == old_score:
            print("  📊 同等")
        else:
            print("  ❌ 改良版が劣化")
        
        print()

def simplify_result(result):
    """結果を簡略化して表示用に変換"""
    if not isinstance(result, dict):
        return result
        
    simplified = {}
    for slot, items in result.items():
        if isinstance(items, list) and items:
            if isinstance(items[0], dict) and 'value' in items[0]:
                simplified[slot] = items[0]['value']
            else:
                simplified[slot] = str(items[0])
        elif items:
            simplified[slot] = str(items)
    
    return simplified

def evaluate_result(expected, actual):
    """結果の精度を評価"""
    if not expected or not actual:
        return 0.0
    
    simplified_actual = simplify_result(actual)
    
    correct = 0
    total = len(expected)
    
    for slot, expected_value in expected.items():
        if slot in simplified_actual:
            actual_value = simplified_actual[slot]
            # 部分一致でもOK
            if (expected_value.lower() in str(actual_value).lower() or 
                str(actual_value).lower() in expected_value.lower()):
                correct += 1
    
    return (correct / total) * 100 if total > 0 else 0.0

if __name__ == "__main__":
    compare_engines()
