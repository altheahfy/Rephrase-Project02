#!/usr/bin/env python3
"""
ケース8専用デバッグ: that関係節の目的語型処理
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def debug_case8():
    """ケース8: 'The car that he drives is new.' の詳細デバッグ"""
    
    sentence = "The car that he drives is new."
    print(f"🔍 ケース8デバッグ: '{sentence}'")
    print("=" * 60)
    
    controller = CentralController()
    
    # 関係節ハンドラーを直接呼び出してデバッグ
    relative_handler = controller.handlers['relative_clause']
    
    print(f"🔍 関係節ハンドラー直接呼び出し:")
    
    # _analyze_relative_clause を直接テスト
    print(f"🔍 _analyze_relative_clause テスト:")
    analysis_result = relative_handler._analyze_relative_clause(sentence, 'that')
    print(f"  success: {analysis_result.get('success')}")
    print(f"  antecedent: {analysis_result.get('antecedent')}")
    print(f"  relative_verb: {analysis_result.get('relative_verb')}")
    
    # _process_that を直接テスト
    print(f"\n🔍 _process_that テスト:")
    that_result = relative_handler._process_that(sentence)
    print(f"📊 _process_that結果:")
    print(json.dumps(that_result, ensure_ascii=False, indent=2))
    
    print(f"\n🔍 process 全体テスト:")
    result = relative_handler.process(sentence)
    
    print(f"📊 関係節ハンドラー結果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print(f"\n🔍 spaCy解析:")
    doc = relative_handler.nlp(sentence)
    for i, token in enumerate(doc):
        print(f"  {i}: '{token.text}' (POS={token.pos_}, DEP={token.dep_}, HEAD={token.head.text})")

if __name__ == "__main__":
    debug_case8()
