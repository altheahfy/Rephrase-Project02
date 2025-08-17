#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正解データとテストデータの整合性チェック
"""

import json

def check_data_consistency():
    """正解データとテストデータの一貫性を確認"""
    
    # テストデータを読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print("正解データとテストデータ整合性チェック")
    print("="*70)
    
    # 様態副詞の配置パターンを詳細分析
    adverb_patterns = []
    
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        main_slots = expected.get('main_slots', {})
        
        # 様態副詞を含む文を抽出
        manner_adverbs = ['smoothly', 'carefully', 'quickly', 'successfully', 'efficiently', 
                         'greatly', 'dramatically', 'properly', 'thoroughly', 'gently']
        
        found_adverbs = []
        for adv in manner_adverbs:
            if adv in sentence.lower():
                found_adverbs.append(adv)
        
        if found_adverbs:
            # 動詞を特定
            words = sentence.replace('.', '').split()
            verb_position = -1
            adverb_position = -1
            
            for adv in found_adverbs:
                if adv in sentence.lower():
                    # 簡単な動詞検出
                    common_verbs = ['runs', 'works', 'saves', 'explains', 'writes', 'was', 'is', 'are', 
                                  'published', 'supervised', 'completed', 'improved', 'became', 'arrived']
                    
                    for i, word in enumerate(words):
                        if word.lower() in common_verbs:
                            verb_position = i
                        if adv in word.lower():
                            adverb_position = i
                    
                    # M配置を確認
                    m_slots = {k: v for k, v in main_slots.items() if k.startswith('M')}
                    adverb_slot = None
                    for slot, value in m_slots.items():
                        if adv in value.lower():
                            adverb_slot = slot
                            break
                    
                    if adverb_slot:
                        adverb_patterns.append({
                            'test_id': test_id,
                            'sentence': sentence,
                            'adverb': adv,
                            'verb_pos': verb_position,
                            'adverb_pos': adverb_position,
                            'relative_pos': 'after' if adverb_position > verb_position else 'before',
                            'assigned_slot': adverb_slot,
                            'm_slots': m_slots
                        })
    
    # パターン分析
    print("動詞後の様態副詞配置パターン:")
    print("-" * 50)
    after_verb_patterns = [p for p in adverb_patterns if p['relative_pos'] == 'after']
    
    for pattern in after_verb_patterns:
        print(f"Test{pattern['test_id']}: {pattern['adverb']} → {pattern['assigned_slot']}")
        print(f"  文: {pattern['sentence']}")
        print(f"  全M配置: {pattern['m_slots']}")
        print()
    
    # 一貫性分析
    print("配置一貫性分析:")
    print("-" * 50)
    slot_counts = {'M1': 0, 'M2': 0, 'M3': 0}
    for pattern in after_verb_patterns:
        slot_counts[pattern['assigned_slot']] += 1
    
    print(f"動詞後様態副詞の配置統計:")
    for slot, count in slot_counts.items():
        print(f"  {slot}: {count}件")
    
    # 最も多い配置パターンを確認
    most_common = max(slot_counts, key=slot_counts.get)
    print(f"\n最頻出配置: {most_common} ({slot_counts[most_common]}件)")
    
    # 不整合例を特定
    print("\n不整合の可能性がある例:")
    print("-" * 30)
    for pattern in after_verb_patterns:
        if pattern['assigned_slot'] != most_common:
            print(f"Test{pattern['test_id']}: {pattern['adverb']} → {pattern['assigned_slot']} (少数派)")

if __name__ == "__main__":
    check_data_consistency()
