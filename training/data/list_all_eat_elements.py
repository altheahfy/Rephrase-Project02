def list_all_eat_elements():
    """eatグループに登場する要素を全部列挙"""
    
    # eatグループの要素分解結果
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
    
    print("=== eatグループに登場する全要素 ===\n")
    
    # 要素タイプ別に実際の単語/句を整理
    element_dict = {}
    
    for i, example in enumerate(examples, 1):
        print(f"例文{i}: {example['sentence']}")
        for word, element_type in example['elements']:
            print(f"  {word} → {element_type}")
            
            if element_type not in element_dict:
                element_dict[element_type] = []
            element_dict[element_type].append(word)
        print()
    
    print("=== 要素タイプ別まとめ ===")
    for element_type in sorted(element_dict.keys()):
        words = element_dict[element_type]
        print(f"{element_type}: {words}")
    
    print(f"\n=== 登場する全要素タイプ ===")
    all_element_types = sorted(element_dict.keys())
    print(f"要素タイプ: {all_element_types}")
    print(f"要素タイプ数: {len(all_element_types)}")

if __name__ == "__main__":
    list_all_eat_elements()
