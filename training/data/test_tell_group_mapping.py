#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tellグループに固定マッピング生成を適用
"""

import json
import sys
sys.path.append('.')
from fixed_mapping_generator import FixedMappingGenerator

def load_tell_group_data():
    """tellグループのデータを読み込み"""
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tell_sentences = []
    
    # tellグループのデータを抽出
    for key, item in data['data'].items():
        if item.get('V_group_key') == 'tell':
            sentence = item['sentence']
            # 句読点を除去して単語リストに変換
            words = sentence.replace('?', '').replace('.', '').split()
            tell_sentences.append({'words': words})
            print(f"例文{len(tell_sentences)}: {sentence}")
            print(f"  単語リスト: {words}")
    
    return tell_sentences

def test_tell_group():
    """tellグループの固定マッピング生成テスト"""
    generator = FixedMappingGenerator()
    
    # tellグループデータ読み込み
    tell_sentences = load_tell_group_data()
    
    print(f"\n読み込み完了: {len(tell_sentences)}例文")
    
    # 固定マッピング生成
    tell_mapping = generator.generate_fixed_mapping("tellグループ", tell_sentences)
    
    return tell_mapping

if __name__ == "__main__":
    result = test_tell_group()
