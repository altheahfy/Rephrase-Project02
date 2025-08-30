"""
Tell Group Order Analysis Tool
tellグループの順序パターン分析・可視化ツール

目的:
- 期待値データからtellグループの順序パターンを逆算
- 4ステップアルゴリズムの動作検証
- ユーザーによる手動検証用データ出力
"""

import json
from typing import Dict, List, Any
from collections import Counter, defaultdict


def analyze_tell_group_patterns():
    """tellグループの期待値から順序パターンを分析"""
    
    print("🔍 Tell Group Order Pattern Analysis")
    print("=" * 50)
    
    # データ読み込み
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # tellグループの例文を抽出
    tell_examples = []
    for key, item in data['data'].items():
        if item.get('V_group_key') == 'tell':
            tell_examples.append({
                'key': key,
                'sentence': item['sentence'],
                'expected_slots': item['expected']['main_slots'],
                'grammar_category': item.get('grammar_category', 'unknown')
            })
    
    print(f"📊 Tell Group Examples Found: {len(tell_examples)}")
    print()
    
    if not tell_examples:
        print("❌ No tell group examples found!")
        return
    
    # ステップ①：全要素抽出（期待値から）
    print("🔍 STEP 1: 全要素抽出")
    all_slots_used = set()
    for example in tell_examples:
        slots = example['expected_slots']
        for slot_name in slots.keys():
            if slots[slot_name].strip():  # 空でないスロット
                all_slots_used.add(slot_name)
    
    print(f"使用される全スロット: {sorted(all_slots_used)}")
    print()
    
    # ステップ②：使用順序観察（期待値から順序を推定）
    print("🔍 STEP 2: 使用順序観察")
    order_patterns = Counter()
    
    for example in tell_examples:
        slots = example['expected_slots']
        # 空でないスロットのみでパターン作成
        pattern = []
        for slot_name in ['S', 'V', 'O1', 'O2', 'C1', 'M1', 'M2', 'M3', 'Aux']:
            if slot_name in slots and slots[slot_name].strip():
                pattern.append(slot_name)
        
        if pattern:
            pattern_tuple = tuple(pattern)
            order_patterns[pattern_tuple] += 1
            
            print(f"  例文 {example['key']}: {example['sentence']}")
            print(f"    スロット: {slots}")
            print(f"    順序パターン: {pattern}")
            print()
    
    # ステップ③：共通順序構築
    print("🔍 STEP 3: 共通順序構築")
    print("順序パターン頻度:")
    for pattern, count in order_patterns.most_common():
        percentage = (count / len(tell_examples)) * 100
        print(f"  {pattern} → {count}回 ({percentage:.1f}%)")
    
    most_common_pattern = order_patterns.most_common(1)[0] if order_patterns else ((), 0)
    standard_order = list(most_common_pattern[0])
    
    print(f"\n📋 基準順序: {standard_order}")
    print(f"信頼度: {most_common_pattern[1]}/{len(tell_examples)} = {(most_common_pattern[1]/len(tell_examples)*100):.1f}%")
    print()
    
    # ステップ④：順序付与シミュレーション
    print("🔍 STEP 4: 順序付与シミュレーション")
    print("各例文に基準順序を適用した結果:")
    
    results = []
    for example in tell_examples:
        slots = example['expected_slots']
        
        # 基準順序に従って番号付与
        absolute_order = {}
        position = 1
        
        for slot_name in standard_order:
            if slot_name in slots and slots[slot_name].strip():
                absolute_order[str(position)] = slot_name
                position += 1
        
        # 基準順序にないスロットは末尾に追加
        for slot_name, value in slots.items():
            if value.strip() and slot_name not in standard_order:
                absolute_order[str(position)] = slot_name
                position += 1
        
        result = {
            'key': example['key'],
            'sentence': example['sentence'],
            'slots': slots,
            'absolute_order': absolute_order,
            'category': example['grammar_category']
        }
        results.append(result)
        
        print(f"  例文 {example['key']}: {example['sentence']}")
        print(f"    絶対順序: {absolute_order}")
        print()
    
    # 結果をファイル出力
    output_data = {
        'analysis_metadata': {
            'target_group': 'tell',
            'total_examples': len(tell_examples),
            'standard_order': standard_order,
            'confidence': most_common_pattern[1] / len(tell_examples),
            'all_patterns': {str(pattern): count for pattern, count in order_patterns.items()}
        },
        'results': results
    }
    
    output_filename = 'tell_group_order_analysis_results.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 分析結果を '{output_filename}' に出力しました")
    
    # 要約表示
    print("\n" + "=" * 50)
    print("📋 TELL GROUP ORDER ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total Examples: {len(tell_examples)}")
    print(f"Standard Order: {standard_order}")
    print(f"Confidence: {(most_common_pattern[1]/len(tell_examples)*100):.1f}%")
    print(f"Output File: {output_filename}")


if __name__ == "__main__":
    analyze_tell_group_patterns()
