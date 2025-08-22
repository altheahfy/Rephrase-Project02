#!/usr/bin/env python3
"""
Stanza vs spaCy 品詞分析精度比較テスト
"""

import stanza
import spacy

def compare_pos_accuracy():
    """品詞分析精度の詳細比較"""
    print("=== Stanza vs spaCy 品詞分析精度比較 ===\n")
    
    # Stanza初期化（品詞分析のみ）
    stanza_nlp = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    
    # spaCy初期化
    spacy_nlp = spacy.load("en_core_web_sm")
    
    # テストケース（品詞判定が難しい例を含む）
    test_cases = [
        # 基本的なケース
        "Children play",
        "The dog runs", 
        "Birds fly",
        
        # 品詞曖昧性が高いケース
        "They play soccer",
        "I watch the play",
        "She runs daily",
        "Home runs are exciting",
        "Time flies",
        "House flies buzz",
        
        # より複雑なケース
        "Running water flows",
        "The running man",
        "She is running",
        "Fast cars drive",
        "He drives fast",
        "The fast is over",
        
        # 過去分詞・現在分詞の曖昧性
        "Broken glass falls",
        "The glass is broken",
        "Flying birds migrate",
        "The plane is flying",
    ]
    
    comparison_results = []
    
    for sentence in test_cases:
        print(f"--- '{sentence}' ---")
        
        # Stanza分析
        stanza_doc = stanza_nlp(sentence)
        stanza_pos = []
        for sent in stanza_doc.sentences:
            for word in sent.words:
                stanza_pos.append((word.text, word.upos, word.xpos))
        
        # spaCy分析
        spacy_doc = spacy_nlp(sentence)
        spacy_pos = [(token.text, token.pos_, token.tag_) for token in spacy_doc]
        
        print(f"Stanza: {stanza_pos}")
        print(f"spaCy:  {spacy_pos}")
        
        # 一致度チェック
        agreement = compare_pos_tags(stanza_pos, spacy_pos)
        print(f"一致度: {agreement['total_agreement']:.1%} ({agreement['agreements']}/{agreement['total']})")
        
        if agreement['differences']:
            print("相違点:")
            for diff in agreement['differences']:
                print(f"  {diff}")
        
        comparison_results.append({
            'sentence': sentence,
            'stanza': stanza_pos,
            'spacy': spacy_pos,
            'agreement': agreement
        })
        print()
    
    return comparison_results

def compare_pos_tags(stanza_pos, spacy_pos):
    """品詞タグ比較分析"""
    agreements = 0
    total = min(len(stanza_pos), len(spacy_pos))
    differences = []
    
    for i in range(total):
        stanza_word, stanza_upos, stanza_xpos = stanza_pos[i]
        spacy_word, spacy_pos_tag, spacy_tag = spacy_pos[i]
        
        if stanza_word == spacy_word:
            # 主要品詞での比較（NOUN, VERB, ADJ, ADV, etc.）
            if stanza_upos == spacy_pos_tag:
                agreements += 1
            else:
                differences.append(f"{stanza_word}: Stanza={stanza_upos}, spaCy={spacy_pos_tag}")
    
    return {
        'agreements': agreements,
        'total': total,
        'total_agreement': agreements / total if total > 0 else 0,
        'differences': differences
    }

def analyze_pos_features():
    """品詞分析機能の詳細比較"""
    print("=== 品詞分析機能詳細比較 ===\n")
    
    stanza_nlp = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    spacy_nlp = spacy.load("en_core_web_sm")
    
    test_sentence = "The running children quickly played soccer"
    
    print(f"テスト文: '{test_sentence}'")
    print()
    
    # Stanza詳細分析
    print("【Stanza品詞分析】")
    stanza_doc = stanza_nlp(test_sentence)
    for sent in stanza_doc.sentences:
        for word in sent.words:
            print(f"  {word.text}:")
            print(f"    UPOS: {word.upos}")
            print(f"    XPOS: {word.xpos}")
            print(f"    Features: {word.feats}")
            print()
    
    # spaCy詳細分析
    print("【spaCy品詞分析】")
    spacy_doc = spacy_nlp(test_sentence)
    for token in spacy_doc:
        print(f"  {token.text}:")
        print(f"    POS: {token.pos_}")
        print(f"    TAG: {token.tag_}")
        print(f"    Lemma: {token.lemma_}")
        print(f"    Morph: {token.morph}")
        print()

def speed_comparison():
    """処理速度比較"""
    import time
    
    print("=== 処理速度比較 ===\n")
    
    stanza_nlp = stanza.Pipeline('en', processors='tokenize,pos', verbose=False)
    spacy_nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        "Children play soccer in the park",
        "The quick brown fox jumps over the lazy dog",
        "Running water flows down the mountain",
        "She quickly finished her homework",
        "The beautiful sunset painted the sky orange"
    ] * 20  # 100文テスト
    
    # Stanza速度テスト
    start_time = time.time()
    for sentence in test_sentences:
        stanza_nlp(sentence)
    stanza_time = time.time() - start_time
    
    # spaCy速度テスト
    start_time = time.time()
    for sentence in test_sentences:
        spacy_nlp(sentence)
    spacy_time = time.time() - start_time
    
    print(f"Stanza: {stanza_time:.3f}秒 ({len(test_sentences)}文)")
    print(f"spaCy:  {spacy_time:.3f}秒 ({len(test_sentences)}文)")
    print(f"spaCy速度比: {stanza_time/spacy_time:.1f}x faster")

def main():
    print("=== Stanza vs spaCy 品詞分析特化比較 ===\n")
    
    try:
        # 精度比較
        results = compare_pos_accuracy()
        
        # 機能比較
        analyze_pos_features()
        
        # 速度比較
        speed_comparison()
        
        # 総合評価
        print("\n=== 総合評価 ===")
        
        total_agreements = sum(r['agreement']['agreements'] for r in results)
        total_comparisons = sum(r['agreement']['total'] for r in results)
        overall_agreement = total_agreements / total_comparisons if total_comparisons > 0 else 0
        
        print(f"全体一致度: {overall_agreement:.1%}")
        print(f"Stanza特徴: 学術的精度、詳細な言語学的情報")
        print(f"spaCy特徴: 実用的速度、豊富なエコシステム")
        print(f"品詞分析特化の推奨: {'spaCy' if overall_agreement > 0.9 else 'Stanza'}")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == '__main__':
    main()
