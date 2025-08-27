#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡略文での副詞ハンドラーテスト
"""

from adverb_handler import AdverbHandler
from basic_five_pattern_handler import BasicFivePatternHandler

# 簡略文のテスト
simplified_text = "The man lives here ."

print(f"🔧 簡略文での副詞ハンドラーテスト: '{simplified_text}'")
print("=" * 60)

# 副詞ハンドラーテスト
adverb_handler = AdverbHandler()
print("📍 副詞ハンドラー処理:")
adverb_result = adverb_handler.process(simplified_text)
print(f"   結果: {adverb_result}")

if adverb_result.get('success'):
    separated_text = adverb_result.get('separated_text')
    modifier_slots = adverb_result.get('modifier_slots', {})
    print(f"   修飾語分離後: '{separated_text}'")
    print(f"   修飾語スロット: {modifier_slots}")
    
    # 5文型ハンドラーで修飾語分離後テキストをテスト
    print("\n📍 5文型ハンドラー処理:")
    five_handler = BasicFivePatternHandler()
    five_result = five_handler.process(separated_text)
    print(f"   結果: {five_result}")
    
    if five_result.get('success'):
        final_slots = five_result['slots'].copy()
        final_slots.update(modifier_slots)
        print(f"   統合後スロット: {final_slots}")
else:
    print(f"   ❌ 副詞ハンドラー失敗: {adverb_result.get('error')}")
