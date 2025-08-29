def list_elements_by_position():
    """位置別に要素を別々にカウント"""
    
    examples = [
        [("What", "O1"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("there", "M2")],
        [("Will", "Aux"), ("he", "S"), ("eat", "V"), ("sushi", "O1"), ("at the park", "M2")],
        [("How", "M2"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("those stuff", "O1")]
    ]
    
    print("=== 位置別要素カウント ===\n")
    
    # 位置別に要素をリスト化
    all_elements = []
    for i, example in enumerate(examples, 1):
        print(f"例文{i}:")
        for pos, (word, element_type) in enumerate(example, 1):
            element_id = f"{element_type}_{pos}"  # 位置込みのID
            all_elements.append((element_id, word, element_type, pos))
            print(f"  位置{pos}: {word}({element_type}) → {element_id}")
        print()
    
    print(f"=== 全要素リスト（位置別） ===")
    for i, (element_id, word, element_type, pos) in enumerate(all_elements, 1):
        print(f"{i:2d}. {element_id}: {word}")
    
    print(f"\n=== 総要素数 ===")
    print(f"総数: {len(all_elements)} 個")
    
    # 要素タイプ別でも位置別に分類
    print(f"\n=== 要素タイプ＋位置別分類 ===")
    element_pos_dict = {}
    for element_id, word, element_type, pos in all_elements:
        if element_id not in element_pos_dict:
            element_pos_dict[element_id] = []
        element_pos_dict[element_id].append(word)
    
    for element_id in sorted(element_pos_dict.keys()):
        words = element_pos_dict[element_id]
        print(f"{element_id}: {words}")

if __name__ == "__main__":
    list_elements_by_position()
