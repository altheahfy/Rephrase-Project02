#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 119専用デバッグスクリプト
"It depends on if you agree." の名詞節処理問題を分析
"""

import spacy
from central_controller import CentralController

def debug_case119():
    """Case 119の詳細デバッグ"""
    print("=" * 60)
    print("Case 119: 'It depends on if you agree.' デバッグ分析")
    print("=" * 60)
    
    sentence = "It depends on if you agree."
    
    # spaCy解析
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    
    print(f"\n📝 原文: {sentence}")
    print(f"📝 予想: S='It', V='depends', M2='', sub-s='on if you', sub-v='agree'")
    
    print("\n🔍 spaCy解析結果:")
    for i, token in enumerate(doc):
        print(f"  [{i}] {token.text:12} | pos={token.pos_:8} | dep={token.dep_:12} | head={token.head.text:10} | head_idx={token.head.i}")
    
    print("\n🔍 依存関係ツリー:")
    for token in doc:
        children = [child.text for child in token.children]
        print(f"  {token.text} -> {children}")
    
    # "if" トークンの詳細分析
    if_token = None
    for token in doc:
        if token.text.lower() == "if":
            if_token = token
            break
    
    if if_token:
        print(f"\n🎯 'if'トークンの詳細:")
        print(f"  位置: {if_token.i}")
        print(f"  品詞: {if_token.pos_}")
        print(f"  依存関係: {if_token.dep_}")
        print(f"  ヘッド: {if_token.head.text} (位置: {if_token.head.i})")
        print(f"  子要素: {[child.text for child in if_token.children]}")
    
    # 前置詞 "on" の分析
    on_token = None
    for token in doc:
        if token.text.lower() == "on":
            on_token = token
            break
    
    if on_token:
        print(f"\n🎯 'on'前置詞の詳細:")
        print(f"  位置: {on_token.i}")
        print(f"  品詞: {on_token.pos_}")
        print(f"  依存関係: {on_token.dep_}")
        print(f"  ヘッド: {on_token.head.text} (位置: {on_token.head.i})")
        print(f"  子要素: {[child.text for child in on_token.children]}")
    
    # CentralController での実際の処理結果
    print("\n🎯 CentralController処理結果:")
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print(f"  成功: {result.get('success', False)}")
    print(f"  メイン・スロット:")
    main_slots = result.get('main_slots', {})
    for slot, value in main_slots.items():
        print(f"    {slot}: '{value}'")
    
    print(f"  サブ・スロット:")
    sub_slots = result.get('sub_slots', {})
    for slot, value in sub_slots.items():
        print(f"    {slot}: '{value}'")
    
    print(f"  ハンドラー: {result.get('metadata', {}).get('primary_handler', 'unknown')}")
    
    return result

if __name__ == "__main__":
    debug_case119()
