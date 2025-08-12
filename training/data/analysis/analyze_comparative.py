#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
比較級・最上級構文のStanza構造分析
統合アーキテクチャ Phase 2: 比較構文パターン解析
"""

import stanza

def analyze_comparative_sentences():
    """比較級・最上級の依存関係構造を分析"""
    print("🔥 比較級・最上級構文 Stanza構造分析開始")
    
    # Stanzaパイプライン初期化
    print("🚀 Stanzaパイプライン初期化中...")
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
    print("✅ 初期化完了\n")
    
    # 分析対象の比較級・最上級文
    test_sentences = [
        # 基本比較級
        "This book is more interesting than that one.",
        "She runs faster than him.",
        "I have more money than you.",
        
        # 最上級
        "This is the most beautiful flower in the garden.",
        "She speaks English most fluently among all students.",
        
        # 特殊比較構文
        "He is as tall as his brother.",
        "The harder you work, the more successful you become.",
        
        # 複合例
        "Because this method is more efficient than the traditional approach, we should adopt it."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 分析{i}: {sentence}")
        doc = nlp(sentence)
        
        for sent in doc.sentences:
            print(f"  🔍 依存関係構造:")
            
            # 比較構文特有の要素を検出
            comparative_elements = {
                'comparative_words': [],
                'superlative_words': [],
                'than_phrases': [],
                'as_phrases': [],
                'most_det': [],
                'comparison_targets': []
            }
            
            for word in sent.words:
                print(f"    {word.id:2}: {word.text:15} | {word.upos:8} | {word.deprel:15} | head:{word.head}")
                
                # 比較級・最上級検出
                if word.text.lower() in ['more', 'most', 'less', 'least']:
                    if word.text.lower() in ['more', 'less']:
                        comparative_elements['comparative_words'].append((word, word.deprel))
                    else:
                        comparative_elements['superlative_words'].append((word, word.deprel))
                
                # -er, -est語尾の検出
                if word.text.endswith('er') and word.upos in ['ADJ', 'ADV']:
                    comparative_elements['comparative_words'].append((word, word.deprel))
                elif word.text.endswith('est') and word.upos in ['ADJ', 'ADV']:
                    comparative_elements['superlative_words'].append((word, word.deprel))
                
                # than句検出
                if word.text.lower() == 'than':
                    comparative_elements['than_phrases'].append((word, word.deprel))
                
                # as句検出
                if word.text.lower() == 'as':
                    comparative_elements['as_phrases'].append((word, word.deprel))
                
                # 定冠詞the (最上級用)
                if word.text.lower() == 'the' and word.deprel == 'det':
                    comparative_elements['most_det'].append((word, word.deprel))
            
            # 検出した比較構文要素を表示
            if any(comparative_elements.values()):
                print(f"  📋 比較構文要素検出:")
                for key, elements in comparative_elements.items():
                    if elements:
                        print(f"    {key}: {[(e[0].text, e[1]) for e in elements]}")
            
            print()
    
    print("🎉 比較級・最上級構文分析完了")

if __name__ == "__main__":
    analyze_comparative_sentences()
