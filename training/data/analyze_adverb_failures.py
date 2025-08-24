#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def analyze_adverb_failures():
    """副詞配置（M1, M2, M3）の失敗例文を詳細分析"""
    
    with open('official_test_results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print('=== 副詞配置（M1, M2, M3）失敗例文の分析 ===')
    m_failures = []

    # 各テスト結果を分析
    for test_id, result in data['results'].items():
        if 'analysis_result' in result and 'main_slots' in result['analysis_result']:
            main_slots = result['analysis_result']['main_slots']
            expected = result.get('expected', {}).get('main_slots', {})
            
            # M1, M2, M3の比較
            for slot in ['M1', 'M2', 'M3']:
                if slot in expected or slot in main_slots:
                    expected_val = expected.get(slot, '')
                    actual_val = main_slots.get(slot, '')
                    if expected_val != actual_val:
                        m_failures.append({
                            'test_id': test_id,
                            'sentence': result['sentence'],
                            'slot': slot,
                            'expected': expected_val,
                            'actual': actual_val,
                            'status': result.get('status', 'unknown')
                        })

    print(f'副詞配置失敗例文数: {len(m_failures)}')
    print()
    
    # 失敗パターンの分析
    slot_stats = {'M1': 0, 'M2': 0, 'M3': 0}
    for failure in m_failures:
        slot_stats[failure['slot']] += 1
    
    print("=== スロット別失敗統計 ===")
    for slot, count in slot_stats.items():
        print(f"{slot}: {count}件の失敗")
    print()
    
    print("=== 失敗例文詳細 ===")
    for i, failure in enumerate(m_failures[:15]):  # 最初の15件を表示
        print(f"例文 {failure['test_id']}: {failure['sentence']}")
        print(f"  {failure['slot']}: 期待='{failure['expected']}' vs 実際='{failure['actual']}'")
        print(f"  ステータス: {failure['status']}")
        print()

if __name__ == "__main__":
    analyze_adverb_failures()
