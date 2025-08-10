#!/usr/bin/env python3
"""
CompleteRephraseParsingEngineの動作診断テスト
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import traceback

def test_current_system():
    print("🔍 現在システム動作診断開始")
    
    try:
        engine = CompleteRephraseParsingEngine()
        print("✅ エンジン初期化成功")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        traceback.print_exc()
        return
    
    # シンプルなテスト文
    test_sentences = [
        "He resembles his mother.",
        "I love cats.",
        "The book is red."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 テスト文: '{sentence}'")
        try:
            result = engine.parse_sentence(sentence)
            print(f"✅ 解析成功:")
            print(f"  スロット: {result.get('slots', {})}")
            print(f"  適用ルール: {result.get('rules_applied', [])}")
            print(f"  文型: {result.get('sentence_pattern', '')}")
        except Exception as e:
            print(f"❌ 解析失敗: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    test_current_system()
