import json
from collections import defaultdict

def analyze_tell_group_positions():
    """tellグループの全ポジションを慎重に数えて並べる"""
    
    # データの読み込み
    with open('tell_group_decomposition.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== tellグループの全ポジション分析 ===\n")
    
    # 各ポジションに登場する要素を記録
    position_elements = defaultdict(list)
    
    # 各例文を分析
    for case_name, case_data in data.items():
        sentence = case_data['sentence']
        main_slots = case_data['actual']['main_slots']
        
        print(f"{case_name}: {sentence}")
        
        # 要素を順番に記録
        for position, (slot, word) in enumerate(main_slots.items(), 1):
            position_elements[position].append({
                'case': case_name,
                'slot': slot,
                'word': word
            })
            print(f"  位置{position}: {slot} = '{word}'")
        
        print()
    
    print("=== ポジション別まとめ ===")
    
    # 全ポジションの最大数を取得
    max_position = max(position_elements.keys())
    
    for pos in range(1, max_position + 1):
        print(f"\n位置{pos}:")
        if pos in position_elements:
            for elem in position_elements[pos]:
                print(f"  {elem['case']}: {elem['slot']} = '{elem['word']}'")
        else:
            print(f"  (空)")
    
    print("\n=== 要素別出現位置 ===")
    
    # 各要素がどの位置に出現するかをまとめ
    element_positions = defaultdict(list)
    for pos, elements in position_elements.items():
        for elem in elements:
            element_positions[elem['slot']].append(pos)
    
    for slot in sorted(element_positions.keys()):
        positions = sorted(set(element_positions[slot]))
        print(f"{slot}: 位置 {positions}")

if __name__ == "__main__":
    analyze_tell_group_positions()
