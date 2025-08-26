#!/usr/bin/env python3
"""ケース5テスト: The game that I played here"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def test_case5():
    """ケース5: The game that I played hereテスト"""
    # 協力者セットアップ
    adverb_handler = AdverbHandler()
    collaborators = {
        'AdverbHandler': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # テストケース
    test_text = "The game that I played here"
    
    print(f"\n🧪 that関係節テスト: {test_text}")
    print("=" * 50)
    
    # 処理実行
    result = rel_handler.process(test_text)
    
    print("📊 結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # sub-m2確認
    success = result.get('success', False)
    sub_slots = result.get('sub_slots', {})
    has_sub_m2 = 'sub-m2' in sub_slots
    
    print(f"\n✅ 成功: {success}")
    print(f"🔧 sub-m2存在: {has_sub_m2}")
    if has_sub_m2:
        print(f"📍 sub-m2値: '{sub_slots['sub-m2']}'")
    
    return success and has_sub_m2

if __name__ == "__main__":
    success = test_case5()
    print(f"\n{'🎉 テスト成功!' if success else '❌ テスト失敗!'}")
