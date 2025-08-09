#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rephrase_rules_v1.0.jsonの全ルール解析スクリプト
"""

import json

def analyze_rules():
    # ルール辞書を読み込む
    with open('rephrase_rules_v1.0.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 基本ルール一覧
    print("=== 基本ルール一覧 ===")
    rules = data.get('rules', [])
    for i, rule in enumerate(rules, 1):
        rule_id = rule.get('id', 'unknown')
        priority = rule.get('priority', 0)
        print(f"{i:2d}. {rule_id} (優先度: {priority})")
    
    # パターンルール一覧
    print("\n=== パターンルール一覧 ===")
    patterns = data.get('patterns', [])
    for i, pattern in enumerate(patterns, 1):
        pattern_id = pattern.get('id', 'unknown')
        label = pattern.get('label', '')
        print(f"{i:2d}. {pattern_id} - {label}")
    
    # 統計情報
    print(f"\n=== 統計情報 ===")
    print(f"基本ルール数: {len(rules)}")
    print(f"パターンルール数: {len(patterns)}")
    print(f"総ルール数: {len(rules) + len(patterns)}")
    
    return rules, patterns

if __name__ == "__main__":
    rules, patterns = analyze_rules()
