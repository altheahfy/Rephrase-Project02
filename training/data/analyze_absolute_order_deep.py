#!/usr/bin/env python3
"""
Order システム深度分析スクリプト - 絶対順序の仕組みを理解
"""
import json

def analyze_absolute_order_system():
    """絶対順序システムの詳細分析"""
    
    with open('slot_order_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # V_group_keyごとの分析
    v_groups = {}
    for item in data:
        v_group = item.get('V_group_key', 'unknown')
        if v_group not in v_groups:
            v_groups[v_group] = []
        v_groups[v_group].append(item)

    print('=== 絶対順序システム詳細分析 ===\n')

    # 各V_group_keyの絶対順序パターンを分析
    for v_group_key, v_group_data in v_groups.items():
        print(f'--- V_group_key: {v_group_key} ---')
        
        # 例文IDごとにグループ化
        examples = {}
        for item in v_group_data:
            ex_id = item.get('例文ID', 'unknown')
            if ex_id not in examples:
                examples[ex_id] = []
            examples[ex_id].append(item)

        print(f'例文数: {len(examples)}')
        
        # 各例文のスロット順序を表示
        absolute_order_map = {}  # スロット位置マップ
        
        for ex_id, ex_data in examples.items():
            # 上位スロットのみを取得
            top_slots = sorted([item for item in ex_data if not item.get('SubslotID')], 
                              key=lambda x: x.get('Slot_display_order', 999))
            
            slot_info = []
            for slot in top_slots:
                slot_name = slot['Slot']
                display_order = slot['Slot_display_order']
                phrase = slot.get('SlotPhrase', '').strip()
                
                # 絶対順序マップに記録
                if display_order not in absolute_order_map:
                    absolute_order_map[display_order] = set()
                absolute_order_map[display_order].add(slot_name)
                
                # 空のフレーズも表示
                if phrase:
                    slot_info.append(f"{slot_name}({display_order})")
                else:
                    slot_info.append(f"{slot_name}({display_order})[EMPTY]")
            
            print(f'  {ex_id}: {" -> ".join(slot_info)}')
        
        # 絶対順序マップの表示
        print(f'  絶対順序マップ:')
        for order in sorted(absolute_order_map.keys()):
            slots = list(absolute_order_map[order])
            print(f'    位置{order}: {slots}')
        
        print()

    print('\n=== 空白スロットと疑問詞の分析 ===')
    
    # 空白スロットの発生パターンを分析
    empty_slot_analysis = {}
    wh_word_analysis = {}
    
    for v_group_key, v_group_data in v_groups.items():
        examples = {}
        for item in v_group_data:
            ex_id = item.get('例文ID', 'unknown')
            if ex_id not in examples:
                examples[ex_id] = []
            examples[ex_id].append(item)
        
        for ex_id, ex_data in examples.items():
            # 空白スロットをカウント
            empty_slots = []
            wh_elements = []
            
            for item in ex_data:
                phrase = item.get('SlotPhrase', '').strip()
                element = item.get('SubslotElement', '').strip()
                
                if not phrase and not item.get('SubslotID'):  # 上位スロットが空白
                    empty_slots.append(item['Slot'])
                
                # wh-word検出
                if element and any(wh in element.lower() for wh in ['who', 'what', 'where', 'when', 'why', 'how']):
                    wh_elements.append(element)
            
            if empty_slots:
                key = f"{v_group_key}_{ex_id}"
                empty_slot_analysis[key] = empty_slots
                
            if wh_elements:
                key = f"{v_group_key}_{ex_id}"
                wh_word_analysis[key] = wh_elements
    
    if empty_slot_analysis:
        print('空白スロット例:')
        for key, slots in list(empty_slot_analysis.items())[:5]:
            print(f'  {key}: {slots}')
    
    if wh_word_analysis:
        print('\nWh-word例:')
        for key, elements in list(wh_word_analysis.items())[:5]:
            print(f'  {key}: {elements}')

if __name__ == "__main__":
    analyze_absolute_order_system()
