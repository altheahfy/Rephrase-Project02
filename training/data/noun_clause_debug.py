#!/usr/bin/env python3
"""
名詞節ハンドラーのデバッグ用スクリプト
失敗ケースの詳細分析
"""

import spacy
from noun_clause_handler import NounClauseHandler
from central_controller import CentralController

def debug_single_case(sentence):
    """個別ケースのデバッグ"""
    print(f"\n🔍 デバッグ開始: '{sentence}'")
    print("="*60)
    
    # 1. CentralControllerでの検出確認
    controller = CentralController()
    patterns = controller.analyze_grammar_structure(sentence)
    print(f"📋 検出されたパターン: {patterns}")
    
    # 2. NounClauseHandlerの直接テスト
    nlp = spacy.load('en_core_web_sm')
    noun_handler = NounClauseHandler(nlp)
    
    # 検出テスト
    clauses = noun_handler.detect_noun_clauses(sentence)
    print(f"🎯 名詞節検出結果: {clauses}")
    
    # 処理テスト
    result = noun_handler.process(sentence)
    print(f"🏗️ 処理結果: {result}")
    
    # 3. spaCy解析の詳細表示
    doc = nlp(sentence)
    print(f"\n📊 spaCy詳細解析:")
    for token in doc:
        print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}")
    
    print("="*60)

def main():
    """失敗ケースのデバッグ実行"""
    
    # 失敗ケース
    failure_cases = [
        "I know what you mean.",  # ケース122: wh-節
        "She doesn't know whether he will come.",  # ケース123: whether節 + 助動詞
        "I wonder where she lives.",  # ケース124: where節
        "That you are here is wonderful.",  # ケース125: that主語節
        "Tell me who came to the party.",  # ケース126: wh-主語節
        "It depends on if you agree.",  # ケース127: if節 
        "I understand how important this is."  # ケース128: how節
    ]
    
    # 成功ケース（比較用）
    success_case = "I believe that he is smart."  # ケース121: that節
    
    print("🎯 成功ケース（比較用）:")
    debug_single_case(success_case)
    
    print("\n" + "="*80)
    print("❌ 失敗ケース詳細分析:")
    
    for i, case in enumerate(failure_cases, 122):
        print(f"\n🔴 ケース{i}: {case}")
        debug_single_case(case)

if __name__ == "__main__":
    main()
