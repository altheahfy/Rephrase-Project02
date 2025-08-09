#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test for "I haven't seen you for a long time" parsing issue

import os
import sys
sys.path.append(os.path.dirname(__file__))

try:
    from Rephrase_Parsing_Engine import RephraseParsingEngine
    
    sentence = "I haven't seen you for a long time."
    print(f"問題文: {sentence}")
    print("-" * 60)
    
    parser = RephraseParsingEngine()
    result = parser.analyze_sentence(sentence)
    
    print("=== パーサー結果 ===")
    if result:
        if isinstance(result, dict):
            for slot, data in result.items():
                if isinstance(data, list) and len(data) > 0:
                    value = data[0].get('value', '')
                    slot_type = data[0].get('type', '')
                    print(f"  {slot}: '{value}' → type='{slot_type}'")
        print(f"\n総スロット数: {len(result)}")
        
        # 問題箇所をチェック
        if 'V' in result:
            v_value = result['V'][0]['value'] if result['V'] else ''
            if v_value == "haven't":
                print("❌ 問題: haven't がVになっています")
            elif 'seen' in v_value:
                print("✅ OK: seen が含まれています")
        
        if 'O1' in result:
            o1_value = result['O1'][0]['value'] if result['O1'] else ''
            if 'for a long time' in o1_value:
                print("❌ 問題: 'for a long time' がO1になっています")
        
        # spaCy認識テスト
        print("\n=== spaCy語彙認識テスト ===")
        if parser.nlp:
            doc = parser.nlp(sentence)
            for token in doc:
                if token.text.lower() == 'seen':
                    print(f"✅ 'seen' 認識: pos={token.pos_}, lemma={token.lemma_}, is_oov={token.is_oov}")
                    break
            else:
                print("❌ 'seen' が認識されていません")
        else:
            print("❌ spaCy利用不可")
    else:
        print("❌ 構文解析失敗")
        
except Exception as e:
    print(f"エラー: {e}")
    import traceback
    traceback.print_exc()
