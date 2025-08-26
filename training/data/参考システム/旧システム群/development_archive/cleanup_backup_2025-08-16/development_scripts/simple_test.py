#!/usr/bin/env python3
"""
軽量テスト - システムの基本動作確認
"""

def test_import():
    """インポートテスト"""
    try:
        print("🔄 システムインポート開始...")
        import torch
        print(f"✅ PyTorch バージョン: {torch.__version__}")
        
        import stanza
        print("✅ Stanza インポート成功")
        
        from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
        print("✅ UnifiedStanzaRephraseMapper インポート成功")
        
        return True
        
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        return False

def simple_test():
    """軽量テスト実行"""
    if not test_import():
        return
    
    print("\n🧪 軽量テスト実行中...")
    try:
        # システム初期化
        mapper = UnifiedStanzaRephraseMapper(log_level='WARNING')  # ログを最小化
        
        # ハンドラー追加
        mapper.add_handler('basic_five_pattern')
        print("✅ 基本ハンドラー準備完了")
        
        # 簡単な例文でテスト
        test_sentence = "I love you."
        print(f"\n📝 テスト例文: {test_sentence}")
        
        result = mapper.process_sentence(test_sentence)
        print(f"✅ 処理成功: {result.get('slots', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

if __name__ == "__main__":
    simple_test()
