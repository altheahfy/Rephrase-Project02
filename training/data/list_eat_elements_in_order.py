def list_eat_elements_in_order():
    """eatの例文の要素を例文の順番通りに列挙"""
    
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
    
    print("=== eatの例文の要素を例文の順番通りに列挙 ===\n")
    
    element_counter = 1
    
    for i, example in enumerate(examples, 1):
        print(f"例文{i}: {example['sentence']}")
        for word, element_type in example['elements']:
            print(f"  {element_counter}. {word} ({element_type})")
            element_counter += 1
        print()
    
    print("=== 順番通りリスト ===")
    element_counter = 1
    all_elements = []
    
    for example in examples:
        for word, element_type in example['elements']:
            all_elements.append(f"{element_counter}. {word} ({element_type})")
            element_counter += 1
    
    for element in all_elements:
        print(element)

if __name__ == "__main__":
    list_eat_elements_in_order()
