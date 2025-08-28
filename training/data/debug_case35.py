#!/usr/bin/env python3
"""
ケース35: whose修飾語デバッグ専用スクリプト
問題: "efficiently"がsub-m2に取得されない
"""

import sys
import os
import json
sys.path.append('.')

from central_controller import CentralController

def debug_case35():
    """ケース35の詳細デバッグ"""
    
    # テストケース
    test_sentence = "The teacher whose class runs efficiently is respected greatly."
    
    print("="*60)
    print(f"📋 ケース35デバッグ: '{test_sentence}'")
    print("="*60)
    
    # CentralController初期化
    controller = CentralController()
    
    # 関係代名詞ハンドラーを直接使用
    rel_handler = controller.relative_clause_handler
    
    # spaCy解析
    doc = rel_handler.nlp(test_sentence)
    print(f"\n🔍 spaCy解析結果:")
    for i, token in enumerate(doc):
        print(f"  {i}: {token.text} | POS: {token.pos_} | TAG: {token.tag_} | DEP: {token.dep_} | HEAD: {token.head.text}")
    
    # whose構造解析
    print(f"\n🔍 whose構造解析:")
    whose_info = rel_handler._analyze_whose_structure(doc)
    print(f"  結果: {whose_info}")
    
    # 協力者による分析
    print(f"\n🔍 協力者による分析:")
    analysis = rel_handler._analyze_relative_clause(test_sentence, 'whose')
    print(f"  成功: {analysis.get('success')}")
    print(f"  修飾語: {analysis.get('modifiers', {})}")
    print(f"  構造分析: {analysis.get('structure_analysis')}")
    
    # AdverbHandlerの直接テスト
    if rel_handler.adverb_handler:
        print(f"\n🔍 AdverbHandler直接テスト:")
        # 関係節部分を抽出
        clause_text = "whose class runs efficiently"
        adverb_result = rel_handler.adverb_handler.process(clause_text)
        print(f"  入力: '{clause_text}'")
        print(f"  結果: {adverb_result}")
    
    # 最終的な_process_whose実行
    print(f"\n🔍 _process_whose最終実行:")
    result = rel_handler._process_whose(test_sentence)
    print(f"  結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result

if __name__ == "__main__":
    debug_case35()
