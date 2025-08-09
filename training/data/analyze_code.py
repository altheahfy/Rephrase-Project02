print("=== Rephrase Parsing Engine 機能分析 ===")
print("総行数: 1000+行 (元々: 270行)")
print()

categories = {
    "基本機能": ["__init__", "load_rules", "get_basic_rules", "analyze_sentence"],
    "疑問文解析": ["is_question", "analyze_question", "analyze_do_question", "analyze_wh_question", 
                 "determine_wh_slot", "analyze_be_question", "analyze_modal_question"],
    "命令文解析": ["is_imperative_with_vocative", "analyze_imperative_with_vocative", 
                 "parse_imperative_objects_modifiers", "extract_imperative_modifiers", "is_manner_adverb"],
    "複文解析": ["contains_subclause", "analyze_complex_sentence", "detect_cognitive_verb_pattern",
                "extract_that_clause", "analyze_that_clause"],
    "単文解析": ["analyze_simple_sentence", "detect_modal_pattern", "detect_perfect_pattern",
                "detect_passive_pattern", "looks_like_past_participle", "detect_be_verb_pattern",
                "detect_basic_svo_pattern"],
    "修飾語処理": ["separate_please_from_phrase", "extract_phrasal_verb", "classify_verb_complement",
                  "classify_remaining_phrase", "separate_object_and_modifiers", "extract_modifiers_from_words"],
    "動詞分類": ["is_intransitive_verb"],
    "spaCy統合": ["enhance_word_recognition", "is_word_recognized", "is_known_word_traditional"],
    "テスト機能": ["test_parsing_engine"]
}

print("機能カテゴリ別メソッド数:")
total = 0
for category, methods in categories.items():
    count = len(methods)
    total += count
    print(f"  {category:12} : {count:2}個")

print(f"\n総メソッド数: {total}個")

# 推定行数分析
print("\n推定行数分析:")
estimated_lines = {
    "基本機能": 80,
    "疑問文解析": 250,  # 7メソッド x 35行
    "命令文解析": 150,  # 5メソッド x 30行
    "複文解析": 150,   # 5メソッド x 30行
    "単文解析": 200,   # 7メソッド x 28行
    "修飾語処理": 180, # 6メソッド x 30行
    "動詞分類": 20,
    "spaCy統合": 50,
    "テスト機能": 70
}

for category, lines in estimated_lines.items():
    print(f"  {category:12} : 約{lines:3}行")

print(f"\n推定総行数: 約{sum(estimated_lines.values())}行")
