#!/usr/bin/env python3
"""
システム動作確認テスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_basic_system():
    print("🧪 システム動作確認テスト")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper()
    print("✅ システム初期化完了")
    
    # 基本的な文をテスト
    test_sentences = [
        "The car is red.",
        "I love you.", 
        "She works carefully."
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 テスト: {sentence}")
        result = mapper.process(sentence)
        print(f"   結果: {result}")
        
        if result.get('slots'):
            print(f"   スロット検出数: {len(result['slots'])}")
            for slot, value in result['slots'].items():
                print(f"     {slot}: {value}")
        else:
            print("   ⚠️ スロットが検出されませんでした")

if __name__ == "__main__":
    test_basic_system()
