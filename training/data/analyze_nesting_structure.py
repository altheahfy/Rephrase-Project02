"""
テスト例文の入れ子構造レベル分析
Rephraseの設計範囲に適した例文の再作成
"""

def analyze_nesting_levels():
    """テスト例文の入れ子構造を詳細分析"""
    
    print("🔍 Nesting Level Analysis of Test Sentences")
    print("=" * 60)
    
    # 現在のテスト例文
    complex_sentences = [
        {
            "sentence": "Having finished the project that was assigned by the teacher, the student who had been working diligently submitted it confidently.",
            "analysis": "三重入れ子構造の分析"
        },
        {
            "sentence": "While she was reading the book that her friend had recommended, she discovered what made the story so compelling.",
            "analysis": "三重入れ子構造の分析"
        },
        {
            "sentence": "Before starting the presentation that he had prepared carefully, Tom asked me what I thought about the topic.",
            "analysis": "三重入れ子構造の分析"
        }
    ]
    
    for i, test_case in enumerate(complex_sentences, 1):
        print(f"\n📝 Example {i}: {test_case['analysis']}")
        sentence = test_case['sentence']
        print(f"Sentence: {sentence}")
        print()
        
        # 入れ子構造の詳細分析
        if i == 1:
            print("🏗️ Nesting Structure Analysis:")
            print("Level 1 (Main): [the student] submitted it confidently")
            print("Level 2 (Sub):  Having finished [the project that was assigned by the teacher]")
            print("Level 3 (Sub-Sub): that was assigned by the teacher  ← 三重入れ子!")
            print("Level 2 (Sub):  [the student] who had been working diligently")
            print("Level 3 (Sub-Sub): who had been working diligently  ← 三重入れ子!")
            print()
            print("❌ 問題: 上位スロット → サブスロット → サブサブスロット の三重構造")
            print("❌ Rephraseの設計範囲外: サブスロットのサブスロットは扱わない")
        
        elif i == 2:
            print("🏗️ Nesting Structure Analysis:")
            print("Level 1 (Main): she discovered [what made the story so compelling]")
            print("Level 2 (Sub):  While she was reading [the book that her friend had recommended]")
            print("Level 3 (Sub-Sub): that her friend had recommended  ← 三重入れ子!")
            print("Level 2 (Sub):  what made [the story] so compelling")
            print("Level 3 (Sub-Sub): made the story so compelling  ← 三重入れ子!")
            print()
            print("❌ 問題: 時間節の中にさらに関係節が入れ子になっている")
        
        elif i == 3:
            print("🏗️ Nesting Structure Analysis:")
            print("Level 1 (Main): Tom asked me [what I thought about the topic]")
            print("Level 2 (Sub):  Before starting [the presentation that he had prepared carefully]")
            print("Level 3 (Sub-Sub): that he had prepared carefully  ← 三重入れ子!")
            print("Level 2 (Sub):  what I thought about the topic")
            print()
            print("❌ 問題: 動名詞句の中に関係節が入れ子になっている")
        
        print("=" * 60)
    
    return True

def create_proper_rephrase_examples():
    """Rephraseの設計範囲に適した例文を作成"""
    
    print("\n🎯 Creating Proper Rephrase-Compatible Examples")
    print("=" * 60)
    print("設計原則: 上位スロット + サブスロット (二重入れ子まで)")
    print("回避対象: サブスロットのサブスロット (三重入れ子)")
    print()
    
    proper_examples = [
        {
            "sentence": "Having finished the project, the student submitted it confidently.",
            "structure": {
                "main_slot": "the student submitted it confidently",
                "sub_slot_1": "Having finished the project",
                "sub_slot_2": None,
                "grammar_items": ["participle_pattern", "svo_pattern"],
                "nesting_level": "✅ 二重入れ子 (適切)"
            },
            "description": "分詞構文 + 主節 (シンプルな二重構造)"
        },
        {
            "sentence": "While she was reading, she discovered what made the story compelling.",
            "structure": {
                "main_slot": "she discovered what made the story compelling",
                "sub_slot_1": "While she was reading",
                "sub_slot_2": "what made the story compelling",
                "grammar_items": ["conjunction_pattern", "noun_clause", "svoc_pattern"],
                "nesting_level": "✅ 二重入れ子 (適切)"
            },
            "description": "時間節 + 名詞節 + 主節 (並列な二重構造)"
        },
        {
            "sentence": "The book that he wrote became very popular.",
            "structure": {
                "main_slot": "The book became very popular",
                "sub_slot_1": "that he wrote",
                "sub_slot_2": None,
                "grammar_items": ["relative_pattern", "svc_pattern"],
                "nesting_level": "✅ 二重入れ子 (適切)"
            },
            "description": "関係節 + 主節 (基本的な二重構造)"
        },
        {
            "sentence": "She made him happy by encouraging him constantly.",
            "structure": {
                "main_slot": "She made him happy",
                "sub_slot_1": "by encouraging him constantly",
                "sub_slot_2": None,
                "grammar_items": ["svoc_pattern", "gerund_pattern"],
                "nesting_level": "✅ 二重入れ子 (適切)"
            },
            "description": "SVOC + 動名詞句 (手段表現の二重構造)"
        },
        {
            "sentence": "Please tell me what you think about this idea.",
            "structure": {
                "main_slot": "Please tell me",
                "sub_slot_1": "what you think about this idea",
                "sub_slot_2": None,
                "grammar_items": ["imperative_pattern", "noun_clause"],
                "nesting_level": "✅ 二重入れ子 (適切)"
            },
            "description": "命令文 + 名詞節 (基本的な二重構造)"
        }
    ]
    
    for i, example in enumerate(proper_examples, 1):
        print(f"📝 Proper Example {i}: {example['description']}")
        print(f"Sentence: {example['sentence']}")
        print("Structure:")
        print(f"  Main Slot: {example['structure']['main_slot']}")
        print(f"  Sub Slot 1: {example['structure']['sub_slot_1']}")
        if example['structure']['sub_slot_2']:
            print(f"  Sub Slot 2: {example['structure']['sub_slot_2']}")
        print(f"  Grammar Items: {example['structure']['grammar_items']}")
        print(f"  Nesting: {example['structure']['nesting_level']}")
        print()
    
    print("🎯 Key Difference:")
    print("❌ 避けるべき: 'the book [that he wrote [when he was young]]' (三重入れ子)")
    print("✅ 適切な形: 'the book [that he wrote]' + '時期については別文で表現'")
    print()
    print("💡 Rephraseの設計哲学:")
    print("- 複雑な文は複数の単純な文に分解")
    print("- 各文は最大二重入れ子まで")
    print("- 理解しやすい構造を優先")
    
    return proper_examples

if __name__ == "__main__":
    analyze_nesting_levels()
    proper_examples = create_proper_rephrase_examples()
