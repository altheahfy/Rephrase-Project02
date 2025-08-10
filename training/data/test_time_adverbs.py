#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
時間副詞句テスト - ago重複・前置詞欠落問題の検証
"""

import sys
sys.path.append('.')
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_time_adverbs():
    """時間副詞句の処理テスト"""
    print("=== 時間副詞句処理テスト ===\n")
    
    # テスト文
    test_sentences = [
        "I met him a few days ago.",
        "She worked there for 2 years.",
        "He left 3 weeks ago.",
        "They lived here for many years.",
        "We started this project 2 months ago."
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
            print(f"  M1: {slots.get('M1', [])}")
            print(f"  M2: {[m.get('value') if isinstance(m, dict) else m for m in slots.get('M2', [])]}")
            print(f"  M3: {[m.get('value') if isinstance(m, dict) else m for m in slots.get('M3', [])]}")
            
            # enhanced_dataの確認（前置詞句情報）
            enhanced = result.get('enhanced_data', {})
            prep_phrases = enhanced.get('prep_phrases', [])
            if prep_phrases:
                print(f"  前置詞句: {prep_phrases}")
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
        
        print()

if __name__ == "__main__":
    test_time_adverbs()
