#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループの固定マッピング - わかりやすい表示版
"""

def analyze_tell_group_clearly():
    """tellグループの要素を分かりやすく分析"""
    
    # tellグループの例文
    sentences = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Did I tell him a truth in the kitchen?",
        "Where did you tell me a story?"
    ]
    
    print("=== tellグループ 例文一覧 ===")
    for i, sentence in enumerate(sentences, 1):
        print(f"例文{i}: {sentence}")
    
    # 各例文を単語分割
    word_lists = []
    for sentence in sentences:
        words = sentence.replace('?', '').replace('.', '').split()
        word_lists.append(words)
    
    print("\n=== 単語分割結果 ===")
    for i, words in enumerate(word_lists, 1):
        print(f"例文{i}: {words}")
    
    # 全ての要素を抽出（重複含む）
    all_elements = []
    element_positions = {}  # 要素 -> [位置のリスト]
    
    for sent_idx, words in enumerate(word_lists):
        for pos, word in enumerate(words):
            all_elements.append((word, sent_idx+1, pos))
            
            if word not in element_positions:
                element_positions[word] = []
            element_positions[word].append((sent_idx+1, pos))
    
    # ユニークな要素を抽出
    unique_elements = list(set([elem[0] for elem in all_elements]))
    unique_elements.sort()
    
    print(f"\n=== 全要素の出現位置 ===")
    print(f"ユニーク要素数: {len(unique_elements)}")
    
    for element in unique_elements:
        positions = element_positions[element]
        print(f"{element:12} → ", end="")
        for sent_num, pos in positions:
            print(f"例文{sent_num}の位置{pos}", end="  ")
        print()
    
    # 語順による平均位置計算
    print(f"\n=== 語順による固定マッピング ===")
    element_avg_positions = {}
    
    for element in unique_elements:
        positions = [pos for sent_num, pos in element_positions[element]]
        avg_pos = sum(positions) / len(positions)
        element_avg_positions[element] = avg_pos
    
    # 平均位置でソート
    sorted_elements = sorted(unique_elements, key=lambda x: element_avg_positions[x])
    
    for i, element in enumerate(sorted_elements, 1):
        avg_pos = element_avg_positions[element]
        print(f"列{i:2d}: {element:12} (平均位置: {avg_pos:.1f})")
    
    return sorted_elements

if __name__ == "__main__":
    result = analyze_tell_group_clearly()
