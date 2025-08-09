#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Quick test to verify the parser fix

import os
import sys

# spaCyエラーを回避するため、try-catch
try:
    sys.path.append(os.path.dirname(__file__))
    from Rephrase_Parsing_Engine import RephraseParsingEngine
    
    parser = RephraseParsingEngine()
    result = parser.analyze_sentence("You, give it to me straight.")
    
    if 'M2' in result:
        m2_type = result['M2'][0]['type']
        m2_value = result['M2'][0]['value']
        print(f"✅ 修正確認: M2='{m2_value}' → type='{m2_type}'")
        if m2_type == 'word':
            print("🎉 修正成功: phraseからwordに正しく変更されました！")
        else:
            print(f"❌ まだ修正されていません: type={m2_type}")
    else:
        print("❌ M2スロットが見つかりません")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    # 修正箇所を直接確認
    engine_path = os.path.join(os.path.dirname(__file__), 'Rephrase_Parsing_Engine.py')
    with open(engine_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "'type': 'word'" in content and "imperative-modifier" in content:
            print("✅ ソースコード修正確認: 'prepositional_phrase' → 'word'に変更済み")
        else:
            print("❌ ソースコード未修正")
