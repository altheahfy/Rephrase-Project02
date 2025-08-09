#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test script for "give it to me straight" parsing issue

import os
import sys

# プロジェクトのdataディレクトリをパスに追加
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

def test_give_straight_sentences():
    """「give it to me straight」シリーズのテスト"""
    
    # テスト対象文
    test_sentences = [
        "You, give it to me straight.",
        "You, give it to him straight.", 
        "You, give it to her straight.",
        "You, give it to them straight."
    ]
    
    print("=== Give It Straight シリーズ解析テスト ===")
    
    # パーサー初期化
    parser = RephraseParsingEngine()
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【テスト{i}】: {sentence}")
        print("-" * 60)
        
        # 構文解析実行
        result = parser.analyze_sentence(sentence)
        
        if result:
            print(f"構文解析成功: {len(result)} スロット")
            
            # 結果がリストの場合とタプルの場合を処理
            if isinstance(result, tuple):
                slots_data = result[0]  # 通常は (slots, examples) の形式
            else:
                slots_data = result
            
            for slot in slots_data:
                if isinstance(slot, dict):
                    phrase_type = slot.get('PhraseType', 'unknown')
                    slot_phrase = slot.get('SlotPhrase', '')
                    slot_name = slot.get('Slot', '')
                    
                    # 「to me」「to him」等のチェック
                    if 'to ' in slot_phrase and slot_name == 'M2':
                        status = "❌ PHRASE" if phrase_type == "phrase" else "✅ WORD"
                        print(f"  {slot_name}: '{slot_phrase}' → {phrase_type} {status}")
                    else:
                        print(f"  {slot_name}: '{slot_phrase}' → {phrase_type}")
                else:
                    print(f"  不正なスロット形式: {slot}")
        else:
            print("❌ 構文解析失敗")

if __name__ == "__main__":
    test_give_straight_sentences()
