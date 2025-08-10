#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import json

# エンジンを初期化
engine = CompleteRephraseParsingEngine()

# テスト文
test_sentence = "Where did you get it?"

print(f"=== テスト文: {test_sentence} ===")

# 文を解析
result = engine.analyze_sentence(test_sentence)

# M3スロットの詳細を確認
if 'main_slots' in result and 'M3' in result['main_slots']:
    m3_data = result['main_slots']['M3']
    print(f"\n🔍 M3スロットの詳細:")
    print(f"M3内容: {m3_data}")
    
    if m3_data:
        for item in m3_data:
            print(f"  - value: '{item.get('value', 'N/A')}'")
            print(f"  - rule_id: '{item.get('rule_id', 'N/A')}'") 
            print(f"  - order: {item.get('order', 'N/A')}")
            print(f"  - confidence: {item.get('confidence', 'N/A')}")
            
# 完全な結果表示
print(f"\n📋 全結果構造:")
print(json.dumps(result, indent=2, ensure_ascii=False))
