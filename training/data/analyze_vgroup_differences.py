#!/usr/bin/env python3
"""
V_group_key別絶対順序パターン差異分析
異なるV_group_keyでの順序構造の違いを詳細分析
"""
import json

def analyze_vgroup_order_differences():
    """V_group_key別の絶対順序パターンの差異を分析"""
    
    with open('slot_order_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # V_group_keyごとの分析
    v_groups = {}
    for item in data:
        v_group = item.get('V_group_key', 'unknown')
        if v_group not in v_groups:
            v_groups[v_group] = []
        v_groups[v_group].append(item)

    print('=== V_group_key別絶対順序パターン差異分析 ===\n')

    # 各V_group_keyの絶対順序パターンを詳細比較
    order_patterns = {}
    
    for v_group_key, v_group_data in v_groups.items():
        # 例文IDごとにグループ化
        examples = {}
        for item in v_group_data:
            ex_id = item.get('例文ID', 'unknown')
            if ex_id not in examples:
                examples[ex_id] = []
            examples[ex_id].append(item)

        # 最初の例文から絶対順序パターンを抽出
        first_ex = list(examples.keys())[0]
        first_ex_data = examples[first_ex]
        
        # 上位スロットのみを取得してパターン化
        top_slots = sorted([item for item in first_ex_data if not item.get('SubslotID')], 
                          key=lambda x: x.get('Slot_display_order', 999))
        
        pattern = []
        for slot in top_slots:
            pattern.append({
                'position': slot['Slot_display_order'],
                'slot': slot['Slot'],
                'has_content': bool(slot.get('SlotPhrase', '').strip())
            })
        
        order_patterns[v_group_key] = {
            'pattern': pattern,
            'length': len(pattern),
            'example_count': len(examples)
        }
    
    # パターンの比較分析
    print('📊 V_group_key別絶対順序パターン比較:')
    print()
    
    for v_group_key, info in order_patterns.items():
        print(f'🔸 {v_group_key} (例文数: {info["example_count"]}):')
        pattern_str = []
        for slot_info in info['pattern']:
            slot_name = slot_info['slot']
            if slot_info['has_content']:
                pattern_str.append(f"{slot_name}({slot_info['position']})")
            else:
                pattern_str.append(f"{slot_name}({slot_info['position']})[空]")
        print(f'   順序: {" → ".join(pattern_str)}')
        print(f'   長さ: {info["length"]}スロット')
        print()
    
    # 重要なパターンの差異を特定
    print('🔍 重要なパターン差異:')
    print()
    
    # 1. スロット数の違い
    lengths = [info['length'] for info in order_patterns.values()]
    print(f'   スロット数範囲: {min(lengths)} ～ {max(lengths)}')
    
    # 2. 特殊な順序パターンを特定
    special_patterns = []
    
    for v_group_key, info in order_patterns.items():
        pattern = info['pattern']
        
        # Auxの位置を確認
        aux_positions = [slot['position'] for slot in pattern if slot['slot'] == 'Aux']
        if aux_positions:
            aux_pos = aux_positions[0]
            print(f'   {v_group_key}: Aux位置 = {aux_pos}')
        
        # 特殊パターンの検出
        if v_group_key == 'think':  # O1が最初に来るパターン
            special_patterns.append(f'{v_group_key}: 疑問文パターン（O1が先頭）')
        elif v_group_key == 'offer':  # Auxがないパターン
            special_patterns.append(f'{v_group_key}: Aux無しパターン')
        elif v_group_key == 'give':  # M2が動詞前にあるパターン
            special_patterns.append(f'{v_group_key}: M2前置パターン')
    
    if special_patterns:
        print('\n   🚨 特殊順序パターン:')
        for pattern in special_patterns:
            print(f'     • {pattern}')
    
    # 3. 設計への影響を分析
    print('\n⚠️ 設計への影響分析:')
    print()
    
    impacts = [
        '各V_group_keyごとに独自の絶対順序テーブルが必要',
        'V_group_key判定の精度がシステム全体の品質を左右',
        '疑問文・肯定文で異なる順序パターンが存在',
        'Auxの有無による順序パターンの分岐',
        'M2の位置が動詞前後で変動する可能性'
    ]
    
    for i, impact in enumerate(impacts, 1):
        print(f'   {i}. {impact}')
    
    # 4. 実装上の考慮点
    print('\n🏗️ 実装上の重要な考慮点:')
    print()
    
    considerations = [
        '絶対順序テーブルは V_group_key をキーとしたマッピングテーブル',
        'V_group_key の自動判定ロジックが最重要コンポーネント',
        '疑問文パターン（think, be capable of）の特別処理が必要',
        '文型によって大幅に異なる順序を許容する柔軟な設計',
        '空白スロットの位置も V_group_key に依存'
    ]
    
    for i, consideration in enumerate(considerations, 1):
        print(f'   {i}. {consideration}')

if __name__ == "__main__":
    analyze_vgroup_order_differences()
