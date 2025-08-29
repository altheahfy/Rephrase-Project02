def create_correct_eat_mapping():
    """実際の語順で重ならないようにeatグループのマッピングを作成"""
    
    # eatグループの実際の語順
    examples = [
        [("What", "O1"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("there", "M2")],
        [("Will", "Aux"), ("he", "S"), ("eat", "V"), ("sushi", "O1"), ("at the park", "M2")],
        [("How", "M2"), ("will", "Aux"), ("you", "S"), ("eat", "V"), ("those stuff", "O1")]
    ]
    
    print("=== 実際の語順で重ならないように配置 ===\n")
    
    # 全ポジションに出現する要素タイプを記録
    all_positions = {}
    
    for i, example in enumerate(examples, 1):
        print(f"例文{i}:")
        for pos, (word, element_type) in enumerate(example, 1):
            print(f"  位置{pos}: {word}({element_type})")
            
            if pos not in all_positions:
                all_positions[pos] = []
            all_positions[pos].append(element_type)
    
    print(f"\n=== 各ポジションの要素タイプ ===")
    for pos in sorted(all_positions.keys()):
        element_types = all_positions[pos]
        print(f"位置{pos}: {element_types}")
    
    print(f"\n=== eatグループの固定マッピング（実際の語順ベース）===")
    
    # 最大5ポジションで、各要素タイプが出現可能な位置を全て含める
    eat_mapping = {}
    for pos, element_types in all_positions.items():
        for element_type in set(element_types):  # 重複を除去
            if element_type not in eat_mapping:
                eat_mapping[element_type] = []
            if pos not in eat_mapping[element_type]:
                eat_mapping[element_type].append(pos)
    
    print("eatグループマッピング:")
    for element_type in sorted(eat_mapping.keys()):
        positions = sorted(eat_mapping[element_type])
        print(f"  {element_type}: 位置{positions}")
    
    print(f"\n=== 固定カラム構造 ===")
    # tellグループのような固定カラム構造を作成
    print("O1/M2-1  Aux-2  S-3  V-4  O1/M2-5")
    print("(位置1と5でO1/M2が競合可能、位置2,3,4は固定)")

if __name__ == "__main__":
    create_correct_eat_mapping()
