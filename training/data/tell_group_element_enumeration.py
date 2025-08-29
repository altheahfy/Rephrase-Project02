#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループの要素を正しく列挙
"""

def enumerate_tell_group_elements():
    """tellグループの要素を正しく列挙"""
    
    # tellグループの例文
    sentences = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Did I tell him a truth in the kitchen?",
        "Where did you tell me a story?"
    ]
    
    print("=== tellグループ例文 ===")
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
        for j, word in enumerate(words):
            print(f"  位置{j}: {word}")
        print()
    
    # 全ての要素を抽出（文中位置を考慮）
    all_elements = set()
    element_details = []  # 詳細情報も保存
    
    for sent_idx, words in enumerate(word_lists):
        print(f"=== 例文{sent_idx+1}の要素分類 ===")
        for pos, word in enumerate(words):
            # 位置に基づく分類
            if pos == 0:  # 文頭
                if word in ['What', 'Where', 'How', 'When', 'Why', 'Who', 'Which']:
                    element_type = f"{word}_wh"
                else:
                    element_type = f"{word}_beginning"
            elif pos == len(words) - 1:  # 文末
                if word in ['there', 'here']:
                    element_type = f"{word}_end"
                else:
                    element_type = f"{word}_end"
            else:  # 文中
                element_type = f"{word}_normal"
            
            all_elements.add(element_type)
            element_details.append({
                'sentence': sent_idx + 1,
                'position': pos,
                'word': word,
                'element_type': element_type
            })
            
            print(f"  位置{pos}: {word} → {element_type}")
    
    print(f"\n=== 抽出された全要素 ===")
    sorted_elements = sorted(list(all_elements))
    print(f"要素数: {len(sorted_elements)}")
    
    for i, element in enumerate(sorted_elements, 1):
        print(f"{i:2d}. {element}")
    
    # 各要素の出現詳細
    print(f"\n=== 各要素の出現詳細 ===")
    for element in sorted_elements:
        appearances = [detail for detail in element_details if detail['element_type'] == element]
        print(f"\n{element}:")
        for app in appearances:
            print(f"  例文{app['sentence']} 位置{app['position']}: {app['word']}")
    
    return sorted_elements, element_details

if __name__ == "__main__":
    elements, details = enumerate_tell_group_elements()
