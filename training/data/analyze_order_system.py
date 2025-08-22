#!/usr/bin/env python3
"""
Order システム構造分析スクリプト
"""
import json

def analyze_order_system():
    """slot_order_data.jsonの構造分析"""
    
    # slot_order_data.jsonの構造分析
    with open('slot_order_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print('=== Order システム構造分析 ===')
    print(f'総データ数: {len(data)}')

    # V_group_keyごとの分析
    v_groups = {}
    for item in data:
        v_group = item.get('V_group_key', 'unknown')
        if v_group not in v_groups:
            v_groups[v_group] = []
        v_groups[v_group].append(item)

    print(f'V_group_key種類数: {len(v_groups)}')

    # 最初のV_groupの詳細分析
    first_vgroup = list(v_groups.keys())[0]
    print(f'\n=== {first_vgroup} V_group詳細 ===')
    first_data = v_groups[first_vgroup]

    # 例文IDごとにグループ化
    examples = {}
    for item in first_data:
        ex_id = item.get('例文ID', 'unknown')
        if ex_id not in examples:
            examples[ex_id] = []
        examples[ex_id].append(item)

    print(f'例文数: {len(examples)}')

    # 最初の例文の構造を詳細表示
    first_ex = list(examples.keys())[0]
    print(f'\n=== 例文 {first_ex} 構造 ===')
    ex_data = examples[first_ex]

    # Slot_display_orderとdisplay_orderを分析
    slots_with_orders = []
    for item in ex_data:
        slots_with_orders.append({
            'Slot': item.get('Slot'),
            'SubslotID': item.get('SubslotID', ''),
            'SlotPhrase': item.get('SlotPhrase', ''),
            'SubslotElement': item.get('SubslotElement', ''),
            'Slot_display_order': item.get('Slot_display_order'),
            'display_order': item.get('display_order')
        })

    # 上位スロット順序表示
    top_slots = sorted([item for item in slots_with_orders if not item['SubslotID']], 
                      key=lambda x: x['Slot_display_order'])
    print('上位スロット順序:')
    for slot in top_slots:
        print(f'  {slot["Slot_display_order"]}: {slot["Slot"]} = "{slot["SlotPhrase"]}"')

    # サブスロット順序表示（S スロットの例）
    s_subslots = sorted([item for item in slots_with_orders if item['SubslotID'] and item['Slot'] == 'S'], 
                       key=lambda x: x['display_order'])
    if s_subslots:
        print('\nSスロット内サブスロット順序:')
        for sub in s_subslots:
            print(f'  {sub["display_order"]}: {sub["SubslotID"]} = "{sub["SubslotElement"]}"')
            
    # 絶対順序の概念を理解するため、複数例文比較
    print(f'\n=== {first_vgroup} 絶対順序分析 ===')
    for ex_id, ex_data in list(examples.items())[:3]:  # 最初の3例文
        print(f'\n例文 {ex_id}:')
        top_slots = sorted([item for item in ex_data if not item.get('SubslotID')], 
                          key=lambda x: x.get('Slot_display_order', 999))
        slot_sequence = [f"{slot['Slot']}({slot['Slot_display_order']})" for slot in top_slots]
        print(f'  スロット順序: {" -> ".join(slot_sequence)}')

if __name__ == "__main__":
    analyze_order_system()
