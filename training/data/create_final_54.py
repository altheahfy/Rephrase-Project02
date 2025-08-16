#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
54例文完全セット作成（31有効+23新規）
"""

import json
import codecs

def create_final_54_sentences():
    """有効31例文+新規23例文=54例文セット作成"""
    
    # expected_results_progress.jsonから有効な31例文を抽出
    try:
        with codecs.open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            expected_file = json.load(f)
            expected_data = expected_file.get('correct_answers', {})
    except:
        expected_data = {}
    
    # confirmed_correct_answers.jsonから新規23例文を抽出
    try:
        with codecs.open('confirmed_correct_answers.json', 'r', encoding='utf-8') as f:
            confirmed_data = json.load(f)
            new_sentences = confirmed_data.get('correct_answers', {})
    except:
        new_sentences = {}
    
    # 有効データを特定（文と正解が整合しているもの）
    valid_sentences = []
    valid_expected = {}
    
    # 有効な31例文を特定（破損した23個を除く全て）
    all_ids = set(expected_data.keys())
    corrupted_ids = {"20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "41", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54"}
    valid_ids = sorted([id for id in all_ids if id not in corrupted_ids], key=int)
    
    # 有効例文を追加
    for vid in valid_ids:
        if vid in expected_data:
            data = expected_data[vid]
            sentence = data.get('sentence', '')
            judgment = data.get('user_judgment', '')
            if sentence and judgment in ['correct', 'corrected']:
                valid_sentences.append(sentence)
                valid_expected[str(len(valid_sentences))] = {
                    "sentence": sentence,
                    "expected": data.get('ai_prediction', {})
                }
    
    # 新規23例文を追加
    new_sentence_list = []
    new_expected = {}
    
    for i, (nid, data) in enumerate(new_sentences.items(), len(valid_sentences) + 1):
        sentence = data.get('sentence', '')
        if sentence:
            new_sentence_list.append(sentence)
            new_expected[str(i)] = {
                "sentence": sentence,
                "expected": data.get('expected', {})
            }
    
    # 完全54例文リスト作成
    final_54_sentences = valid_sentences + new_sentence_list
    
    # 完全正解データ作成
    final_expected_data = {}
    final_expected_data.update(valid_expected)
    final_expected_data.update(new_expected)
    
    print(f"✅ 有効例文: {len(valid_sentences)}個")
    print(f"✅ 新規例文: {len(new_sentence_list)}個") 
    print(f"✅ 合計: {len(final_54_sentences)}個")
    
    # custom_test.py用例文リスト出力
    print("\n" + "="*60)
    print("custom_test.py用例文リスト:")
    print("="*60)
    for i, sentence in enumerate(final_54_sentences, 1):
        print(f'        "{sentence}",  # {i}')
    
    # 正解データ保存
    with codecs.open('final_54_test_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            "meta": {
                "total_count": len(final_54_sentences),
                "valid_count": len(valid_sentences),
                "new_count": len(new_sentence_list)
            },
            "data": final_expected_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 final_54_test_data.json 保存完了")
    
    return final_54_sentences, final_expected_data

if __name__ == "__main__":
    create_final_54_sentences()
