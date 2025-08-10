#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
所有格代名詞テスト - 現在のエンジンの処理確認
"""

import sys
sys.path.append('.')
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_possessive_pronouns():
    """所有格代名詞を含む文のテスト"""
    print("=== 所有格代名詞処理テスト ===\n")
    
    # テスト文
    test_sentences = [
        "He resembles his mother.",
        "She resembles her father.", 
        "Tom resembles his uncle.",
        "They resemble their parents."
    ]
    
    # エンジン初期化
    engine = CompleteRephraseParsingEngine()
    
    for sentence in test_sentences:
        print(f"テスト文: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # メインスロットの確認
            slots = result.get('rephrase_slots', {})
            print(f"  S: {slots.get('S', [])}")
            print(f"  V: {[v.get('value') if isinstance(v, dict) else v for v in slots.get('V', [])]}")
            print(f"  O1: {[o.get('value') if isinstance(o, dict) else o for o in slots.get('O1', [])]}")
            print(f"  O2: {slots.get('O2', [])}")
            print(f"  C1: {slots.get('C1', [])}")
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
        
        print()

if __name__ == "__main__":
    test_possessive_pronouns()
