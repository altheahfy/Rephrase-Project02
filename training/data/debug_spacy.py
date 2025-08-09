import warnings
warnings.filterwarnings('ignore')

print("=== spaCy動作確認 ===")
try:
    import spacy
    print(f"spaCy version: {spacy.__version__}")
    
    # モデル読み込みテスト
    nlp = spacy.load("en_core_web_sm")
    print("✅ en_core_web_sm モデル読み込み成功")
    
    # 簡単な解析テスト
    test_text = "He has recovered quickly"
    doc = nlp(test_text)
    
    print(f"\n=== '{test_text}' の解析結果 ===")
    for token in doc:
        print(f"単語: {token.text}")
        print(f"  lemma: {token.lemma_}")
        print(f"  POS: {token.pos_}")
        print(f"  is_oov (未知語): {token.is_oov}")
        print(f"  is_alpha: {token.is_alpha}")
        print("---")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()
