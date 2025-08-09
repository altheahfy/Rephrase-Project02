from Rephrase_Parsing_Engine import RephraseParsingEngine

engine = RephraseParsingEngine()

# テスト語彙（難しい単語を含む）
test_words = [
    'recovered', 'quickly', 'injury', 'lie', 'bed',  # 基本語彙
    'rehabilitation', 'sophisticated', 'entrepreneurship',  # 複雑語彙
    'unforgettable', 'misunderstanding', 'extraordinary',  # 長い語彙
    'running', 'played', 'better', 'fastest',  # 活用形
    'unknown_xyz_123'  # 未知語
]

print("=== spaCy vs 従来形態素 語彙認識比較 ===")
for word in test_words:
    spacy_result = engine.is_word_recognized(word)
    traditional_result = engine.is_known_word_traditional(word)
    
    print(f"{word:20} | spaCy: {'✅' if spacy_result else '❌'} | 従来: {'✅' if traditional_result else '❌'}")
