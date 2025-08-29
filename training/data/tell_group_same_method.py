#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループに同じ方法を適用
①要素列挙（位置別分類）→ ②語順配置
"""

import sys
sys.path.append('.')
from fixed_mapping_generator import FixedMappingGenerator

def apply_same_method_to_tell_group():
    """eatグループと同じ方法をtellグループに適用"""
    
    # tellグループの例文データ
    tell_sentences = [
        {'words': ['What', 'did', 'he', 'tell', 'her', 'at', 'the', 'store']},
        {'words': ['Did', 'he', 'tell', 'her', 'a', 'secret', 'there']},
        {'words': ['Did', 'I', 'tell', 'him', 'a', 'truth', 'in', 'the', 'kitchen']},
        {'words': ['Where', 'did', 'you', 'tell', 'me', 'a', 'story']}
    ]
    
    print("=== tellグループ例文 ===")
    for i, sentence_data in enumerate(tell_sentences, 1):
        print(f"例文{i}: {' '.join(sentence_data['words'])}")
    
    # eatグループと同じFixedMappingGeneratorを使用
    generator = FixedMappingGenerator()
    
    # 固定マッピング生成（eatグループと同じ処理）
    tell_mapping = generator.generate_fixed_mapping("tellグループ", tell_sentences)
    
    return tell_mapping

if __name__ == "__main__":
    result = apply_same_method_to_tell_group()
