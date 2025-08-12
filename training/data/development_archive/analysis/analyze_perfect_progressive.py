#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完了進行形構文のStanza構造分析
統合アーキテクチャ Phase 2: 完了進行形パターン解析
"""

import stanza

def analyze_perfect_progressive_sentences():
    """完了進行形の依存関係構造を分析"""
    print("🔥 完了進行形構文 Stanza構造分析開始")
    
    # Stanzaパイプライン初期化
    print("🚀 Stanzaパイプライン初期化中...")
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
    print("✅ 初期化完了\n")
    
    # 分析対象の完了進行形文
    test_sentences = [
        # 現在完了進行形
        "I have been working here for three years.",
        "How long have you been studying English?",
        "She has been waiting for an hour.",
        
        # 過去完了進行形
        "She had been waiting for an hour when I arrived.",
        "He was tired because he had been running all morning.",
        
        # 未来完了進行形
        "By next year, I will have been living here for five years.",
        
        # 特殊構文
        "The project has been being developed since January.",
        "If I had been studying harder, I would have passed the exam.",
        
        # 複合例
        "Because I have been working here for three years, I understand the company culture well."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 分析{i}: {sentence}")
        doc = nlp(sentence)
        
        for sent in doc.sentences:
            print(f"  🔍 依存関係構造:")
            
            # 完了進行形特有の要素を検出
            perfect_progressive_elements = {
                'auxiliaries': [],
                'main_verb': None,
                'present_participle': None,
                'time_expressions': [],
                'duration_phrases': [],
                'been_words': []
            }
            
            for word in sent.words:
                print(f"    {word.id:2}: {word.text:15} | {word.upos:8} | {word.deprel:15} | head:{word.head}")
                
                # 助動詞検出
                if word.upos == 'AUX':
                    perfect_progressive_elements['auxiliaries'].append((word, word.deprel))
                
                # been検出
                if word.text.lower() == 'been':
                    perfect_progressive_elements['been_words'].append((word, word.deprel))
                
                # 現在分詞検出 (-ing語尾)
                if word.text.endswith('ing') and word.upos == 'VERB':
                    perfect_progressive_elements['present_participle'] = (word, word.deprel)
                
                # 主動詞検出 (root)
                if word.deprel == 'root':
                    perfect_progressive_elements['main_verb'] = (word, word.deprel)
                
                # 時間表現検出
                if word.text.lower() in ['for', 'since', 'when', 'by', 'already', 'just', 'still']:
                    perfect_progressive_elements['time_expressions'].append((word, word.deprel))
                
                # 期間表現検出
                if word.deprel in ['obl:tmod', 'obl', 'advmod'] and any(time_word in word.text.lower() for time_word in ['year', 'month', 'hour', 'day', 'minute']):
                    perfect_progressive_elements['duration_phrases'].append((word, word.deprel))
            
            # 検出した完了進行形要素を表示
            if any(perfect_progressive_elements.values()):
                print(f"  📋 完了進行形要素検出:")
                for key, elements in perfect_progressive_elements.items():
                    if elements:
                        if isinstance(elements, list):
                            print(f"    {key}: {[(e[0].text, e[1]) for e in elements]}")
                        else:
                            print(f"    {key}: {(elements[0].text, elements[1])}")
            
            # 助動詞チェーン分析
            aux_chain = []
            for aux, _ in perfect_progressive_elements['auxiliaries']:
                aux_chain.append(aux.text)
            for been, _ in perfect_progressive_elements['been_words']:
                aux_chain.append(been.text)
            
            if aux_chain:
                print(f"  🔗 助動詞チェーン: {' + '.join(aux_chain)}")
            
            # 完了進行形パターン判定
            pattern = None
            if 'have' in aux_chain or 'has' in aux_chain:
                if 'been' in aux_chain:
                    pattern = "現在完了進行形 (have/has been + Ving)"
            elif 'had' in aux_chain and 'been' in aux_chain:
                pattern = "過去完了進行形 (had been + Ving)"
            elif 'will' in aux_chain and 'have' in aux_chain and 'been' in aux_chain:
                pattern = "未来完了進行形 (will have been + Ving)"
            
            if pattern:
                print(f"  ✅ パターン識別: {pattern}")
            
            print()
    
    print("🎉 完了進行形構文分析完了")

if __name__ == "__main__":
    analyze_perfect_progressive_sentences()
