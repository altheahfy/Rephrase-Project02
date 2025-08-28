#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from central_controller import CentralController

def debug_case12():
    """ケース12の構造分析デバッグ"""
    
    # コントローラー初期化
    controller = CentralController()
    
    # テスト例文
    sentence = "The man whose car is red lives here."
    
    print(f"🔍 ケース12デバッグ: '{sentence}'")
    print("=" * 60)
    
    # 処理実行
    result = controller.process_sentence(sentence)
    
    print(f"\n📊 最終結果:")
    print(f"✅ 成功: {result.get('success')}")
    print(f"📍 main_slots: {result.get('main_slots', {})}")
    print(f"📍 sub_slots: {result.get('sub_slots', {})}")
    
    # 関係節ハンドラーのデバッグ（構造分析結果）
    print(f"\n🔍 構造分析デバッグ:")
    relative_handler = controller.handlers['relative_clause']
    five_pattern_handler = controller.handlers['basic_five_pattern']
    
    # 関係節部分だけを分析
    clause_text = "car is red"
    print(f"🎯 関係節部分分析: '{clause_text}'")
    
    if five_pattern_handler:
        structure_result = five_pattern_handler.process(clause_text)
        print(f"📊 5文型解析結果: {structure_result}")
    else:
        print("⚠️ 5文型ハンドラーが見つかりません")
    
    # より詳細な関係節分析
    print(f"\n🔍 関係節内部分析:")
    analysis = relative_handler._analyze_relative_clause(sentence, 'whose')
    print(f"📊 関係節分析結果:")
    print(f"  - structure_analysis: {analysis.get('structure_analysis', {})}")
    print(f"  - modifiers: {analysis.get('modifiers', {})}")
    print(f"  - passive_analysis: {analysis.get('passive_analysis', {})}")
    
    # original_clause_text の抽出確認
    print(f"\n🔍 関係節テキスト抽出:")
    original_clause_text = relative_handler._extract_relative_clause_text_original(sentence, 'whose')
    print(f"📊 抽出されたテキスト: '{original_clause_text}'")
    
    # デバッグ用：spaCy解析の詳細
    print(f"\n🔍 spaCy解析詳細:")
    doc = relative_handler.nlp(sentence)
    for i, token in enumerate(doc):
        print(f"  {i}: '{token.text}' (POS={token.pos_}, DEP={token.dep_})")
    
    # whose位置と主節動詞位置の確認
    whose_idx = None
    main_root_idx = None
    for i, token in enumerate(doc):
        if token.text.lower() == 'whose':
            whose_idx = i
        if token.dep_ == 'ROOT':
            main_root_idx = i
    
    print(f"📊 whose位置: {whose_idx}, 主節動詞位置: {main_root_idx}")
    
    # cleaned_clause の確認 
    print(f"\n🔍 副詞除去処理:")
    cleaned_clause = original_clause_text
    adverb_handler = controller.handlers['adverb']
    if adverb_handler and original_clause_text:
        adverb_result = adverb_handler.process(original_clause_text)
        print(f"📊 副詞ハンドラー結果: {adverb_result}")
        if adverb_result.get('success'):
            cleaned_clause = adverb_result.get('separated_text', original_clause_text)
            print(f"📊 クリーンされたテキスト: '{cleaned_clause}'")
    
    # cleaned_clause で5文型分析
    print(f"\n🔍 クリーンテキストで5文型分析:")
    if cleaned_clause:
        structure_result = five_pattern_handler.process(cleaned_clause)
        print(f"📊 クリーンテキスト構造分析: {structure_result}")
    

if __name__ == "__main__":
    debug_case12()
