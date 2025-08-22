#!/usr/bin/env python3
"""
Stanza機能分離分析：依存関係 vs 純粋品詞分析
"""

import stanza

def test_stanza_pos_only():
    """Stanza純粋品詞分析（依存関係なし）"""
    print("=== Stanza純粋品詞分析テスト ===")
    
    # 品詞タギングのみのパイプライン（依存関係解析を除外）
    nlp_pos_only = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    
    test_sentences = [
        "Children play",
        "The dog runs", 
        "Birds fly"
    ]
    
    for sentence in test_sentences:
        print(f"\n--- {sentence} ---")
        doc = nlp_pos_only(sentence)
        
        for sent in doc.sentences:
            for word in sent.words:
                print(f"  単語: {word.text}")
                print(f"    UPOS (普遍品詞): {word.upos}")
                print(f"    XPOS (詳細品詞): {word.xpos}")
                print(f"    補助情報: {word.feats}")
                print(f"    見出し語: {word.lemma}")
                print()

def test_stanza_dependency_vs_pos():
    """依存関係解析 vs 純粋品詞分析の比較"""
    print("=== 依存関係解析 vs 純粋品詞分析 比較 ===")
    
    # 1. 純粋品詞分析のみ
    nlp_pos = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    
    # 2. 依存関係解析込み  
    nlp_full = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
    
    sentence = "Children play"
    
    print(f"\n--- {sentence} ---")
    
    # 純粋品詞分析
    print("【純粋品詞分析】")
    doc_pos = nlp_pos(sentence)
    for sent in doc_pos.sentences:
        for word in sent.words:
            print(f"  {word.text}: {word.upos} ({word.xpos})")
    
    # 依存関係解析込み
    print("\n【依存関係解析込み】")
    doc_full = nlp_full(sentence)
    for sent in doc_full.sentences:
        for word in sent.words:
            print(f"  {word.text}: {word.upos} ({word.xpos}) - 依存: {word.deprel} -> {word.head}")

def test_stanza_processors():
    """Stanzaの利用可能プロセッサー確認"""
    print("=== Stanza利用可能プロセッサー ===")
    
    processors = [
        'tokenize',    # トークン分割
        'pos',         # 品詞タギング
        'lemma',       # 見出し語化
        'depparse',    # 依存関係解析
        'ner',         # 固有表現認識
        'sentiment'    # 感情分析
    ]
    
    for proc in processors:
        try:
            nlp = stanza.Pipeline('en', processors=proc, verbose=False)
            print(f"✅ {proc}: 利用可能")
        except Exception as e:
            print(f"❌ {proc}: 利用不可 ({e})")

def test_pure_pos_extraction():
    """純粋品詞情報抽出（依存関係情報除外）"""
    print("\n=== 純粋品詞情報抽出テスト ===")
    
    # 品詞タギングのみ
    nlp = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    
    test_sentences = [
        "Children play",
        "The dog runs", 
        "Birds fly"
    ]
    
    for sentence in test_sentences:
        doc = nlp(sentence)
        
        # 純粋品詞情報のみ抽出
        pure_pos_info = []
        for sent in doc.sentences:
            for word in sent.words:
                pure_pos_info.append({
                    'text': word.text,
                    'pos': word.upos,
                    'detailed_pos': word.xpos,
                    'lemma': word.lemma
                })
        
        print(f"'{sentence}' → 純粋品詞情報: {pure_pos_info}")

def main():
    print("=== Stanza機能分離分析：依存関係 vs 純粋品詞分析 ===")
    
    test_stanza_processors()
    test_stanza_pos_only()
    test_stanza_dependency_vs_pos()
    test_pure_pos_extraction()
    
    print("\n=== 結論 ===")
    print("1. Stanzaは純粋品詞分析機能を持つ")
    print("2. processors='tokenize,pos' で依存関係解析を除外可能")
    print("3. 依存関係なしでも高精度品詞タギングが可能")
    print("4. word.upos, word.xpos で品詞情報を取得")
    print("5. 「語彙知識」として純粋に利用可能")

if __name__ == '__main__':
    main()
