#!/usr/bin/env python3
"""
簡単なシステムテスト - PyTorchエラー回避版
"""

import sys
import os

# Stanzaライブラリの問題を回避するため、軽量テストから開始
def simple_test():
    """単純な動作確認テスト"""
    try:
        print("🔧 システム初期化テスト開始...")
        
        # まずインポートテスト
        print("📦 ライブラリインポートテスト...")
        from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
        print("✅ UnifiedStanzaRephraseMapperインポート成功")
        
        # 初期化テスト
        print("🚀 システム初期化テスト...")
        mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
        print("✅ システム初期化成功")
        
        # ハンドラー追加テスト
        print("🔧 ハンドラー追加テスト...")
        mapper.add_handler('basic_five_pattern')
        mapper.add_handler('relative_clause')
        mapper.add_handler('passive_voice')
        mapper.add_handler('adverbial_modifier')
        print("✅ 4ハンドラー追加成功")
        
        # 簡単な例文テスト
        print("📝 簡単な例文テスト...")
        test_sentence = "I love you."
        result = mapper.process(test_sentence)
        
        print(f"例文: {test_sentence}")
        print(f"結果: {result.get('slots', {})}")
        print(f"サブスロット: {result.get('sub_slots', {})}")
        print("✅ 基本テスト成功")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n🎉 基本システムテスト完了 - 次のステップに進めます")
    else:
        print("\n⚠️ システムに問題があります")
