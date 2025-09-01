#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 119 名詞節検出デバッグスクリプト
"It depends on if you agree." の名詞節処理問題を詳細分析
"""

import spacy
from noun_clause_handler import NounClauseHandler

def debug_case119_noun_clause():
    """Case 119の名詞節検出を詳細デバッグ"""
    print("=" * 60)
    print("Case 119: 名詞節検出詳細デバッグ")
    print("=" * 60)
    
    sentence = "It depends on if you agree."
    
    # spaCy解析
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    
    print(f"\n📝 原文: {sentence}")
    
    print(f"\n🔍 spaCy解析結果:")
    for i, token in enumerate(doc):
        print(f"  [{i}] {token.text:12} | pos={token.pos_:8} | dep={token.dep_:12} | head={token.head.text:10} | head_idx={token.head.i}")
    
    # NounClauseHandler初期化
    noun_handler = NounClauseHandler(nlp)
    
    print(f"\n🔍 NounClauseHandler.detect_noun_clauses():")
    detected_clauses = noun_handler.detect_noun_clauses(sentence)
    print(f"検出結果: {detected_clauses}")
    
    if detected_clauses:
        print(f"\n🎯 検出された名詞節:")
        for i, clause in enumerate(detected_clauses):
            print(f"  節{i+1}: {clause}")
    else:
        print(f"\n❌ 名詞節が検出されませんでした")
    
    print(f"\n🔍 NounClauseHandler.process():")
    process_result = noun_handler.process(sentence)
    print(f"処理結果: {process_result}")
    
    if process_result.get('success'):
        print(f"\n✅ 名詞節処理成功:")
        print(f"  main_slots: {process_result.get('main_slots', {})}")
        print(f"  sub_slots: {process_result.get('sub_slots', {})}")
    else:
        print(f"\n❌ 名詞節処理失敗:")
        print(f"  error: {process_result.get('error', 'Unknown error')}")
    
    # 手動での内部メソッド確認
    print(f"\n🔍 内部メソッド直接テスト:")
    doc = nlp(sentence)
    
    # _detect_noun_clauses を直接呼び出し
    print(f"  _detect_noun_clauses():")
    internal_result = noun_handler._detect_noun_clauses(doc, sentence)
    print(f"  結果: {internal_result}")
    
    # _detect_by_pos_analysis を直接呼び出し
    print(f"  _detect_by_pos_analysis():")
    pos_result = noun_handler._detect_by_pos_analysis(doc, sentence)
    print(f"  結果: {pos_result}")

if __name__ == "__main__":
    debug_case119_noun_clause()
