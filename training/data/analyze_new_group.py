import json

def analyze_new_group_positions():
    """新しいグループの例文を慎重に数えて並べる"""
    
    sentences = [
        "What will you eat there?",
        "Will he eat sushi at the park?", 
        "How will you eat those stuff?"
    ]
    
    print("=== 新しいグループの例文分析 ===\n")
    
    # 各例文を仮の分解で分析（実際の分解結果がないため、推測で進める）
    # この分解は仮のもので、実際のシステムによる分解が必要
    
    estimated_decompositions = [
        {
            "sentence": "What will you eat there?",
            "elements": ["What", "will", "you", "eat", "there"]
        },
        {
            "sentence": "Will he eat sushi at the park?",
            "elements": ["Will", "he", "eat", "sushi", "at the park"]
        },
        {
            "sentence": "How will you eat those stuff?",
            "elements": ["How", "will", "you", "eat", "those stuff"]
        }
    ]
    
    for i, item in enumerate(estimated_decompositions, 1):
        print(f"例文{i}: {item['sentence']}")
        print(f"要素数: {len(item['elements'])}個")
        print("要素の並び:")
        for j, element in enumerate(item['elements'], 1):
            print(f"  {j}. {element}")
        print()
    
    print("=== ポジション別分析 ===")
    
    # 各ポジションに出現する要素を記録
    max_elements = max(len(item['elements']) for item in estimated_decompositions)
    
    for pos in range(1, max_elements + 1):
        print(f"\n位置{pos}:")
        for i, item in enumerate(estimated_decompositions, 1):
            if pos <= len(item['elements']):
                print(f"  例文{i}: {item['elements'][pos-1]}")
            else:
                print(f"  例文{i}: (空)")

if __name__ == "__main__":
    analyze_new_group_positions()
