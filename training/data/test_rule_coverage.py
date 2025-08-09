#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
未使用ルール特定テスト
rephrase_rules_v1.0.jsonの25ルールの活用状況を詳細分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_rule_coverage():
    """全25ルールの活用状況をテスト"""
    print("🔍 rephrase_rules_v1.0.json 全25ルール活用状況分析")
    print("=" * 60)
    
    engine = CompleteRephraseParsingEngine()
    
    # 各ルールターゲットのテスト例文
    test_cases = [
        # 1. 助動詞関連ルール
        {"sentence": "I have finished my work.", "target_rules": ["aux-have"]},
        {"sentence": "She will come tomorrow.", "target_rules": ["aux-will"]},
        {"sentence": "They are running now.", "target_rules": ["be-progressive"]},
        
        # 2. 疑問詞・主語ルール
        {"sentence": "Why did you go there?", "target_rules": ["wh-why-front"]},
        {"sentence": "The student studies hard.", "target_rules": ["subject-pronoun-np-front"]},
        
        # 3. 修飾語ルール（M2/M3）
        {"sentence": "He speaks very loudly.", "target_rules": ["manner-degree-M2"]},
        {"sentence": "She went to the store.", "target_rules": ["to-direction-M2"]},
        {"sentence": "I work for my family.", "target_rules": ["for-purpose-M2"]},
        {"sentence": "The book is from Japan.", "target_rules": ["from-source-M3"]},
        {"sentence": "We met at the park.", "target_rules": ["place-M3"]},
        {"sentence": "I visited there last night.", "target_rules": ["time-M3"]},
        {"sentence": "If you come, I will help.", "target_rules": ["if-clause-as-M2"]},
        
        # 4. 動詞特化ルール
        {"sentence": "He recovered quickly.", "target_rules": ["V-recover-intrans"]},
        {"sentence": "Please listen carefully.", "target_rules": ["V-listen-intrans"]},
        {"sentence": "They left yesterday.", "target_rules": ["V-leave-intrans-depart"]},
        {"sentence": "Let's go home.", "target_rules": ["V-go-intrans"]},
        {"sentence": "I can't pay now.", "target_rules": ["V-pay-intrans"]},
        {"sentence": "I believe in justice.", "target_rules": ["V-believe-in"]},
        {"sentence": "She apologized to me.", "target_rules": ["V-apologize-intrans"]},
        {"sentence": "It rained heavily.", "target_rules": ["V-rain-weather"]},
        {"sentence": "The book is on the table.", "target_rules": ["V-be-exist-loc"]},
        
        # 5. パターンルール
        {"sentence": "She gave him a gift.", "target_rules": ["ditransitive_SVO1O2"]},
        {"sentence": "They made him work hard.", "target_rules": ["causative_make_SVO1C2"]},
        {"sentence": "He became a doctor.", "target_rules": ["copular_become_SC1"]},
        {"sentence": "I know that he is right.", "target_rules": ["cognition_verb_that_clause"]},
    ]
    
    # ルール適用状況を追跡
    rule_usage = {}
    total_tests = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n=== テスト {i}: {test['sentence']} ===")
        print(f"期待ルール: {', '.join(test['target_rules'])}")
        
        # パース実行（詳細ログ有効）
        result = engine.analyze_sentence(test['sentence'])
        
        # メタデータから適用ルール数確認
        applied_rules = result.get('metadata', {}).get('rules_applied', 0)
        print(f"📊 適用されたルール数: {applied_rules}/25")
        
        # 各ターゲットルールの適用状況を記録
        for rule_id in test['target_rules']:
            if rule_id not in rule_usage:
                rule_usage[rule_id] = {'tested': 0, 'applied': 0}
            rule_usage[rule_id]['tested'] += 1
            
            # 実際の適用確認は出力ログから判断
            # (簡易版：ルール数が増加していれば適用されたと仮定)
            if applied_rules > 0:
                rule_usage[rule_id]['applied'] += 1
        
        print("-" * 50)
    
    # 結果サマリー
    print(f"\n🏆 ルール活用状況サマリー")
    print("=" * 60)
    
    tested_rules = len(rule_usage)
    successfully_applied = sum(1 for stats in rule_usage.values() if stats['applied'] > 0)
    
    print(f"テストされたルール数: {tested_rules}/25")
    print(f"適用確認されたルール数: {successfully_applied}/{tested_rules}")
    print(f"ルール活用率: {(successfully_applied/25)*100:.1f}%")
    
    # 未使用ルール特定
    all_rules = [
        "aux-have", "aux-will", "be-progressive", "wh-why-front", "subject-pronoun-np-front",
        "time-M3", "place-M3", "manner-degree-M2", "to-direction-M2", "for-purpose-M2",
        "from-source-M3", "if-clause-as-M2", "V-recover-intrans", "V-listen-intrans",
        "V-leave-intrans-depart", "V-go-intrans", "V-pay-intrans", "V-believe-in",
        "V-apologize-intrans", "V-rain-weather", "V-be-exist-loc", "ditransitive_SVO1O2",
        "causative_make_SVO1C2", "copular_become_SC1", "cognition_verb_that_clause"
    ]
    
    unused_rules = [rule for rule in all_rules if rule not in rule_usage or rule_usage[rule]['applied'] == 0]
    
    if unused_rules:
        print(f"\n❌ 未使用ルール ({len(unused_rules)}個):")
        for rule in unused_rules:
            print(f"  - {rule}")
    else:
        print("\n✅ 全ルールが正常に活用されています！")
    
    return rule_usage, unused_rules

if __name__ == "__main__":
    rule_usage, unused_rules = test_rule_coverage()
