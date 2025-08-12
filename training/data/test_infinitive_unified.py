#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不定詞エンジン統合型テスト"""

from engines.infinitive_engine import InfinitiveEngine
import stanza

def test_infinitive_engine():
    """不定詞エンジンテスト"""
    print("🔥 不定詞エンジン統合型リファクタリングテスト開始")
    
    # テスト文
    test_sentences = [
        "To learn is important.",      # 主語不定詞
        "He decided to go home.",      # 目的語不定詞  
        "She came to help us.",        # 副詞的不定詞
        "I have work to finish."       # 形容詞修飾不定詞
    ]
    
    engine = InfinitiveEngine()
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト{i}: {sentence}")
        try:
            result = engine.process(sentence)
            if result:
                print(f"✅ 統合型結果: {result}")
            else:
                print("❌ 処理失敗")
        except Exception as e:
            print(f"💥 エラー: {e}")
    
    print("\n🎯 不定詞エンジン統合型リファクタリング完了テスト終了")

if __name__ == "__main__":
    test_infinitive_engine()
