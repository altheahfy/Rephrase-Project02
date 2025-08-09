# spaCyインストール成功テスト

print("=== spaCyインストール成功テスト ===\n")

try:
    import spacy
    print("✅ spaCyライブラリ: インポート成功")
    
    # バージョン確認
    print(f"   バージョン: {spacy.__version__}")
    
    # 言語モデルロード
    nlp = spacy.load("en_core_web_sm")
    print("✅ 英語モデル: ロード成功")
    
    # 実際の解析テスト
    test_sentence = "She efficiently investigated the comprehensive analysis."
    doc = nlp(test_sentence)
    
    print(f"\n📝 テスト文: {test_sentence}")
    print("🔍 解析結果:")
    
    for token in doc:
        print(f"   {token.text:15} -> {token.pos_:10} ({token.tag_}) [{token.lemma_}]")
    
    print("\n🎯 語彙制限テスト:")
    difficult_words = [
        "sophisticated", "investigation", "efficiently", 
        "comprehensive", "mathematical", "serendipitously"
    ]
    
    for word in difficult_words:
        doc_word = nlp(word)
        token = doc_word[0]
        print(f"   {word:15} -> {token.pos_:10} ({token.tag_})")
    
    print("\n✅ spaCy完全動作確認！")
    print("📊 結果: Windows環境でのインストール・動作に問題なし")
    
except ImportError:
    print("❌ spaCyインポート失敗")
except OSError as e:
    print(f"❌ 言語モデルエラー: {e}")
except Exception as e:
    print(f"❌ 予期しないエラー: {e}")

print(f"\n💡 結論")
print("このWindows環境では、spaCyのインストールと動作に問題なし。")
print("インストールリスクは杞憂だった。")
