#!/usr/bin/env python3
"""
辞書システムの品詞誤認識原因分析
"""

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

def analyze_word_ambiguity(word):
    """単語の品詞曖昧性分析"""
    print(f"\n=== '{word}' の品詞曖昧性分析 ===")
    
    # WordNetの全品詞情報を取得
    synsets = wordnet.synsets(word.lower())
    
    pos_counts = {}
    print("WordNet品詞情報:")
    for synset in synsets[:10]:  # 最初の10個まで
        pos = synset.pos()
        definition = synset.definition()
        print(f"  {pos}: {definition[:60]}...")
        pos_counts[pos] = pos_counts.get(pos, 0) + 1
    
    print(f"品詞分布: {pos_counts}")
    
    # 単独での品詞タギング
    single_tag = pos_tag([word])
    print(f"単独品詞タギング: {single_tag}")
    
    return pos_counts

def test_context_dependency():
    """文脈依存性テスト"""
    print("=== 文脈依存性テスト ===")
    
    test_cases = [
        "play",           # 単独
        "Children play",  # 動詞として
        "a play",         # 名詞として
        "play time",      # 形容詞として？
        
        "runs", 
        "dog runs",       # 動詞として
        "home runs",      # 名詞として
        
        "flies",
        "bird flies",     # 動詞として  
        "house flies",    # 名詞として
    ]
    
    for case in test_cases:
        tokens = word_tokenize(case)
        tags = pos_tag(tokens)
        print(f"'{case}' → {tags}")

def main():
    # NLTK データ準備
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True) 
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        nltk.download('wordnet', quiet=True)
    except:
        pass
    
    print("=== 辞書システム品詞誤認識原因分析 ===")
    
    # 問題単語の曖昧性分析
    analyze_word_ambiguity("play")
    analyze_word_ambiguity("runs")
    analyze_word_ambiguity("children")
    
    # 文脈依存性テスト
    test_context_dependency()
    
    print("\n=== 結論 ===")
    print("1. 英語は品詞曖昧性が高い言語")
    print("2. 同じ単語が名詞・動詞・形容詞になる")
    print("3. 文脈なしでは正確な品詞判定は困難")
    print("4. 統計的品詞タガーも完璧ではない")

if __name__ == '__main__':
    main()
