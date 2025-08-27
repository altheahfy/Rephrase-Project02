#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5文型ハンドラー単体テスト：簡略文処理確認
"""

from basic_five_pattern_handler import BasicFivePatternHandler

# 簡略文
simplified_text = "The man lives here ."

print(f"🔧 5文型ハンドラー単体テスト")
print("=" * 50)
print(f"📝 簡略文: {simplified_text}")

handler = BasicFivePatternHandler()
result = handler.process(simplified_text)

print(f"📊 結果: {result}")

if result.get('success'):
    slots = result.get('slots', {})
    print(f"✅ 成功")
    print(f"📍 スロット: {slots}")
    
    if 'M2' in slots and 'here' in slots['M2']:
        print(f"✅ M2に'here'が正しく配置: {slots['M2']}")
    else:
        print(f"❌ M2に'here'が配置されていない")
else:
    print(f"❌ 失敗: {result.get('error', 'Unknown error')}")
