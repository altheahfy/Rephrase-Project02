#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expected_results_progress.jsonの不整合チェック
sentenceとexpectedの一致性を確認
"""

import json
import codecs

def extract_key_words_from_sentence(sentence):
    """例文から主要な単語を抽出"""
    words = sentence.lower().replace('.', '').replace(',', '').split()
    # 冠詞や前置詞を除外
    exclude = {'the', 'a', 'an', 'is', 'was', 'were', 'are', 'be', 'been', 'being', 'to', 'of', 'in', 'at', 'on', 'by', 'for', 'with'}
    return [w for w in words if w not in exclude]

def extract_key_words_from_expected(expected):
    """expected結果から主要な単語を抽出"""
    if not expected or 'main_slots' not in expected:
        return []
    
    words = []
    main_slots = expected['main_slots']
    
    for slot_value in main_slots.values():
        if slot_value:
            slot_words = str(slot_value).lower().replace('.', '').replace(',', '').split()
            words.extend(slot_words)
    
    # sub_slotsも確認
    if 'sub_slots' in expected:
        sub_slots = expected['sub_slots']
        for slot_value in sub_slots.values():
            if slot_value and '[omitted]' not in str(slot_value):
                slot_words = str(slot_value).lower().replace('.', '').replace(',', '').split()
                words.extend(slot_words)
    
    # 冠詞や前置詞を除外
    exclude = {'the', 'a', 'an', 'is', 'was', 'were', 'are', 'be', 'been', 'being', 'to', 'of', 'in', 'at', 'on', 'by', 'for', 'with'}
    return [w for w in words if w not in exclude]

def check_consistency(sentence, expected):
    """sentenceとexpectedの一致性をチェック"""
    sentence_words = set(extract_key_words_from_sentence(sentence))
    expected_words = set(extract_key_words_from_expected(expected))
    
    # 共通する単語の割合
    if not sentence_words or not expected_words:
        return 0.0, [], []
    
    common_words = sentence_words.intersection(expected_words)
    consistency_ratio = len(common_words) / len(sentence_words.union(expected_words))
    
    only_in_sentence = sentence_words - expected_words
    only_in_expected = expected_words - sentence_words
    
    return consistency_ratio, list(only_in_sentence), list(only_in_expected)

def main():
    # データ読み込み
    with codecs.open('expected_results_progress.json', 'r', 'utf-8') as f:
        raw_data = json.load(f)
    
    # correct_answersセクションを取得
    data = raw_data.get('correct_answers', {})
    
    print("🔍 expected_results_progress.json 不整合チェック")
    print("=" * 60)
    
    inconsistent_entries = []
    
    # metaキーを除外して数値キーのみ処理
    numeric_keys = [k for k in data.keys() if k.isdigit()]
    
    for entry_id in sorted(numeric_keys, key=int):
        entry = data[entry_id]
        
        if 'sentence' not in entry or 'expected' not in entry:
            continue
            
        sentence = entry['sentence']
        expected = entry['expected']
        
        if expected is None:
            print(f"❌ {entry_id}: expected が null")
            inconsistent_entries.append(entry_id)
            continue
            
        consistency_ratio, only_sentence, only_expected = check_consistency(sentence, expected)
        
        # 一致率が低い場合（閾値0.3以下）を不整合とみなす
        if consistency_ratio < 0.3:
            print(f"❌ {entry_id}: 不整合 (一致率: {consistency_ratio:.2f})")
            print(f"   sentence: {sentence}")
            if expected and 'main_slots' in expected:
                main_s = expected['main_slots'].get('S', '')
                main_v = expected['main_slots'].get('V', '')
                print(f"   expected: S='{main_s}', V='{main_v}'")
            print(f"   sentence only: {only_sentence}")
            print(f"   expected only: {only_expected}")
            print()
            inconsistent_entries.append(entry_id)
        elif consistency_ratio < 0.7:
            print(f"⚠️  {entry_id}: 部分不整合 (一致率: {consistency_ratio:.2f})")
            print(f"   sentence: {sentence}")
            if expected and 'main_slots' in expected:
                main_s = expected['main_slots'].get('S', '')
                main_v = expected['main_slots'].get('V', '')
                print(f"   expected: S='{main_s}', V='{main_v}'")
            print()
    
    print("=" * 60)
    print(f"📊 総エントリ数: {len(data)}")
    print(f"📊 不整合エントリ数: {len(inconsistent_entries)}")
    print(f"📊 不整合エントリID: {inconsistent_entries}")

if __name__ == "__main__":
    main()
