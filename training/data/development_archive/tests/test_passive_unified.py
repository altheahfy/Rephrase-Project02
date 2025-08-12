#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""受動態エンジン統合型テスト"""

from engines.passive_voice_engine import PassiveVoiceEngine

def test_passive_voice_engine():
    """受動態エンジンテスト"""
    print("🔥 受動態エンジン統合型実装テスト開始")
    
    # テスト文
    test_sentences = [
        "The book was read.",                           # 単純受動態
        "The book was read by him.",                    # by句付き受動態
        "The house is being built.",                    # 進行受動態
        "The work has been completed by the team.",     # 完了受動態 + by句
        "She writes letters."                           # 能動態（対照テスト）
    ]
    
    engine = PassiveVoiceEngine()
    
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
    
    print("\n🎯 受動態エンジン統合型実装テスト終了")

if __name__ == "__main__":
    test_passive_voice_engine()
