#!/usr/bin/env python3
"""
上位スロット分解が本当に動的処理かテスト用の別の文で確認
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pure_stanza_engine_v2 import PureStanzaEngine

def test_different_sentence():
    """全く違う文で上位スロット分解をテスト"""
    engine = PureStanzaEngine()
    
    # 元の例文とは全く違う構造の文
    test_sentences = [
        "I like you.",
        "The cat is sleeping.",
        "She gave him a book yesterday.",
        "Students study English every day."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"🎯 テスト文: {sentence}")
        print(f"{'='*60}")
        
        result = engine.decompose(sentence)
        if result:
            print(f"\n✅ 分解成功: {len(result)}個のスロット検出")
        else:
            print("\n❌ 分解失敗")

if __name__ == "__main__":
    test_different_sentence()
