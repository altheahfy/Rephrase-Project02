def test_eat_group_order():
    """eatグループのorder順で文を再構築してテスト"""
    
    # order結果
    ordered_results = [
        {
            "original": "What will you eat there?",
            "ordered": ['1:there', '2:will', '3:you', '4:eat', '5:What']
        },
        {
            "original": "Will he eat sushi at the park?", 
            "ordered": ['1:at the park', '2:Will', '3:he', '4:eat', '5:sushi']
        },
        {
            "original": "How will you eat those stuff?",
            "ordered": ['1:How', '2:will', '3:you', '4:eat', '5:those stuff']
        }
    ]
    
    print("=== eatグループのorder順で文を再構築 ===\n")
    
    for i, result in enumerate(ordered_results, 1):
        print(f"例文{i}:")
        print(f"  元の文: {result['original']}")
        
        # order順に並べた単語を抽出
        ordered_words = [item.split(':', 1)[1] for item in result['ordered']]
        reconstructed = ' '.join(ordered_words) + '?'
        
        print(f"  order順: {result['ordered']}")
        print(f"  再構築: {reconstructed}")
        
        # 文法的に成立するかチェック
        if is_grammatically_valid(reconstructed):
            print("  結果: ✓ 文法的に成立")
        else:
            print("  結果: ✗ 文法的に不成立")
        print()

def is_grammatically_valid(sentence):
    """簡易的な文法チェック（基本的なパターンのみ）"""
    
    # 明らかに不自然なパターンをチェック
    problematic_patterns = [
        "there will",    # 場所詞が文頭で疑問文の形になっていない
        "at the park will",  # 場所句が文頭で疑問文の形になっていない
    ]
    
    sentence_lower = sentence.lower()
    for pattern in problematic_patterns:
        if sentence_lower.startswith(pattern):
            return False
    
    # 基本的には成立していると仮定
    return True

if __name__ == "__main__":
    test_eat_group_order()
