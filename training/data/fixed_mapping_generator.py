#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AbsoluteOrderManager用 固定マッピング生成システム
①グループ要素列挙（位置別分類）→ ②語順配置 の2段階処理
"""

import json
from collections import defaultdict

class FixedMappingGenerator:
    def __init__(self):
        self.position_types = {
            'wh_front': ['What', 'How', 'Where', 'When', 'Why', 'Who', 'Which'],
            'beginning': ['Yesterday', 'Today', 'Tomorrow', 'Usually', 'Often'],
            'normal': 'default',
            'end': ['there', 'here', 'at that time', 'in the morning', 'yesterday']
        }
    
    def classify_element_position(self, element, sentence_position, sentence):
        """要素の文中位置を分類"""
        # wh疑問詞・疑問副詞（文頭）
        if element in self.position_types['wh_front'] and sentence_position == 0:
            return f"{element}_wh_front"
        
        # 文頭副詞
        if element in self.position_types['beginning'] and sentence_position == 0:
            return f"{element}_beginning"
        
        # 文尾副詞
        if (element in self.position_types['end'] or 
            any(end_phrase in element for end_phrase in self.position_types['end'])) and \
           sentence_position == len(sentence) - 1:
            return f"{element}_end"
        
        # 通常位置
        return f"{element}_normal"
    
    def extract_group_elements(self, group_sentences):
        """①グループ要素列挙（位置別分類）"""
        elements_set = set()
        
        print(f"=== ①要素列挙段階 ===")
        
        for i, sentence_data in enumerate(group_sentences):
            sentence = sentence_data['words']
            print(f"例文{i+1}: {' '.join(sentence)}")
            
            for pos, word in enumerate(sentence):
                classified_element = self.classify_element_position(word, pos, sentence)
                elements_set.add(classified_element)
                print(f"  位置{pos}: {word} → {classified_element}")
        
        elements_list = sorted(list(elements_set))
        print(f"\n抽出要素数: {len(elements_list)}")
        print("要素リスト:", elements_list)
        
        return elements_list
    
    def create_word_order_sequence(self, group_sentences, elements_list):
        """②語順配置段階"""
        print(f"\n=== ②語順配置段階 ===")
        
        # 全例文から語順パターンを解析
        word_order_positions = {}
        
        for sentence_data in group_sentences:
            sentence = sentence_data['words']
            for pos, word in enumerate(sentence):
                classified_element = self.classify_element_position(word, pos, sentence)
                if classified_element not in word_order_positions:
                    word_order_positions[classified_element] = []
                word_order_positions[classified_element].append(pos)
        
        # 平均位置でソート
        def get_average_position(element):
            positions = word_order_positions.get(element, [0])
            return sum(positions) / len(positions)
        
        ordered_elements = sorted(elements_list, key=get_average_position)
        
        print("語順ベース配置:")
        fixed_mapping = {}
        for i, element in enumerate(ordered_elements, 1):
            fixed_mapping[i] = element
            avg_pos = get_average_position(element)
            print(f"列{i}: {element} (平均位置: {avg_pos:.1f})")
        
        return fixed_mapping
    
    def generate_fixed_mapping(self, group_name, group_sentences):
        """固定マッピング生成メイン処理"""
        print(f"\n{'='*50}")
        print(f"グループ: {group_name}")
        print(f"{'='*50}")
        
        # ①要素列挙
        elements_list = self.extract_group_elements(group_sentences)
        
        # ②語順配置
        fixed_mapping = self.create_word_order_sequence(group_sentences, elements_list)
        
        print(f"\n=== {group_name} 固定マッピング完成 ===")
        print(f"列数: {len(fixed_mapping)}")
        for col, element in fixed_mapping.items():
            print(f"列{col}: {element}")
        
        return fixed_mapping

def test_system():
    generator = FixedMappingGenerator()
    
    # テストデータ: eatグループ
    eat_group_sentences = [
        {'words': ['What', 'will', 'you', 'eat', 'there']},
        {'words': ['How', 'will', 'you', 'eat', 'sushi', 'there']},
        {'words': ['You', 'will', 'eat', 'sushi', 'there']}
    ]
    
    # 固定マッピング生成
    eat_mapping = generator.generate_fixed_mapping("eatグループ", eat_group_sentences)
    
    return eat_mapping

if __name__ == "__main__":
    result = test_system()
