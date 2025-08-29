import json

def count_and_list_elements():
    """tellグループの例文の要素を数えて並べる"""
    
    # データの読み込み
    with open('tell_group_decomposition.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== tellグループの例文を数えて並べる ===\n")
    
    for case_name, case_data in data.items():
        sentence = case_data['sentence']
        main_slots = case_data['actual']['main_slots']
        
        print(f"{case_name}: {sentence}")
        print(f"要素数: {len(main_slots)}個")
        print("要素の並び:")
        
        # 要素を順番に並べる
        for i, (slot, word) in enumerate(main_slots.items(), 1):
            print(f"  {i}. {slot}: {word}")
        
        print()

if __name__ == "__main__":
    count_and_list_elements()
