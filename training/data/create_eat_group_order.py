def create_eat_group_order():
    """eatグループの固定カラム構造を作成してorderを割り当て"""
    
    # eatグループの要素分解結果
    decompositions = [
        {
            "case": "eat_1",
            "sentence": "What will you eat there?",
            "elements": [("What", "O1"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("there", "M2")]
        },
        {
            "case": "eat_2", 
            "sentence": "Will he eat sushi at the park?",
            "elements": [("Will", "Aux"), ("he", "S"), ("eat", "V"), ("sushi", "O1"), ("at the park", "M2")]
        },
        {
            "case": "eat_3",
            "sentence": "How will you eat those stuff?",
            "elements": [("How", "M2"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("those stuff", "O1")]
        }
    ]
    
    print("=== eatグループの要素タイプ分析 ===")
    
    # 出現する要素タイプを集計
    element_types = set()
    for item in decompositions:
        for word, element_type in item['elements']:
            element_types.add(element_type)
    
    print(f"出現要素タイプ: {sorted(element_types)}")
    
    # tellグループの原理を参考に、eatグループの固定カラム構造を推定
    # 各要素タイプが文法的に競合しないよう固定ポジションを割り当て
    
    print("\n=== eatグループ固定カラム構造（推定）===")
    
    # eatグループ専用の固定マッピングを作成
    # 要素タイプごとに固定ポジションを割り当て
    eat_group_mapping = {
        "M2": 1,    # How, there, at the park
        "Aux": 2,   # will, Will  
        "S": 3,     # you, he
        "V": 4,     # eat
        "O1": 5     # What, sushi, those stuff
    }
    
    print("eatグループ固定マッピング:")
    for element_type, position in eat_group_mapping.items():
        print(f"  {element_type} → 位置{position}")
    
    print("\n=== 各例文にorderを割り当て ===")
    
    for item in decompositions:
        print(f"\n{item['case']}: {item['sentence']}")
        ordered_elements = []
        
        for word, element_type in item['elements']:
            position = eat_group_mapping[element_type]
            ordered_elements.append((position, element_type, word))
            print(f"  {word}({element_type}) → 位置{position}")
        
        # 位置順にソート
        ordered_elements.sort(key=lambda x: x[0])
        print(f"  順序結果: {[f'{pos}:{word}' for pos, _, word in ordered_elements]}")

if __name__ == "__main__":
    create_eat_group_order()
