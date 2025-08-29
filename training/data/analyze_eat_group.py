def analyze_eat_group():
    """eatグループの要素分解結果を分析"""
    
    decompositions = [
        {
            "sentence": "What will you eat there?",
            "elements": [("What", "O1"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("there", "M2")]
        },
        {
            "sentence": "Will he eat sushi at the park?", 
            "elements": [("Will", "Aux"), ("he", "S"), ("eat", "V"), ("sushi", "O1"), ("at the park", "M2")]
        },
        {
            "sentence": "How will you eat those stuff?",
            "elements": [("How", "M2"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("those stuff", "O1")]
        }
    ]
    
    print("=== eatグループの要素分解結果 ===\n")
    
    for i, item in enumerate(decompositions, 1):
        print(f"例文{i}: {item['sentence']}")
        for j, (word, element_type) in enumerate(item['elements'], 1):
            print(f"  位置{j}: {word} → {element_type}")
        print()
    
    print("=== ポジション別分析 ===")
    
    # 各ポジションに出現する要素タイプを記録
    for pos in range(1, 6):  # 5つの位置
        print(f"\n位置{pos}:")
        for i, item in enumerate(decompositions, 1):
            if pos <= len(item['elements']):
                word, element_type = item['elements'][pos-1]
                print(f"  例文{i}: {element_type} ({word})")
    
    print("\n=== 要素タイプ別出現位置 ===")
    
    # 各要素タイプがどの位置に出現するかをまとめ
    element_positions = {}
    for i, item in enumerate(decompositions):
        for pos, (word, element_type) in enumerate(item['elements'], 1):
            if element_type not in element_positions:
                element_positions[element_type] = []
            element_positions[element_type].append(pos)
    
    for element_type in sorted(element_positions.keys()):
        positions = sorted(set(element_positions[element_type]))
        print(f"{element_type}: 位置 {positions}")

if __name__ == "__main__":
    analyze_eat_group()
