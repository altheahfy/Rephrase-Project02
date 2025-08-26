#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ルール辞書とエンジン全体照合診断
"""

import sys
import json
import os
sys.path.append('.')
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def analyze_rule_conflicts():
    """ルール競合・優先度問題の診断"""
    print("=== ルール辞書とエンジン全体照合診断 ===\n")
    
    # エンジン初期化
    engine = CompleteRephraseParsingEngine()
    
    # ルールデータ確認
    print("📋 ルールファイル情報:")
    rules_file = os.path.join(os.path.dirname(__file__), 'rephrase_rules_v1.0.json')
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules_data = json.load(f)
    
    print(f"  バージョン: {rules_data.get('version')}")
    print(f"  更新日: {rules_data.get('updated_at')}")
    print(f"  総ルール数: {len(rules_data.get('rules', []))}")
    
    # 時間・期間関連ルールの詳細確認
    print("\n🕐 時間・期間関連ルール:")
    time_related_rules = []
    
    for rule in rules_data.get('rules', []):
        rule_id = rule.get('id', '')
        
        # 時間関連ルールを特定
        if any(keyword in rule_id.lower() for keyword in ['time', 'ago', 'for', 'manner', 'degree']):
            priority = rule.get('priority', 50)
            trigger = rule.get('trigger', {})
            assign = rule.get('assign', {})
            
            time_related_rules.append({
                'id': rule_id,
                'priority': priority,
                'trigger': trigger,
                'slot': assign.get('slot', 'Unknown')
            })
            
            print(f"  {rule_id}:")
            print(f"    優先度: {priority}")
            print(f"    スロット: {assign.get('slot', 'Unknown')}")
            if 'pattern' in trigger:
                print(f"    パターン: {trigger['pattern'][:60]}...")
            if 'pos' in trigger:
                print(f"    POS: {trigger['pos']}")
            print()
    
    # 優先度順でソート
    time_related_rules.sort(key=lambda x: x['priority'])
    
    print("📊 時間関連ルールの優先度順序:")
    for rule in time_related_rules:
        print(f"  {rule['priority']:2d}: {rule['id']} → {rule['slot']}")
    
    # テスト文での実際の適用順序確認
    print("\n🧪 実際のテスト:")
    test_sentence = "I met him a few days ago."
    print(f"テスト文: {test_sentence}")
    
    # ルール適用過程を詳細表示
    result = engine.analyze_sentence(test_sentence)
    
    # 結果の詳細分析
    rephrase_slots = result.get('rephrase_slots', {})
    print("\n📋 結果分析:")
    
    for slot, values in rephrase_slots.items():
        if values:  # 空でないスロットのみ表示
            print(f"  {slot}: {values}")
    
    # 重複や問題の特定
    print("\n🚨 問題の特定:")
    
    # M2スロットの重複チェック
    m2_values = rephrase_slots.get('M2', [])
    if len(m2_values) > 1:
        print(f"  M2重複: {m2_values}")
        # "ago"の重複をチェック
        ago_count = sum(1 for v in m2_values if 'ago' in str(v))
        if ago_count > 1:
            print(f"    → 'ago'が{ago_count}回重複")
    
    # M3との重複チェック
    m3_values = rephrase_slots.get('M3', [])
    if m2_values and m3_values:
        for m2_val in m2_values:
            for m3_val in m3_values:
                if str(m2_val) in str(m3_val) or str(m3_val) in str(m2_val):
                    print(f"    → M2とM3で重複: '{m2_val}' vs '{m3_val}'")

if __name__ == "__main__":
    analyze_rule_conflicts()
