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

# 全スロットのorder値を確認
print(f"\n🔍 全スロットのorder値確認:")

for slot_name in ['S', 'Aux', 'V', 'O1', 'M3']:
    if slot_name in result['main_slots'] and result['main_slots'][slot_name]:
        for item in result['main_slots'][slot_name]:
            value = item.get('value', 'N/A')
            order = item.get('order', 'N/A')
            rule_id = item.get('rule_id', 'N/A')
            print(f"  {slot_name}: '{value}' - order: {order} (rule: {rule_id})")

print(f"\n📊 Order値の分布:")
order_counts = {}
for slot_name, items in result['main_slots'].items():
    for item in items:
        order = item.get('order', 'N/A')
        order_key = str(order)  # 文字列に変換してソート問題を回避
        if order_key not in order_counts:
            order_counts[order_key] = []
        order_counts[order_key].append(f"{slot_name}: {item.get('value', 'N/A')}")

for order_key in sorted(order_counts.keys(), key=lambda x: (x == 'N/A', int(x) if x != 'N/A' else 0)):
    items = order_counts[order_key]
    print(f"  order {order_key}: {items}")
