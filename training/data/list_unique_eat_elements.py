def list_unique_eat_elements():
    """eatの例文の要素を重複を除いて列挙"""
    
    examples = [
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
    
    print("=== eatの例文の要素（重複除去） ===\n")
    
    unique_elements = []
    seen_positions = set()
    
    for example in examples:
        for pos, (word, element_type) in enumerate(example['elements'], 1):
            # 文法的位置を判定
            if element_type == "O1" and pos == 1:  # 疑問詞位置のO1
                position_key = "O1_wh"
            elif element_type == "M2" and pos == 1:  # 疑問詞位置のM2  
                position_key = "M2_wh"
            elif element_type == "O1" and pos > 1:  # 普通の位置のO1
                position_key = "O1_normal"
            elif element_type == "M2" and pos > 1:  # 普通の位置のM2
                position_key = "M2_normal"
            else:
                position_key = element_type  # Aux, S, V
            
            if position_key not in seen_positions:
                unique_elements.append((word, element_type, position_key))
                seen_positions.add(position_key)
    
    for i, (word, element_type, position_key) in enumerate(unique_elements, 1):
        print(f"{i}. {word} ({element_type}) - {position_key}")

if __name__ == "__main__":
    list_unique_eat_elements()
