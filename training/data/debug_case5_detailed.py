#!/usr/bin/env python3
"""ケース5デバッグ: that関係節の修飾語取得問題"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def debug_case5_detailed():
    """ケース5詳細デバッグ"""
    # 協力者セットアップ
    adverb_handler = AdverbHandler()
    collaborators = {
        'AdverbHandler': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # 問題のケース
    test_text = "The person that works here is kind."
    
    print(f"🔍 ケース5詳細デバッグ: {test_text}")
    print("=" * 60)
    
    # 1. AdverbHandlerでの修飾語分離確認
    print("📋 Step 1: AdverbHandlerでの修飾語分離")
    adverb_result = adverb_handler.process(test_text)
    print(f"分離結果: '{adverb_result.get('separated_text', test_text)}'")
    print(f"修飾語: {adverb_result.get('modifiers', {})}")
    
    # 2. 関係節抽出確認
    print("\n📋 Step 2: 関係節テキスト抽出")
    rel_handler.original_text = test_text
    clause_text = rel_handler._extract_relative_clause_text_original(test_text, 'that')
    print(f"抽出関係節: '{clause_text}'")
    
    # 3. 関係節に対してAdverbHandler適用
    print("\n📋 Step 3: 関係節にAdverbHandler適用")
    if clause_text:
        rel_adverb_result = adverb_handler.process(clause_text)
        print(f"関係節分離結果: '{rel_adverb_result.get('separated_text', clause_text)}'")
        print(f"関係節修飾語: {rel_adverb_result.get('modifiers', {})}")
    
    # 4. RelativeClauseHandlerでの処理結果
    print("\n📋 Step 4: RelativeClauseHandler処理結果")
    result = rel_handler.process(test_text)
    print("最終結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 5. sub-m2の有無確認
    sub_slots = result.get('sub_slots', {})
    has_sub_m2 = 'sub-m2' in sub_slots
    print(f"\n📍 sub-m2存在: {has_sub_m2}")
    if has_sub_m2:
        print(f"📍 sub-m2値: '{sub_slots['sub-m2']}'")

if __name__ == "__main__":
    debug_case5_detailed()
