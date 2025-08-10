#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import json

# エンジンを初期化
engine = CompleteRephraseParsingEngine()

# テスト文
test_sentence = "Where did you get it?"

print(f"=== テスト文: {test_sentence} ===")

# 文を解析
result = engine.analyze_sentence(test_sentence)

# 結果を表示
print("\n📋 スロット分析:")
print(f"結果の型: {type(result)}")
print(f"結果のキー: {list(result.keys()) if isinstance(result, dict) else 'Dictではない'}")

# main_slotsキーがあるかチェック
if 'main_slots' in result:
    main_slots = result['main_slots']
    print(f"main_slotsの型: {type(main_slots)}")
    print(f"main_slotsのキー: {list(main_slots.keys()) if isinstance(main_slots, dict) else 'Dictではない'}")
    
    for slot, values in main_slots.items():
        if values and slot in ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']:
            print(f"\n  {slot}:")
            for value in values:
                print(f"    - '{value}'")
else:
    # 直接的なスロット構造の場合
    slot_keys = [k for k in result.keys() if k in ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']]
    if slot_keys:
        print("直接スロット構造:")
        for slot in slot_keys:
            values = result[slot]
            if values:
                print(f"\n  {slot}:")
                for value in values:
                    print(f"    - '{value}'")

# whereの分類確認
where_found = False

# main_slotsの中を検索
if 'main_slots' in result:
    for slot, values in result['main_slots'].items():
        if values and any('where' in str(value).lower() for value in values):
            print(f"\n🔍 'where' の分類確認:")
            print(f"  ✅ 'where' が {slot} に分類されています: {values}")
            where_found = True
else:
    # 直接的なスロット構造の場合
    for slot, values in result.items():
        if values and any('where' in str(value).lower() for value in values):
            print(f"\n🔍 'where' の分類確認:")
            print(f"  ✅ 'where' が {slot} に分類されています: {values}")
            where_found = True

if not where_found:
    print(f"\n❌ 'where' がどのスロットにも分類されていません")
    
    # 実際のM3スロットの内容を確認
    m3_content = None
    if 'main_slots' in result and 'M3' in result['main_slots']:
        m3_content = result['main_slots']['M3']
    elif 'M3' in result:
        m3_content = result['M3']
    
    if m3_content:
        print(f"  M3スロットの内容: {m3_content}")
    
    # spaCy解析結果を確認
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(test_sentence)
    
    print(f"\n🔍 spaCy解析結果:")
    for token in doc:
        print(f"  '{token.text}' [POS: {token.pos_}, Tag: {token.tag_}, Dep: ('{token.dep_}', '{token.dep_}'), Head: {token.head.text}]")
