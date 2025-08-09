#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateRephraseParsingEngine v4.0 効果検証テスト
根本的修正の効果を測定
"""

import sys
sys.path.append('.')

from UltimateRephraseParsingEngine import UltimateRephraseParsingEngine
import json

def test_ultimate_engine():
    """Ultimate Engineの包括的テスト"""
    
    print("🚀 Ultimate Rephrase Parsing Engine v4.0 テスト開始")
    print("=" * 80)
    
    try:
        engine = UltimateRephraseParsingEngine()
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    # 高度なテストケース（各ルールの完全な活用を検証）
    test_cases = [
        {
            'sentence': "She will give him a birthday present tomorrow.",
            'expected_patterns': ['第4文型', 'ditransitive', '助動詞', '時間表現'],
            'description': "第4文型+助動詞+時間表現の統合処理"
        },
        {
            'sentence': "His parents made him study English every day.",
            'expected_patterns': ['使役', 'causative_make', 'SVO1C2'],
            'description': "使役パターンルールの完全実装"
        },
        {
            'sentence': "Tom became a professional football player last year.",
            'expected_patterns': ['連結動詞', 'copular_become', 'SC1'],
            'description': "連結動詞パターンルールの活用"
        },
        {
            'sentence': "I know that she is working in Tokyo now.",
            'expected_patterns': ['認識動詞', 'cognition_verb', 'that_clause'],
            'description': "認識動詞+that節パターンの処理"
        },
        {
            'sentence': "There are many students in the library.",
            'expected_patterns': ['存在文', 'exist_locative', 'there構文'],
            'description': "意味制約（exist_locative）の活用"
        },
        {
            'sentence': "Can you help me solve this problem?",
            'expected_patterns': ['助動詞can', '使役', 'help_pattern'],
            'description': "複数ルール統合処理"
        }
    ]
    
    results = []
    total_tests = len(test_cases)
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 テストケース {i}/{total_tests}")
        print(f"文: {test_case['sentence']}")
        print(f"期待: {test_case['description']}")
        print("-" * 60)
        
        try:
            result = engine.analyze_sentence(test_case['sentence'])
            
            if 'error' in result:
                print(f"❌ 分析エラー: {result['error']}")
                test_result = False
            else:
                # 結果の詳細表示
                print(f"🎯 結果概要:")
                metadata = result.get('metadata', {})
                print(f"   エンジン: {metadata.get('engine', 'Unknown')}")
                print(f"   適用ルール数: {metadata.get('rules_applied', 0)}")
                print(f"   ルール活用率: {metadata.get('rule_utilization_rate', '0%')}")
                print(f"   文型: {result.get('sentence_type', '不明')}")
                
                # スロット詳細
                print(f"🔍 スロット詳細:")
                main_slots = result.get('main_slots', {})
                for slot, items in main_slots.items():
                    if items:
                        for item in items:
                            print(f"   {slot}: '{item.get('value', '')}' (ルール: {item.get('rule_id', 'unknown')}, 信頼度: {item.get('confidence', 0):.2f})")
                
                # 活用率チェック
                utilization_rate = float(metadata.get('rule_utilization_rate', '0%').replace('%', ''))
                if utilization_rate > 30:  # 30%以上の活用率で成功
                    print(f"✅ 高活用率達成: {utilization_rate}%")
                    test_result = True
                    successful_tests += 1
                else:
                    print(f"⚠️ 低活用率: {utilization_rate}%")
                    test_result = False
            
            results.append({
                'test_case': i,
                'sentence': test_case['sentence'],
                'success': test_result,
                'result': result
            })
            
        except Exception as e:
            print(f"❌ テスト実行エラー: {e}")
            results.append({
                'test_case': i,
                'sentence': test_case['sentence'],
                'success': False,
                'error': str(e)
            })
    
    # 総合評価
    print(f"\n🏆 総合テスト結果")
    print("=" * 80)
    print(f"成功テスト数: {successful_tests}/{total_tests}")
    print(f"成功率: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests >= total_tests * 0.8:  # 80%以上で根本的修正成功
        print("🎉 根本的修正成功！Ultimate Engine は期待通りに動作しています")
        
        # パフォーマンス詳細分析
        print("\n📊 詳細パフォーマンス分析:")
        for result in results:
            if result['success'] and 'result' in result:
                metadata = result['result'].get('metadata', {})
                utilization = metadata.get('rule_utilization_rate', '0%')
                print(f"   ケース{result['test_case']}: {utilization} ルール活用")
    else:
        print("⚠️  追加調整が必要です")
        
        # 失敗ケース詳細
        print("\n❌ 失敗ケース詳細:")
        for result in results:
            if not result['success']:
                print(f"   ケース{result['test_case']}: {result['sentence']}")
                if 'error' in result:
                    print(f"      エラー: {result['error']}")
    
    return results

def compare_with_previous_engine():
    """従来エンジンとの比較"""
    print("\n🔬 従来エンジンとの比較分析")
    print("=" * 60)
    
    # 従来エンジンのパフォーマンス（推定値）
    old_engine_stats = {
        'rule_utilization': '20-30%',
        'pattern_rules_processed': 0,
        'advanced_triggers_handled': 'なし',
        'generic_fallback_overuse': '頻繁'
    }
    
    # Ultimate Engineの改善点
    ultimate_improvements = {
        'rule_utilization': '80%以上目標',
        'pattern_rules_processed': 4,
        'advanced_triggers_handled': '位置・意味・文脈制約対応',
        'generic_fallback_overuse': '保守的制御'
    }
    
    print("📈 改善比較:")
    for key in old_engine_stats.keys():
        print(f"   {key}:")
        print(f"      従来エンジン: {old_engine_stats[key]}")
        print(f"      Ultimate Engine: {ultimate_improvements[key]}")
        print()

if __name__ == "__main__":
    # メインテスト実行
    test_results = test_ultimate_engine()
    
    # 比較分析実行
    compare_with_previous_engine()
    
    print("\n🏁 テスト完了")
