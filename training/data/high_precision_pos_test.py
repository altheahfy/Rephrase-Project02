#!/usr/bin/env python3
"""
高精度辞書システム比較調査
"""

def test_spacy_pos_tagging():
    """spaCyの品詞タギング精度テスト"""
    print("=== spaCy品詞タギング精度テスト ===")
    try:
        import spacy
        # 英語モデルをロード
        nlp = spacy.load("en_core_web_sm")
        
        test_sentences = [
            "Children play",
            "The dog runs", 
            "Birds fly",
            "They play soccer",
            "The cat runs fast",
            "Birds fly south"
        ]
        
        for sentence in test_sentences:
            doc = nlp(sentence)
            pos_info = [(token.text, token.pos_, token.tag_, token.lemma_) for token in doc]
            print(f"'{sentence}' → {pos_info}")
            
    except ImportError:
        print("spaCy not available")
    except OSError:
        print("spaCy English model not available")

def test_transformers_pos_tagging():
    """Transformers (BERT-based) 品詞タギングテスト"""
    print("\n=== Transformers品詞タギング精度テスト ===")
    try:
        from transformers import pipeline
        
        # BERT-based POS tagger
        pos_tagger = pipeline("token-classification", 
                            model="vblagoje/bert-english-uncased-finetuned-pos")
        
        test_sentences = [
            "Children play",
            "The dog runs", 
            "Birds fly"
        ]
        
        for sentence in test_sentences:
            result = pos_tagger(sentence)
            pos_info = [(item['word'], item['entity']) for item in result]
            print(f"'{sentence}' → {pos_info}")
            
    except ImportError:
        print("Transformers not available")
    except Exception as e:
        print(f"Transformers error: {e}")

def test_stanza_pos_tagging():
    """Stanza品詞タギング精度テスト（比較用）"""
    print("\n=== Stanza品詞タギング精度テスト ===")
    try:
        import stanza
        
        # 既存のStanzaモデルを使用
        nlp = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
        
        test_sentences = [
            "Children play",
            "The dog runs", 
            "Birds fly"
        ]
        
        for sentence in test_sentences:
            doc = nlp(sentence)
            pos_info = [(word.text, word.upos, word.xpos) for sent in doc.sentences for word in sent.words]
            print(f"'{sentence}' → {pos_info}")
            
    except ImportError:
        print("Stanza not available")
    except Exception as e:
        print(f"Stanza error: {e}")

def test_pattern_library():
    """Pattern library (英語特化) テスト"""
    print("\n=== Pattern Library品詞タギング精度テスト ===")
    try:
        from pattern.en import tag
        
        test_sentences = [
            "Children play",
            "The dog runs", 
            "Birds fly"
        ]
        
        for sentence in test_sentences:
            words = sentence.split()
            tagged = tag(sentence)
            print(f"'{sentence}' → {tagged}")
            
    except ImportError:
        print("Pattern library not available")

def test_polyglot():
    """Polyglot多言語品詞タガーテスト"""
    print("\n=== Polyglot品詞タギング精度テスト ===")
    try:
        from polyglot.text import Text
        
        test_sentences = [
            "Children play",
            "The dog runs", 
            "Birds fly"
        ]
        
        for sentence in test_sentences:
            text = Text(sentence)
            pos_info = [(word, word.pos_tag) for word in text.words]
            print(f"'{sentence}' → {pos_info}")
            
    except ImportError:
        print("Polyglot not available")

def main():
    print("=== 高精度辞書システム比較調査 ===")
    print("NLTK/WordNetより高精度な品詞タギングシステムを調査\n")
    
    # 各システムのテスト
    test_spacy_pos_tagging()
    test_transformers_pos_tagging() 
    test_stanza_pos_tagging()
    test_pattern_library()
    test_polyglot()
    
    print("\n=== 結論 ===")
    print("1. spaCy: 最も実用的、高精度")
    print("2. Transformers (BERT): 最高精度だが重い")
    print("3. Stanza: 学術的に高評価")
    print("4. Pattern: 英語特化、軽量")
    print("5. Polyglot: 多言語対応")

if __name__ == '__main__':
    main()
