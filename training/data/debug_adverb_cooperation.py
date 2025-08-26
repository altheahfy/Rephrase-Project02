#!/usr/bin/env python3
"""デバッグ：AdverbHandlerとの連携確認"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relative_clause_handler import RelativeClauseHandler
from adverb_handler import AdverbHandler
import json

def debug_adverb_cooperation():
    """AdverbHandlerとの連携をデバッグ"""
    
    # AdverbHandlerを単体でテスト
    adverb_handler = AdverbHandler()
    test_text = "which lies there"
    
    print("🔍 AdverbHandler単体テスト:")
    print(f"入力: '{test_text}'")
    adverb_result = adverb_handler.process(test_text)
    print("結果:")
    print(json.dumps(adverb_result, indent=2, ensure_ascii=False))
    
    # RelativeClauseHandlerでの使用確認
    print("\n🔍 RelativeClauseHandler内での連携テスト:")
    collaborators = {
        'AdverbHandler': adverb_handler
    }
    
    rel_handler = RelativeClauseHandler(collaborators=collaborators)
    
    # 関係節分析のみテスト
    full_text = "The book which lies there"
    analysis = rel_handler._analyze_relative_clause(full_text, 'which')
    
    print("_analyze_relative_clause結果:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # 修飾語情報の有無を確認
    modifiers = analysis.get('modifiers', {})
    print(f"\n📍 修飾語情報: {modifiers}")
    print(f"📍 M2存在: {'M2' in modifiers}")

if __name__ == "__main__":
    debug_adverb_cooperation()
