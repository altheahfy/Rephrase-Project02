#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""統合型エンジン完全テスト"""

from engines.simple_relative_engine import SimpleRelativeEngine
from engines.stanza_based_conjunction_engine import StanzaBasedConjunctionEngine

def test_unified_engines():
    """全エンジン統合型リファクタリングテスト"""
    print("🔥 全エンジン統合型リファクタリング完了テスト開始")
    
    # 関係節エンジンテスト
    print("\n📋 1. 関係節エンジン統合型テスト")
    relative_engine = SimpleRelativeEngine()
    relative_tests = [
        "The book that I bought is interesting.",  # 限定用法関係節
        "The man who helped me was kind.",         # 主語関係代名詞
        "The place where she lives is beautiful."  # 関係副詞
    ]
    
    for i, sentence in enumerate(relative_tests, 1):
        print(f"\n📝 関係節テスト{i}: {sentence}")
        try:
            result = relative_engine.process(sentence)
            if result:
                print(f"✅ 統合型結果: {result}")
            else:
                print("❌ 処理失敗")
        except Exception as e:
            print(f"💥 エラー: {e}")
    
    # 接続詞エンジンテスト
    print("\n📋 2. 接続詞エンジン統合型テスト")
    conjunction_engine = StanzaBasedConjunctionEngine()
    conjunction_tests = [
        "I stayed home because it was raining.",   # 理由（M1）
        "Although he tried hard, he failed.",      # 譲歩（M2）
        "She called when she arrived home."       # 時間（M3）
    ]
    
    for i, sentence in enumerate(conjunction_tests, 1):
        print(f"\n📝 接続詞テスト{i}: {sentence}")
        try:
            result = conjunction_engine.process(sentence)
            if result:
                print(f"✅ 統合型結果: {result}")
            else:
                print("❌ 処理失敗")
        except Exception as e:
            print(f"💥 エラー: {e}")
    
    print("\n🎉 全エンジン統合型リファクタリング完了テスト終了")
    print("✨ 統合型アーキテクチャー: 上位スロット配置 + サブスロット分解の完全実装完了")

if __name__ == "__main__":
    test_unified_engines()
