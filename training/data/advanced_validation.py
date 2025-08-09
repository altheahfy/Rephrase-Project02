#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高度な検証テスト - エンジンの精度と効率性をチェック
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_edge_cases():
    """エッジケースのテスト"""
    print("🔬 エッジケーステスト")
    print("="*60)
    
    engine = CompleteRephraseParsingEngine()
    
    edge_cases = [
        # 複雑な文構造
        ("The book that I bought yesterday is on the table.", "複雑な関係節"),
        ("Having finished his work, he went home.", "分詞構文"),
        ("Not only did he come, but he also helped.", "倒置構文"),
        ("What he said was true.", "what節"),
        
        # 重複要素
        ("She is very, very happy.", "副詞の重複"),
        ("The big, big house is beautiful.", "形容詞の重複"),
        
        # 省略構文
        ("He can swim and she can too.", "省略構文"),
        ("Better late than never.", "比較構文の省略"),
        
        # 慣用表現
        ("It's raining cats and dogs.", "慣用表現"),
        ("Break a leg!", "成句"),
        
        # 疑問文・感嘆文
        ("What a beautiful day it is!", "感嘆文"),
        ("How fast he runs!", "感嘆文"),
        
        # 否定文の複雑性
        ("I don't think he will come.", "否定の転移"),
        ("Nobody said nothing.", "二重否定"),
    ]
    
    issues = []
    
    for i, (sentence, description) in enumerate(edge_cases, 1):
        print(f"\n=== テスト {i}: {sentence} ===")
        print(f"種類: {description}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 基本的な妥当性チェック
            if not result.get('slots'):
                issues.append(f"テスト{i}: スロットが空")
            
            # V（動詞）の存在チェック
            if not result['slots'].get('V') or not result['slots']['V']:
                issues.append(f"テスト{i}: 動詞が検出されていない")
            
            # 重複チェック
            for slot_name, slot_values in result['slots'].items():
                if len(slot_values) > 3:  # 異常に多い重複
                    issues.append(f"テスト{i}: {slot_name}に{len(slot_values)}個の値（重複疑い）")
            
            print(f"✅ 処理成功: 文型={result.get('sentence_pattern', 'N/A')}")
            
        except Exception as e:
            issues.append(f"テスト{i}: 例外発生 - {str(e)}")
            print(f"❌ エラー: {e}")
    
    return issues

def test_performance_patterns():
    """パフォーマンスパターンのテスト"""
    print("\n🚀 パフォーマンステスト")
    print("="*60)
    
    engine = CompleteRephraseParsingEngine()
    
    # 長文テスト
    long_sentences = [
        "The quick brown fox jumps over the lazy dog while the cat sleeps peacefully under the warm sunshine in the beautiful garden.",
        "Although he had been working very hard for many years, he still could not achieve the success that he had always dreamed of.",
        "When I was young, my grandmother used to tell me stories about her childhood in the countryside where she lived with her family.",
    ]
    
    issues = []
    
    for i, sentence in enumerate(long_sentences, 1):
        print(f"\n=== 長文テスト {i} ===")
        print(f"文字数: {len(sentence)}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # ルール適用過多チェック
            total_rules_applied = sum(len(values) for values in result['slots'].values())
            if total_rules_applied > 15:  # 閾値
                issues.append(f"長文{i}: ルール適用過多({total_rules_applied}個)")
            
            print(f"✅ 適用ルール数: {total_rules_applied}")
            
        except Exception as e:
            issues.append(f"長文{i}: 例外発生 - {str(e)}")
    
    return issues

def test_rule_conflicts():
    """ルール競合のテスト"""
    print("\n⚡ ルール競合テスト")
    print("="*60)
    
    engine = CompleteRephraseParsingEngine()
    
    # 複数ルールが適用される可能性のある文
    conflict_cases = [
        ("He went to school yesterday.", ["V-go-intrans", "to-direction-M2", "time-M3"]),
        ("She is working in the office.", ["be-progressive", "place-M3"]),
        ("I believe in God deeply.", ["V-believe-in", "place-M3", "manner-degree-M2"]),
    ]
    
    issues = []
    
    for i, (sentence, expected_rules) in enumerate(conflict_cases, 1):
        print(f"\n=== 競合テスト {i}: {sentence} ===")
        print(f"期待ルール: {expected_rules}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 各スロットで複数の値が競合していないかチェック
            for slot_name, slot_values in result['slots'].items():
                if len(slot_values) > 1:
                    rule_ids = [v.get('rule_id', 'unknown') for v in slot_values]
                    confidence_scores = [v.get('confidence', 0) for v in slot_values]
                    
                    # 信頼度が大きく異なる場合は問題なし、似たような場合は競合の可能性
                    if len(set(confidence_scores)) == 1:  # 全て同じ信頼度
                        issues.append(f"競合{i}: {slot_name}で同信頼度の複数値({rule_ids})")
            
            print(f"✅ 競合チェック完了")
            
        except Exception as e:
            issues.append(f"競合{i}: 例外発生 - {str(e)}")
    
    return issues

def test_accuracy_verification():
    """精度検証テスト"""
    print("\n🎯 精度検証テスト")
    print("="*60)
    
    engine = CompleteRephraseParsingEngine()
    
    # 明確な正解がある文
    accuracy_tests = [
        {
            'sentence': "John gave Mary a book.",
            'expected': {'S': ['John'], 'V': ['gave'], 'O1': ['Mary'], 'O2': ['a book']},
            'pattern': 'SVOO'
        },
        {
            'sentence': "The cat is sleeping.",
            'expected': {'S': ['The cat'], 'V': ['is sleeping'], 'Aux': ['is']},
            'pattern': 'SV'
        },
        {
            'sentence': "He became a teacher.",
            'expected': {'S': ['He'], 'V': ['became'], 'C1': ['a teacher']},
            'pattern': 'SVC'
        },
    ]
    
    issues = []
    accuracy_count = 0
    
    for i, test_case in enumerate(accuracy_tests, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        expected_pattern = test_case['pattern']
        
        print(f"\n=== 精度テスト {i}: {sentence} ===")
        print(f"期待文型: {expected_pattern}")
        
        try:
            result = engine.analyze_sentence(sentence)
            actual_pattern = result.get('sentence_pattern', 'Unknown')
            
            # 文型チェック
            if actual_pattern != expected_pattern:
                issues.append(f"精度{i}: 文型不一致 期待={expected_pattern} 実際={actual_pattern}")
            else:
                accuracy_count += 1
            
            # スロット内容チェック
            for slot_name, expected_values in expected.items():
                actual_values = result['slots'].get(slot_name, [])
                if not actual_values:
                    issues.append(f"精度{i}: {slot_name}が空")
                else:
                    # 最低でも1つは期待値に近い値があるかチェック
                    found = False
                    for expected_val in expected_values:
                        for actual_val in actual_values:
                            actual_text = actual_val.get('value', '').lower()
                            if expected_val.lower() in actual_text or actual_text in expected_val.lower():
                                found = True
                                break
                        if found:
                            break
                    
                    if not found:
                        issues.append(f"精度{i}: {slot_name}に期待値'{expected_values}'が見つからない")
            
            print(f"文型: {actual_pattern} {'✅' if actual_pattern == expected_pattern else '❌'}")
            
        except Exception as e:
            issues.append(f"精度{i}: 例外発生 - {str(e)}")
    
    accuracy_rate = accuracy_count / len(accuracy_tests) * 100
    print(f"\n📊 精度率: {accuracy_rate:.1f}% ({accuracy_count}/{len(accuracy_tests)})")
    
    return issues, accuracy_rate

def main():
    """メインテスト実行"""
    print("🔬 CompleteRephraseParsingEngine 高度検証テスト")
    print("="*60)
    
    all_issues = []
    
    # 各テストを実行
    all_issues.extend(test_edge_cases())
    all_issues.extend(test_performance_patterns())
    all_issues.extend(test_rule_conflicts())
    
    issues, accuracy_rate = test_accuracy_verification()
    all_issues.extend(issues)
    
    # 結果サマリー
    print("\n" + "="*60)
    print("🏆 検証結果サマリー")
    print("="*60)
    
    if all_issues:
        print(f"❌ 発見された問題点: {len(all_issues)}個")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ 問題は発見されませんでした")
    
    print(f"\n📊 総合精度: {accuracy_rate:.1f}%")
    
    if accuracy_rate >= 90:
        print("🌟 優秀な精度です！")
    elif accuracy_rate >= 70:
        print("👍 良好な精度です")
    else:
        print("⚠️ 精度改善が必要です")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
